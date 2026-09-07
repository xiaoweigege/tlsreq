import asyncio
import unittest

from tlsreq import Session
from tlsreq.backends.base import merge_extra, split_data
from tlsreq.errors import UnknownBackend, UnknownFingerprint
from tlsreq.response import Response, cookies_to_dict, headers_to_dict, status_code_of
from tlsreq.utls_release import UTLS_RELEASE, XUTLS_DIST, fingerprint_from_preset


def _can_import(name: str) -> bool:
    try:
        __import__(name)
        return True
    except ImportError:
        return False


class ApiTests(unittest.TestCase):
    def test_unknown_backend(self):
        with self.assertRaises(UnknownBackend):
            Session("not-a-backend")

    def test_merge_extra_overrides(self):
        out = merge_extra({"timeout": 30, "verify": True}, {"timeout": 5, "ja3": "x"})
        self.assertEqual(out["timeout"], 5)
        self.assertEqual(out["ja3"], "x")
        self.assertTrue(out["verify"])

    def test_split_data(self):
        self.assertEqual(split_data(None), {})
        self.assertEqual(split_data({"a": 1}), {"data": {"a": 1}})
        self.assertEqual(split_data(b"raw"), {"content": b"raw"})
        self.assertEqual(split_data("raw"), {"content": "raw"})

    def test_headers_and_cookies(self):
        self.assertEqual(headers_to_dict({"A": "1"}), {"A": "1"})
        self.assertEqual(cookies_to_dict({"sid": "abc"}), {"sid": "abc"})

        class Obj:
            status_code = 204

        self.assertEqual(status_code_of(Obj()), 204)

    def test_response_json(self):
        resp = Response(
            status_code=200,
            content=b'{"ok": true}',
            headers={"content-type": "application/json"},
            url="https://example.com",
        )
        self.assertEqual(resp.json(), {"ok": True})
        self.assertEqual(resp.text, '{"ok": true}')

    @unittest.skipUnless(_can_import("utls"), "utls not installed")
    def test_chrome152_preset(self):
        import utls

        self.assertEqual(XUTLS_DIST, "xutls")
        self.assertEqual(UTLS_RELEASE, "2026.9.7")
        fp = fingerprint_from_preset(utls, "chrome:152")
        ja4 = str(getattr(fp, "ja4_hash", ""))
        self.assertTrue(ja4.startswith("t13d1517h2"), ja4)


class ConstructTests(unittest.TestCase):
    @unittest.skipUnless(_can_import("httpx") and _can_import("utls"), "httpx/utls not installed")
    def test_httpx_sync_and_async_construct(self):
        from tlsreq import AsyncSession

        s = Session("httpx", "chrome152")
        self.assertEqual(type(s.raw).__name__, "Client")
        s.close()
        async_s = AsyncSession("httpx", "chrome152")
        self.assertEqual(type(async_s.raw).__name__, "AsyncClient")
        asyncio.run(async_s.close())

    @unittest.skipUnless(_can_import("niquests") and _can_import("utls"), "niquests/utls not installed")
    def test_niquests_construct(self):
        from tlsreq import AsyncSession

        s = Session("niquests", "chrome152")
        self.assertTrue(hasattr(s.raw, "request"))
        s.close()
        async_s = AsyncSession("niquests", "chrome152")
        self.assertTrue(hasattr(async_s.raw, "request"))
        asyncio.run(async_s.close())

    @unittest.skipUnless(_can_import("wreq"), "wreq not installed")
    def test_wreq_construct(self):
        s = Session("wreq", "chrome149")
        self.assertTrue(s.raw is not None)
        s.close()

    @unittest.skipUnless(_can_import("httpx") and _can_import("utls"), "httpx/utls not installed")
    def test_httpx_unknown_fingerprint(self):
        with self.assertRaises(UnknownFingerprint):
            Session("httpx", "chrome149")


if __name__ == "__main__":
    unittest.main()
