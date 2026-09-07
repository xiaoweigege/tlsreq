# tlsreq

[English](README.md) | 简体中文

同一套 `Session` / `AsyncSession` API，底下可选四个带 TLS 能力的 HTTP 栈：

`curl_cffi` · `wreq` · `niquests` + `xutls` · `httpx` + `xutls`

换库只改 `backend` 和 `impersonate`，请求代码不用动。

[![PyPI](https://img.shields.io/pypi/v/tlsreq.svg)](https://pypi.org/project/tlsreq/)
[![Python](https://img.shields.io/pypi/pyversions/tlsreq.svg)](https://pypi.org/project/tlsreq/)
[![License: MIT](https://img.shields.io/pypi/l/tlsreq.svg)](LICENSE)

## 安装

```bash
pip install tlsreq
pip install "tlsreq[httpx]"       # 或 niquests / wreq / curl_cffi / all
```

| Extra | 会装上 | 说明 |
| --- | --- | --- |
| `httpx` | httpx, httpcore, h2, **xutls** | Chrome 152 TLS + HTTP/2 补丁 |
| `niquests` | niquests, **xutls** | Chrome 152 TLS + HTTP/2 补丁 |
| `wreq` | wreq | 需要 Python ≥ 3.11 |
| `curl_cffi` | curl_cffi | |
| `all` | 以上全部 | |

`httpx` / `niquests` extra 会装 [xutls](https://pypi.org/project/xutls/)（import 名仍是 `utls`）。**不要再装官方 `utls`**，两个包会抢同一个模块。之后升级：`pip install -U xutls`。

## 快速开始

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

需要底层库的专有参数时，用 `session.raw`。

## 后端

| `backend` | 默认 impersonate | 当前最新 Chrome 别名 | Sync | Async |
| --- | --- | --- | --- | --- |
| `niquests` | `chrome:152` | `chrome152` | 是 | 是 |
| `httpx` | `chrome:152` | `chrome152` | 是 | 是 |
| `curl_cffi` | `chrome150` | `chrome150` | 是 | 是 |
| `wreq` | `Chrome149` | `chrome149` | 是 | 是 |

无法识别的 `backend` 或 `impersonate` 会直接报错，不会静默换成别的指纹。

`chrome` / `chromestable` 映射到该后端当前默认值。

## Chrome 152（niquests / httpx）

这两个后端在 `xutls` 的 ClientHello 伪装之上，再套 Chrome 152 的 HTTP/2 帧：

| 信号 | 值 |
| --- | --- |
| SETTINGS | `1:65536;2:0;4:6291456;6:262144` |
| WINDOW_UPDATE | `15663105` |
| HEADERS priority | exclusive，weight `256` |
| 伪头顺序 | `m,a,s,p` |
| JA4 | `t13d1517h2_8daaf6152771_cb7bf5808d99` |
| Akamai fingerprint | `1:65536;2:0;4:6291456;6:262144\|15663105\|0\|m,a,s,p` |

对照 [tls.peet.ws](https://tls.peet.ws/api/all) 验证过。

`curl_cffi` 和 `wreq` 走各自的栈，不套这套 HTTP/2 补丁。

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

支持上下文管理器。`AsyncSession` 的方法都是协程。

### 请求

`get` / `post` / `put` / `patch` / `delete` / `head` / `options` 都走 `request`。

| 参数 | 含义 |
| --- | --- |
| `headers` | 单次请求头 |
| `params` | 查询字符串 |
| `data` | 表单 dict，或原始 body（`str` / `bytes`） |
| `json` | JSON body |
| `cookies` | 单次请求 cookie |
| `timeout` | 覆盖 session 超时 |
| `allow_redirects` | 覆盖 session 重定向开关 |
| `header_order` | 请求头在线上的顺序（后端支持时生效） |
| `extra` | 这次调用的后端专有参数 |

session 上的 `extra` 会并进底层构造函数；请求上的 `extra` 并进这一次调用。后写覆盖先写。

### `Response`

包装时已经把 body 读完。无论同步还是异步 Session，`.text` / `.json()` 都是同步的。

| 属性 | 类型 |
| --- | --- |
| `status_code` | `int` |
| `content` | `bytes` |
| `text` | `str` |
| `headers` | `dict[str, str]` |
| `cookies` | `dict[str, str]` |
| `url` | `str` |
| `http_version` | `str \| None` |
| `raw` | 底层响应对象 |

`session.cookies` 是 cookie 罐的 dict。`session.set_cookies(dict, url=None)` 写入。

## 许可证

[MIT](LICENSE)
