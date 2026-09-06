# tlsreq

把 `curl_cffi`、`wreq`、`niquests+utls`、`httpx+utls` 收成同一套 Session API。换库只改 `backend` 和 `impersonate`。

GitHub: https://github.com/xiaoweigege/tlsreq

## 安装

```bash
pip install tlsreq
pip install "tlsreq[httpx]"      # 或 niquests / wreq / curl_cffi / all
```

Chrome 152 不在 PyPI 的 `utls` 里。httpx / niquests 需要再装 GitHub 2026.9.4：

https://github.com/xiaoweigege/utls/releases/tag/2026.9.4

```bash
python -m tlsreq.install_utls
# 或 tlsreq-install-utls
```

## 用法

```python
from tlsreq import AsyncSession, Session

async with AsyncSession(
    backend="niquests",           # curl_cffi / wreq / niquests / httpx
    impersonate="chrome152",
    proxy="http://user:pass@host:port",
    timeout=30,
    extra={"pool_maxsize": 1},    # 只传给当前库
) as s:
    r = await s.get(url, headers=headers)
    print(r.status_code, r.text, r.cookies, r.http_version)
    r = await s.post(url, data=body, headers=headers, header_order=["user-agent", "accept"])

s = Session(backend="wreq", impersonate="chrome149", proxy=proxy)
r = s.get(url, headers=headers)
```

`extra=` 会合并进底层构造函数或单次请求，后写覆盖统一层映射。底层 client 在 `s.raw`。

niquests / httpx 默认带 Chrome 152 的 HTTP/2 SETTINGS、窗口和 HEADERS Priority，JA4 / peetprint / akamai_fingerprint 对齐真机。
