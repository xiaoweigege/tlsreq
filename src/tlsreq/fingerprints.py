from __future__ import annotations

from .errors import UnknownFingerprint

# 统一名 -> 各库原生指纹。缺的不静默降级。
CURL_CFFI = {
    "chrome99": "chrome99",
    "chrome100": "chrome100",
    "chrome101": "chrome101",
    "chrome104": "chrome104",
    "chrome107": "chrome107",
    "chrome110": "chrome110",
    "chrome116": "chrome116",
    "chrome119": "chrome119",
    "chrome120": "chrome120",
    "chrome123": "chrome123",
    "chrome124": "chrome124",
    "chrome131": "chrome131",
    "chrome133a": "chrome133a",
    "chrome136": "chrome136",
    "chrome142": "chrome142",
    "chrome145": "chrome145",
    "chrome146": "chrome146",
    "chrome150": "chrome150",
    "chrome": "chrome150",
    "chromestable": "chrome150",
    "chromeandroid": "chrome131_android",
    "chrome131android": "chrome131_android",
    "edge99": "edge99",
    "edge101": "edge101",
    "firefox133": "firefox133",
    "firefox135": "firefox135",
    "firefox144": "firefox144",
    "firefox147": "firefox147",
    "firefox": "firefox147",
}

WREQ = {
    **{f"chrome{n}": f"Chrome{n}" for n in range(100, 150)},
    "chrome101": "Chrome101",
    "chrome104": "Chrome104",
    "chrome105": "Chrome105",
    "chrome106": "Chrome106",
    "chrome107": "Chrome107",
    "chrome108": "Chrome108",
    "chrome109": "Chrome109",
    "chrome110": "Chrome110",
    "chrome114": "Chrome114",
    "chrome116": "Chrome116",
    "chrome117": "Chrome117",
    "chrome118": "Chrome118",
    "chrome119": "Chrome119",
    "chrome120": "Chrome120",
    "chrome123": "Chrome123",
    "chrome124": "Chrome124",
    "chrome126": "Chrome126",
    "chrome127": "Chrome127",
    "chrome128": "Chrome128",
    "chrome129": "Chrome129",
    "chrome130": "Chrome130",
    "chrome131": "Chrome131",
    "chrome132": "Chrome132",
    "chrome133": "Chrome133",
    "chrome134": "Chrome134",
    "chrome135": "Chrome135",
    "chrome136": "Chrome136",
    "chrome137": "Chrome137",
    "chrome138": "Chrome138",
    "chrome139": "Chrome139",
    "chrome140": "Chrome140",
    "chrome141": "Chrome141",
    "chrome142": "Chrome142",
    "chrome143": "Chrome143",
    "chrome144": "Chrome144",
    "chrome145": "Chrome145",
    "chrome146": "Chrome146",
    "chrome147": "Chrome147",
    "chrome148": "Chrome148",
    "chrome149": "Chrome149",
    "chrome": "Chrome149",
    "chromestable": "Chrome149",
}

# niquests / httpx。chrome152 需要 PyPI xutls>=2026.9.7，不要装官方 utls。
UTLS = {
    "chrome131": "chrome:131",
    "chrome142": "chrome:142",
    "chrome146": "chrome:146",
    "chrome148": "chrome:148",
    "chrome150": "chrome:150",
    "chrome152": "chrome:152",
    "chromestable": "chrome:stable",
    "chrome": "chrome:stable",
}

TABLES = {
    "curl_cffi": CURL_CFFI,
    "wreq": WREQ,
    "niquests": UTLS,
    "httpx": UTLS,
}

DEFAULTS = {
    "curl_cffi": "chrome150",
    "wreq": "Chrome149",
    "niquests": "chrome:152",
    "httpx": "chrome:152",
}


def normalize(name: str) -> str:
    s = name.strip().lower()
    for ch in ("_", "-", " ", ":"):
        s = s.replace(ch, "")
    return s


def resolve(backend: str, impersonate: str | None) -> str:
    table = TABLES[backend]
    if impersonate is None:
        return DEFAULTS[backend]
    key = normalize(impersonate)
    if key in table:
        return table[key]
    native = {normalize(v): v for v in table.values()}
    if key in native:
        return native[key]
    available = sorted(set(table.values()))
    raise UnknownFingerprint(
        f"{backend} 没有指纹 {impersonate!r}。可用: {available}"
    )
