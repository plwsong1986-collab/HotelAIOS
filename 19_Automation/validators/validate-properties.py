#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIGOS 多物业配置校验器

文件：
19_Automation/validators/validate-properties.py

主要功能：
1. 校验 17_Config/properties.yaml 是否存在且格式正确；
2. 校验 property_id 是否唯一并符合命名规范；
3. 校验注册表中的物业目录是否真实存在；
4. 校验每家物业所需配置文件是否齐全；
5. 校验物业目录名、注册表 property_id 与配置文件中的 property_id 是否一致；
6. 校验删除保护是否启用；
7. 校验物业状态和物业类型是否合法；
8. 校验 Canonical Domain 是否重复；
9. 校验 OTA 平台物业编号是否重复；
10. 校验平台 Profile URL 是否重复；
11. 检测 Git 变更中是否删除受保护物业；
12. 检测 Git 变更中是否修改稳定的 property_id；
13. 忽略 template、_template 等模板目录；
14. 输出适合本地和 GitHub Actions 使用的退出状态码。

依赖：
    PyYAML

安装：
    uv add pyyaml

本地运行：
    python 19_Automation/validators/validate-properties.py

指定仓库根目录：
    python 19_Automation/validators/validate-properties.py --root .

检查相对某个 Git 基线的破坏性变更：
    python 19_Automation/validators/validate-properties.py --base-ref origin/main

将警告视为错误：
    python 19_Automation/validators/validate-properties.py --warnings-as-errors
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:
    print(
        "错误：缺少 PyYAML。\n"
        "请先运行：uv add pyyaml",
        file=sys.stderr,
    )
    raise SystemExit(2)


# ==========================================================
# 常量
# ==========================================================

PROPERTY_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

DEFAULT_SUPPORTED_STATUSES = {
    "draft",
    "active",
    "inactive",
    "archived",
}

DEFAULT_SUPPORTED_PROPERTY_TYPES = {
    "hotel",
    "inn",
    "homestay",
    "guesthouse",
    "hostel",
    "resort",
    "lodge",
    "serviced-apartment",
    "boutique-hotel",
    "heritage-hotel",
    "other-accommodation",
}

DEFAULT_REQUIRED_PROPERTY_FILES = {
    "hotel.yaml",
    "brand.yaml",
    "website.yaml",
    "seo.yaml",
    "ota.yaml",
}

# 模板目录和系统目录不属于正式物业，不需要登记到 properties.yaml。
IGNORED_PROPERTY_DIRECTORIES = {
    "_template",
    "template",
    "templates",
    "_templates",
    ".gitkeep",
    "__pycache__",
}


# ==========================================================
# 校验信息模型
# ==========================================================


@dataclass(frozen=True)
class ValidationMessage:
    """单条校验信息。"""

    level: str
    code: str
    message: str
    path: str | None = None

    def format(self) -> str:
        prefix = {
            "error": "错误",
            "warning": "警告",
            "info": "信息",
        }.get(self.level, self.level.upper())

        location = f" [{self.path}]" if self.path else ""
        return f"{prefix} {self.code}{location}：{self.message}"


class ValidationReporter:
    """收集并输出校验结果。"""

    def __init__(self, quiet: bool = False) -> None:
        self.quiet = quiet
        self.messages: list[ValidationMessage] = []

    def error(
        self,
        code: str,
        message: str,
        path: Path | str | None = None,
    ) -> None:
        self.messages.append(
            ValidationMessage(
                level="error",
                code=code,
                message=message,
                path=str(path) if path else None,
            )
        )

    def warning(
        self,
        code: str,
        message: str,
        path: Path | str | None = None,
    ) -> None:
        self.messages.append(
            ValidationMessage(
                level="warning",
                code=code,
                message=message,
                path=str(path) if path else None,
            )
        )

    def info(
        self,
        code: str,
        message: str,
        path: Path | str | None = None,
    ) -> None:
        self.messages.append(
            ValidationMessage(
                level="info",
                code=code,
                message=message,
                path=str(path) if path else None,
            )
        )

    @property
    def error_count(self) -> int:
        return sum(message.level == "error" for message in self.messages)

    @property
    def warning_count(self) -> int:
        return sum(message.level == "warning" for message in self.messages)

    @property
    def info_count(self) -> int:
        return sum(message.level == "info" for message in self.messages)

    def print_messages(self) -> None:
        if not self.quiet:
            for message in self.messages:
                print(message.format())

        print()
        print(
            "校验完成："
            f"{self.error_count} 个错误，"
            f"{self.warning_count} 个警告。"
        )


