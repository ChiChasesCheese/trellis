"""loop.mockserver.maps — local mock of the "POST body -> PNG map" service the int01
(BikeMap) problem talks to. stdlib only: `http.server` + our own `_png` encoder.

Endpoints
---------
POST /render
    body (JSON): {"points": [[lat, lng], ...], "width"?: int, "height"?: int,
                  "markers"?: [[lat, lng, "label"], ...]}
    -> 200 image/png: the points projected into a `width`x`height` canvas (default
       400x300) and connected with a polyline; each marker painted as a small dot.
    errors:
      - body is not valid JSON, or not a JSON object          -> 400 invalid_request_error
      - "points" missing / not a list / fewer than 2 points   -> 400 invalid_request_error
      - more than 10000 points                                -> 413

GET /health
    -> 200 {"ok": true}

Every response also carries a `Request-Id: req_<hex>` header (see loop/mockserver/README.md).

Run standalone: `python3 -m loop.mockserver.maps --port 0` (0 = OS-assigned; the actual
port is printed as `listening on http://127.0.0.1:<port>`). Import `serve`/`start_in_thread`
to run it in-process for tests / problem fixtures.
"""

from __future__ import annotations

import argparse
import json
import secrets
import signal
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import _png

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 300
MAX_POINTS = 10000
LINE_COLOR = (30, 90, 220)
MARKER_COLOR = (220, 40, 40)


def _error(handler: BaseHTTPRequestHandler, status: int, error_type: str, message: str) -> None:
    body = json.dumps({"error": {"type": error_type, "message": message}}).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Request-Id", f"req_{secrets.token_hex(8)}")
    handler.end_headers()
    handler.wfile.write(body)


def _json_ok(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Request-Id", f"req_{secrets.token_hex(8)}")
    handler.end_headers()
    handler.wfile.write(body)


def _project(points, markers, width, height, padding=10):
    lats = [p[0] for p in points] + [m[0] for m in markers]
    lngs = [p[1] for p in points] + [m[1] for m in markers]
    lat_min, lat_max = min(lats), max(lats)
    lng_min, lng_max = min(lngs), max(lngs)
    if lat_max == lat_min:
        lat_max += 1e-6
        lat_min -= 1e-6
    if lng_max == lng_min:
        lng_max += 1e-6
        lng_min -= 1e-6
    pad = min(padding, (width - 1) // 2, (height - 1) // 2) if width > 1 and height > 1 else 0

    def to_px(lat, lng):
        x = pad + (lng - lng_min) / (lng_max - lng_min) * (width - 2 * pad)
        y = pad + (lat_max - lat) / (lat_max - lat_min) * (height - 2 * pad)  # lat grows "up"
        return x, y

    return to_px


def render_png(points, markers, width, height) -> bytes:
    to_px = _project(points, markers, width, height)
    canvas = _png.new_canvas(width, height, bg=(255, 255, 255))
    pixel_points = [to_px(lat, lng) for lat, lng in points]
    _png.draw_polyline(canvas, width, height, pixel_points, LINE_COLOR, thickness=2)
    for m in markers:
        lat, lng = m[0], m[1]
        x, y = to_px(lat, lng)
        _png.draw_marker(canvas, width, height, x, y, MARKER_COLOR, radius=3)
    return _png.write_png(width, height, canvas)


class Handler(BaseHTTPRequestHandler):
    server_version = "loop-mockserver-maps/0.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # silence default stderr access log
        pass

    def do_GET(self):
        if self.path == "/health":
            _json_ok(self, 200, {"ok": True})
            return
        _error(self, 404, "invalid_request_error", f"unknown path {self.path!r}")

    def do_POST(self):
        if self.path != "/render":
            _error(self, 404, "invalid_request_error", f"unknown path {self.path!r}")
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            _error(self, 400, "invalid_request_error", "request body is not valid JSON")
            return
        if not isinstance(body, dict):
            _error(self, 400, "invalid_request_error", "request body must be a JSON object")
            return

        points = body.get("points")
        if not isinstance(points, list) or len(points) < 2:
            _error(
                self, 400, "invalid_request_error", "'points' must be a list of at least 2 [lat, lng] pairs"
            )
            return
        if len(points) > MAX_POINTS:
            _error(self, 413, "invalid_request_error", f"too many points (max {MAX_POINTS})")
            return
        try:
            points = [(float(p[0]), float(p[1])) for p in points]
        except (TypeError, ValueError, IndexError):
            _error(self, 400, "invalid_request_error", "each point must be a [lat, lng] pair of numbers")
            return

        markers = body.get("markers", [])
        if not isinstance(markers, list):
            _error(self, 400, "invalid_request_error", "'markers' must be a list")
            return
        try:
            markers = [(float(m[0]), float(m[1]), str(m[2]) if len(m) > 2 else "") for m in markers]
        except (TypeError, ValueError, IndexError):
            _error(self, 400, "invalid_request_error", "each marker must be a [lat, lng, label] triple")
            return

        width = body.get("width", DEFAULT_WIDTH)
        height = body.get("height", DEFAULT_HEIGHT)
        if (
            not isinstance(width, int)
            or not isinstance(height, int)
            or not (1 <= width <= 4000)
            or not (1 <= height <= 4000)
        ):
            _error(self, 400, "invalid_request_error", "'width'/'height' must be integers in [1, 4000]")
            return

        png_bytes = render_png(points, markers, width, height)
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(png_bytes)))
        self.send_header("Request-Id", f"req_{secrets.token_hex(8)}")
        self.end_headers()
        self.wfile.write(png_bytes)


def _build_server(port: int = 0, host: str = "127.0.0.1") -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


def serve(port: int = 0, host: str = "127.0.0.1", **_opts):
    """Start the maps mockserver in a daemon thread. Returns (server, thread)."""
    server = _build_server(port, host)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


start_in_thread = serve


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python3 -m loop.mockserver.maps")
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args(argv)
    server = _build_server(args.port)
    print(f"listening on http://127.0.0.1:{server.server_address[1]}", flush=True)

    def _stop(signum, frame):  # SIGINT (Ctrl-C) -> graceful shutdown; also handle SIGTERM
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
