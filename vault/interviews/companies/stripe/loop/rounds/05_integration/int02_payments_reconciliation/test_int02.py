"""int02 Payments reconciliation client — tests. Uses the `impl` fixture from the
repo-root conftest.py (loads solution.py, or starter.py under IMPL=starter) and the
`payments_server` fixture from this directory's conftest.py (a real
loop.mockserver.payments instance seeded to match data/ledger.csv: seed=7, n=20).
`run_script` (repo-root conftest.py) drives the module as a subprocess for io tests.
"""

from __future__ import annotations

import random
import time
import urllib.error
from pathlib import Path

import pytest

from loop.mockserver import payments

DATA_DIR = Path(__file__).parent / "data"
LEDGER_PATH = str(DATA_DIR / "ledger.csv")
API_KEY = "sk_test_123"

EXPECTED_MISSING_LOCAL = ["ch_bz8wtp1dk7gj2at9kl4istbo", "ch_j1rumyt24d6nxpl38ep128rc"]
EXPECTED_MISSING_REMOTE = ["ch_local_only_1", "ch_local_only_2"]
EXPECTED_MISMATCH_IDS = ["ch_89ti8lmanrshsajdobakivt1", "ch_9pdvdut8wchnw8vrer9rlf00"]


def _http_error(code, headers=None):
    return urllib.error.HTTPError("http://x/y", code, "msg", headers or {}, None)


# --------------------------------------------------------------------------- Part 1: fetch_all_charges


@pytest.mark.part1
def test_fetch_all_charges_happy_path(impl, payments_server):
    charges = impl.fetch_all_charges(payments_server, API_KEY)
    assert len(charges) == 20
    assert len(charges) == len({c["id"] for c in charges})  # no duplicates


@pytest.mark.part1
def test_fetch_all_charges_paginates_across_multiple_pages(impl):
    server, thread = payments.start_in_thread(port=0, seed=42, n=250, rate=1000, fail_every=0)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        charges = impl.fetch_all_charges(base, API_KEY, limit=100)
        assert len(charges) == 250
        assert len(charges) == len({c["id"] for c in charges})
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.part1
@pytest.mark.edge
def test_fetch_all_charges_bad_auth_raises_401(impl, payments_server):
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        impl.fetch_all_charges(payments_server, "totally-wrong-key-without-the-sk_test-prefix")
    assert exc_info.value.code == 401


@pytest.mark.part1
@pytest.mark.edge
def test_fetch_all_charges_connection_refused_raises(impl):
    with pytest.raises((urllib.error.URLError, OSError)):
        impl.fetch_all_charges("http://127.0.0.1:1", API_KEY)


# --------------------------------------------------------------------------- Part 2: with_retry


@pytest.mark.part2
def test_with_retry_retries_429_using_retry_after_header(impl):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] == 1:
            raise _http_error(429, {"Retry-After": "3"})
        return "ok"

    sleeps = []
    result = impl.with_retry(fn, sleep=sleeps.append)
    assert result == "ok"
    assert calls["n"] == 2
    assert sleeps == [3.0]


@pytest.mark.part2
def test_with_retry_exponential_backoff_on_5xx(impl):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] <= 2:
            raise _http_error(500)
        return "ok"

    sleeps = []
    result = impl.with_retry(fn, sleep=sleeps.append, rng=lambda: 0.0)
    assert result == "ok"
    assert calls["n"] == 3
    # base = 0.05 * 2**(attempt-1); rng()==0 so no jitter added
    assert sleeps[0] == pytest.approx(0.05)
    assert sleeps[1] == pytest.approx(0.10)


@pytest.mark.part2
@pytest.mark.edge
def test_with_retry_does_not_retry_non_429_4xx(impl):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise _http_error(400)

    with pytest.raises(urllib.error.HTTPError) as exc_info:
        impl.with_retry(fn, sleep=lambda s: None)
    assert exc_info.value.code == 400
    assert calls["n"] == 1  # not retried at all


@pytest.mark.part2
@pytest.mark.edge
def test_with_retry_reraises_after_max_attempts(impl):
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise _http_error(500)

    with pytest.raises(urllib.error.HTTPError):
        impl.with_retry(fn, max_attempts=3, sleep=lambda s: None, rng=lambda: 0.0)
    assert calls["n"] == 3


