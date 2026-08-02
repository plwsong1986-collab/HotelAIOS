#!/usr/bin/env python3
"""
HotelAIOS Website Data Generator
File: 19_Automation/generators/website_generator.py
Version: 1.0.0
Updated: 2026-08-03

功能：
1. 加载单个物业的 hotel / brand / website / seo / ota 配置。
2. 解析 website.yaml 中的 SSOT 引用。
3. 生成前端可直接使用的 website.json。
4. 保留事实来源，不自动编造缺失数据。
5. 只读取源配置，不修改任何 YAML 文件。

推荐调用：
uv run python 19_Automation/generators/website_generator.py \
  sanlitian-oxygen-guesthouse-001

输出：
19_Automation/output/website/<property_id>/website.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "1.0.0"
AUTOMATION_DIR_NAME = "19_Automation"
LOADER_FILE_NAME = "load_property_config.py"


class WebsiteGenerationError(RuntimeError):
    """官网数据生成错误。"""


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "17_Config" / "properties.yaml").is_file() and (
            candidate / AUTOMATION_DIR_NAME / LOADER_FILE_NAME
        ).is_file():
            return candidate
    raise WebsiteGenerationError(f"无法从 {start} 向上找到 HotelAIOS 项目根目录。")


def load_loader_module(project_root: Path) -> Any:
    loader_path = project_root / AUTOMATION_DIR_NAME / LOADER_FILE_NAME
    spec = importlib.util.spec_from_file_location(
        "hotelaios_load_property_config",
        loader_path,
    )
    if spec is None or spec.loader is None:
        raise WebsiteGenerationError(f"无法加载模块：{loader_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_nested(data: Any, path: str, default: Any = None) -> Any:
    """
    按点路径读取字典。

    示例：
    get_nested(config, "hotel.property.property_name")
    """
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
    解析配置引用。

    支持：
      brand.yaml:slogans.primary.zh
      hotel.yaml:contact.phone.primary

    非引用值原样返回。
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


def language_pair(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {"zh": "", "en": ""}

    return {
        "zh": str(first_non_empty(value.get("zh"), value.get("zh-CN"), default="")),
        "en": str(first_non_empty(value.get("en"), default="")),
    }


def normalize_navigation(website: dict[str, Any]) -> list[dict[str, Any]]:
    items = get_nested(website, "navigation.header", [])
    result: list[dict[str, Any]] = []

    if not isinstance(items, list):
        return result

    for index, item in enumerate(items):
        if isinstance(item, str):
            result.append(
                {
                    "id": item,
                    "label": {"zh": item, "en": item},
                    "order": index,
                    "enabled": True,
                }
            )
            continue

        if isinstance(item, dict):
            item_id = str(
                first_non_empty(
                    item.get("id"),
                    item.get("key"),
                    item.get("slug"),
                    default=f"item-{index + 1}",
                )
            )
            result.append(
                {
                    "id": item_id,
                    "label": {
                        "zh": str(
                            first_non_empty(
                                item.get("zh"),
                                item.get("label_zh"),
                                item.get("name_zh"),
                                default=item_id,
                            )
                        ),
                        "en": str(
                            first_non_empty(
                                item.get("en"),
                                item.get("label_en"),
                                item.get("name_en"),
                                default=item_id,
                            )
                        ),
                    },
                    "href": first_non_empty(
                        item.get("href"),
                        item.get("url"),
                        default=f"#{item_id}",
                    ),
                    "order": index,
                    "enabled": bool(item.get("enabled", True)),
                }
            )

    return result


def normalize_room_types(hotel: dict[str, Any]) -> list[dict[str, Any]]:
    rooms = get_nested(hotel, "accommodation.room_types", [])
    result: list[dict[str, Any]] = []

    if not isinstance(rooms, list):
        return result

    for room in rooms:
        if not isinstance(room, dict):
            continue

        bed = room.get("bed_configuration")
        if not isinstance(bed, dict):
            bed = {}

        result.append(
            {
                "id": room.get("room_type_id", ""),
                "name": {
                    "zh": room.get("name_zh", ""),
                    "en": room.get("name_en", ""),
                },
                "quantity": room.get("quantity"),
                "maximum_guests": room.get("maximum_guests"),
                "room_size_sqm": room.get("room_size_sqm"),
                "bed": {
                    "type": bed.get("bed_type", ""),
                    "count": bed.get("bed_count"),
                    "size": bed.get("bed_size", ""),
                },
                "oxygen_supply": room.get("oxygen_supply"),
                "status": room.get("status", ""),
            }
        )

    return result


def normalize_facilities(hotel: dict[str, Any]) -> list[dict[str, Any]]:
    facilities = hotel.get("facilities")
    if not isinstance(facilities, dict):
        return []

    result: list[dict[str, Any]] = []

    for facility_id, item in facilities.items():
        if not isinstance(item, dict):
            continue

        available = item.get("available")
        if available is False:
            continue

        result.append(
            {
                "id": facility_id,
                "available": available,
                "name": {
                    "zh": item.get("name_zh", facility_id),
                    "en": item.get("name_en", facility_id),
                },
                "description": {
                    "zh": item.get("description_zh", ""),
                    "en": item.get("description_en", ""),
                },
            }
        )

    return result


def normalize_gallery(hotel: dict[str, Any], website: dict[str, Any]) -> dict[str, Any]:
    media = hotel.get("media")
    if not isinstance(media, dict):
        media = {}

    branding = website.get("branding")
    if not isinstance(branding, dict):
        branding = {}

    gallery = media.get("gallery")
    if not isinstance(gallery, list):
        gallery = []

    return {
        "logo": first_non_empty(
            branding.get("logo"),
            media.get("logo"),
            default="",
        ),
        "favicon": branding.get("favicon", ""),
        "cover_image": first_non_empty(
            get_nested(website, "homepage.hero.cover_image"),
            media.get("cover_image"),
            default="",
        ),
        "gallery": gallery,
        "room_galleries": media.get("room_galleries", {}),
        "floor_plans": media.get("floor_plans", []),
        "virtual_tour_url": media.get("virtual_tour_url", ""),
        "video_urls": media.get("video_urls", []),
        "verification_status": media.get(
            "media_verification_status",
            "not-provided",
        ),
    }


def normalize_contact(hotel: dict[str, Any]) -> dict[str, Any]:
    return {
        "phone": {
            "primary": get_nested(hotel, "contact.phone.primary", ""),
            "normalized": get_nested(hotel, "contact.phone.normalized", ""),
            "reservations": get_nested(hotel, "contact.phone.reservations", ""),
            "emergency": get_nested(hotel, "contact.phone.emergency", ""),
        },
        "email": {
            "primary": get_nested(hotel, "contact.email.primary", ""),
            "reservations": get_nested(hotel, "contact.email.reservations", ""),
        },
        "wechat": {
            "account": get_nested(hotel, "contact.wechat.account", ""),
            "display": get_nested(hotel, "contact.wechat.display", ""),
        },
        "whatsapp": {
            "number": get_nested(hotel, "contact.whatsapp.number", ""),
            "normalized": get_nested(
                hotel,
                "contact.whatsapp.normalized",
                "",
            ),
        },
        "website": {
            "url": get_nested(hotel, "contact.website.url", ""),
            "status": get_nested(
                hotel,
                "contact.website.status",
                "coming-soon",
            ),
        },
    }


def normalize_location(hotel: dict[str, Any]) -> dict[str, Any]:
    return {
        "country": {
            "code": get_nested(hotel, "location.country.code", ""),
            "zh": get_nested(hotel, "location.country.name_zh", ""),
            "en": get_nested(hotel, "location.country.name_en", ""),
        },
        "province": {
            "zh": get_nested(hotel, "location.province.name_zh", ""),
            "en": get_nested(hotel, "location.province.name_en", ""),
        },
        "city": {
            "zh": get_nested(hotel, "location.city.name_zh", ""),
            "en": get_nested(hotel, "location.city.name_en", ""),
        },
        "district": {
            "zh": get_nested(hotel, "location.district.name_zh", ""),
            "en": get_nested(hotel, "location.district.name_en", ""),
        },
        "locality": {
            "zh": get_nested(hotel, "location.locality.name_zh", ""),
            "en": get_nested(hotel, "location.locality.name_en", ""),
        },
        "neighborhood": {
            "zh": get_nested(hotel, "location.neighborhood.name_zh", ""),
            "en": get_nested(hotel, "location.neighborhood.name_en", ""),
        },
        "street": {
            "zh": get_nested(hotel, "location.street.name_zh", ""),
            "en": get_nested(hotel, "location.street.name_en", ""),
        },
        "full_address": {
            "zh": get_nested(hotel, "location.full_address.zh", ""),
            "en": get_nested(hotel, "location.full_address.en", ""),
        },
        "postal_code": get_nested(hotel, "location.postal_code", ""),
        "coordinates": {
            "latitude": get_nested(hotel, "location.coordinates.latitude"),
            "longitude": get_nested(hotel, "location.coordinates.longitude"),
            "verification_status": get_nested(
                hotel,
                "location.coordinates.verification_status",
                "",
            ),
        },
        "altitude_meters": get_nested(hotel, "location.altitude_meters"),
        "timezone": get_nested(hotel, "location.timezone", ""),
    }


def build_website_payload(
    unified_config: dict[str, Any],
) -> dict[str, Any]:
    configs = unified_config.get("config")
    if not isinstance(configs, dict):
        raise WebsiteGenerationError("统一配置缺少 config 对象。")

    hotel = configs.get("hotel")
    brand = configs.get("brand")
    website = configs.get("website")
    seo = configs.get("seo")

    if not all(isinstance(item, dict) for item in (hotel, brand, website, seo)):
        raise WebsiteGenerationError("统一配置缺少 hotel、brand、website 或 seo。")

    title_source = get_nested(website, "homepage.hero.title_source", "")
    description_source = get_nested(
        website,
        "homepage.hero.description_source",
        "",
    )

    hero_title = resolve_reference(configs, title_source)
    hero_description = resolve_reference(configs, description_source)

    if not isinstance(hero_title, dict):
        hero_title = {
            "zh": first_non_empty(
                get_nested(hotel, "property.property_name"),
                get_nested(brand, "brand.property_name"),
                default="",
            ),
            "en": first_non_empty(
                get_nested(hotel, "property.property_name_en"),
                get_nested(brand, "brand.property_name_en"),
                default="",
            ),
        }

    if not isinstance(hero_description, dict):
        hero_description = {
            "zh": first_non_empty(
                get_nested(brand, "messaging.short_description_zh"),
                get_nested(
                    seo,
                    "meta.homepage.description.zh",
                ),
                default="",
            ),
            "en": first_non_empty(
                get_nested(brand, "messaging.short_description_en"),
                get_nested(
                    seo,
                    "meta.homepage.description.en",
                ),
                default="",
            ),
        }

    booking = website.get("booking")
    if not isinstance(booking, dict):
        booking = {}

    primary_cta = get_nested(website, "homepage.hero.primary_cta", {})
    secondary_cta = get_nested(website, "homepage.hero.secondary_cta", {})

    payload = {
        "generator": {
            "name": "HotelAIOS Website Data Generator",
            "version": VERSION,
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "property": {
            "property_id": unified_config.get("property_id", ""),
            "name": {
                "zh": get_nested(hotel, "property.property_name", ""),
                "en": get_nested(hotel, "property.property_name_en", ""),
            },
            "short_name": {
                "zh": get_nested(hotel, "property.short_name", ""),
                "en": get_nested(hotel, "property.short_name_en", ""),
            },
            "property_type": get_nested(
                hotel,
                "property.property_type",
                "",
            ),
            "property_type_name": {
                "zh": get_nested(
                    hotel,
                    "property.property_type_name",
                    "",
                ),
                "en": get_nested(
                    hotel,
                    "property.property_type_name_en",
                    "",
                ),
            },
            "lifecycle_status": get_nested(
                hotel,
                "property.lifecycle_status",
                "",
            ),
        },
        "site": {
            "site_id": get_nested(website, "website.site_id", ""),
            "site_name": get_nested(website, "website.site_name", ""),
            "enabled": bool(get_nested(website, "website.enabled", False)),
            "default_language": get_nested(
                website,
                "website.default_language",
                "zh-CN",
            ),
            "supported_languages": get_nested(
                website,
                "website.supported_languages",
                ["zh-CN"],
            ),
            "domain": get_nested(
                website,
                "deployment.domain.primary",
                "",
            ),
            "domain_status": get_nested(
                website,
                "deployment.domain.status",
                "coming-soon",
            ),
            "environment": get_nested(
                website,
                "deployment.environment",
                "development",
            ),
        },
        "branding": {
            "brand_name": {
                "zh": first_non_empty(
                    get_nested(brand, "identity.brand_name.zh"),
                    get_nested(brand, "brand.brand_name"),
                    get_nested(hotel, "property.property_name"),
                    default="",
                ),
                "en": first_non_empty(
                    get_nested(brand, "identity.brand_name.en"),
                    get_nested(brand, "brand.brand_name_en"),
                    get_nested(hotel, "property.property_name_en"),
                    default="",
                ),
            },
            "slogan": language_pair(
                first_non_empty(
                    get_nested(brand, "slogans.primary"),
                    get_nested(brand, "slogan.primary"),
                    default={},
                )
            ),
            "theme": get_nested(website, "branding.theme", {}),
            "media": normalize_gallery(hotel, website),
        },
        "navigation": normalize_navigation(website),
        "hero": {
            "enabled": bool(get_nested(website, "homepage.hero.enabled", True)),
            "title": language_pair(hero_title),
            "description": language_pair(hero_description),
            "primary_cta": language_pair(primary_cta),
            "secondary_cta": language_pair(secondary_cta),
        },
        "homepage": {
            "sections": get_nested(website, "homepage.sections", []),
        },
        "pages": website.get("pages", {}),
        "footer": website.get("footer", {}),
        "booking": {
            "enabled": bool(booking.get("enabled", False)),
            "booking_engine": booking.get("booking_engine", ""),
            "reservation_email": resolve_reference(
                configs,
                booking.get("reservation_email_source", ""),
                default=get_nested(
                    hotel,
                    "contact.email.reservations",
                    "",
                ),
            ),
            "reservation_phone": resolve_reference(
                configs,
                booking.get("reservation_phone_source", ""),
                default=get_nested(
                    hotel,
                    "contact.phone.reservations",
                    "",
                ),
            ),
        },
        "contact": normalize_contact(hotel),
        "location": normalize_location(hotel),
        "operations": {
            "front_desk": get_nested(hotel, "operations.front_desk", {}),
            "check_in": get_nested(hotel, "operations.check_in", {}),
            "check_out": get_nested(hotel, "operations.check_out", {}),
            "capacity": get_nested(hotel, "operations.capacity", {}),
            "languages": get_nested(hotel, "operations.languages", {}),
        },
        "rooms": normalize_room_types(hotel),
        "facilities": normalize_facilities(hotel),
        "services": {
            "oxygen": hotel.get("oxygen_service", {}),
            "breakfast": hotel.get("breakfast", {}),
            "internet": hotel.get("internet", {}),
            "laundry": hotel.get("laundry", {}),
            "parking": hotel.get("parking", {}),
            "transportation": hotel.get("transportation", {}),
        },
        "brand_content": {
            "story": brand.get("story", {}),
            "mission": brand.get("mission", {}),
            "vision": brand.get("vision", {}),
            "promise": first_non_empty(
                brand.get("brand_promise"),
                brand.get("promise"),
                default={},
            ),
            "guest_memory": brand.get("guest_memory", {}),
            "values": brand.get("values", []),
            "voice": brand.get("voice", {}),
        },
        "seo": {
            "title": get_nested(seo, "meta.homepage.title", {}),
            "description": get_nested(
                seo,
                "meta.homepage.description",
                {},
            ),
            "keywords": get_nested(
                seo,
                "meta.homepage.keywords",
                {},
            ),
            "canonical_url": get_nested(
                seo,
                "site.canonical_url",
                "",
            ),
            "robots": get_nested(
                seo,
                "site.robots",
                "index,follow",
            ),
            "open_graph": seo.get("open_graph", {}),
            "structured_data_type": get_nested(
                seo,
                "structured_data.type",
                "LodgingBusiness",
            ),
        },
        "social": website.get("social", {}),
        "analytics": website.get("analytics", {}),
        "governance": {
            "source_of_truth": True,
            "manual_review_required": bool(
                get_nested(
                    website,
                    "governance.manual_review_required",
                    True,
                )
            ),
            "validation_required_before_publish": bool(
                get_nested(
                    website,
                    "governance.validation_required_before_publish",
                    True,
                )
            ),
            "unverified_claims_included": False,
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
    parser = argparse.ArgumentParser(description="生成 HotelAIOS 前端官网数据 JSON。")
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
        payload = build_website_payload(unified)

        if args.output:
            output_path = args.output
            if not output_path.is_absolute():
                output_path = project_root / output_path
        else:
            output_path = (
                project_root
                / AUTOMATION_DIR_NAME
                / "output"
                / "website"
                / args.property_id
                / "website.json"
            )

        output_path = output_path.resolve()
        write_json(output_path, payload)

    except (WebsiteGenerationError, Exception) as exc:
        print(f"错误 WEBSITE_GENERATION_FAILED：{exc}", file=sys.stderr)
        return 1

    print("=" * 72)
    print(f"HotelAIOS Website Data Generator v{VERSION}")
    print("=" * 72)
    print(f"物业：{args.property_id}")
    print(f"输出：{output_path}")
    print(f"导航项：{len(payload['navigation'])}")
    print(f"房型数：{len(payload['rooms'])}")
    print(f"设施数：{len(payload['facilities'])}")
    print("官网数据生成成功。")

    if args.stdout:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
