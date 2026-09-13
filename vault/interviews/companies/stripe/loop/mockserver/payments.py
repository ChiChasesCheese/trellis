"""loop.mockserver.payments — a Stripe-flavored local mock for the int02 (payments
reconciliation) problem. stdlib only: `http.server`, `hmac`/`hashlib` for webhook
signing, `urllib.request` to deliver the one outbound webhook test call.

Endpoints (see loop/mockserver/README.md for one-line-each + curl + docs.stripe.com
cross-references; semantics follow loop/raw/stripe_official_and_api.md §3.1/3.3/3.4/3.5):

  GET  /v1/charges?limit=&starting_after=&ending_before=
  GET  /v1/charges/{id}
  POST /v1/refunds                      (Idempotency-Key aware)
  POST /v1/webhook_endpoints/test       (delivers one signed charge.refunded event)

Cross-cutting, applied in this order to every /v1/* request:
  1. rate limit (sliding 1s window, per client key = Authorization header else remote
     addr) -> 429 {"error": {"type": "rate_limit_error", ...}} + `Retry-After: 1`
  2. --fail-every N: every Nth request (that got past rate limiting) -> 500
  3. auth: missing/malformed `Authorization: Bearer sk_test_...` -> 401 authentication_error
  4. route dispatch

Every response carries a `Request-Id: req_<hex>` header.

Pure functions `sign`/`verify` (HMAC-SHA256 over `f"{t}.{payload}"`, Stripe-Signature
header shape `t=<unix>,v1=<hex>`) are reusable directly by a problem's solution.py — that
mirrors how a real integration would implement webhook verification.

Run standalone: `python3 -m loop.mockserver.payments --port 0 [--seed 0] [--n 250]
[--rate 5] [--fail-every 0]`. Import `serve`/`start_in_thread` for tests / fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac as hmac_mod
import json
import random
import secrets
import signal
import string
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WEBHOOK_SECRET = "whsec_test_secret"
STATUSES = ("succeeded", "failed", "refunded")
STATUS_WEIGHTS = (0.7, 0.2, 0.1)
CURRENCIES = ("usd", "usd", "usd", "eur", "gbp")


# --------------------------------------------------------------------------- webhook signing


def sign(payload: bytes, secret: str, t: int) -> str:
    """Build a `Stripe-Signature` header value for `payload`, signed at unix time `t`."""
    signed_payload = f"{t}.".encode() + payload
    mac = hmac_mod.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return f"t={t},v1={mac}"


def verify(payload: bytes, header: str, secret: str, tolerance: int = 300) -> bool:
    """Verify a `Stripe-Signature` header value against `payload`. `tolerance` seconds is
    the max allowed skew between the embedded timestamp and now (Stripe's own default is
    300s / 5 min — see loop/raw/stripe_official_and_api.md §3.4). Non-`v1` schemes inside
    the header (e.g. a future `v2`) are ignored, matching Stripe's documented behavior."""
    t = None
    v1_sigs = []
    for part in header.split(","):
        if "=" not in part:
            continue
        k, _, v = part.partition("=")
        k = k.strip()
        if k == "t":
            t = v.strip()
        elif k == "v1":
            v1_sigs.append(v.strip())
    if t is None or not v1_sigs:
        return False
    try:
        t_int = int(t)
    except ValueError:
        return False
    if abs(time.time() - t_int) > tolerance:
        return False
    signed_payload = f"{t}.".encode() + payload
    expected = hmac_mod.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return any(hmac_mod.compare_digest(expected, sig) for sig in v1_sigs)


# --------------------------------------------------------------------------- fixture data


def _rand_id(rng: random.Random, prefix: str, n: int = 24) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return prefix + "".join(rng.choices(alphabet, k=n))