@pytest.mark.part2
@pytest.mark.edge
def test_with_retry_does_not_retry_timeout_or_connection_errors(impl):
    """`with_retry` only understands `urllib.error.HTTPError`; a timeout/connection
    failure (`TimeoutError`, a `URLError` subclass) must propagate immediately, not get
    treated as a retryable HTTP status."""
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        raise TimeoutError("timed out")

    with pytest.raises(TimeoutError):
        impl.with_retry(fn, sleep=lambda s: None)
    assert calls["n"] == 1


@pytest.mark.part2
def test_with_retry_success_first_try_never_sleeps(impl):
    sleeps = []
    result = impl.with_retry(lambda: "ok", sleep=sleeps.append)
    assert result == "ok"
    assert sleeps == []


# --------------------------------------------------------------------------- Part 3: refund + reconcile


@pytest.mark.part3
def test_refund_happy_path(impl, payments_server):
    charges = impl.fetch_all_charges(payments_server, API_KEY)
    target = next(c for c in charges if c["status"] == "succeeded")
    r = impl.refund(payments_server, API_KEY, target["id"], 100, "test-idem-happy")
    assert r["charge"] == target["id"]
    assert r["amount"] == 100
    assert r["id"].startswith("re_")


@pytest.mark.part3
@pytest.mark.edge
def test_refund_idempotent_replay_returns_same_id(impl, payments_server):
    charges = impl.fetch_all_charges(payments_server, API_KEY)
    target = next(c for c in charges if c["status"] == "succeeded")
    r1 = impl.refund(payments_server, API_KEY, target["id"], 50, "test-idem-replay")
    r2 = impl.refund(payments_server, API_KEY, target["id"], 50, "test-idem-replay")
    assert r1["id"] == r2["id"]


@pytest.mark.part3
@pytest.mark.edge
def test_refund_idempotent_key_reused_different_body_400(impl, payments_server):
    charges = impl.fetch_all_charges(payments_server, API_KEY)
    target = next(c for c in charges if c["status"] == "succeeded")
    impl.refund(payments_server, API_KEY, target["id"], 10, "test-idem-conflict")
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        impl.refund(payments_server, API_KEY, target["id"], 20, "test-idem-conflict")
    assert exc_info.value.code == 400


@pytest.mark.part3
def test_load_ledger_parses_all_rows(impl):
    rows = impl.load_ledger(LEDGER_PATH)
    assert len(rows) == 20
    assert all(isinstance(r["amount_cents"], int) for r in rows)
    first = rows[0]
    assert first["charge_id"] == "ch_xctncsbpcdp3eiw8uo9b4kfe"
    assert first["amount_cents"] == 248977
    assert first["status"] == "succeeded"


@pytest.mark.part3
def test_worked_example_reconcile(impl, payments_server):
    remote = impl.fetch_all_charges(payments_server, API_KEY)
    local = impl.load_ledger(LEDGER_PATH)
    diff = impl.reconcile(local, remote)
    assert diff["missing_local"] == EXPECTED_MISSING_LOCAL
    assert diff["missing_remote"] == EXPECTED_MISSING_REMOTE
    assert [m["charge_id"] for m in diff["amount_mismatch"]] == EXPECTED_MISMATCH_IDS
    by_id = {m["charge_id"]: m for m in diff["amount_mismatch"]}
    assert by_id["ch_9pdvdut8wchnw8vrer9rlf00"] == {
        "charge_id": "ch_9pdvdut8wchnw8vrer9rlf00",
        "local_amount_cents": 16800,
        "remote_amount_cents": 16817,
    }


@pytest.mark.part3
@pytest.mark.edge
def test_reconcile_empty_inputs(impl):
    assert impl.reconcile([], []) == {"missing_local": [], "missing_remote": [], "amount_mismatch": []}


@pytest.mark.part3
@pytest.mark.edge
def test_reconcile_all_matching_has_no_diffs(impl):
    local = [{"charge_id": "ch_a", "amount_cents": 100, "status": "succeeded"}]
    remote = [{"id": "ch_a", "amount": 100, "status": "succeeded"}]
    diff = impl.reconcile(local, remote)
    assert diff == {"missing_local": [], "missing_remote": [], "amount_mismatch": []}


@pytest.mark.part3
@pytest.mark.fmt
def test_reconcile_lists_are_sorted_by_charge_id(impl):
    local = [
        {"charge_id": "ch_z", "amount_cents": 1, "status": "succeeded"},
        {"charge_id": "ch_a", "amount_cents": 1, "status": "succeeded"},
    ]
    remote = [
        {"id": "ch_m", "amount": 1, "status": "succeeded"},
        {"id": "ch_b", "amount": 1, "status": "succeeded"},
    ]
    diff = impl.reconcile(local, remote)
    assert diff["missing_remote"] == ["ch_a", "ch_z"]
    assert diff["missing_local"] == ["ch_b", "ch_m"]


