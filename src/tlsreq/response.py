from __future__ import annotations

import json
from typing import Any, Optional


def _as_str(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("latin-1")
    return str(value)


def headers_to_dict(headers: Any) -> dict[str, str]:
    if headers is None:
        return {}
    if hasattr(headers, "multi_items"):
        items = list(headers.multi_items())
    elif hasattr(headers, "items"):
        items = list(headers.items())
    elif isinstance(headers, (list, tuple)):
        items = list(headers)
    else:
        return {}
    out: dict[str, str] = {}
    for key, value in items:
        if isinstance(value, (list, tuple)):
            value = ", ".join(_as_str(part) for part in value)
        out[_as_str(key)] = _as_str(value)
    return out


def cookies_to_dict(cookies: Any) -> dict[str, str]:
    if cookies is None:
        return {}
    if isinstance(cookies, dict):
        return {str(k): str(v) for k, v in cookies.items()}
    if hasattr(cookies, "get_dict"):
        return dict(cookies.get_dict())
    if hasattr(cookies, "items"):
        try:
            return {str(k): str(v) for k, v in cookies.items()}
        except TypeError:
            pass
    out: dict[str, str] = {}
    try:
        for cookie in cookies:
            name = getattr(cookie, "name", None)
            value = getattr(cookie, "value", None)
            if name is not None:
                out[str(name)] = str(value)
    except TypeError:
        return {}
    return out


def status_code_of(resp: Any) -> int:
    value = getattr(resp, "status_code", None)
    if value is None:
        value = getattr(resp, "status", 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        as_int = getattr(value, "as_int", None) or getattr(value, "as_u16", None)
        if callable(as_int):
            return int(as_int())
        return int(getattr(value, "value", 0) or 0)


def http_version_of(resp: Any) -> Optional[str]:
    value = getattr(resp, "http_version", None)
    if value is None:
        value = getattr(resp, "version", None)
    if value is None:
        extensions = getattr(resp, "extensions", None) or {}
        value = extensions.get("http_version")
    if value is None:
        return None
    if isinstance(value, bytes):
        value = value.decode("latin-1")
    return str(value)


class Response:
    """统一响应。body 在包装时已读完，`.text` / `.json()` 都是同步的。"""

    def __init__(
        self,
        *,
        status_code: int,
        content: bytes,
        headers: dict[str, str],
        url: str,
        cookies: Optional[dict[str, str]] = None,
        http_version: Optional[str] = None,
        encoding: str = "utf-8",
        raw: Any = None,
    ) -> None:
        self.status_code = status_code
        self.content = content or b""
        self.headers = headers
        self.url = url
        self.cookies = cookies or {}
        self.http_version = http_version
        self.encoding = encoding
        self.raw = raw

    @property
    def text(self) -> str:
        return self.content.decode(self.encoding, errors="replace")

    def json(self) -> Any:
        return json.loads(self.text)

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise RuntimeError(f"HTTP {self.status_code} for {self.url}")

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}] {self.url}>"
