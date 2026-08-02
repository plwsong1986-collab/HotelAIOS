#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HotelAIOS Validator Engine
File: 18_Validator/validate-properties.py
Version: 2.0.0
Updated: 2026-08-02

职责：
1. 定位 HotelAIOS 项目根目录。
2. 加载 17_Config/properties.yaml。
3. 使用 17_Config/schemas/*.schema.yaml 校验注册表和物业配置。
4. 执行目录、property_id、版本、房量、引用等跨文件校验。
5. 在终端输出中文报告，并可选生成 JSON 报告。

本程序只读取配置，不会自动修改、删除或覆盖任何文件。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "缺少依赖 PyYAML。请在项目根目录运行：uv add pyyaml"
    ) from exc

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:
    raise SystemExit(
        "缺少依赖 jsonschema。请在项目根目录运行：uv add jsonschema"
    ) from exc


VERSION = "2.0.0"

CONFIG_DIR_NAME = "17_Config"
REGISTRY_FILE_NAME = "properties.yaml"
PROPERTY_FILES = (
    "hotel.yaml",
    "brand.yaml",
    "website.yaml",
    "seo.yaml",
    "ota.yaml",
)
SCHEMA_MAP = {
    "properties.yaml": "properties.schema.yaml",
    "hotel.yaml": "hotel.schema.yaml",
    "brand.yaml": "brand.schema.yaml",
    "website.yaml": "website.schema.yaml",
    "seo.yaml": "seo.schema.yaml",
    "ota.yaml": "ota.schema.yaml",
}
PROPERTY_ID_PATHS = {
    "hotel.yaml": ("property", "property_id"),
    "brand.yaml": ("brand", "property_id"),
    "website.yaml": ("website", "property_id"),
    "seo.yaml": ("seo", "property_id"),
    "ota.yaml": ("ota", "property_id"),
}
SUPPORTED_LIFECYCLE_STATUSES = {"draft", "active", "inactive", "archived"}


@dataclass(frozen=True)
class Finding:
    """一条校验结果。"""

    level: str
    code: str
    message: str
    file: str = ""
    path: str = ""

    def display(self) -> str:
        location_parts = [item for item in (self.file, self.path) if item]
        location = f" [{': '.join(location_parts)}]" if location_parts else ""
        return f"{self.level} {self.code}{location}：{self.message}"


@dataclass
class ValidationSummary:
    """校验汇总。"""

    validator_version: str
    project_root: str
    started_at: str
    finished_at: str = ""
    properties_checked: int = 0
    files_checked: int = 0
    schemas_checked: int = 0
    findings: list[Finding] | None = None

    def __post_init__(self) -> None:
        if self.findings is None:
            self.findings = []

    @property
    def errors(self) -> int:
        return sum(1 for item in self.findings or [] if item.level == "错误")

    @property
    def warnings(self) -> int:
        return sum(1 for item in self.findings or [] if item.level == "警告")

    @property
    def passed(self) -> bool:
        return self.errors == 0


class HotelAIOSValidator:
    """HotelAIOS 配置校验器。"""

    def __init__(self, project_root: Path, strict: bool = False) -> None:
        self.project_root = project_root.resolve()
        self.strict = strict
        self.config_root = self.project_root / CONFIG_DIR_NAME
        self.registry_path = self.config_root / REGISTRY_FILE_NAME
        self.properties_root = self.config_root / "properties"
        self.schemas_root = self.config_root / "schemas"
        self.summary = ValidationSummary(
            validator_version=VERSION,
            project_root=str(self.project_root),
            started_at=datetime.now().astimezone().isoformat(timespec="seconds"),
        )
        self._yaml_cache: dict[Path, Any] = {}
        self._schema_cache: dict[Path, Any] = {}

    def add(
        self,
        level: str,
        code: str,
        message: str,
        file: Path | str | None = None,
        path: str = "",
    ) -> None:
        relative_file = ""
        if file:
            file_path = Path(file)
            try:
                relative_file = file_path.resolve().relative_to(
                    self.project_root
                ).as_posix()
            except (ValueError, OSError):
                relative_file = str(file)
        self.summary.findings.append(
            Finding(
                level=level,
                code=code,
                message=message,
                file=relative_file,
                path=path,
            )
        )

    def validate(self) -> ValidationSummary:
        """执行完整校验。"""

        self._validate_foundation()
        if self.summary.errors:
            self.summary.finished_at = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
            return self.summary

        registry = self._load_yaml(self.registry_path)
        if registry is None:
            self.summary.finished_at = datetime.now().astimezone().isoformat(
                timespec="seconds"
            )
            return self.summary

        self._validate_with_schema(self.registry_path, registry)
        property_records = self._extract_property_records(registry)
        self._validate_registry_records(property_records)
        self._validate_registered_properties(property_records)
        self._validate_unregistered_directories(property_records)

        self.summary.finished_at = datetime.now().astimezone().isoformat(
            timespec="seconds"
        )
        return self.summary

    def _validate_foundation(self) -> None:
        required_paths = (
            self.config_root,
            self.registry_path,
            self.properties_root,
            self.schemas_root,
        )
        for path in required_paths:
            if not path.exists():
                self.add(
                    "错误",
                    "REQUIRED_PATH_MISSING",
                    "必需路径不存在。",
                    path,
                )

        for config_name, schema_name in SCHEMA_MAP.items():
            schema_path = self.schemas_root / schema_name
            if not schema_path.is_file():
                self.add(
                    "错误",
                    "SCHEMA_FILE_MISSING",
                    f"{config_name} 对应的 Schema 不存在：{schema_name}",
                    schema_path,
                )

    def _load_yaml(self, path: Path) -> Any | None:
        if path in self._yaml_cache:
            return self._yaml_cache[path]

        if not path.is_file():
            self.add("错误", "YAML_FILE_MISSING", "YAML 文件不存在。", path)
            return None

        try:
            with path.open("r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
        except UnicodeDecodeError as exc:
            self.add(
                "错误",
                "INVALID_ENCODING",
                f"文件不是有效的 UTF-8：{exc}",
                path,
            )
            return None
        except yaml.YAMLError as exc:
            self.add(
                "错误",
                "INVALID_YAML",
                f"YAML 语法错误：{exc}",
                path,
            )
            return None
        except OSError as exc:
            self.add(
                "错误",
                "FILE_READ_FAILED",
                f"读取文件失败：{exc}",
                path,
            )
            return None

        if data is None:
            self.add("错误", "EMPTY_YAML", "YAML 文件内容为空。", path)
            return None
        if not isinstance(data, dict):
            self.add(
                "错误",
                "INVALID_YAML_ROOT",
                "YAML 顶层必须是对象（mapping）。",
                path,
            )
            return None

        self._yaml_cache[path] = data
        self.summary.files_checked += 1
        return data

    def _load_schema(self, path: Path) -> Any | None:
        if path in self._schema_cache:
            return self._schema_cache[path]

        schema = self._load_yaml(path)
        if schema is None:
            return None

        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            schema_path = ".".join(str(item) for item in exc.path)
            self.add(
                "错误",
                "INVALID_SCHEMA",
                f"Schema 本身无效：{exc.message}",
                path,
                schema_path,
            )
            return None

        self._schema_cache[path] = schema
        self.summary.schemas_checked += 1
        return schema

    def _validate_with_schema(self, config_path: Path, data: dict[str, Any]) -> None:
        schema_name = SCHEMA_MAP.get(config_path.name)
        if not schema_name:
            self.add(
                "警告",
                "SCHEMA_MAPPING_MISSING",
                "未找到该配置文件的 Schema 映射。",
                config_path,
            )
            return

        schema_path = self.schemas_root / schema_name
        schema = self._load_schema(schema_path)
        if schema is None:
            return

        validator = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
        errors = sorted(
            validator.iter_errors(data),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
        for error in errors:
            data_path = self._format_json_path(error.absolute_path)
            self.add(
                "错误",
                "SCHEMA_VALIDATION_ERROR",
                error.message,
                config_path,
                data_path,
            )

    def _extract_property_records(
        self, registry: dict[str, Any]
    ) -> list[dict[str, Any]]:
        records = registry.get("properties")
        if records is None:
            self.add(
                "错误",
                "MISSING_PROPERTIES_LIST",
                "注册表缺少 properties 列表。",
                self.registry_path,
                "properties",
            )
            return []
        if not isinstance(records, list):
            self.add(
                "错误",
                "INVALID_PROPERTIES_LIST",
                "properties 必须是列表。",
                self.registry_path,
                "properties",
            )
            return []
        if not records:
            self.add(
                "警告",
                "EMPTY_PROPERTIES_LIST",
                "当前注册表中尚未登记任何正式物业。",
                self.registry_path,
                "properties",
            )
        return [item for item in records if isinstance(item, dict)]

    def _validate_registry_records(
        self, records: list[dict[str, Any]]
    ) -> None:
        seen_ids: set[str] = set()
        seen_paths: set[str] = set()

        for index, record in enumerate(records):
            base_path = f"properties[{index}]"
            property_id = record.get("property_id")
            config_path = record.get("config_path")
            status = record.get("status")
            deletion_protection = record.get("deletion_protection")

            if not isinstance(property_id, str) or not property_id.strip():
                self.add(
                    "错误",
                    "MISSING_PROPERTY_ID",
                    "物业记录缺少有效的 property_id。",
                    self.registry_path,
                    f"{base_path}.property_id",
                )
                continue

            if property_id in seen_ids:
                self.add(
                    "错误",
                    "DUPLICATE_PROPERTY_ID",
                    f"property_id 重复：{property_id}",
                    self.registry_path,
                    f"{base_path}.property_id",
                )
            seen_ids.add(property_id)

            if not isinstance(config_path, str) or not config_path.strip():
                self.add(
                    "错误",
                    "MISSING_CONFIG_PATH",
                    f"物业 {property_id} 缺少 config_path。",
                    self.registry_path,
                    f"{base_path}.config_path",
                )
            elif config_path in seen_paths:
                self.add(
                    "错误",
                    "DUPLICATE_CONFIG_PATH",
                    f"config_path 重复：{config_path}",
                    self.registry_path,
                    f"{base_path}.config_path",
                )
            else:
                seen_paths.add(config_path)

            if status not in SUPPORTED_LIFECYCLE_STATUSES:
                self.add(
                    "错误",
                    "UNSUPPORTED_PROPERTY_STATUS",
                    f"物业 {property_id} 使用了不支持的状态：{status!r}。",
                    self.registry_path,
                    f"{base_path}.status",
                )

            if deletion_protection is not True:
                self.add(
                    "错误",
                    "DELETION_PROTECTION_REQUIRED",
                    f"物业 {property_id} 必须启用 deletion_protection。",
                    self.registry_path,
                    f"{base_path}.deletion_protection",
                )

    def _validate_registered_properties(
        self, records: list[dict[str, Any]]
    ) -> None:
        for record in records:
            property_id = record.get("property_id")
            config_path = record.get("config_path")
            if not isinstance(property_id, str) or not isinstance(config_path, str):
                continue

            property_dir = self._resolve_config_path(config_path)
            self.summary.properties_checked += 1

            if not property_dir.is_dir():
                self.add(
                    "错误",
                    "PROPERTY_DIRECTORY_MISSING",
                    f"物业目录不存在：{config_path}",
                    property_dir,
                )
                continue

            if property_dir.name != property_id:
                self.add(
                    "错误",
                    "PROPERTY_DIRECTORY_ID_MISMATCH",
                    (
                        f"目录名 {property_dir.name!r} 与 property_id "
                        f"{property_id!r} 不一致。"
                    ),
                    property_dir,
                )

            loaded_configs: dict[str, dict[str, Any]] = {}
            for file_name in PROPERTY_FILES:
                config_file = property_dir / file_name
                if not config_file.is_file():
                    self.add(
                        "错误",
                        "REQUIRED_PROPERTY_FILE_MISSING",
                        f"物业缺少必需文件：{file_name}",
                        config_file,
                    )
                    continue

                data = self._load_yaml(config_file)
                if data is None:
                    continue
                loaded_configs[file_name] = data
                self._validate_with_schema(config_file, data)
                self._validate_cross_file_property_id(
                    property_id,
                    file_name,
                    config_file,
                    data,
                )

            self._validate_hotel_business_rules(
                property_id,
                property_dir,
                loaded_configs.get("hotel.yaml"),
            )
            self._validate_file_references(property_dir, loaded_configs)
            self._validate_version_consistency(property_dir, loaded_configs)

    def _validate_cross_file_property_id(
        self,
        expected_property_id: str,
        file_name: str,
        config_file: Path,
        data: dict[str, Any],
    ) -> None:
        key_path = PROPERTY_ID_PATHS[file_name]
        actual = self._get_nested(data, key_path)

        if actual is None:
            self.add(
                "错误",
                "CONFIG_FILE_MISSING_PROPERTY_ID",
                f"{file_name} 缺少 {'.'.join(key_path)}。",
                config_file,
                ".".join(key_path),
            )
        elif actual != expected_property_id:
            self.add(
                "错误",
                "CROSS_FILE_PROPERTY_ID_MISMATCH",
                (
                    f"{file_name} 中的 property_id 为 {actual!r}，"
                    f"应为 {expected_property_id!r}。"
                ),
                config_file,
                ".".join(key_path),
            )

    def _validate_hotel_business_rules(
        self,
        property_id: str,
        property_dir: Path,
        hotel: dict[str, Any] | None,
    ) -> None:
        if not hotel:
            return

        hotel_path = property_dir / "hotel.yaml"
        total_rooms = self._get_nested(hotel, ("accommodation", "total_rooms"))
        total_room_types = self._get_nested(
            hotel, ("accommodation", "total_room_types")
        )
        room_types = self._get_nested(hotel, ("accommodation", "room_types"))

        if isinstance(room_types, list):
            quantities: list[int] = []
            room_ids: list[str] = []
            for room in room_types:
                if not isinstance(room, dict):
                    continue
                quantity = room.get("quantity")
                if isinstance(quantity, int):
                    quantities.append(quantity)
                room_id = room.get("room_type_id")
                if isinstance(room_id, str):
                    room_ids.append(room_id)

            if isinstance(total_rooms, int) and sum(quantities) != total_rooms:
                self.add(
                    "错误",
                    "ROOM_INVENTORY_TOTAL_MISMATCH",
                    (
                        f"物业 {property_id} 的房型数量合计为 "
                        f"{sum(quantities)}，但 total_rooms 为 {total_rooms}。"
                    ),
                    hotel_path,
                    "accommodation",
                )

            if (
                isinstance(total_room_types, int)
                and len(room_types) != total_room_types
            ):
                self.add(
                    "错误",
                    "ROOM_TYPE_COUNT_MISMATCH",
                    (
                        f"room_types 实际有 {len(room_types)} 项，"
                        f"但 total_room_types 为 {total_room_types}。"
                    ),
                    hotel_path,
                    "accommodation",
                )

            duplicate_room_ids = self._find_duplicates(room_ids)
            for room_id in sorted(duplicate_room_ids):
                self.add(
                    "错误",
                    "DUPLICATE_ROOM_TYPE_ID",
                    f"房型 ID 重复：{room_id}",
                    hotel_path,
                    "accommodation.room_types",
                )

        metadata_version = self._get_nested(
            hotel, ("metadata", "file_version")
        )
        configuration_version = self._get_nested(
            hotel, ("configuration", "file_version")
        )
        if (
            metadata_version is not None
            and configuration_version is not None
            and metadata_version != configuration_version
        ):
            self.add(
                "错误",
                "FILE_VERSION_MISMATCH",
                (
                    f"metadata.file_version={metadata_version!r} 与 "
                    f"configuration.file_version={configuration_version!r} 不一致。"
                ),
                hotel_path,
            )

    def _validate_file_references(
        self,
        property_dir: Path,
        configs: dict[str, dict[str, Any]],
    ) -> None:
        for file_name, data in configs.items():
            references = data.get("references")
            if not isinstance(references, dict):
                continue

            for reference_name, reference_value in references.items():
                if not isinstance(reference_value, str) or not reference_value:
                    continue
                if ":" in reference_value:
                    # 字段引用，例如 hotel.yaml:contact.phone.primary。
                    target_file = reference_value.split(":", maxsplit=1)[0]
                else:
                    target_file = reference_value

                if target_file.endswith((".yaml", ".yml")):
                    target_path = (property_dir / target_file).resolve()
                    if not target_path.exists():
                        self.add(
                            "错误",
                            "BROKEN_FILE_REFERENCE",
                            (
                                f"{file_name} 的引用 {reference_name!r} "
                                f"指向不存在的文件：{target_file}"
                            ),
                            property_dir / file_name,
                            f"references.{reference_name}",
                        )

    def _validate_version_consistency(
        self,
        property_dir: Path,
        configs: dict[str, dict[str, Any]],
    ) -> None:
        versions: dict[str, str] = {}
        for file_name, data in configs.items():
            version = self._get_nested(data, ("metadata", "file_version"))
            if isinstance(version, str):
                versions[file_name] = version

        unique_versions = set(versions.values())
        if len(unique_versions) > 1:
            message = "；".join(
                f"{file_name}={version}"
                for file_name, version in sorted(versions.items())
            )
            level = "错误" if self.strict else "警告"
            self.add(
                level,
                "PROPERTY_FILE_VERSION_INCONSISTENT",
                f"同一物业的配置文件版本不一致：{message}",
                property_dir,
            )

    def _validate_unregistered_directories(
        self, records: list[dict[str, Any]]
    ) -> None:
        registered_ids = {
            record.get("property_id")
            for record in records
            if isinstance(record.get("property_id"), str)
        }

        if not self.properties_root.is_dir():
            return

        ignored_names = {"_template", "template", ".gitkeep"}
        for child in sorted(self.properties_root.iterdir()):
            if not child.is_dir() or child.name in ignored_names:
                continue
            if child.name not in registered_ids:
                self.add(
                    "警告",
                    "UNREGISTERED_PROPERTY_DIRECTORY",
                    "目录存在，但未在 properties.yaml 中登记。",
                    child,
                )

    def _resolve_config_path(self, config_path: str) -> Path:
        path = Path(config_path)
        if path.is_absolute():
            return path
        # Registry 路径约定相对于 17_Config。
        return (self.config_root / path).resolve()

    @staticmethod
    def _get_nested(data: Any, path: Iterable[str]) -> Any:
        current = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    @staticmethod
    def _format_json_path(path: Iterable[Any]) -> str:
        result = "$"
        for part in path:
            if isinstance(part, int):
                result += f"[{part}]"
            else:
                result += f".{part}"
        return result

    @staticmethod
    def _find_duplicates(values: Iterable[str]) -> set[str]:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for value in values:
            if value in seen:
                duplicates.add(value)
            seen.add(value)
        return duplicates


def find_project_root(start: Path) -> Path:
    """从指定位置向上查找 HotelAIOS 项目根目录。"""

    current = start.resolve()
    candidates = (current, *current.parents)

    for candidate in candidates:
        config_root = candidate / CONFIG_DIR_NAME
        if (
            config_root.is_dir()
            and (config_root / REGISTRY_FILE_NAME).is_file()
        ):
            return candidate

    raise FileNotFoundError(
        f"无法从 {start} 向上找到包含 "
        f"{CONFIG_DIR_NAME}/{REGISTRY_FILE_NAME} 的项目根目录。"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="校验 HotelAIOS 多物业配置、Schema 与跨文件一致性。"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="HotelAIOS 项目根目录。默认从当前目录自动查找。",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：将部分一致性警告升级为错误。",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="可选：把完整结果写入 JSON 报告。",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def write_json_report(path: Path, summary: ValidationSummary) -> None:
    report = asdict(summary)
    report["errors"] = summary.errors
    report["warnings"] = summary.warnings
    report["passed"] = summary.passed

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_summary(summary: ValidationSummary) -> None:
    print("=" * 72)
    print(f"HotelAIOS 配置校验器 v{summary.validator_version}")
    print("=" * 72)

    if summary.findings:
        for finding in summary.findings:
            print(finding.display())
    else:
        print("未发现错误或警告。")

    print("-" * 72)
    print(f"已检查物业：{summary.properties_checked}")
    print(f"已读取文件：{summary.files_checked}")
    print(f"已验证 Schema：{summary.schemas_checked}")
    print(
        f"校验完成：{summary.errors} 个错误，"
        f"{summary.warnings} 个警告。"
    )

    if summary.passed:
        print("HotelAIOS 多物业配置校验通过。")
    else:
        print("HotelAIOS 多物业配置校验失败。请先修复错误。")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        root = args.root.resolve() if args.root else find_project_root(Path.cwd())
    except FileNotFoundError as exc:
        print(f"错误 PROJECT_ROOT_NOT_FOUND：{exc}", file=sys.stderr)
        return 2

    validator = HotelAIOSValidator(root, strict=args.strict)
    summary = validator.validate()
    print_summary(summary)

    if args.report:
        try:
            write_json_report(args.report, summary)
            print(f"JSON 报告已生成：{args.report.resolve()}")
        except OSError as exc:
            print(f"错误 REPORT_WRITE_FAILED：{exc}", file=sys.stderr)
            return 2

    return 0 if summary.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
