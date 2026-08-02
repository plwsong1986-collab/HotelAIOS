#!/usr/bin/env python3
"""
HotelAIOS SEO Data Generator
File: 19_Automation/generators/seo_generator.py
Version: 1.0.0
Updated: 2026-08-03

功能：
1. 加载单个物业的 hotel / brand / website / seo / ota 配置。
2. 解析 seo.yaml 中的 SSOT 引用。
3. 生成可供网站、搜索引擎和部署流程使用的 seo.json。
4. 生成 Meta、Open Graph、Twitter Card、JSON-LD、robots 与 sitemap 配置。
5. 不编造缺失信息，不修改任何源 YAML 文件。

推荐调用：
uv run python 19_Automation/generators/seo_generator.py \
  sanlitian-oxygen-guesthouse-001

默认输出：
19_Automation/output/seo/<property_id>/seo.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

VERSION = "1.0.0"
AUTOMATION_DIR_NAME = "19_Automation"
LOADER_FILE_NAME = "load_property_config.py"


class SEOGenerationError(RuntimeError):
    """SEO 数据生成错误。"""


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "17_Config" / "properties.yaml").is_file() and (
            candidate / AUTOMATION_DIR_NAME / LOADER_FILE_NAME
        ).is_file():
            return candidate
    raise SEOGenerationError(f"无法从 {start} 向上找到 HotelAIOS 项目根目录。")


def load_loader_module(project_root: Path) -> Any:
    loader_path = project_root / AUTOMATION_DIR_NAME / LOADER_FILE_NAME
    spec = importlib.util.spec_from_file_location(
        "hotelaios_load_property_config",
        loader_path,
    )
    if spec is None or spec.loader is None:
        raise SEOGenerationError(f"无法加载模块：{loader_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_nested(data: Any, path: str, default: Any = None) -> Any:
    current = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def first_non_empty(*values: Any, default: Any = "") -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return default


def resolve_reference(
    configs: dict[str, dict[str, Any]],
    reference: Any,
    default: Any = "",
) -> Any:
    """
    解析形如 hotel.yaml:contact.phone.primary 的配置引用。
    """
    if not isinstance(reference, str):
        return reference

    if ":" not in reference:
        return reference

    filename, data_path = reference.split(":", 1)
    config_key = filename.removesuffix(".yaml").removesuffix(".yml")
    source = configs.get(config_key)

    if not isinstance(source, dict):
        return default

    return get_nested(source, data_path, default)


def normalize_language_pair(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {"zh": "", "en": ""}

    return {
        "zh": str(
            first_non_empty(
                value.get("zh"),
                value.get("zh-CN"),
                default="",
            )
        ),
        "en": str(first_non_empty(value.get("en"), default="")),
    }


def normalize_keywords(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {"zh": [], "en": []}

    def clean(items: Any) -> list[str]:
        if not isinstance(items, list):
            return []
        result: list[str] = []
        seen: set[str] = set()
        for item in items:
            if not isinstance(item, str):
                continue
            normalized = item.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(normalized)
        return result

    return {
        "zh": clean(first_non_empty(value.get("zh"), value.get("zh-CN"), default=[])),
        "en": clean(value.get("en", [])),
    }


def normalize_base_url(
    seo: dict[str, Any],
    website: dict[str, Any],
    hotel: dict[str, Any],
) -> str:
    value = first_non_empty(
        get_nested(seo, "site.canonical_url"),
        get_nested(website, "deployment.domain.primary"),
        get_nested(hotel, "contact.website.url"),
        default="",
    )
    if not isinstance(value, str):
        return ""

    value = value.strip()
    if not value:
        return ""

    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"

    return value.rstrip("/") + "/"


def make_absolute_url(base_url: str, value: Any) -> str:
    if not isinstance(value, str):
        return ""

    value = value.strip()
    if not value:
        return ""

    if value.startswith(("http://", "https://")):
        return value

    if not base_url:
        return value

    return urljoin(base_url, value.lstrip("/"))


def normalize_address(hotel: dict[str, Any]) -> dict[str, Any]:
    return {
        "@type": "PostalAddress",
        "streetAddress": first_non_empty(
            get_nested(hotel, "location.full_address.zh"),
            get_nested(hotel, "location.street.name_zh"),
            default="",
        ),
        "addressLocality": get_nested(hotel, "location.city.name_zh", ""),
        "addressRegion": get_nested(hotel, "location.province.name_zh", ""),
        "postalCode": get_nested(hotel, "location.postal_code", ""),
        "addressCountry": first_non_empty(
            get_nested(hotel, "location.country.code"),
            get_nested(hotel, "location.country.name_en"),
            default="CN",
        ),
    }


def normalize_geo(hotel: dict[str, Any]) -> dict[str, Any] | None:
    latitude = get_nested(hotel, "location.coordinates.latitude")
    longitude = get_nested(hotel, "location.coordinates.longitude")

    if latitude in (None, "") or longitude in (None, ""):
        return None

    return {
        "@type": "GeoCoordinates",
        "latitude": latitude,
        "longitude": longitude,
    }


def normalize_images(
    seo: dict[str, Any],
    website: dict[str, Any],
    hotel: dict[str, Any],
    base_url: str,
) -> list[str]:
    candidates: list[Any] = [
        get_nested(seo, "open_graph.image"),
        get_nested(seo, "structured_data.image"),
        get_nested(website, "homepage.hero.cover_image"),
        get_nested(website, "branding.logo"),
        get_nested(hotel, "media.cover_image"),
        get_nested(hotel, "media.logo"),
    ]

    gallery = get_nested(hotel, "media.gallery", [])
    if isinstance(gallery, list):
        candidates.extend(gallery)

    result: list[str] = []
    seen: set[str] = set()

    for candidate in candidates:
        absolute = make_absolute_url(base_url, candidate)
        if absolute and absolute not in seen:
            seen.add(absolute)
            result.append(absolute)

    return result


def normalize_pages(
    website: dict[str, Any],
    base_url: str,
) -> list[dict[str, Any]]:
    pages = website.get("pages")
    if not isinstance(pages, dict):
        return []

    result: list[dict[str, Any]] = []

    for page_id, enabled in pages.items():
        if enabled is not True:
            continue

        if page_id == "home":
            path = "/"
        else:
            path = f"/{str(page_id).strip('/')}/"

        result.append(
            {
                "id": page_id,
                "path": path,
                "url": make_absolute_url(base_url, path),
                "enabled": True,
            }
        )

    return result


def build_json_ld(
    configs: dict[str, dict[str, Any]],
    base_url: str,
    images: list[str],
) -> dict[str, Any]:
    hotel = configs["hotel"]
    seo = configs["seo"]

    structured = seo.get("structured_data")
    if not isinstance(structured, dict):
        structured = {}

    name = resolve_reference(
        configs,
        structured.get("name_source"),
        default=get_nested(hotel, "property.property_name", ""),
    )
    phone = resolve_reference(
        configs,
        structured.get("phone_source"),
        default=get_nested(hotel, "contact.phone.primary", ""),
    )
    address = resolve_reference(
        configs,
        structured.get("address_source"),
        default=None,
    )
    geo = resolve_reference(
        configs,
        structured.get("geo_source"),
        default=None,
    )

    if not isinstance(address, dict):
        address = normalize_address(hotel)

    if not isinstance(geo, dict):
        geo = normalize_geo(hotel)

    json_ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": structured.get("type", "LodgingBusiness"),
        "name": name,
        "url": base_url.rstrip("/") if base_url else "",
        "telephone": phone,
        "address": address,
    }

    description = first_non_empty(
        get_nested(seo, "meta.homepage.description.zh"),
        get_nested(seo, "meta.homepage.description.en"),
        default="",
    )
    if description:
        json_ld["description"] = description

    if geo:
        json_ld["geo"] = geo

    if images:
        json_ld["image"] = images

    price_range = structured.get("price_range")
    if price_range not in (None, ""):
        json_ld["priceRange"] = price_range

    email = get_nested(hotel, "contact.email.primary", "")
    if email:
        json_ld["email"] = email

    return {
        key: value for key, value in json_ld.items() if value not in (None, "", [], {})
    }


def build_seo_payload(
    unified_config: dict[str, Any],
) -> dict[str, Any]:
    configs = unified_config.get("config")
    if not isinstance(configs, dict):
        raise SEOGenerationError("统一配置缺少 config 对象。")

    required = ("hotel", "brand", "website", "seo", "ota")
    missing = [name for name in required if not isinstance(configs.get(name), dict)]
    if missing:
        raise SEOGenerationError(f"统一配置缺少模块：{', '.join(missing)}")

    hotel = configs["hotel"]
    website = configs["website"]
    seo = configs["seo"]

    base_url = normalize_base_url(seo, website, hotel)
    images = normalize_images(seo, website, hotel, base_url)
    pages = normalize_pages(website, base_url)

    title = normalize_language_pair(get_nested(seo, "meta.homepage.title", {}))
    description = normalize_language_pair(
        get_nested(seo, "meta.homepage.description", {})
    )
    keywords = normalize_keywords(get_nested(seo, "meta.homepage.keywords", {}))

    open_graph = seo.get("open_graph")
    if not isinstance(open_graph, dict):
        open_graph = {}

    twitter = seo.get("twitter")
    if not isinstance(twitter, dict):
        twitter = {}

    sitemap_path = get_nested(seo, "site.sitemap", "sitemap.xml")
    robots_value = get_nested(seo, "site.robots", "index,follow")

    payload = {
        "generator": {
            "name": "HotelAIOS SEO Data Generator",
            "version": VERSION,
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "property_id": unified_config.get("property_id", ""),
        "site": {
            "base_url": base_url,
            "canonical_url": base_url.rstrip("/") if base_url else "",
            "robots": robots_value,
            "sitemap": {
                "path": sitemap_path,
                "url": make_absolute_url(base_url, sitemap_path),
            },
            "default_language": get_nested(
                seo,
                "seo.default_language",
                "zh-CN",
            ),
            "supported_languages": get_nested(
                seo,
                "seo.supported_languages",
                ["zh-CN"],
            ),
        },
        "meta": {
            "homepage": {
                "title": title,
                "description": description,
                "keywords": keywords,
            }
        },
        "open_graph": {
            "type": open_graph.get("type", "website"),
            "site_name": open_graph.get(
                "site_name",
                first_non_empty(
                    get_nested(hotel, "property.property_name"),
                    default="",
                ),
            ),
            "locale": open_graph.get("locale", "zh_CN"),
            "url": base_url.rstrip("/") if base_url else "",
            "image": first_non_empty(images[0] if images else "", default=""),
            "title": title,
            "description": description,
        },
        "twitter": {
            "card": twitter.get("card", "summary_large_image"),
            "site": twitter.get("site", ""),
            "creator": twitter.get("creator", ""),
            "image": first_non_empty(images[0] if images else "", default=""),
            "title": title,
            "description": description,
        },
        "structured_data": build_json_ld(configs, base_url, images),
        "pages": pages,
        "images": images,
        "ai_search": seo.get("ai_search", {}),
        "rendering": {
            "meta_tags": {
                "title_zh": title["zh"],
                "title_en": title["en"],
                "description_zh": description["zh"],
                "description_en": description["en"],
                "keywords_zh": ", ".join(keywords["zh"]),
                "keywords_en": ", ".join(keywords["en"]),
                "canonical": base_url.rstrip("/") if base_url else "",
                "robots": robots_value,
            },
            "robots_txt": {
                "user_agent": "*",
                "allow": "/",
                "sitemap": make_absolute_url(base_url, sitemap_path),
            },
            "sitemap_entries": [
                {
                    "loc": page["url"],
                    "changefreq": "weekly",
                    "priority": 1.0 if page["id"] == "home" else 0.8,
                }
                for page in pages
                if page.get("url")
            ],
        },
        "governance": {
            "factual_only": bool(get_nested(seo, "ai_search.factual_only", True)),
            "prohibit_unverified_claims": bool(
                get_nested(
                    seo,
                    "ai_search.prohibit_unverified_claims",
                    True,
                )
            ),
            "manual_review_required": bool(
                get_nested(
                    seo,
                    "governance.manual_review_required",
                    True,
                )
            ),
            "validation_required_before_publish": bool(
                get_nested(
                    seo,
                    "governance.validation_required_before_publish",
                    True,
                )
            ),
        },
        "sources": unified_config.get("sources", {}),
    }

    return payload


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="生成 HotelAIOS SEO、Open Graph 与 JSON-LD 数据。"
    )
    parser.add_argument(
        "property_id",
        help="物业唯一 ID，例如 sanlitian-oxygen-guesthouse-001。",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="HotelAIOS 项目根目录；默认自动查找。",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="自定义输出文件路径。",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="同时在终端输出完整 JSON。",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        project_root = (
            args.root.resolve() if args.root else find_project_root(Path.cwd())
        )

        loader = load_loader_module(project_root)
        unified = loader.load_property_configuration(
            project_root,
            args.property_id,
        )
        payload = build_seo_payload(unified)

        if args.output:
            output_path = args.output
            if not output_path.is_absolute():
                output_path = project_root / output_path
        else:
            output_path = (
                project_root
                / AUTOMATION_DIR_NAME
                / "output"
                / "seo"
                / args.property_id
                / "seo.json"
            )

        output_path = output_path.resolve()
        write_json(output_path, payload)

    except Exception as exc:
        print(f"错误 SEO_GENERATION_FAILED：{exc}", file=sys.stderr)
        return 1

    print("=" * 72)
    print(f"HotelAIOS SEO Data Generator v{VERSION}")
    print("=" * 72)
    print(f"物业：{args.property_id}")
    print(f"输出：{output_path}")
    print(f"页面数：{len(payload['pages'])}")
    print(f"图片数：{len(payload['images'])}")
    print("Canonical：" + (payload["site"]["canonical_url"] or "未配置"))
    print("SEO 数据生成成功。")

    if args.stdout:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
