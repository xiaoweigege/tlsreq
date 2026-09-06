from __future__ import annotations

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


def _normalize_backend(name: str) -> str:
    key = name.strip().lower().replace("-", "_")
    return _ALIASES.get(key, key)


def create_sync_backend(
    backend: str,
    impersonate: Optional[str] = None,
    **kwargs: Any,
) -> SyncBackend:
    name = _normalize_backend(backend)
    if name == "curl_cffi":
        from .curl_cffi import CurlCffiSync
        return CurlCffiSync(impersonate=impersonate, **kwargs)
    if name == "wreq":
        from .wreq import WreqSync
        return WreqSync(impersonate=impersonate, **kwargs)
    if name == "niquests":
        from .niquests import NiquestsSync
        return NiquestsSync(impersonate=impersonate, **kwargs)
    if name == "httpx":
        from .httpx import HttpxSync
        return HttpxSync(impersonate=impersonate, **kwargs)
    raise UnknownBackend(f"未知 backend {backend!r}。可选: curl_cffi, wreq, niquests, httpx")


def create_async_backend(
    backend: str,
    impersonate: Optional[str] = None,
    **kwargs: Any,
) -> AsyncBackend:
    name = _normalize_backend(backend)
    if name == "curl_cffi":
        from .curl_cffi import CurlCffiAsync
        return CurlCffiAsync(impersonate=impersonate, **kwargs)
    if name == "wreq":
        from .wreq import WreqAsync
        return WreqAsync(impersonate=impersonate, **kwargs)
    if name == "niquests":
        from .niquests import NiquestsAsync
        return NiquestsAsync(impersonate=impersonate, **kwargs)
    if name == "httpx":
        from .httpx import HttpxAsync
        return HttpxAsync(impersonate=impersonate, **kwargs)
    raise UnknownBackend(f"未知 backend {backend!r}。可选: curl_cffi, wreq, niquests, httpx")
