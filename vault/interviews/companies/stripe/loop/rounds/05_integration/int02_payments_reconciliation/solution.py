"""int02 Payments reconciliation client — reference solution.

Talks to the local `payments` mockserver (`loop/mockserver/payments.py`, a
Stripe-flavored charges/refunds/webhooks API) to: page through every charge, retry
429/5xx responses with backoff, issue idempotent refunds and reconcile a local ledger
against the remote charge list, and verify + de-dupe inbound webhook events.

Public API (same shape as starter.py / starter_template.py):
    fetch_all_charges(base_url, api_key, limit=100, sleep=time.sleep) -> list[dict]  Part 1
    with_retry(fn, max_attempts=5, sleep=time.sleep, rng=random.random)              Part 2
    refund(base_url, api_key, charge_id, amount, idempotency_key, sleep=...) -> dict  Part 3
    load_ledger(path) -> list[dict]                                                   Part 3
    reconcile(local_rows, remote_charges) -> dict                                     Part 3
    verify_webhook(payload, sig_header, secret, now, tolerance=300) -> bool           Part 4
    handle_event(event, store) -> bool                                                Part 4
    main(stdin=sys.stdin, stdout=sys.stdout) -> None                                  PART n driver

Only stdlib: `urllib.request`/`urllib.error`, `json`, `csv`, `hmac`, `hashlib`, `random`, `time`.
"""

from __future__ import annotations

import csv
import hashlib
import hmac
import json
import random
import sys
import time
import urllib.error
import urllib.request


# --------------------------------------------------------------------------- Part 2 (used by Part 1 + 3)


def with_retry(fn, max_attempts: int = 5, sleep=time.sleep, rng=random.random):
    """Call `fn()` (a zero-arg callable that performs one HTTP attempt and raises
    `urllib.error.HTTPError` for a non-2xx response). Retries:
      - 429: sleeps for the `Retry-After` header (seconds, default 1 if absent/invalid),
        then retries — no exponential growth (the server is telling us exactly how long
        to wait).
      - 5xx: exponential backoff with jitter: base = 0.05 * 2**(attempt-1) seconds,
        actual sleep = base + rng() * base (rng() in [0, 1), so up to 2x base).
      - anything else (4xx other than 429, or `fn` succeeding): not retried — a 4xx other
        than 429 re-raises immediately, success returns immediately.
    After `max_attempts` total attempts, the last exception is re-raised. `sleep` and
    `rng` are injectable so tests never actually wait."""
    attempt = 0
    while True:
        attempt += 1
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if attempt >= max_attempts:
                raise
            if e.code == 429:
                retry_after_raw = e.headers.get("Retry-After") if e.headers else None
                try:
                    retry_after = float(retry_after_raw) if retry_after_raw else 1.0
                except ValueError:
                    retry_after = 1.0
                sleep(retry_after)
                continue
            if 500 <= e.code < 600:
                base = 0.05 * (2 ** (attempt - 1))
                sleep(base + rng() * base)
                continue
            raise


# --------------------------------------------------------------------------- HTTP transport (shared by
# Part 1, Part 3 and the PART-n driver — the only place that touches `urllib` directly, so pagination,
# reconciliation and the refund/idempotency logic never have to know how a request is actually built)


def _request(
    base_url: str, method: str, path: str, api_key: str, body: bytes | None = None, extra_headers=None
):
    """One HTTP attempt against the payments API. Returns the parsed JSON body; raises
    `urllib.error.HTTPError` for a non-2xx response (the shape `with_retry`'s `fn` must
    raise) and `urllib.error.URLError`/`OSError` for connection failures/timeouts (not
    caught here — those are not retried, see `with_retry`'s docstring)."""
    headers = {"Authorization": f"Bearer {api_key}"}
    headers.update(extra_headers or {})
    req = urllib.request.Request(base_url.rstrip("/") + path, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


# --------------------------------------------------------------------------- Part 1


def fetch_all_charges(base_url: str, api_key: str, limit: int = 100, sleep=time.sleep) -> list[dict]:
    """Page through GET /v1/charges (cursor pagination: `limit` + `starting_after`)
    until `has_more` is false, retrying transient failures via `with_retry`. Returns
    every charge in reverse-chronological order (the order the API returns them)."""
    charges: list[dict] = []
    starting_after: str | None = None
    while True:
        qs = f"limit={limit}"
        if starting_after is not None:
            qs += f"&starting_after={starting_after}"
        path = f"/v1/charges?{qs}"
        page = with_retry(lambda p=path: _request(base_url, "GET", p, api_key), sleep=sleep)
        charges.extend(page["data"])
        if not page.get("has_more"):
            break
        starting_after = page["data"][-1]["id"]
    return charges


# --------------------------------------------------------------------------- Part 3


def refund(
    base_url: str,
    api_key: str,
    charge_id: str,
    amount: int,
    idempotency_key: str,
    sleep=time.sleep,
) -> dict:
    """POST /v1/refunds with an Idempotency-Key header. Replaying the same key + same
    (charge, amount) returns the exact same refund object (same `id`) — the server does
    the de-duplication; this function just has to send the header on every attempt,
    including retries (an idempotency key must survive a retry, or the retry would
    create a second refund)."""
    body = json.dumps({"charge": charge_id, "amount": amount}).encode("utf-8")
    headers = {"Content-Type": "application/json", "Idempotency-Key": idempotency_key}
    return with_retry(
        lambda: _request(base_url, "POST", "/v1/refunds", api_key, body=body, extra_headers=headers),
        sleep=sleep,
    )


def load_ledger(path: str) -> list[dict]:
    """Read the local ledger CSV (`charge_id,amount_cents,status`) into
    [{"charge_id": str, "amount_cents": int, "status": str}, ...]."""
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "charge_id": row["charge_id"].strip(),
                    "amount_cents": int(row["amount_cents"]),
                    "status": row["status"].strip(),
                }
            )
    return rows


