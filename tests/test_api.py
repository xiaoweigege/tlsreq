import unittest

from tlsreq import AsyncSession, Session
from tlsreq.backends.base import merge_extra, split_data
from tlsreq.errors import UnknownBackend, UnknownFingerprint
from tlsreq.response import Response, cookies_to_dict, headers_to_dict, status_code_of
from tlsreq.utls_release import UTLS_RELEASE, utls_version, wheel_url


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

    def test_utls_release_pin(self):
        self.assertEqual(UTLS_RELEASE, "2026.9.4")
        self.assertGreaterEqual(utls_version(), UTLS_RELEASE)
        self.assertTrue(wheel_url().startswith("https://github.com/xiaoweigege/utls/releases/download/"))


class ConstructTests(unittest.TestCase):
    def test_httpx_sync_and_async_construct(self):
        s = Session("httpx", "chrome152")
        self.assertEqual(type(s.raw).__name__, "Client")
        s.close()

    def test_niquests_construct(self):
        s = Session("niquests", "chrome152")
        self.assertTrue(hasattr(s.raw, "request"))
        s.close()

    def test_wreq_construct(self):
        s = Session("wreq", "chrome149")
        self.assertTrue(s.raw is not None)
        s.close()

    def test_httpx_unknown_fingerprint(self):
        with self.assertRaises(UnknownFingerprint):
            Session("httpx", "chrome149")


if __name__ == "__main__":
    unittest.main()