def _generate_charges(rng: random.Random, n: int) -> list:
    charges = []
    created = int(time.time())
    for _ in range(n):
        created -= rng.randint(30, 3600)
        amount = rng.randint(500, 250_000)
        status = rng.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        charge = {
            "id": _rand_id(rng, "ch_"),
            "object": "charge",
            "amount": amount,
            "currency": rng.choice(CURRENCIES),
            "status": status,
            "created": created,
            "customer": _rand_id(rng, "cus_", 14),
            "metadata": {"order_id": f"order_{rng.randint(100000, 999999)}"},
            "refunded_amount": amount if status == "refunded" else 0,
        }
        charges.append(charge)
    return charges  # already reverse-chronological (created descending)


class PaymentsState:
    def __init__(self, seed: int = 0, n: int = 250, rate: int = 5, fail_every: int = 0):
        rng = random.Random(seed)
        self.charges = _generate_charges(rng, n)
        self.by_id = {c["id"]: c for c in self.charges}
        self.rate = rate
        self.fail_every = fail_every
        self.lock = threading.Lock()
        self._rate_windows: dict = {}  # client key -> list[float] recent request timestamps
        self._request_count = 0
        self._idempotency: dict = {}  # key -> (status, body_dict, response_dict)
        self._rng = rng
        self.last_refund = None

    def public_charge(self, c: dict) -> dict:
        return {k: v for k, v in c.items() if k != "refunded_amount"}

    # -- cross-cutting checks, called under self.lock by the handler --

    def check_rate_limit(self, client_key: str) -> bool:
        """Returns True if this request is allowed (and records it)."""
        now = time.time()
        window = self._rate_windows.setdefault(client_key, [])
        window[:] = [t for t in window if now - t < 1.0]
        if len(window) >= self.rate:
            return False
        window.append(now)
        return True

    def bump_and_should_fail(self) -> bool:
        self._request_count += 1
        return self.fail_every > 0 and self._request_count % self.fail_every == 0


def _error_body(error_type: str, message: str, code: str = None) -> bytes:
    err = {"type": error_type, "message": message}
    if code:
        err["code"] = code
    return json.dumps({"error": err}).encode()


