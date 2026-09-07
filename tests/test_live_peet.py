import asyncio
import os
import unittest

from tlsreq import AsyncSession, Session

PEET = "https://tls.peet.ws/api/all"
CHROME152_JA4 = "t13d1517h2_8daaf6152771_cb7bf5808d99"
CHROME152_PEETPRINT = (
    "GREASE-772-771|2-1.1|GREASE-4588-29-23-24|"
    "GREASE-2308-2309-2310-1027-2052-1025-1283-2053-1281-2054-1537|1|2|"
    "GREASE-4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53|"
    "0-10-11-13-16-17613-18-23-27-35-43-45-5-51-51764-65037-65281-GREASE-GREASE"
)
CHROME152_AKAMAI = "1:65536;2:0;4:6291456;6:262144|15663105|0|m,a,s,p"
HEADERS = {
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-ch-ua": '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
    ),
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
}
HEADER_ORDER = [
    "pragma", "cache-control", "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
    "dnt", "upgrade-insecure-requests", "user-agent", "accept",
    "sec-fetch-site", "sec-fetch-mode", "sec-fetch-user", "sec-fetch-dest",
    "accept-encoding", "accept-language", "priority",
]


def _pack(response) -> dict:
    data = response.json()
    data["_status"] = response.status_code
    data["_http_version"] = data.get("http_version")
    return data


def _peet_sync(backend: str, impersonate: str) -> dict:
    with Session(backend, impersonate, timeout=45) as session:
        response = session.get(PEET, headers=HEADERS, header_order=HEADER_ORDER)
    return _pack(response)


async def _peet(backend: str, impersonate: str) -> dict:
    async with AsyncSession(backend, impersonate, timeout=45) as session:
        response = await session.get(PEET, headers=HEADERS, header_order=HEADER_ORDER)
    return _pack(response)


def _can_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except ImportError:
        return False


@unittest.skipIf(os.environ.get("TLSREQ_SKIP_LIVE"), "live peet skipped")
class LivePeetTests(unittest.TestCase):
    def _assert_chrome152(self, data: dict) -> None:
        self.assertEqual(data["_status"], 200)
        self.assertEqual(data.get("http_version"), "h2")
        tls = data["tls"]
        http2 = data["http2"]
        self.assertEqual(tls["ja4"], CHROME152_JA4)
        self.assertEqual(tls["peetprint"], CHROME152_PEETPRINT)
        self.assertEqual(http2["akamai_fingerprint"], CHROME152_AKAMAI)
        frames = [frame["frame_type"] for frame in http2["sent_frames"]]
        self.assertEqual(frames, ["SETTINGS", "WINDOW_UPDATE", "HEADERS"])
        headers_frame = next(frame for frame in http2["sent_frames"] if frame["frame_type"] == "HEADERS")
        self.assertEqual(headers_frame["length"], 492)
        self.assertIn("Priority (0x20)", headers_frame.get("flags") or [])
        self.assertEqual(headers_frame["priority"]["weight"], 256)
        self.assertEqual(headers_frame["priority"]["exclusive"], 1)

    @unittest.skipUnless(_can_import("httpx") and _can_import("utls"), "httpx/utls not installed")
    def test_httpx_chrome152_async(self):
        self._assert_chrome152(asyncio.run(_peet("httpx", "chrome152")))

    @unittest.skipUnless(_can_import("httpx") and _can_import("utls"), "httpx/utls not installed")
    def test_httpx_chrome152_sync(self):
        self._assert_chrome152(_peet_sync("httpx", "chrome152"))

    @unittest.skipUnless(_can_import("niquests") and _can_import("utls"), "niquests/utls not installed")
    def test_niquests_chrome152_async(self):
        self._assert_chrome152(asyncio.run(_peet("niquests", "chrome152")))

    @unittest.skipUnless(_can_import("niquests") and _can_import("utls"), "niquests/utls not installed")
    def test_niquests_chrome152_sync(self):
        self._assert_chrome152(_peet_sync("niquests", "chrome152"))

    @unittest.skipUnless(_can_import("wreq"), "wreq not installed")
    def test_wreq_sync(self):
        with Session("wreq", "chrome149", timeout=45) as session:
            response = session.get(PEET, headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertIn("tls", response.json())

    @unittest.skipUnless(_can_import("wreq"), "wreq not installed")
    def test_wreq_async(self):
        async def _run():
            async with AsyncSession("wreq", "chrome149", timeout=45) as session:
                return await session.get(PEET, headers=HEADERS)

        response = asyncio.run(_run())
        self.assertEqual(response.status_code, 200)
        self.assertIn("tls", response.json())


if __name__ == "__main__":
    unittest.main()