# ==========================================================
# 命令行参数
# ==========================================================


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验 AIGOS 多物业配置与删除保护规则。"
    )

    parser.add_argument(
        "--root",
        default=".",
        help="仓库根目录，默认是当前目录。",
    )

    parser.add_argument(
        "--registry",
        default="17_Config/properties.yaml",
        help="物业注册表相对于仓库根目录的位置。",
    )

    parser.add_argument(
        "--base-ref",
        default=None,
        help=(
            "可选 Git 基线，例如 origin/main。"
            "指定后会检测相对该基线删除物业或修改 property_id 的行为。"
        ),
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="不输出逐条校验信息，仅输出最终结果。",
    )

    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="将警告也视为校验失败。",
    )

    return parser.parse_args()


# ==========================================================
# 通用工具函数
# ==========================================================


def load_yaml_file(
    path: Path,
    reporter: ValidationReporter,
) -> dict[str, Any] | None:
    """读取并解析 YAML 文件。"""

    if not path.exists():
        reporter.error("FILE_NOT_FOUND", "文件不存在。", path)
        return None

    if not path.is_file():
        reporter.error("NOT_A_FILE", "路径不是文件。", path)
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        reporter.error(
            "INVALID_YAML",
            f"YAML 语法错误：{exc}",
            path,
        )
        return None
    except OSError as exc:
        reporter.error(
            "FILE_READ_ERROR",
            f"无法读取文件：{exc}",
            path,
        )
        return None

    if content is None:
        reporter.error("EMPTY_YAML", "YAML 文件为空。", path)
        return None

    if not isinstance(content, dict):
        reporter.error(
            "INVALID_ROOT_TYPE",
            "YAML 顶层必须是对象结构。",
            path,
        )
        return None

    return content


def get_nested(
    data: dict[str, Any],
    keys: Iterable[str],
    default: Any = None,
) -> Any:
    """安全读取嵌套字段。"""

    current: Any = data

    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]

    return current


def normalize_string(value: Any) -> str:
    """将任意值转换为去除首尾空格的字符串。"""

    if value is None:
        return ""

    return str(value).strip()


def normalize_url(value: Any) -> str:
    """标准化 URL，用于重复检测。"""

    url = normalize_string(value).lower()

    while url.endswith("/"):
        url = url[:-1]

    return url


def walk_mapping(
    value: Any,
    path: tuple[str, ...] = (),
) -> Iterable[tuple[tuple[str, ...], Any]]:
    """递归遍历字典与列表。"""

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path + (str(key),)
            yield child_path, child
            yield from walk_mapping(child, child_path)

    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = path + (str(index),)
            yield child_path, child
            yield from walk_mapping(child, child_path)


def is_ignored_property_directory(path: Path) -> bool:
    """判断一个目录是否是模板目录或系统目录。"""

    directory_name = path.name.strip()

    if directory_name in IGNORED_PROPERTY_DIRECTORIES:
        return True

    if directory_name.startswith("."):
        return True

    if directory_name.lower() in {
        item.lower() for item in IGNORED_PROPERTY_DIRECTORIES
    }:
        return True

    return False


# ==========================================================
# 注册表结构校验
# ==========================================================


