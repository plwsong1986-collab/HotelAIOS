#!/usr/bin/env python3
"""
HotelAIOS Runtime Loader
File: 20_Runtime/runtime_loader.py
Version: 1.0.0
Updated: 2026-08-03

只读加载 19_Automation/output 下的物业运行时 JSON，
建立内存缓存，并提供查询、刷新与状态接口。
"""

from __future__ import annotations

import json
import threading
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final

VERSION: Final = "1.0.0"
OUTPUT_ROOT: Final = Path("19_Automation") / "output"

MODULE_FILES: Final[dict[str, tuple[str, ...]]] = {
    "property": (
        "property/{property_id}/property.json",
        "property/{property_id}.json",
        "property/sanlitian-property-config.json",
    ),
    "website": ("website/{property_id}/website.json",),
    "seo": ("seo/{property_id}/seo.json",),
    "ota": ("ota/{property_id}/ota.json",),
    "prompt": (
        "prompt/{property_id}/ai_prompt.json",
        "prompt/{property_id}/prompt.json",
        "prompt/ai_prompt.json",
    ),
}


class RuntimeLoaderError(RuntimeError):
    """Runtime Loader 基础异常。"""


class RuntimePropertyNotFoundError(RuntimeLoaderError):
    """指定物业不存在。"""


class RuntimeModuleNotFoundError(RuntimeLoaderError):
    """指定运行时模块不存在。"""


class RuntimeDataError(RuntimeLoaderError):
    """运行时 JSON 无效。"""


@dataclass(frozen=True)
class ModuleState:
    module: str
    path: str
    loaded: bool
    modified_at: str | None
    size_bytes: int | None
    error: str | None = None


@dataclass(frozen=True)
class PropertyState:
    property_id: str
    ready: bool
    loaded_modules: tuple[str, ...]
    missing_modules: tuple[str, ...]
    loaded_at: str


def find_project_root(start: Path) -> Path:
    """从当前目录向上查找 HotelAIOS 项目根目录。"""
    current = start.resolve()

    for candidate in (current, *current.parents):
        if (candidate / "17_Config" / "properties.yaml").is_file() and (
            candidate / OUTPUT_ROOT
        ).is_dir():
            return candidate

    raise RuntimeLoaderError(f"无法从 {start} 向上找到 HotelAIOS 项目根目录。")


