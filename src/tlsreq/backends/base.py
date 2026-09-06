from __future__ import annotations

from typing import Any, Optional

from ..response import Response


def merge_extra(mapped: dict[str, Any], extra: Optional[dict[str, Any]]) -> dict[str, Any]:
    if not extra:
        return mapped
    out = dict(mapped)
    out.update(extra)
    return out


def split_data(data: Any) -> dict[str, Any]:
    """httpx: dict 走 data= 表单，str/bytes 走 content=。"""
    if data is None:
        return {}
    if isinstance(data, (dict, list, tuple)):
        return {"data": data}
    return {"content": data}


class SyncBackend:
    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        raise NotImplementedError

    def close(self) -> None:
        return None

    def get_cookies(self) -> dict[str, str]:
        return {}

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        return None

    @property
    def raw(self) -> Any:
        raise NotImplementedError


class AsyncBackend:
    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        raise NotImplementedError

    async def aclose(self) -> None:
        return None

    def get_cookies(self) -> dict[str, str]:
        return {}

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        return None

    @property
    def raw(self) -> Any:
        raise NotImplementedError
