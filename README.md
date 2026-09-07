# tlsreq

English | [简体中文](README.zh-CN.md)

A single `Session` / `AsyncSession` API over four TLS-capable HTTP stacks:

`curl_cffi` · `wreq` · `niquests` + `xutls` · `httpx` + `xutls`

Change `backend` and `impersonate`. Request code stays the same.

[![PyPI](https://img.shields.io/pypi/v/tlsreq.svg)](https://pypi.org/project/tlsreq/)
[![Python](https://img.shields.io/pypi/pyversions/tlsreq.svg)](https://pypi.org/project/tlsreq/)
[![License: MIT](https://img.shields.io/pypi/l/tlsreq.svg)](LICENSE)

## Install

```bash
pip install tlsreq
pip install "tlsreq[httpx]"       # or niquests / wreq / curl_cffi / all
```

| Extra | Pulls in | Notes |
| --- | --- | --- |
| `httpx` | httpx, httpcore, h2, **xutls** | Chrome 152 TLS + HTTP/2 patches |
| `niquests` | niquests, **xutls** | Chrome 152 TLS + HTTP/2 patches |
| `wreq` | wreq | Requires Python ≥ 3.11 |
| `curl_cffi` | curl_cffi | |
| `all` | everything above | |

`httpx` / `niquests` extras install [xutls](https://pypi.org/project/xutls/) (import name is still `utls`). Do **not** also install the upstream `utls` package — both provide the `utls` module. To upgrade later: `pip install -U xutls`.

## Quick start

```python
import asyncio
from tlsreq import AsyncSession, Session

async def main():
    async with AsyncSession(
        backend="niquests",
        impersonate="chrome152",
        proxy="http://user:pass@host:port",
        timeout=30,
        extra={"pool_maxsize": 1},
    ) as s:
        r = await s.get("https://tls.peet.ws/api/all")
        print(r.status_code, r.http_version, r.cookies)
        print(r.json()["tls"]["ja4"])

        r = await s.post(
            "https://example.com/login",
            data=b"user=a&pass=b",
            headers={"content-type": "application/x-www-form-urlencoded"},
            header_order=["user-agent", "accept", "content-type"],
        )
        print(r.status_code, r.text)

asyncio.run(main())

with Session("wreq", "chrome149", proxy="http://127.0.0.1:7890") as s:
    r = s.get("https://example.com")
    print(r.status_code, r.headers)
```

The native client is on `session.raw` when you need a backend-specific knob.

## Backends

| `backend` | Default impersonate | Latest Chrome alias | Sync | Async |
| --- | --- | --- | --- | --- |
| `niquests` | `chrome:152` | `chrome152` | yes | yes |
| `httpx` | `chrome:152` | `chrome152` | yes | yes |
| `curl_cffi` | `chrome150` | `chrome150` | yes | yes |
| `wreq` | `Chrome149` | `chrome149` | yes | yes |

Unknown `backend` or `impersonate` values raise. There is no silent fallback to another profile.

`chrome` / `chromestable` map to that backend’s current default. `wreq` also accepts its native names (`Firefox151`, `Safari18_5`, `Edge148`, `Opera131`, `OkHttp5`, …). `curl_cffi` accepts `firefox`, `safari`, `edge`, `chrome_android`, `tor`, and the library’s versioned profiles.

httpx / niquests offer both HTTP/2 and HTTP/1.1. The protocol is chosen from the negotiated TLS ALPN (`h2` vs `http/1.1`); an HTTP/1.1-only origin falls back instead of failing.

## Chrome 152 (niquests / httpx)

These two backends apply Chrome 152 HTTP/2 framing on top of `xutls` ClientHello impersonation:

| Signal | Value |
| --- | --- |
| SETTINGS | `1:65536;2:0;4:6291456;6:262144` |
| WINDOW_UPDATE | `15663105` |
| HEADERS priority | exclusive, weight `256` |
| Pseudo-header order | `m,a,s,p` |
| JA4 | `t13d1517h2_8daaf6152771_cb7bf5808d99` |
| Akamai fingerprint | `1:65536;2:0;4:6291456;6:262144\|15663105\|0\|m,a,s,p` |

Checked against [tls.peet.ws](https://tls.peet.ws/api/all).

`curl_cffi` and `wreq` use their own stacks; they do not take this HTTP/2 patch.

## API

### `Session` / `AsyncSession`

```python
Session(
    backend: str,
    impersonate: str | None = None,
    *,
    proxy: str | None = None,
    timeout: float = 30,
    verify: bool = True,
    headers: dict | None = None,
    cookies: dict | None = None,
    allow_redirects: bool = True,
    extra: dict | None = None,
)
```

Context-manager safe. `AsyncSession` methods are coroutines.

### Requests

`get` / `post` / `put` / `patch` / `delete` / `head` / `options` all call `request`.

| Argument | Meaning |
| --- | --- |
| `headers` | Per-request headers |
| `params` | Query string |
| `data` | Form dict or raw body (`str` / `bytes`) |
| `json` | JSON body |
| `cookies` | Per-request cookies |
| `timeout` | Override session timeout |
| `allow_redirects` | Override session redirect flag |
| `header_order` | Wire order of header names, when the backend supports it |
| `extra` | Backend-specific kwargs for this call |

`extra` on the session is merged into the underlying constructor; `extra` on a request is merged into that call. Later keys win.

### `Response`

Body is fully read when the response is wrapped. `.text` and `.json()` are synchronous on both Session types.

| Attribute | Type |
| --- | --- |
| `status_code` | `int` |
| `content` | `bytes` |
| `text` | `str` |
| `headers` | `dict[str, str]` |
| `cookies` | `dict[str, str]` |
| `url` | `str` |
| `http_version` | `str \| None` |
| `raw` | native response |

`session.cookies` is the cookie jar as a dict. `session.set_cookies(dict, url=None)` writes into it.

## License

[MIT](LICENSE)
