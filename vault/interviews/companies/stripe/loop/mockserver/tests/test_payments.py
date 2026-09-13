"""Tests for loop.mockserver.payments — a Stripe-flavored local mock the int02 (payments
reconciliation) problem talks to: cursor pagination, rate limiting, idempotent refunds,
webhook signing. Starts a real ThreadingHTTPServer on port 0 and drives it with urllib,
plus a tiny local receiver server for the webhook-delivery test.
"""

import json
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from loop.mockserver import payments

AUTH = {"Authorization": "Bearer sk_test_123"}


def _start(**opts):
    srv, thread = payments.serve(port=0, **opts)
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    return srv, base


@pytest.fixture()
def server():
    srv, base = _start(seed=0, n=30, rate=100, fail_every=0)
    yield base
    srv.shutdown()
    srv.server_close()


def _req(base, path, method="GET", headers=None, body=None):
    data = None
    hdrs = dict(headers or {})
    if body is not None:
        data = json.dumps(body).encode()
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(base + path, data=data, method=method, headers=hdrs)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return resp.status, dict(resp.headers), json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, dict(e.headers), (json.loads(raw) if raw else {})


# --------------------------------------------------------------------------- auth


def test_missing_auth_401(server):
    status, headers, body = _req(server, "/v1/charges")
    assert status == 401
    assert body["error"]["type"] == "authentication_error"


def test_request_id_header_present(server):
    status, headers, body = _req(server, "/v1/charges", headers=AUTH)
    assert status == 200
    assert headers.get("Request-Id", "").startswith("req_")


# --------------------------------------------------------------------------- list charges


def test_list_charges_default_limit(server):
    status, headers, body = _req(server, "/v1/charges", headers=AUTH)
    assert status == 200
    assert body["object"] == "list"
    assert len(body["data"]) == 10
    assert body["has_more"] is True


def test_list_charges_are_reverse_chronological(server):
    status, headers, body = _req(server, "/v1/charges?limit=30", headers=AUTH)
    created = [c["created"] for c in body["data"]]
    assert created == sorted(created, reverse=True)
    assert body["has_more"] is False


def test_list_charges_pagination_starting_after_no_overlap(server):
    _, _, page1 = _req(server, "/v1/charges?limit=5", headers=AUTH)
    last_id = page1["data"][-1]["id"]
    _, _, page2 = _req(server, f"/v1/charges?limit=5&starting_after={last_id}", headers=AUTH)
    ids1 = {c["id"] for c in page1["data"]}
    ids2 = {c["id"] for c in page2["data"]}
    assert ids1.isdisjoint(ids2)
    assert len(page2["data"]) == 5


def test_list_charges_pagination_ending_before_returns_previous_page(server):
    _, _, page1 = _req(server, "/v1/charges?limit=5", headers=AUTH)
    _, _, page2 = _req(server, "/v1/charges?limit=5&starting_after=" + page1["data"][-1]["id"], headers=AUTH)
    first_id_of_page2 = page2["data"][0]["id"]
    _, _, back = _req(server, f"/v1/charges?limit=5&ending_before={first_id_of_page2}", headers=AUTH)
    assert [c["id"] for c in back["data"]] == [c["id"] for c in page1["data"]]


def test_list_charges_invalid_cursor_400(server):
    status, headers, body = _req(server, "/v1/charges?starting_after=ch_doesnotexist", headers=AUTH)
    assert status == 400
    assert body["error"]["type"] == "invalid_request_error"


def test_list_charges_invalid_limit_400(server):
    status, headers, body = _req(server, "/v1/charges?limit=0", headers=AUTH)
    assert status == 400
    status2, _, _ = _req(server, "/v1/charges?limit=101", headers=AUTH)
    assert status2 == 400


def test_list_charges_both_cursors_400(server):
    status, headers, body = _req(server, "/v1/charges?starting_after=ch_x&ending_before=ch_y", headers=AUTH)
    assert status == 400


# --------------------------------------------------------------------------- get charge


def test_get_charge_by_id(server):
    _, _, listing = _req(server, "/v1/charges?limit=1", headers=AUTH)
    charge_id = listing["data"][0]["id"]
    status, headers, body = _req(server, f"/v1/charges/{charge_id}", headers=AUTH)
    assert status == 200
    assert body["id"] == charge_id


def test_get_charge_not_found_404(server):
    status, headers, body = _req(server, "/v1/charges/ch_doesnotexist", headers=AUTH)
    assert status == 404
    assert body["error"]["code"] == "resource_missing"


# --------------------------------------------------------------------------- refunds


def _find_refundable(base):
    _, _, listing = _req(base, "/v1/charges?limit=30", headers=AUTH)
    for c in listing["data"]:
        if c["status"] == "succeeded":
            return c
    raise AssertionError("no succeeded charge in fixture data (adjust seed/n)")


def test_refund_success(server):
    charge = _find_refundable(server)
    status, headers, body = _req(
        server, "/v1/refunds", method="POST", headers=AUTH, body={"charge": charge["id"], "amount": 100}
    )
    assert status == 200
    assert body["charge"] == charge["id"]
    assert body["amount"] == 100
    assert body["id"].startswith("re_")


def test_refund_idempotency_replay_same_response(server):
    charge = _find_refundable(server)
    headers = dict(AUTH, **{"Idempotency-Key": "test-key-1"})
    body_req = {"charge": charge["id"], "amount": 50}
    status1, _, body1 = _req(server, "/v1/refunds", method="POST", headers=headers, body=body_req)
    status2, _, body2 = _req(server, "/v1/refunds", method="POST", headers=headers, body=body_req)
    assert status1 == status2 == 200
    assert body1["id"] == body2["id"]  # same refund object replayed, not a new one