def validate_registry_structure(
    registry: dict[str, Any],
    registry_path: Path,
    reporter: ValidationReporter,
) -> list[dict[str, Any]]:
    """校验 properties.yaml 顶层结构。"""

    properties = registry.get("properties")

    if properties is None:
        reporter.error(
            "MISSING_PROPERTIES_LIST",
            "注册表缺少 properties 列表。",
            registry_path,
        )
        return []

    if not isinstance(properties, list):
        reporter.error(
            "INVALID_PROPERTIES_LIST",
            "properties 必须是列表。",
            registry_path,
        )
        return []

    if not properties:
        reporter.warning(
            "EMPTY_PROPERTIES_LIST",
            "当前注册表中尚未登记任何正式物业。",
            registry_path,
        )

    required_files = registry.get("required_property_files")

    if required_files is not None and not isinstance(required_files, list):
        reporter.error(
            "INVALID_REQUIRED_FILES",
            "required_property_files 必须是列表。",
            registry_path,
        )

    supported_types = registry.get("supported_property_types")

    if supported_types is not None and not isinstance(supported_types, list):
        reporter.error(
            "INVALID_SUPPORTED_TYPES",
            "supported_property_types 必须是列表。",
            registry_path,
        )

    supported_statuses = registry.get("supported_statuses")

    if supported_statuses is not None and not isinstance(
        supported_statuses,
        list,
    ):
        reporter.error(
            "INVALID_SUPPORTED_STATUSES",
            "supported_statuses 必须是列表。",
            registry_path,
        )

    valid_properties: list[dict[str, Any]] = []

    for index, item in enumerate(properties):
        if not isinstance(item, dict):
            reporter.error(
                "INVALID_PROPERTY_ENTRY",
                f"properties[{index}] 必须是对象结构。",
                registry_path,
            )
            continue

        valid_properties.append(item)

    return valid_properties


def validate_registry_deletion_protection(
    registry: dict[str, Any],
    registry_path: Path,
    reporter: ValidationReporter,
) -> None:
    """校验注册表的全局删除保护设置。"""

    registry_settings = registry.get("registry", {})
    defaults = registry.get("defaults", {})
    validation = registry.get("validation", {})

    if not isinstance(registry_settings, dict):
        reporter.error(
            "INVALID_REGISTRY_SETTINGS",
            "registry 必须是对象结构。",
            registry_path,
        )
        return

    if not isinstance(defaults, dict):
        reporter.error(
            "INVALID_DEFAULTS_SETTINGS",
            "defaults 必须是对象结构。",
            registry_path,
        )
        return

    if not isinstance(validation, dict):
        reporter.error(
            "INVALID_VALIDATION_SETTINGS",
            "validation 必须是对象结构。",
            registry_path,
        )
        return

    checks = [
        (
            registry_settings.get("default_deletion_protection"),
            True,
            "registry.default_deletion_protection",
        ),
        (
            registry_settings.get("allow_automatic_deletion"),
            False,
            "registry.allow_automatic_deletion",
        ),
        (
            registry_settings.get("allow_bulk_deletion"),
            False,
            "registry.allow_bulk_deletion",
        ),
        (
            registry_settings.get("allow_property_id_reuse"),
            False,
            "registry.allow_property_id_reuse",
        ),
        (
            defaults.get("deletion_protection"),
            True,
            "defaults.deletion_protection",
        ),
        (
            validation.get("prevent_property_id_change"),
            True,
            "validation.prevent_property_id_change",
        ),
        (
            validation.get("prevent_protected_property_deletion"),
            True,
            "validation.prevent_protected_property_deletion",
        ),
        (
            validation.get("prevent_existing_directory_overwrite"),
            True,
            "validation.prevent_existing_directory_overwrite",
        ),
    ]

    for actual, expected, field_name in checks:
        if actual is not expected:
            reporter.error(
                "UNSAFE_REGISTRY_SETTING",
                (
                    f"{field_name} 必须设置为 "
                    f"{str(expected).lower()}。"
                ),
                registry_path,
            )


# ==========================================================
# 注册物业校验
# ==========================================================


