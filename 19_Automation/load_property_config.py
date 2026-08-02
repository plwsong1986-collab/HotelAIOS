#!/usr/bin/env python3
"""
HotelAIOS Property Configuration Loader
File: 19_Automation/load_property_config.py
Version: 1.0.0
Updated: 2026-08-03

功能：
1. 自动定位 HotelAIOS 项目根目录。
2. 读取 17_Config/properties.yaml。
3. 按 property_id 加载 hotel.yaml、brand.yaml、website.yaml、seo.yaml、ota.yaml。
4. 检查五个配置文件中的 property_id 是否一致。
5. 输出统一 Property Configuration JSON，可供后续 Website / SEO / OTA Generator 使用。

本程序只读取配置，不修改任何源文件。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("缺少依赖 PyYAML。请在项目根目录运行：uv add pyyaml") from exc


VERSION = "1.0.0"
CONFIG_DIR = "17_Config"
REGISTRY_FILE = "properties.yaml"
PROPERTY_FILES = (
    "hotel.yaml",
    "brand.yaml",
    "website.yaml",
    "seo.yaml",
    "ota.yaml",
)
PROPERTY_ID_PATHS = {
    "hotel.yaml": ("property", "property_id"),
    "brand.yaml": ("brand", "property_id"),
    "website.yaml": ("website", "property_id"),
    "seo.yaml": ("seo", "property_id"),
    "ota.yaml": ("ota", "property_id"),
}


class ConfigurationError(RuntimeError):
    """HotelAIOS 配置读取错误。"""


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        registry = candidate / CONFIG_DIR / REGISTRY_FILE
        if registry.is_file():
            return candidate
    raise ConfigurationError(f"无法从 {start} 向上找到 {CONFIG_DIR}/{REGISTRY_FILE}。")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigurationError(f"配置文件不存在：{path}")

    try:
        with path.open("r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"YAML 语法错误：{path}\n{exc}") from exc
    except OSError as exc:
        raise ConfigurationError(f"无法读取文件：{path}\n{exc}") from exc

    if not isinstance(data, dict):
        raise ConfigurationError(f"YAML 顶层必须是对象：{path}")

    return data


def get_nested(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def find_property_record(
    registry: dict[str, Any],
    property_id: str,
) -> dict[str, Any]:
    records = registry.get("properties")
    if not isinstance(records, list):
        raise ConfigurationError("properties.yaml 中 properties 必须是列表。")

    for record in records:
        if isinstance(record, dict) and record.get("property_id") == property_id:
            return record

    raise ConfigurationError(f"properties.yaml 中未登记物业：{property_id}")


def resolve_property_directory(
    project_root: Path,
    record: dict[str, Any],
) -> Path:
    config_path = record.get("config_path")
    if not isinstance(config_path, str) or not config_path.strip():
        raise ConfigurationError("物业记录缺少有效 config_path。")

    path = Path(config_path)
    if not path.is_absolute():
        path = project_root / CONFIG_DIR / path

    path = path.resolve()
    if not path.is_dir():
        raise ConfigurationError(f"物业配置目录不存在：{path}")

    return path


def load_property_configuration(
    project_root: Path,
    property_id: str,
) -> dict[str, Any]:
    registry_path = project_root / CONFIG_DIR / REGISTRY_FILE
    registry = load_yaml(registry_path)
    record = find_property_record(registry, property_id)
    property_dir = resolve_property_directory(project_root, record)

    if property_dir.name != property_id:
        raise ConfigurationError(
            f"目录名 {property_dir.name!r} 与 property_id {property_id!r} 不一致。"
        )

    configs: dict[str, dict[str, Any]] = {}

    for filename in PROPERTY_FILES:
        file_path = property_dir / filename
        data = load_yaml(file_path)

        id_path = PROPERTY_ID_PATHS[filename]
        actual_property_id = get_nested(data, id_path)

        if actual_property_id != property_id:
            raise ConfigurationError(
                f"{filename} 中 {'.'.join(id_path)}="
                f"{actual_property_id!r}，应为 {property_id!r}。"
            )

        configs[filename.removesuffix(".yaml")] = data

    return {
        "loader": {
            "name": "HotelAIOS Property Configuration Loader",
            "version": VERSION,
        },
        "property_id": property_id,
        "registry_record": record,
        "sources": {
            "registry": str(registry_path.relative_to(project_root)),
            "property_directory": str(property_dir.relative_to(project_root)),
            "files": list(PROPERTY_FILES),
        },
        "config": configs,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="加载并合并 HotelAIOS 单个物业的五份核心配置。"
    )
    parser.add_argument(
        "property_id",
        help="物业唯一 ID，例如 sanlitian-oxygen-guesthouse-001。",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="HotelAIOS 项目根目录；默认从当前目录自动查找。",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="可选：将统一配置输出为 JSON 文件。",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="在终端打印完整格式化 JSON。",
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
        root = args.root.resolve() if args.root else find_project_root(Path.cwd())
        result = load_property_configuration(root, args.property_id)
    except ConfigurationError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    if args.output:
        output_path = args.output
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path = output_path.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"统一配置已生成：{output_path}")

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 72)
        print("HotelAIOS Property Configuration Loader")
        print("=" * 72)
        print(f"物业：{args.property_id}")
        print("已加载：hotel.yaml")
        print("已加载：brand.yaml")
        print("已加载：website.yaml")
        print("已加载：seo.yaml")
        print("已加载：ota.yaml")
        print("配置加载成功。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