# --------------------------------------------------------------------------- Part 4: webhooks


@pytest.mark.part4
def test_verify_webhook_valid_signature(impl):
    payload = b'{"id":"evt_1","type":"charge.refunded"}'
    now = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", now)
    assert impl.verify_webhook(payload, header, "whsec_test_secret", now) is True


@pytest.mark.part4
@pytest.mark.edge
def test_verify_webhook_wrong_secret(impl):
    payload = b'{"id":"evt_1"}'
    now = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", now)
    assert impl.verify_webhook(payload, header, "whsec_totally_different", now) is False


@pytest.mark.part4
@pytest.mark.edge
def test_verify_webhook_tampered_payload(impl):
    payload = b'{"id":"evt_1"}'
    now = int(time.time())
    header = payments.sign(payload, "whsec_test_secret", now)
    assert impl.verify_webhook(b'{"id":"evt_2"}', header, "whsec_test_secret", now) is False


@pytest.mark.part4
@pytest.mark.edge
def test_verify_webhook_expired_timestamp(impl):
    payload = b'{"id":"evt_1"}'
    old_t = int(time.time()) - 1000
    header = payments.sign(payload, "whsec_test_secret", old_t)
    assert impl.verify_webhook(payload, header, "whsec_test_secret", int(time.time())) is False


@pytest.mark.part4
@pytest.mark.edge
def test_verify_webhook_within_tolerance_boundary(impl):
    payload = b'{"id":"evt_1"}'
    now = 1_000_000
    t = now - 300  # exactly at the default 5-minute tolerance boundary
    header = payments.sign(payload, "whsec_test_secret", t)
    assert impl.verify_webhook(payload, header, "whsec_test_secret", now, tolerance=300) is True
    header2 = payments.sign(payload, "whsec_test_secret", now - 301)
    assert impl.verify_webhook(payload, header2, "whsec_test_secret", now, tolerance=300) is False


@pytest.mark.part4
@pytest.mark.edge
def test_verify_webhook_malformed_header(impl):
    payload = b'{"id":"evt_1"}'
    assert impl.verify_webhook(payload, "not-a-valid-header", "whsec_test_secret", int(time.time())) is False
    assert impl.verify_webhook(payload, "", "whsec_test_secret", int(time.time())) is False


@pytest.mark.part4
def test_handle_event_idempotent(impl):
    store = set()
    evt = {"id": "evt_dup"}
    assert impl.handle_event(evt, store) is True
    assert impl.handle_event(evt, store) is False
    assert impl.handle_event({"id": "evt_other"}, store) is True
    assert store == {"evt_dup", "evt_other"}


# --------------------------------------------------------------------------- io


@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script, payments_server):
    r = run_script(f"PART 1\n{payments_server}\n{API_KEY}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "20 charges\n"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3(run_script, payments_server):
    r = run_script(f"PART 3\n{payments_server}\n{API_KEY}\n{LEDGER_PATH}\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "missing_local: " + ",".join(EXPECTED_MISSING_LOCAL)
    assert lines[1] == "missing_remote: " + ",".join(EXPECTED_MISSING_REMOTE)
    assert lines[2].startswith("amount_mismatch: ch_89ti8lmanrshsajdobakivt1(local=1400,remote=1449)")


@pytest.mark.part4
@pytest.mark.io
def test_io_part4(run_script):
    payload = '{"id":"evt_io"}'
    now = int(time.time())
    header = payments.sign(payload.encode(), "whsec_io_secret", now)
    r = run_script(f"PART 4\nwhsec_io_secret\n{now}\n{header}\n{payload}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "True\n"


@pytest.mark.part1
@pytest.mark.io
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""


# --------------------------------------------------------------------------- perf


@pytest.mark.part3
@pytest.mark.perf
def test_perf_reconcile_100k_rows(impl):
    rng = random.Random(0)
    local = [
        {"charge_id": f"ch_{i}", "amount_cents": rng.randint(100, 100_000), "status": "succeeded"}
        for i in range(100_000)
    ]
    remote = [
        {
            "id": f"ch_{i}",
            "amount": local[i]["amount_cents"] if i % 7 else local[i]["amount_cents"] + 1,
            "status": "succeeded",
        }
        for i in range(100_000)
    ]
    t0 = time.perf_counter()
    diff = impl.reconcile(local, remote)
    elapsed = time.perf_counter() - t0
    assert len(diff["amount_mismatch"]) > 0
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"