def validate_registry_entries(
    root: Path,
    registry: dict[str, Any],
    properties: list[dict[str, Any]],
    registry_path: Path,
    reporter: ValidationReporter,
) -> dict[str, Path]:
    """校验注册表中的每一条物业记录。"""

    supported_statuses = set(
        registry.get("supported_statuses")
        or DEFAULT_SUPPORTED_STATUSES
    )

    supported_property_types = set(
        registry.get("supported_property_types")
        or DEFAULT_SUPPORTED_PROPERTY_TYPES
    )

    seen_property_ids: dict[str, int] = {}
    property_paths: dict[str, Path] = {}

    for index, item in enumerate(properties):
        entry_path = f"{registry_path}#properties[{index}]"

        property_id = normalize_string(item.get("property_id"))
        property_name = normalize_string(item.get("property_name"))
        property_type = normalize_string(item.get("property_type"))
        status = normalize_string(item.get("status"))
        config_path_raw = normalize_string(item.get("config_path"))
        deletion_protection = item.get("deletion_protection")

        if not property_id:
            reporter.error(
                "MISSING_PROPERTY_ID",
                "物业记录缺少 property_id。",
                entry_path,
            )
            continue

        if not PROPERTY_ID_PATTERN.fullmatch(property_id):
            reporter.error(
                "INVALID_PROPERTY_ID",
                (
                    f"property_id '{property_id}' 不符合规则。"
                    "只能使用小写英文字母、数字和连字符。"
                ),
                entry_path,
            )

        if property_id in seen_property_ids:
            reporter.error(
                "DUPLICATE_PROPERTY_ID",
                (
                    f"property_id '{property_id}' 重复，"
                    f"首次出现在索引 {seen_property_ids[property_id]}。"
                ),
                entry_path,
            )
        else:
            seen_property_ids[property_id] = index

        if not property_name:
            reporter.error(
                "MISSING_PROPERTY_NAME",
                f"物业 '{property_id}' 缺少 property_name。",
                entry_path,
            )

        if not property_type:
            reporter.error(
                "MISSING_PROPERTY_TYPE",
                f"物业 '{property_id}' 缺少 property_type。",
                entry_path,
            )
        elif property_type not in supported_property_types:
            reporter.error(
                "UNSUPPORTED_PROPERTY_TYPE",
                (
                    f"物业 '{property_id}' 的 property_type "
                    f"'{property_type}' 不在支持列表中。"
                ),
                entry_path,
            )

        if not status:
            reporter.error(
                "MISSING_PROPERTY_STATUS",
                f"物业 '{property_id}' 缺少 status。",
                entry_path,
            )
        elif status not in supported_statuses:
            reporter.error(
                "UNSUPPORTED_PROPERTY_STATUS",
                (
                    f"物业 '{property_id}' 的 status "
                    f"'{status}' 不在支持列表中。"
                ),
                entry_path,
            )

        if deletion_protection is not True:
            reporter.error(
                "DELETION_PROTECTION_DISABLED",
                (
                    f"物业 '{property_id}' 必须设置 "
                    "deletion_protection: true。"
                ),
                entry_path,
            )

        if not config_path_raw:
            reporter.error(
                "MISSING_CONFIG_PATH",
                f"物业 '{property_id}' 缺少 config_path。",
                entry_path,
            )
            continue

        config_path = (root / "17_Config" / config_path_raw).resolve()
        expected_parent = (
            root / "17_Config" / "properties"
        ).resolve()

        try:
            config_path.relative_to(expected_parent)
        except ValueError:
            reporter.error(
                "CONFIG_PATH_OUTSIDE_PROPERTIES",
                (
                    f"物业 '{property_id}' 的 config_path "
                    "必须位于 17_Config/properties/ 内。"
                ),
                entry_path,
            )
            continue

        if config_path.name != property_id:
            reporter.error(
                "PROPERTY_DIRECTORY_MISMATCH",
                (
                    f"物业目录名 '{config_path.name}' 与 "
                    f"property_id '{property_id}' 不一致。"
                ),
                config_path,
            )

        if not config_path.exists():
            reporter.error(
                "PROPERTY_DIRECTORY_NOT_FOUND",
                f"物业 '{property_id}' 的配置目录不存在。",
                config_path,
            )
            continue

        if not config_path.is_dir():
            reporter.error(
                "PROPERTY_PATH_NOT_DIRECTORY",
                f"物业 '{property_id}' 的 config_path 不是目录。",
                config_path,
            )
            continue

        property_paths[property_id] = config_path

    return property_paths


