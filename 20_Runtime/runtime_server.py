#!/usr/bin/env python3
"""
HotelAIOS Runtime Server
File: 20_Runtime/runtime_server.py
Version: 1.1.0
Updated: 2026-08-03

功能：
1. 使用 runtime_loader.py 建立内存缓存。
2. 提供健康检查、物业列表、物业 Bundle 与单模块查询接口。
3. 支持手动刷新全部物业或指定物业。
4. 只读取 19_Automation/output，不修改任何源文件。
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    import uvicorn
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
except ImportError as exc:
    raise SystemExit(
        "缺少 Runtime 依赖。请在项目根目录运行：uv add fastapi uvicorn"
    ) from exc

from runtime_loader import (
    RuntimeDataError,
    RuntimeLoader,
    RuntimeLoaderError,
    RuntimeModuleNotFoundError,
    RuntimePropertyNotFoundError,
    find_project_root,
)

VERSION = "1.1.0"


def create_app(project_root: Path) -> FastAPI:
    loader = RuntimeLoader(project_root, auto_load=True)

    app = FastAPI(
        title="HotelAIOS Runtime API",
        version=VERSION,
        description="HotelAIOS 只读物业运行时数据接口。",
    )

    @app.get("/")
    def root() -> dict[str, Any]:
        return {
            "service": "HotelAIOS Runtime API",
            "version": VERSION,
            "status": "running",
            "docs": "/docs",
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return loader.health()

    @app.get("/api/v1/properties")
    def list_properties() -> dict[str, Any]:
        property_ids = loader.property_ids()
        return {
            "count": len(property_ids),
            "properties": property_ids,
        }

    @app.get("/api/v1/properties/{property_id}")
    def get_property(property_id: str) -> JSONResponse:
        try:
            data = loader.get_property(property_id)
        except RuntimePropertyNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeLoaderError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        return JSONResponse(content=data)

    @app.get("/api/v1/properties/{property_id}/state")
    def get_property_state(property_id: str) -> JSONResponse:
        try:
            data = loader.get_state(property_id)
        except RuntimePropertyNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return JSONResponse(content=data)

    @app.get("/api/v1/properties/{property_id}/modules/{module}")
    def get_property_module(
        property_id: str,
        module: str,
    ) -> JSONResponse:
        try:
            data = loader.get_module(property_id, module)
        except RuntimePropertyNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeModuleNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeDataError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        return JSONResponse(content=data)

    @app.post("/api/v1/runtime/reload")
    def reload_all() -> dict[str, Any]:
        try:
            states = loader.reload_all()
        except RuntimeLoaderError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        return {
            "status": "reloaded",
            "properties": len(states),
            "health": loader.health(),
        }

    @app.post("/api/v1/runtime/reload/{property_id}")
    def reload_property(property_id: str) -> dict[str, Any]:
        try:
            state = loader.reload_property(property_id)
        except RuntimePropertyNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeLoaderError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

        return {
            "status": "reloaded",
            "property_id": property_id,
            "ready": state.ready,
            "loaded_modules": list(state.loaded_modules),
            "missing_modules": list(state.missing_modules),
            "loaded_at": state.loaded_at,
        }

    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="启动 HotelAIOS Runtime API。")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="HotelAIOS 项目根目录；默认自动查找。",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="监听地址，默认 127.0.0.1。",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="监听端口，默认 8000。",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        project_root = (
            args.root.resolve() if args.root else find_project_root(Path.cwd())
        )
    except RuntimeLoaderError as exc:
        print(f"错误：{exc}")
        return 1

    app = create_app(project_root)

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
