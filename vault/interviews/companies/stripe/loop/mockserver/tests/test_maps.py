"""Tests for loop.mockserver.maps — the local "POST points -> PNG" mock the int01
(BikeMap) problem talks to. Starts a real ThreadingHTTPServer on port 0 and drives it
with urllib, the same way a problem's solution.py would.
"""

import json
import struct
import urllib.error
import urllib.request

import pytest

from loop.mockserver import maps


@pytest.fixture()
def server():
    srv, thread = maps.serve(port=0)
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield base
    srv.shutdown()
    srv.server_close()


def _post(base, path, body_obj=None, raw_body=None):
    data = raw_body if raw_body is not None else json.dumps(body_obj).encode()
    req = urllib.request.Request(
        base + path, data=data, method="POST", headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, resp.getheader("Content-Type"), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()


def _get(base, path):
    req = urllib.request.Request(base + path, method="GET")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_health(server):
    status, body = _get(server, "/health")
    assert status == 200
    assert json.loads(body) == {"ok": True}


def test_render_returns_png(server):
    points = [[52.5, 13.4], [52.51, 13.41], [52.52, 13.42]]
    status, ctype, body = _post(server, "/render", {"points": points})
    assert status == 200
    assert ctype == "image/png"
    assert body[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_respects_custom_width_height(server):
    points = [[0, 0], [1, 1]]
    status, ctype, body = _post(server, "/render", {"points": points, "width": 120, "height": 80})
    assert status == 200
    # IHDR chunk starts right after the 8-byte signature + 4-byte length + 4-byte type
    width, height = struct.unpack(">II", body[16:24])
    assert (width, height) == (120, 80)


def test_render_with_markers_does_not_error(server):
    points = [[52.5, 13.4], [52.52, 13.42]]
    markers = [[52.51, 13.41, "landmark"]]
    status, ctype, body = _post(server, "/render", {"points": points, "markers": markers})
    assert status == 200
    assert body[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_invalid_json_body_400(server):
    status, ctype, body = _post(server, "/render", raw_body=b"{not json")
    assert status == 400
    err = json.loads(body)["error"]
    assert err["type"] == "invalid_request_error"


def test_render_missing_points_400(server):
    status, ctype, body = _post(server, "/render", {"width": 100})
    assert status == 400
    assert json.loads(body)["error"]["type"] == "invalid_request_error"


def test_render_fewer_than_two_points_400(server):
    status, ctype, body = _post(server, "/render", {"points": [[0, 0]]})
    assert status == 400


def test_render_too_many_points_413(server):
    points = [[0.0001 * i, 0.0001 * i] for i in range(10001)]
    status, ctype, body = _post(server, "/render", {"points": points})
    assert status == 413


def test_render_request_id_header_present(server):
    points = [[0, 0], [1, 1]]
    data = json.dumps({"points": points}).encode()
    req = urllib.request.Request(
        server + "/render", data=data, method="POST", headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=5)
    assert resp.getheader("Request-Id", "").startswith("req_")