def validate_property_directories_against_registry(
    root: Path,
    registered_paths: dict[str, Path],
    reporter: ValidationReporter,
) -> None:
    """校验 properties 目录中是否存在未注册的正式物业目录。"""

    properties_root = root / "17_Config" / "properties"

    if not properties_root.exists():
        reporter.error(
            "PROPERTIES_DIRECTORY_NOT_FOUND",
            "17_Config/properties 目录不存在。",
            properties_root,
        )
        return

    if not properties_root.is_dir():
        reporter.error(
            "PROPERTIES_PATH_NOT_DIRECTORY",
            "17_Config/properties 不是目录。",
            properties_root,
        )
        return

    registered_directory_names = {
        path.name for path in registered_paths.values()
    }

    for path in sorted(properties_root.iterdir()):
        if not path.is_dir():
            continue

        # 忽略 template、_template、隐藏目录和系统目录。
        if is_ignored_property_directory(path):
            continue

        if path.name not in registered_directory_names:
            reporter.warning(
                "UNREGISTERED_PROPERTY_DIRECTORY",
                (
                    f"目录 '{path.name}' 未登记到 "
                    "17_Config/properties.yaml。"
                ),
                path,
            )


def validate_required_property_files(
    registry: dict[str, Any],
    property_paths: dict[str, Path],
    reporter: ValidationReporter,
) -> None:
    """校验每家正式物业所需配置文件是否齐全。"""

    required_files = set(
        registry.get("required_property_files")
        or DEFAULT_REQUIRED_PROPERTY_FILES
    )

    for property_id, property_path in property_paths.items():
        for filename in sorted(required_files):
            file_path = property_path / filename

            if not file_path.exists():
                reporter.error(
                    "REQUIRED_PROPERTY_FILE_MISSING",
                    (
                        f"物业 '{property_id}' 缺少必需文件 "
                        f"'{filename}'。"
                    ),
                    file_path,
                )
            elif not file_path.is_file():
                reporter.error(
                    "REQUIRED_PROPERTY_FILE_NOT_FILE",
                    (
                        f"物业 '{property_id}' 的 '{filename}' "
                        "不是普通文件。"
                    ),
                    file_path,
                )


def validate_property_file_identity(
    property_id: str,
    property_path: Path,
    reporter: ValidationReporter,
) -> None:
    """校验 hotel.yaml 中的物业身份与删除保护。"""

    hotel_path = property_path / "hotel.yaml"
    hotel_data = load_yaml_file(hotel_path, reporter)

    if not hotel_data:
        return

    file_property_id = normalize_string(
        get_nested(
            hotel_data,
            ("property", "property_id"),
        )
    )

    if not file_property_id:
        reporter.error(
            "HOTEL_FILE_MISSING_PROPERTY_ID",
            "hotel.yaml 缺少 property.property_id。",
            hotel_path,
        )
        return

    if file_property_id != property_id:
        reporter.error(
            "HOTEL_PROPERTY_ID_MISMATCH",
            (
                f"注册表 property_id 为 '{property_id}'，"
                f"hotel.yaml 中为 '{file_property_id}'。"
            ),
            hotel_path,
        )

    deletion_protection = get_nested(
        hotel_data,
        ("property", "deletion_protection"),
    )

    if deletion_protection is not True:
        reporter.error(
            "HOTEL_DELETION_PROTECTION_DISABLED",
            (
                f"物业 '{property_id}' 的 hotel.yaml 必须设置 "
                "property.deletion_protection: true。"
            ),
            hotel_path,
        )