def test_refund_idempotency_conflict_different_body_400(server):
    charge = _find_refundable(server)
    headers = dict(AUTH, **{"Idempotency-Key": "test-key-2"})
    _req(server, "/v1/refunds", method="POST", headers=headers, body={"charge": charge["id"], "amount": 10})
    status, _, body = _req(
        server, "/v1/refunds", method="POST", headers=headers, body={"charge": charge["id"], "amount": 20}
    )
    assert status == 400
    assert body["error"]["type"] == "idempotency_error"


def test_refund_amount_too_large_400(server):
    charge = _find_refundable(server)
    status, _, body = _req(
        server,
        "/v1/refunds",
        method="POST",
        headers=AUTH,
        body={"charge": charge["id"], "amount": charge["amount"] + 1},
    )
    assert status == 400
    assert body["error"]["code"] == "amount_too_large"


def test_refund_charge_already_refunded_400(server):
    charge = _find_refundable(server)
    # fully refund it first
    _req(
        server,
        "/v1/refunds",
        method="POST",
        headers=AUTH,
        body={"charge": charge["id"], "amount": charge["amount"]},
    )
    status, _, body = _req(
        server, "/v1/refunds", method="POST", headers=AUTH, body={"charge": charge["id"], "amount": 1}
    )
    assert status == 400
    assert body["error"]["code"] == "charge_already_refunded"


def test_refund_without_idempotency_key_creates_new_refund_each_time(server):
    charge = _find_refundable(server)
    _, _, body1 = _req(
        server, "/v1/refunds", method="POST", headers=AUTH, body={"charge": charge["id"], "amount": 1}
    )
    _, _, body2 = _req(
        server, "/v1/refunds", method="POST", headers=AUTH, body={"charge": charge["id"], "amount": 1}
    )
    assert body1["id"] != body2["id"]


# --------------------------------------------------------------------------- rate limiting


def test_rate_limit_429_with_retry_after():
    srv, base = _start(seed=1, n=10, rate=2, fail_every=0)
    try:
        statuses = []
        for _ in range(4):
            status, headers, body = _req(base, "/v1/charges", headers=AUTH)
            statuses.append((status, headers.get("Retry-After")))
        assert any(s == 429 for s, _ in statuses)
        limited = next(h for s, h in statuses if s == 429)
        assert limited == "1"
    finally:
        srv.shutdown()
        srv.server_close()


def test_rate_limit_error_body_type():
    srv, base = _start(seed=2, n=10, rate=1, fail_every=0)
    try:
        _req(base, "/v1/charges", headers=AUTH)
        status, headers, body = _req(base, "/v1/charges", headers=AUTH)
        assert status == 429
        assert body["error"]["type"] == "rate_limit_error"
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- fail-every


def test_fail_every_returns_500():
    srv, base = _start(seed=3, n=10, rate=1000, fail_every=3)
    try:
        statuses = []
        for _ in range(3):
            status, _, _ = _req(base, "/v1/charges", headers=AUTH)
            statuses.append(status)
        assert statuses == [200, 200, 500]
    finally:
        srv.shutdown()
        srv.server_close()


# --------------------------------------------------------------------------- webhook signing (pure functions)


def test_sign_and_verify_roundtrip():
    payload = b'{"id": "evt_1", "type": "charge.refunded"}'
    t = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", t)
    assert payments.verify(payload, header, "whsec_test_secret")


def test_verify_rejects_tampered_payload():
    payload = b'{"id": "evt_1"}'
    t = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", t)
    assert not payments.verify(b'{"id": "evt_2"}', header, "whsec_test_secret")


def test_verify_rejects_expired_timestamp():
    payload = b'{"id": "evt_1"}'
    old_t = int(time.time()) - 10_000
    header = payments.sign(payload, "whsec_test_secret", old_t)
    assert not payments.verify(payload, header, "whsec_test_secret", tolerance=300)


def test_verify_wrong_secret_fails():
    payload = b'{"id": "evt_1"}'
    t = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", t)
    assert not payments.verify(payload, header, "whsec_wrong_secret")


# --------------------------------------------------------------------------- webhook delivery endpoint


class _CapturingReceiver(BaseHTTPRequestHandler):
    captured = []

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        _CapturingReceiver.captured.append((body, self.headers.get("Stripe-Signature")))
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, fmt, *args):
        pass


def test_webhook_endpoints_test_delivers_signed_event(server):
    _CapturingReceiver.captured = []
    receiver = HTTPServer(("127.0.0.1", 0), _CapturingReceiver)
    thread = threading.Thread(target=receiver.serve_forever, daemon=True)
    thread.start()
    try:
        receiver_url = f"http://127.0.0.1:{receiver.server_address[1]}/hook"
        status, headers, body = _req(
            server, "/v1/webhook_endpoints/test", method="POST", headers=AUTH, body={"url": receiver_url}
        )
        assert status == 200
        assert body["delivered"] is True
        assert body["event"]["type"] == "charge.refunded"

        assert len(_CapturingReceiver.captured) == 1
        received_payload, sig_header = _CapturingReceiver.captured[0]
        assert payments.verify(received_payload, sig_header, payments.WEBHOOK_SECRET)
        assert json.loads(received_payload)["id"] == body["event"]["id"]
    finally:
        receiver.shutdown()
        receiver.server_close()