class RuntimeLoader:
    """
    HotelAIOS 只读运行时加载器。

    线程安全；读取结果缓存在内存中。
    所有公开读取方法默认返回深拷贝，防止调用方修改缓存。
    """

    def __init__(
        self,
        project_root: Path,
        *,
        required_modules: tuple[str, ...] = ("website", "seo", "ota"),
        auto_load: bool = True,
    ) -> None:
        self.project_root = project_root.resolve()
        self.output_root = self.project_root / OUTPUT_ROOT
        self.required_modules = required_modules

        self._lock = threading.RLock()
        self._cache: dict[str, dict[str, dict[str, Any]]] = {}
        self._states: dict[str, PropertyState] = {}
        self._module_states: dict[str, dict[str, ModuleState]] = {}
        self._last_reload_at: str | None = None

        if not self.output_root.is_dir():
            raise RuntimeLoaderError(f"运行时输出目录不存在：{self.output_root}")

        unknown = set(required_modules) - set(MODULE_FILES)
        if unknown:
            raise RuntimeLoaderError(f"不支持的必需模块：{', '.join(sorted(unknown))}")

        if auto_load:
            self.reload_all()

    @staticmethod
    def _now() -> str:
        return datetime.now().astimezone().isoformat(timespec="seconds")

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as stream:
                data = json.load(stream)
        except FileNotFoundError:
            raise
        except json.JSONDecodeError as exc:
            raise RuntimeDataError(f"JSON 文件无效：{path}；{exc}") from exc
        except OSError as exc:
            raise RuntimeDataError(f"无法读取 JSON：{path}；{exc}") from exc

        if not isinstance(data, dict):
            raise RuntimeDataError(f"JSON 顶层必须是对象：{path}")

        return data

    def _candidate_paths(
        self,
        property_id: str,
        module: str,
    ) -> tuple[Path, ...]:
        patterns = MODULE_FILES.get(module)
        if patterns is None:
            raise RuntimeModuleNotFoundError(f"不支持的运行时模块：{module}")

        return tuple(
            self.output_root / pattern.format(property_id=property_id)
            for pattern in patterns
        )

    def _resolve_module_path(
        self,
        property_id: str,
        module: str,
    ) -> Path | None:
        for path in self._candidate_paths(property_id, module):
            if path.is_file():
                return path
        return None

    def discover_property_ids(self) -> list[str]:
        """从 Website、SEO、OTA 等标准输出目录发现物业。"""
        discovered: set[str] = set()

        for module in ("website", "seo", "ota"):
            module_root = self.output_root / module
            if not module_root.is_dir():
                continue

            for child in module_root.iterdir():
                if child.is_dir():
                    expected = child / f"{module}.json"
                    if expected.is_file():
                        discovered.add(child.name)

        property_root = self.output_root / "property"
        if property_root.is_dir():
            for child in property_root.iterdir():
                if child.is_dir():
                    discovered.add(child.name)

        return sorted(discovered)

    def _load_property_uncached(
        self,
        property_id: str,
    ) -> tuple[
        dict[str, dict[str, Any]],
        PropertyState,
        dict[str, ModuleState],
    ]:
        loaded: dict[str, dict[str, Any]] = {}
        module_states: dict[str, ModuleState] = {}
        missing: list[str] = []

        for module in MODULE_FILES:
            path = self._resolve_module_path(property_id, module)

            if path is None:
                if module in self.required_modules:
                    missing.append(module)

                module_states[module] = ModuleState(
                    module=module,
                    path="",
                    loaded=False,
                    modified_at=None,
                    size_bytes=None,
                )
                continue

            try:
                data = self._read_json(path)
                stat = path.stat()
                loaded[module] = data
                module_states[module] = ModuleState(
                    module=module,
                    path=str(path.relative_to(self.project_root)),
                    loaded=True,
                    modified_at=datetime.fromtimestamp(stat.st_mtime)
                    .astimezone()
                    .isoformat(timespec="seconds"),
                    size_bytes=stat.st_size,
                )
            except (RuntimeDataError, OSError) as exc:
                if module in self.required_modules:
                    missing.append(module)

                module_states[module] = ModuleState(
                    module=module,
                    path=str(path.relative_to(self.project_root)),
                    loaded=False,
                    modified_at=None,
                    size_bytes=None,
                    error=str(exc),
                )

        loaded_at = self._now()
        state = PropertyState(
            property_id=property_id,
            ready=not missing,
            loaded_modules=tuple(sorted(loaded)),
            missing_modules=tuple(sorted(set(missing))),
            loaded_at=loaded_at,
        )
        return loaded, state, module_states

    def reload_property(self, property_id: str) -> PropertyState:
        """重新加载指定物业并原子替换缓存。"""
        if not property_id or "/" in property_id or "\\" in property_id:
            raise RuntimeLoaderError(f"无效 property_id：{property_id!r}")

        discovered = set(self.discover_property_ids())
        if property_id not in discovered:
            raise RuntimePropertyNotFoundError(f"未发现物业运行时输出：{property_id}")

        loaded, state, module_states = self._load_property_uncached(property_id)

        with self._lock:
            self._cache[property_id] = loaded
            self._states[property_id] = state
            self._module_states[property_id] = module_states
            self._last_reload_at = self._now()

        return state

    def reload_all(self) -> dict[str, PropertyState]:
        """重新发现并加载全部物业。"""
        property_ids = self.discover_property_ids()

        new_cache: dict[str, dict[str, dict[str, Any]]] = {}
        new_states: dict[str, PropertyState] = {}
        new_module_states: dict[str, dict[str, ModuleState]] = {}

        for property_id in property_ids:
            loaded, state, module_states = self._load_property_uncached(property_id)
            new_cache[property_id] = loaded
            new_states[property_id] = state
            new_module_states[property_id] = module_states

        with self._lock:
            self._cache = new_cache
            self._states = new_states
            self._module_states = new_module_states
            self._last_reload_at = self._now()

        return deepcopy(new_states)

    def property_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._cache)

    def has_property(self, property_id: str) -> bool:
        with self._lock:
            return property_id in self._cache

    def get_property(
        self,
        property_id: str,
        *,
        require_ready: bool = False,
    ) -> dict[str, Any]:
        """
        返回单物业 Runtime Bundle。

        require_ready=True 时，缺少必需模块会抛出异常。
        """
        with self._lock:
            modules = self._cache.get(property_id)
            state = self._states.get(property_id)

            if modules is None or state is None:
                raise RuntimePropertyNotFoundError(f"物业不存在：{property_id}")

            if require_ready and not state.ready:
                raise RuntimeLoaderError(
                    f"物业尚未就绪：{property_id}；"
                    f"缺少模块：{', '.join(state.missing_modules)}"
                )

            return deepcopy(
                {
                    "property_id": property_id,
                    "runtime_loader_version": VERSION,
                    "ready": state.ready,
                    "loaded_at": state.loaded_at,
                    "loaded_modules": list(state.loaded_modules),
                    "missing_modules": list(state.missing_modules),
                    "modules": modules,
                }
            )

    def get_module(
        self,
        property_id: str,
        module: str,
    ) -> dict[str, Any]:
        with self._lock:
            property_data = self._cache.get(property_id)
            if property_data is None:
                raise RuntimePropertyNotFoundError(f"物业不存在：{property_id}")

            if module not in MODULE_FILES:
                raise RuntimeModuleNotFoundError(f"不支持的运行时模块：{module}")

            data = property_data.get(module)
            if data is None:
                raise RuntimeModuleNotFoundError(
                    f"物业 {property_id} 缺少运行时模块：{module}"
                )

            return deepcopy(data)

    def get_state(self, property_id: str) -> dict[str, Any]:
        with self._lock:
            state = self._states.get(property_id)
            module_states = self._module_states.get(property_id)

            if state is None or module_states is None:
                raise RuntimePropertyNotFoundError(f"物业不存在：{property_id}")

            return {
                "property_id": state.property_id,
                "ready": state.ready,
                "loaded_modules": list(state.loaded_modules),
                "missing_modules": list(state.missing_modules),
                "loaded_at": state.loaded_at,
                "modules": {
                    name: {
                        "module": item.module,
                        "path": item.path,
                        "loaded": item.loaded,
                        "modified_at": item.modified_at,
                        "size_bytes": item.size_bytes,
                        "error": item.error,
                    }
                    for name, item in module_states.items()
                },
            }

    def health(self) -> dict[str, Any]:
        with self._lock:
            property_count = len(self._cache)
            ready_count = sum(1 for state in self._states.values() if state.ready)
            return {
                "status": ("healthy" if property_count == ready_count else "degraded"),
                "runtime_loader_version": VERSION,
                "project_root": str(self.project_root),
                "output_root": str(self.output_root),
                "properties": property_count,
                "ready_properties": ready_count,
                "last_reload_at": self._last_reload_at,
            }


def create_runtime_loader(
    project_root: Path | None = None,
    *,
    required_modules: tuple[str, ...] = ("website", "seo", "ota"),
    auto_load: bool = True,
) -> RuntimeLoader:
    """创建标准 RuntimeLoader 实例。"""
    root = (
        project_root.resolve()
        if project_root is not None
        else find_project_root(Path.cwd())
    )
    return RuntimeLoader(
        root,
        required_modules=required_modules,
        auto_load=auto_load,
    )


if __name__ == "__main__":
    loader = create_runtime_loader()
    print(json.dumps(loader.health(), ensure_ascii=False, indent=2))