class Handler(BaseHTTPRequestHandler):
    server_version = "loop-mockserver-payments/0.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # silence default stderr access log
        pass

    # -- response helpers --

    def _send_json(self, status: int, payload: dict, extra_headers: dict = None) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Request-Id", f"req_{secrets.token_hex(8)}")
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _send_error_body(self, status: int, body: bytes, extra_headers: dict = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Request-Id", f"req_{secrets.token_hex(8)}")
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _error(
        self, status: int, error_type: str, message: str, code: str = None, extra_headers: dict = None
    ) -> None:
        self._send_error_body(status, _error_body(error_type, message, code), extra_headers)

    # -- cross-cutting pipeline --

    def _client_key(self) -> str:
        auth = self.headers.get("Authorization")
        return auth if auth else self.client_address[0]

    def _run_pipeline(self) -> bool:
        """Rate limit -> fail-every -> auth. Returns True if the request may proceed to
        route dispatch (having already sent a response and returned False otherwise)."""
        state: PaymentsState = self.server.state
        with state.lock:
            allowed = state.check_rate_limit(self._client_key())
            if not allowed:
                self._error(429, "rate_limit_error", "Too many requests", extra_headers={"Retry-After": "1"})
                return False
            should_fail = state.bump_and_should_fail()
        if should_fail:
            self._error(500, "api_error", "simulated failure (--fail-every)")
            return False
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer sk_test_"):
            self._error(401, "authentication_error", "No valid API key provided")
            return False
        return True

    def _read_json_or_form(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip()
        if not raw:
            return {}
        if ctype == "application/json" or (not ctype and raw.strip().startswith(b"{")):
            return json.loads(raw.decode("utf-8"))
        parsed = urllib.parse.parse_qs(raw.decode("utf-8"), keep_blank_values=True)
        return {k: v[0] for k, v in parsed.items()}

    # -- routing --

    def do_GET(self):
        if not self._run_pipeline():
            return
        parts = urllib.parse.urlsplit(self.path)
        path = parts.path
        query = urllib.parse.parse_qs(parts.query)
        state: PaymentsState = self.server.state
        if path == "/v1/charges":
            self._list_charges(state, query)
        elif path.startswith("/v1/charges/"):
            charge_id = path[len("/v1/charges/") :]
            self._get_charge(state, charge_id)
        else:
            self._error(404, "invalid_request_error", f"unknown path {path!r}")

    def do_POST(self):
        if not self._run_pipeline():
            return
        state: PaymentsState = self.server.state
        if self.path == "/v1/refunds":
            self._create_refund(state)
        elif self.path == "/v1/webhook_endpoints/test":
            self._webhook_test(state)
        else:
            self._error(404, "invalid_request_error", f"unknown path {self.path!r}")

    # -- GET /v1/charges --

    def _list_charges(self, state: PaymentsState, query: dict) -> None:
        limit_raw = query.get("limit", ["10"])[0]
        try:
            limit = int(limit_raw)
        except ValueError:
            self._error(400, "invalid_request_error", "'limit' must be an integer")
            return
        if not (1 <= limit <= 100):
            self._error(400, "invalid_request_error", "'limit' must be between 1 and 100")
            return

        starting_after = query.get("starting_after", [None])[0]
        ending_before = query.get("ending_before", [None])[0]
        if starting_after and ending_before:
            self._error(
                400, "invalid_request_error", "cannot specify both 'starting_after' and 'ending_before'"
            )
            return

        charges = state.charges  # already reverse-chronological
        if starting_after is not None:
            if starting_after not in state.by_id:
                self._error(400, "invalid_request_error", f"No such charge (cursor): {starting_after!r}")
                return
            idx = next(i for i, c in enumerate(charges) if c["id"] == starting_after)
            candidates = charges[idx + 1 :]
            page = candidates[:limit]
            has_more = len(candidates) > limit
        elif ending_before is not None:
            if ending_before not in state.by_id:
                self._error(400, "invalid_request_error", f"No such charge (cursor): {ending_before!r}")
                return
            idx = next(i for i, c in enumerate(charges) if c["id"] == ending_before)
            candidates = charges[:idx]
            page = candidates[-limit:] if limit else []
            has_more = len(candidates) > limit
        else:
            page = charges[:limit]
            has_more = len(charges) > limit

        self._send_json(
            200,
            {
                "object": "list",
                "url": "/v1/charges",
                "has_more": has_more,
                "data": [state.public_charge(c) for c in page],
            },
        )

    # -- GET /v1/charges/{id} --

    def _get_charge(self, state: PaymentsState, charge_id: str) -> None:
        c = state.by_id.get(charge_id)
        if c is None:
            self._error(
                404, "invalid_request_error", f"No such charge: {charge_id!r}", code="resource_missing"
            )
            return
        self._send_json(200, state.public_charge(c))

    # -- POST /v1/refunds --

    def _create_refund(self, state: PaymentsState) -> None:
        try:
            body = self._read_json_or_form()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._error(400, "invalid_request_error", "request body is not valid JSON")
            return
        if not isinstance(body, dict):
            self._error(400, "invalid_request_error", "request body must be an object")
            return

        idem_key = self.headers.get("Idempotency-Key")
        normalized = {"charge": body.get("charge"), "amount": body.get("amount")}

        if idem_key:
            with state.lock:
                cached = state._idempotency.get(idem_key)
            if cached is not None:
                cached_body, status, response = cached
                if cached_body != normalized:
                    self._error(
                        400,
                        "idempotency_error",
                        f"Keys for idempotent requests can only be used once; a request with "
                        f"the key {idem_key!r} was already used with different parameters.",
                    )
                    return
                self._send_json(status, response)
                return

        charge_id = body.get("charge")
        if not charge_id:
            self._error(400, "invalid_request_error", "missing required param: 'charge'")
            return
        c = state.by_id.get(charge_id)
        if c is None:
            self._error(400, "invalid_request_error", f"No such charge: {charge_id!r}")
            return

        amount_raw = body.get("amount")
        try:
            amount = int(amount_raw) if amount_raw is not None else c["amount"] - c["refunded_amount"]
        except (TypeError, ValueError):
            self._error(400, "invalid_request_error", "'amount' must be an integer")
            return

        with state.lock:
            if c["status"] != "succeeded" or c["refunded_amount"] >= c["amount"]:
                self._error(
                    400,
                    "invalid_request_error",
                    "Charge has already been refunded",
                    code="charge_already_refunded",
                )
                if idem_key:
                    state._idempotency[idem_key] = (
                        normalized,
                        400,
                        json.loads(
                            _error_body(
                                "invalid_request_error",
                                "Charge has already been refunded",
                                "charge_already_refunded",
                            )
                        ),
                    )
                return
            remaining = c["amount"] - c["refunded_amount"]
            if amount <= 0 or amount > remaining:
                self._error(
                    400,
                    "invalid_request_error",
                    "Refund amount is greater than unrefunded amount on charge",
                    code="amount_too_large",
                )
                if idem_key:
                    state._idempotency[idem_key] = (
                        normalized,
                        400,
                        json.loads(
                            _error_body(
                                "invalid_request_error",
                                "Refund amount is greater than unrefunded amount on charge",
                                "amount_too_large",
                            )
                        ),
                    )
                return

            c["refunded_amount"] += amount
            if c["refunded_amount"] >= c["amount"]:
                c["status"] = "refunded"
            refund = {
                "id": _rand_id(state._rng, "re_"),
                "object": "refund",
                "charge": charge_id,
                "amount": amount,
                "currency": c["currency"],
                "status": "succeeded",
                "created": int(time.time()),
            }
            state.last_refund = refund
            if idem_key:
                state._idempotency[idem_key] = (normalized, 200, refund)

        self._send_json(200, refund)

    # -- POST /v1/webhook_endpoints/test --

    def _webhook_test(self, state: PaymentsState) -> None:
        try:
            body = self._read_json_or_form()
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._error(400, "invalid_request_error", "request body is not valid JSON")
            return
        url = body.get("url") if isinstance(body, dict) else None
        if not url:
            self._error(400, "invalid_request_error", "missing required param: 'url'")
            return

        refund = getattr(state, "last_refund", None) or {
            "id": _rand_id(state._rng, "re_"),
            "object": "refund",
            "charge": state.charges[0]["id"] if state.charges else None,
            "amount": 0,
            "currency": "usd",
            "status": "succeeded",
            "created": int(time.time()),
        }
        event = {
            "id": _rand_id(state._rng, "evt_"),
            "object": "event",
            "type": "charge.refunded",
            "created": int(time.time()),
            "data": {"object": refund},
        }
        payload = json.dumps(event).encode()
        t = int(time.time())
        header = sign(payload, WEBHOOK_SECRET, t)

        req = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json", "Stripe-Signature": header},
        )
        delivered = False
        response_status = None
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                response_status = resp.status
                delivered = 200 <= resp.status < 300
        except urllib.error.HTTPError as e:
            response_status = e.code
            delivered = False
        except (urllib.error.URLError, OSError, TimeoutError):
            delivered = False

        self._send_json(
            200,
            {
                "delivered": delivered,
                "response_status": response_status,
                "event": event,
            },
        )


def _build_server(
    port: int = 0, host: str = "127.0.0.1", seed: int = 0, n: int = 250, rate: int = 5, fail_every: int = 0
) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), Handler)
    server.state = PaymentsState(seed=seed, n=n, rate=rate, fail_every=fail_every)
    return server


def serve(
    port: int = 0,
    host: str = "127.0.0.1",
    seed: int = 0,
    n: int = 250,
    rate: int = 5,
    fail_every: int = 0,
    **_opts,
):
    """Start the payments mockserver in a daemon thread. Returns (server, thread)."""
    server = _build_server(port, host, seed=seed, n=n, rate=rate, fail_every=fail_every)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


start_in_thread = serve


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python3 -m loop.mockserver.payments")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n", type=int, default=250)
    parser.add_argument("--rate", type=int, default=5)
    parser.add_argument("--fail-every", type=int, default=0)
    args = parser.parse_args(argv)
    server = _build_server(args.port, seed=args.seed, n=args.n, rate=args.rate, fail_every=args.fail_every)
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
