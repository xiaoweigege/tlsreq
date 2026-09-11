"""GET https://tls.peet.ws/api/all with the default httpx Chrome 152 stack.

    python examples/peet.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "src"
if src.is_dir() and str(src) not in sys.path:
    sys.path.insert(0, str(src))

from tlsreq import Session

URL = "https://tls.peet.ws/api/all"
HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    ),
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


def main() -> None:
    with Session("httpx", "chrome152", timeout=45) as session:
        response = session.get(URL, headers=HEADERS)

    data = response.json()
    tls = data.get("tls") or {}
    http2 = data.get("http2") or {}

    print(f"status          {response.status_code}")
    print(f"http_version    {data.get('http_version') or response.http_version}")
    print(f"ja4             {tls.get('ja4')}")
    print(f"peetprint_hash  {tls.get('peetprint_hash')}")
    print(f"akamai          {http2.get('akamai_fingerprint')}")
    print()
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