def validate_cross_file_property_ids(
    property_id: str,
    property_path: Path,
    reporter: ValidationReporter,
) -> None:
    """校验所有物业级文件中的 property_id 是否一致。"""

    file_mappings = {
        "brand.yaml": ("brand", "property_id"),
        "website.yaml": ("website", "property_id"),
        "seo.yaml": ("seo", "property_id"),
        "ota.yaml": ("distribution", "property_id"),
    }

    for filename, key_path in file_mappings.items():
        file_path = property_path / filename
        data = load_yaml_file(file_path, reporter)

        if not data:
            continue

        file_property_id = normalize_string(
            get_nested(data, key_path)
        )

        if not file_property_id:
            reporter.error(
                "CONFIG_FILE_MISSING_PROPERTY_ID",
                (
                    f"{filename} 缺少 "
                    f"{'.'.join(key_path)}。"
                ),
                file_path,
            )
            continue

        if file_property_id != property_id:
            reporter.error(
                "CONFIG_PROPERTY_ID_MISMATCH",
                (
                    f"注册表 property_id 为 '{property_id}'，"
                    f"{filename} 中为 '{file_property_id}'。"
                ),
                file_path,
            )


def validate_all_yaml_files(
    property_paths: dict[str, Path],
    reporter: ValidationReporter,
) -> None:
    """校验所有正式物业 YAML 文件的语法。"""

    for property_path in property_paths.values():
        for yaml_path in sorted(property_path.glob("*.yaml")):
            load_yaml_file(yaml_path, reporter)


# ==========================================================
# 跨物业重复数据校验
# ==========================================================


def collect_canonical_domains(
    property_paths: dict[str, Path],
    reporter: ValidationReporter,
) -> None:
    """检测不同物业是否使用重复的主域名。"""

    seen_domains: dict[str, tuple[str, Path]] = {}

    for property_id, property_path in property_paths.items():
        website_path = property_path / "website.yaml"
        website_data = load_yaml_file(
            website_path,
            reporter,
        )

        if not website_data:
            continue

        candidates = [
            get_nested(
                website_data,
                ("domain", "primary_domain"),
            ),
            get_nested(
                website_data,
                ("domain", "canonical_base_url"),
            ),
        ]

        for candidate in candidates:
            domain = normalize_url(candidate)

            if not domain:
                continue

            if domain in seen_domains:
                previous_property_id, previous_path = (
                    seen_domains[domain]
                )

                if previous_property_id != property_id:
                    reporter.error(
                        "DUPLICATE_CANONICAL_DOMAIN",
                        (
                            f"域名 '{domain}' 同时被物业 "
                            f"'{previous_property_id}' 和 "
                            f"'{property_id}' 使用。"
                        ),
                        website_path,
                    )
                    reporter.info(
                        "DUPLICATE_DOMAIN_ORIGIN",
                        "首次出现位置。",
                        previous_path,
                    )
            else:
                seen_domains[domain] = (
                    property_id,
                    website_path,
                )


