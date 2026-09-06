import ssl
import unittest
from typing import Optional

from tlsreq.backends.httpx import _SSLObjectAdapter, _fill_sslerror_strerror


class _FakeSSL:
    def __init__(self, exc: Optional[BaseException] = None) -> None:
        self._exc = exc
        self.context = type("C", (), {"server_side": False})()

    def read(self, n: int = 1024, buffer=None):
        if self._exc is not None:
            raise self._exc
        if buffer is None:
            return b"ok"
        buffer[:2] = b"ok"
        return 2

    def do_handshake(self) -> None:
        if self._exc is not None:
            raise self._exc


class SSLAdapterTests(unittest.TestCase):
    def test_close_notify_becomes_empty_read(self):
        inner = _FakeSSL(ssl.SSLZeroReturnError("peer sent close_notify; no more data will be received"))
        adapter = _SSLObjectAdapter(inner)
        self.assertEqual(adapter.read(1024), b"")
        buf = bytearray(8)
        self.assertEqual(adapter.read(1024, buf), 0)

    def test_strerror_none_is_filled(self):
        exc = ssl.SSLError("tls boom")
        exc.strerror = None
        _fill_sslerror_strerror(exc)
        self.assertIsInstance(exc.strerror, str)
        self.assertIn("tls boom", exc.strerror)

    def test_zero_return_strerror_marked_as_eof(self):
        exc = ssl.SSLZeroReturnError("peer sent close_notify; no more data will be received")
        exc.strerror = None
        _fill_sslerror_strerror(exc)
        self.assertIn("UNEXPECTED_EOF_WHILE_READING", exc.strerror)

    def test_getattr_fills_strerror_then_reraises(self):
        exc = ssl.SSLError("handshake failed")
        exc.strerror = None
        adapter = _SSLObjectAdapter(_FakeSSL(exc))
        with self.assertRaises(ssl.SSLError) as caught:
            adapter.do_handshake()
        self.assertIsInstance(caught.exception.strerror, str)


if __name__ == "__main__":
    unittest.main()
