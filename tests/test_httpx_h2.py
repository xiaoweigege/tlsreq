import unittest

from hyperframe.frame import Frame, SettingsFrame

from tlsreq.backends._httpx_patch import (
    _accept_advertised_decoder_limits,
    _chrome_local_settings,
    _restore_local_only,
)
from tlsreq.chrome_h2 import CONNECTION_WINDOW_INCREMENT, HEADER_TABLE_SIZE, MAX_HEADER_LIST_SIZE


class ChromeH2Tests(unittest.TestCase):
    def test_settings_order_and_values(self):
        settings = _chrome_local_settings()
        self.assertEqual([int(key) for key in settings], [1, 2, 4, 6])
        self.assertEqual(settings[1], 65536)
        self.assertEqual(settings[2], 0)
        self.assertEqual(settings[4], 6291456)
        self.assertEqual(settings[6], 262144)

    def test_serialized_preface_matches_chrome_akamai(self):
        import h2.config
        import h2.connection

        conn = h2.connection.H2Connection(
            config=h2.config.H2Configuration(client_side=True, validate_inbound_headers=False)
        )
        conn.local_settings = _chrome_local_settings()
        conn.initiate_connection()
        _restore_local_only(conn.local_settings)
        conn.increment_flow_control_window(CONNECTION_WINDOW_INCREMENT)
        data = conn.data_to_send()
        preface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
        self.assertTrue(data.startswith(preface))
        rest = data[len(preface):]
        frames = []
        index = 0
        while index < len(rest):
            frame, _consumed = Frame.parse_frame_header(rest[index:index + 9])
            length = int.from_bytes(rest[index:index + 3], "big")
            frame.parse_body(memoryview(rest[index + 9:index + 9 + length]))
            frames.append(frame)
            index += 9 + length
        self.assertIsInstance(frames[0], SettingsFrame)
        self.assertEqual(dict(frames[0].settings), {1: 65536, 2: 0, 4: 6291456, 6: 262144})
        self.assertEqual(frames[1].window_increment, 15663105)

        conn.send_headers(
            1,
            [
                (b":method", b"GET"),
                (b":authority", b"tls.peet.ws"),
                (b":scheme", b"https"),
                (b":path", b"/api/all"),
            ],
            end_stream=True,
            priority_weight=256,
            priority_depends_on=0,
            priority_exclusive=True,
        )
        header_data = conn.data_to_send()
        header_frame, _consumed = Frame.parse_frame_header(header_data[:9])
        length = int.from_bytes(header_data[:3], "big")
        header_frame.parse_body(memoryview(header_data[9:9 + length]))
        self.assertIn("PRIORITY", header_frame.flags)

    def test_decoder_allows_peer_table_size_before_ack(self):
        import h2.config
        import h2.connection
        from hpack import Encoder

        conn = h2.connection.H2Connection(
            config=h2.config.H2Configuration(client_side=True, validate_inbound_headers=False)
        )
        conn.local_settings = _chrome_local_settings()
        conn.initiate_connection()
        _restore_local_only(conn.local_settings)
        _accept_advertised_decoder_limits(conn)
        self.assertEqual(conn.decoder.max_allowed_table_size, HEADER_TABLE_SIZE)
        self.assertEqual(conn.decoder.max_header_list_size, MAX_HEADER_LIST_SIZE)

        peer = Encoder()
        peer.header_table_size = HEADER_TABLE_SIZE
        block = peer.encode([(b":status", b"200"), (b"content-type", b"text/plain")])
        decoded = list(conn.decoder.decode(block, raw=True))
        self.assertIn((b":status", b"200"), decoded)


if __name__ == "__main__":
    unittest.main()