def collect_ota_identifiers(
    property_paths: dict[str, Path],
    reporter: ValidationReporter,
) -> None:
    """检测 OTA ID 和平台 URL 是否跨物业重复。"""

    seen_platform_ids: dict[
        tuple[str, str],
        tuple[str, Path],
    ] = {}

    seen_profile_urls: dict[str, tuple[str, Path]] = {}

    for property_id, property_path in property_paths.items():
        ota_path = property_path / "ota.yaml"
        ota_data = load_yaml_file(ota_path, reporter)

        if not ota_data:
            continue

        ota_platforms = get_nested(
            ota_data,
            ("ota", "platforms"),
            default={},
        )

        if isinstance(ota_platforms, dict):
            for platform_key, platform_data in ota_platforms.items():
                if not isinstance(platform_data, dict):
                    continue

                platform_property_id = normalize_string(
                    platform_data.get("property_id")
                )

                if platform_property_id:
                    unique_key = (
                        normalize_string(platform_key).lower(),
                        platform_property_id,
                    )

                    if unique_key in seen_platform_ids:
                        previous_property_id, previous_path = (
                            seen_platform_ids[unique_key]
                        )

                        if previous_property_id != property_id:
                            reporter.error(
                                "DUPLICATE_OTA_PROPERTY_ID",
                                (
                                    f"OTA 平台 '{platform_key}' 的 "
                                    f"property_id "
                                    f"'{platform_property_id}' "
                                    f"同时被物业 "
                                    f"'{previous_property_id}' 和 "
                                    f"'{property_id}' 使用。"
                                ),
                                ota_path,
                            )
                            reporter.info(
                                "DUPLICATE_OTA_ID_ORIGIN",
                                "首次出现位置。",
                                previous_path,
                            )
                    else:
                        seen_platform_ids[unique_key] = (
                            property_id,
                            ota_path,
                        )

        for key_path, value in walk_mapping(ota_data):
            if not key_path:
                continue

            key = key_path[-1]

            if key not in {
                "profile_url",
                "booking_url",
                "business_profile_url",
                "host_profile_url",
            }:
                continue

            url = normalize_url(value)

            if not url:
                continue

            if url in seen_profile_urls:
                previous_property_id, previous_path = (
                    seen_profile_urls[url]
                )

                if previous_property_id != property_id:
                    reporter.error(
                        "DUPLICATE_PLATFORM_PROFILE_URL",
                        (
                            f"平台地址 '{url}' 同时被物业 "
                            f"'{previous_property_id}' 和 "
                            f"'{property_id}' 使用。"
                        ),
                        ota_path,
                    )
                    reporter.info(
                        "DUPLICATE_PROFILE_URL_ORIGIN",
                        "首次出现位置。",
                        previous_path,
                    )
            else:
                seen_profile_urls[url] = (
                    property_id,
                    ota_path,
                )


# ==========================================================
# Git 删除与重命名保护
# ==========================================================


def run_git_command(
    root: Path,
    arguments: list[str],
) -> subprocess.CompletedProcess[str] | None:
    """执行 Git 命令。"""

    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        return None


