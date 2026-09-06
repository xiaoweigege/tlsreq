"""Chrome 152 HTTP/2 常量。SETTINGS 顺序必须是 1,2,4,6。"""

from __future__ import annotations

HEADER_TABLE_SIZE = 65536
ENABLE_PUSH = 0
INITIAL_WINDOW_SIZE = 6291456
MAX_HEADER_LIST_SIZE = 262144
CONNECTION_WINDOW_INCREMENT = 15663105
PRIORITY_WEIGHT = 256
PRIORITY_DEPENDS_ON = 0
PRIORITY_EXCLUSIVE = True

H2_HOP_BY_HOP = frozenset({
    b"host",
    b"connection",
    b"keep-alive",
    b"proxy-connection",
    b"transfer-encoding",
    b"upgrade",
})

HTTP1_KEEP_LOWER = frozenset({
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
    "sec-fetch-site",
    "sec-fetch-mode",
    "sec-fetch-dest",
    "sec-fetch-user",
    "dnt",
    "priority",
})


def chrome_http1_header_name(name: str) -> str:
    lower = name.lower().replace("_", "-")
    if lower in HTTP1_KEEP_LOWER or lower.startswith("sec-"):
        return lower
    return "-".join(part.capitalize() for part in lower.split("-"))
