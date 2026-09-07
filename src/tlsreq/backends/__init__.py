from __future__ import annotations

from importlib import import_module
from typing import Any, Optional

from ..errors import UnknownBackend
from .base import AsyncBackend, SyncBackend

_ALIASES = {
    "curl": "curl_cffi",
    "cffi": "curl_cffi",
    "nirequest": "niquests",
    "nirequests": "niquests",
    "nio": "niquests",
}

_BACKENDS = {
    "curl_cffi": ("curl_cffi", "CurlCffiSync", "CurlCffiAsync"),
    "wreq": ("wreq", "WreqSync", "WreqAsync"),
    "niquests": ("niquests", "NiquestsSync", "NiquestsAsync"),
    "httpx": ("httpx", "HttpxSync", "HttpxAsync"),
}


def _normalize_backend(name: str) -> str:
    key = name.strip().lower().replace("-", "_")
    return _ALIASES.get(key, key)


def _backend_class(backend: str, is_async: bool) -> type:
    name = _normalize_backend(backend)
    spec = _BACKENDS.get(name)
    if spec is None:
        raise UnknownBackend(
            f"未知 backend {backend!r}。可选: curl_cffi, wreq, niquests, httpx"
        )
    module_name, sync_name, async_name = spec
    module = import_module(f".{module_name}", __package__)
    return getattr(module, async_name if is_async else sync_name)


def create_sync_backend(
    backend: str,
    impersonate: Optional[str] = None,
    **kwargs: Any,
) -> SyncBackend:
    return _backend_class(backend, False)(impersonate=impersonate, **kwargs)


def create_async_backend(
    backend: str,
    impersonate: Optional[str] = None,
    **kwargs: Any,
) -> AsyncBackend:
    return _backend_class(backend, True)(impersonate=impersonate, **kwargs)