def validate_git_base_ref(
    root: Path,
    base_ref: str | None,
    reporter: ValidationReporter,
) -> None:
    """检测相对 Git 基线的删除与重命名操作。"""

    if not base_ref:
        return

    inside_repo = run_git_command(
        root,
        ["rev-parse", "--is-inside-work-tree"],
    )

    if inside_repo is None:
        reporter.warning(
            "GIT_NOT_AVAILABLE",
            "系统未安装 Git，跳过 Git 删除保护检查。",
        )
        return

    if inside_repo.returncode != 0:
        reporter.warning(
            "NOT_A_GIT_REPOSITORY",
            "当前目录不是 Git 仓库，跳过 Git 删除保护检查。",
            root,
        )
        return

    verify_ref = run_git_command(
        root,
        ["rev-parse", "--verify", base_ref],
    )

    if verify_ref is None or verify_ref.returncode != 0:
        reporter.error(
            "INVALID_GIT_BASE_REF",
            f"无法解析 Git 基线 '{base_ref}'。",
            root,
        )
        return

    diff_result = run_git_command(
        root,
        [
            "diff",
            "--name-status",
            "--find-renames",
            f"{base_ref}...HEAD",
            "--",
            "17_Config/properties",
            "17_Config/properties.yaml",
        ],
    )

    if diff_result is None or diff_result.returncode != 0:
        reporter.error(
            "GIT_DIFF_FAILED",
            f"无法计算相对 '{base_ref}' 的配置变更。",
            root,
        )
        return

    for line in diff_result.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")
        status = parts[0]

        if status.startswith("D") and len(parts) >= 2:
            deleted_path = parts[1]
            deleted_path_object = Path(deleted_path)

            if deleted_path == "17_Config/properties.yaml":
                reporter.error(
                    "REGISTRY_DELETED",
                    "禁止删除多物业注册表。",
                    deleted_path,
                )
                continue

            path_parts = deleted_path_object.parts

            if len(path_parts) >= 3:
                property_directory_name = path_parts[2]

                if property_directory_name in {
                    "_template",
                    "template",
                    "_templates",
                    "templates",
                }:
                    reporter.warning(
                        "TEMPLATE_FILE_DELETED",
                        "检测到模板文件被删除，请确认是否为有意变更。",
                        deleted_path,
                    )
                    continue

            reporter.error(
                "PROTECTED_PROPERTY_FILE_DELETED",
                (
                    "检测到物业配置文件被删除。"
                    "永久删除必须经过仓库所有者明确授权。"
                ),
                deleted_path,
            )

        if status.startswith("R") and len(parts) >= 3:
            old_path = parts[1]
            new_path = parts[2]

            old_parts = Path(old_path).parts
            new_parts = Path(new_path).parts

            if (
                len(old_parts) >= 3
                and len(new_parts) >= 3
                and old_parts[:2]
                == ("17_Config", "properties")
                and new_parts[:2]
                == ("17_Config", "properties")
            ):
                old_property_id = old_parts[2]
                new_property_id = new_parts[2]

                ignored_names = {
                    "_template",
                    "template",
                    "_templates",
                    "templates",
                }

                if (
                    old_property_id not in ignored_names
                    and new_property_id not in ignored_names
                    and old_property_id != new_property_id
                ):
                    reporter.error(
                        "PROPERTY_DIRECTORY_RENAMED",
                        (
                            f"禁止将物业目录 '{old_property_id}' "
                            f"重命名为 '{new_property_id}'。"
                            "property_id 创建后必须保持稳定。"
                        ),
                        f"{old_path} -> {new_path}",
                    )


# ==========================================================
# 主程序
# ==========================================================


def main() -> int:
    args = parse_arguments()

    root = Path(args.root).resolve()
    registry_path = (root / args.registry).resolve()

    reporter = ValidationReporter(
        quiet=args.quiet,
    )

    if not root.exists():
        reporter.error(
            "ROOT_NOT_FOUND",
            "仓库根目录不存在。",
            root,
        )
        reporter.print_messages()
        return 2

    registry = load_yaml_file(
        registry_path,
        reporter,
    )

    if registry is None:
        reporter.print_messages()
        return 1

    validate_registry_deletion_protection(
        registry=registry,
        registry_path=registry_path,
        reporter=reporter,
    )

    properties = validate_registry_structure(
        registry=registry,
        registry_path=registry_path,
        reporter=reporter,
    )

    property_paths = validate_registry_entries(
        root=root,
        registry=registry,
        properties=properties,
        registry_path=registry_path,
        reporter=reporter,
    )

    validate_property_directories_against_registry(
        root=root,
        registered_paths=property_paths,
        reporter=reporter,
    )

    validate_required_property_files(
        registry=registry,
        property_paths=property_paths,
        reporter=reporter,
    )

    validate_all_yaml_files(
        property_paths=property_paths,
        reporter=reporter,
    )

    for property_id, property_path in property_paths.items():
        validate_property_file_identity(
            property_id=property_id,
            property_path=property_path,
            reporter=reporter,
        )

        validate_cross_file_property_ids(
            property_id=property_id,
            property_path=property_path,
            reporter=reporter,
        )

    collect_canonical_domains(
        property_paths=property_paths,
        reporter=reporter,
    )

    collect_ota_identifiers(
        property_paths=property_paths,
        reporter=reporter,
    )

    validate_git_base_ref(
        root=root,
        base_ref=args.base_ref,
        reporter=reporter,
    )

    reporter.print_messages()

    if reporter.error_count > 0:
        return 1

    if args.warnings_as_errors and reporter.warning_count > 0:
        return 1

    print("AIGOS 多物业配置校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())