def reconcile(local_rows: list[dict], remote_charges: list[dict]) -> dict:
    """Compare the local ledger against the remote charge list. Returns:
      - "missing_local": charge ids present remotely but absent from the local ledger
      - "missing_remote": charge ids present in the local ledger but absent remotely
      - "amount_mismatch": [{"charge_id", "local_amount_cents", "remote_amount_cents"}]
        for ids present in both, where the amounts disagree
    All three lists are sorted by charge_id for deterministic output."""
    local_by_id = {r["charge_id"]: r for r in local_rows}
    remote_by_id = {c["id"]: c for c in remote_charges}

    missing_local = sorted(set(remote_by_id) - set(local_by_id))
    missing_remote = sorted(set(local_by_id) - set(remote_by_id))

    amount_mismatch = []
    for cid in sorted(set(local_by_id) & set(remote_by_id)):
        local_amt = local_by_id[cid]["amount_cents"]
        remote_amt = remote_by_id[cid]["amount"]
        if local_amt != remote_amt:
            amount_mismatch.append(
                {
                    "charge_id": cid,
                    "local_amount_cents": local_amt,
                    "remote_amount_cents": remote_amt,
                }
            )

    return {
        "missing_local": missing_local,
        "missing_remote": missing_remote,
        "amount_mismatch": amount_mismatch,
    }


# --------------------------------------------------------------------------- Part 4


def verify_webhook(payload: bytes, sig_header: str, secret: str, now: int, tolerance: int = 300) -> bool:
    """Verify a `Stripe-Signature`-shaped header (`t=<unix>,v1=<hex>[,v1=<hex>...]`)
    against `payload`, implemented from scratch (HMAC-SHA256 over `f"{t}.{payload}"`,
    constant-time comparison, `tolerance` seconds max skew between `t` and `now`) —
    mirrors `docs.stripe.com/webhooks` and intentionally does not import
    `loop.mockserver.payments.verify`, even though that function does the same thing,
    so this module doesn't depend on the mock server package at runtime."""
    t = None
    v1_sigs: list[str] = []
    for part in sig_header.split(","):
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
    if abs(now - t_int) > tolerance:
        return False
    signed_payload = f"{t}.".encode("utf-8") + payload
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return any(hmac.compare_digest(expected, sig) for sig in v1_sigs)


def handle_event(event: dict, store: set) -> bool:
    """Idempotent webhook event processing: `store` is the set of already-processed
    `event["id"]` values (mutated in place, so callers reuse it across calls). Returns
    True if this call actually processed the event (first time seen), False if it was a
    duplicate delivery (per docs.stripe.com/webhooks: "endpoints might occasionally
    receive the same event more than once" — track event ids, not `created`)."""
    evt_id = event.get("id")
    if evt_id in store:
        return False
    store.add(evt_id)
    return True


# --------------------------------------------------------------------------- PART n stdin driver


def _read_nonblank(stdin) -> list[str]:
    return [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = _read_nonblank(stdin)
    if not lines or not lines[0].upper().startswith("PART"):
        return
    part = int(lines[0].split()[1])
    args = lines[1:]
    out: list[str] = []

    if part == 1:
        server, api_key = args
        charges = fetch_all_charges(server, api_key)
        out = [f"{len(charges)} charges"]

    elif part == 2:
        server, api_key = args
        page = with_retry(lambda: _request(server, "GET", "/v1/charges?limit=100", api_key))
        out = [f"{len(page['data'])} charges has_more={page['has_more']}"]

    elif part == 3:
        server, api_key, ledger_path = args
        remote = fetch_all_charges(server, api_key)
        local = load_ledger(ledger_path)
        diff = reconcile(local, remote)
        out.append("missing_local: " + ",".join(diff["missing_local"]))
        out.append("missing_remote: " + ",".join(diff["missing_remote"]))
        mismatch_parts = [
            f"{m['charge_id']}(local={m['local_amount_cents']},remote={m['remote_amount_cents']})"
            for m in diff["amount_mismatch"]
        ]
        out.append("amount_mismatch: " + ",".join(mismatch_parts))

    elif part == 4:
        secret, now_raw, sig_header, payload_json = args
        result = verify_webhook(payload_json.encode("utf-8"), sig_header, secret, int(now_raw))
        out = [str(result)]

    else:
        raise ValueError(f"unknown PART {part!r}")

    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
