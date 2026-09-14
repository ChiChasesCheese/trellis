"""Puts src/ on sys.path so `import minihttp` works whether this repo is run in place or copied
elsewhere wholesale (loop/mock.py copies the whole problem dir, minus solution/ and REPORT.md,
into loop/work/<id>/ and runs pytest there -- this file must keep working after that copy).

Also provides `local_server`: a real `http.server.HTTPServer` on an OS-assigned loopback port,
run in a background thread, that records every request it receives (method, path, headers, body)
and replies from a small caller-configurable queue of canned responses. This lets the integration
tests exercise a real socket round trip without depending on the network or on any particular
port being free.
"""

from __future__ import annotations

import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class _RecordingServer(HTTPServer):
    """An HTTPServer that keeps a log of received requests and a queue of responses to send back,
    one response per request, in order. When the queue runs dry it keeps replying 200 empty."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = []
        self.responses = []  # list of (status_code, headers_dict, body_bytes)

    def queue_response(self, status_code: int, headers: dict | None = None, body: bytes = b""):
        self.responses.append((status_code, headers or {}, body))


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # silence the default per-request stderr logging
        pass

    def _handle(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else b""
        self.server.requests.append(
            {"method": self.command, "path": self.path, "headers": dict(self.headers), "body": body}
        )
        if self.server.responses:
            status, headers, resp_body = self.server.responses.pop(0)
        else:
            status, headers, resp_body = 200, {}, b""
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)

    do_GET = _handle
    do_POST = _handle
    do_PUT = _handle
    do_DELETE = _handle


@pytest.fixture
def local_server():
    server = _RecordingServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
