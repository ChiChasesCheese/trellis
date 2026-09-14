"""A tiny local HTTP server used only by this test suite, standing in for whatever real API
`fetchrace` would normally point at. Not part of the library under test -- it's test
infrastructure, the same role `loop/mockserver/` plays for the integration rounds.

Routes:
  GET /ok/<id>              -> 200, body b"ok:<id>"
  GET /json/<id>            -> 200, body {"id": "<id>"} as JSON
  GET /always-fail          -> always 500
  GET /flaky/<id>           -> 500 for the first `fail_times` requests to this <id>, then 200
                               (`fail_times` is set when the server is created)

Runs on a background thread (`ThreadingHTTPServer`) so the test process's asyncio event loop is
free to make requests against it concurrently.
"""

from __future__ import annotations

import http.server
import json
import threading
from collections import defaultdict


class _State:
    def __init__(self, fail_times: int):
        self.lock = threading.Lock()
        self.fail_times = fail_times
        self.flaky_counters: dict = defaultdict(int)


def _make_handler(state: _State):
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):  # noqa: D401 - silence default stderr access logging
            pass

        def do_GET(self):
            parts = self.path.strip("/").split("/")
            if parts[0] == "ok" and len(parts) == 2:
                self._respond(200, f"ok:{parts[1]}".encode())
            elif parts[0] == "json" and len(parts) == 2:
                self._respond(200, json.dumps({"id": parts[1]}).encode())
            elif parts[0] == "always-fail":
                self._respond(500, b"error")
            elif parts[0] == "flaky" and len(parts) == 2:
                key = parts[1]
                with state.lock:
                    state.flaky_counters[key] += 1
                    attempt = state.flaky_counters[key]
                if attempt <= state.fail_times:
                    self._respond(500, b"error")
                else:
                    self._respond(200, f"ok:{key}".encode())
            else:
                self._respond(404, b"not found")

        def _respond(self, code: int, body: bytes) -> None:
            self.send_response(code)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler


def make_server(fail_times: int = 2):
    """Start the server on an OS-assigned free port and return (base_url, server). Caller is
    responsible for calling `server.shutdown()` when done (see the `http_server` fixture)."""
    state = _State(fail_times)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _make_handler(state))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    return base_url, server
