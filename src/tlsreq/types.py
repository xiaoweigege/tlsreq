from typing import Literal

BackendName = Literal[
    "httpx",
    "niquests",
    "wreq",
    "curl_cffi",
    "curl",
    "cffi",
    "nirequest",
    "nirequests",
    "nio",
]

ImpersonateName = Literal[
    "chrome152",
    "chrome150",
    "chrome149",
    "chrome",
    "chromestable",
    "firefox",
    "safari",
    "edge",
    "opera",
    "okhttp",
    "chrome_android",
    "tor",
]
