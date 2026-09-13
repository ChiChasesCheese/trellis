import random

import pytest

# ---------------------------------------------------------------------- shared fixtures / data
EX1 = """\
INIT m1 0
CREATE p1 m1 100 card
CONFIRM p1
CREATE p2 m1 50 bank_debit
CONFIRM p2
SETTLE p2
BALANCE m1"""
EX1_OUT = [
    "CREATE p1 OK",
    "CONFIRM p1 succeeded",
    "CREATE p2 OK",
    "CONFIRM p2 processing",
    "SETTLE p2 OK",
    "BALANCE m1 150",
]

EX2 = """\
INIT m1 0
CREATE p1 m1 100 card
UPDATE p1 80
CHANGE_METHOD p1 bank_debit
CONFIRM p1
SETTLE p1
UPDATE p1 999
BALANCE m1"""
EX2_OUT = [
    "CREATE p1 OK",
    "UPDATE p1 OK",
    "CHANGE_METHOD p1 OK",
    "CONFIRM p1 processing",
    "SETTLE p1 OK",
    "UPDATE p1 IGNORED",
    "BALANCE m1 80",
]

EX3 = """\
INIT m1 0
CREATE p1 m1 100 bank_debit
CONFIRM p1
FAIL p1
CONFIRM p1
FAIL p1
CONFIRM p1
FAIL p1
CONFIRM p1
CREATE p2 m1 40 card
CANCEL p2
CREATE p3 m1 20 bank_debit
CONFIRM p3
CANCEL p3
BALANCE m1"""
EX3_OUT = [
    "CREATE p1 OK",
    "CONFIRM p1 processing",
    "FAIL p1 OK",
    "CONFIRM p1 processing",
    "FAIL p1 OK",
    "CONFIRM p1 processing",
    "FAIL p1 OK",
    "CONFIRM p1 canceled",
    "CREATE p2 OK",
    "CANCEL p2 OK",
    "CREATE p3 OK",
    "CONFIRM p3 processing",
    "CANCEL p3 OK",
    "BALANCE m1 0",
]

EX4 = """\
1 INIT m1 0
2 CREATE p1 m1 100 bank_debit 5
3 CONFIRM p1
8 SETTLE p1
2 CREATE p2 m1 50 bank_debit 5
3 CONFIRM p2
20 EXPIRE p2
2 CREATE p3 m1 30 bank_debit 0
3 CONFIRM p3
3 SETTLE p3
2 CREATE p4 m1 10 bank_debit -1
3 CONFIRM p4
20 BALANCE m1"""
EX4_OUT = [
    "CREATE p1 OK",
    "CONFIRM p1 processing",
    "SETTLE p1 OK",
    "CREATE p2 OK",
    "CONFIRM p2 processing",
    "EXPIRE p2 OK",
    "CREATE p3 OK",
    "CONFIRM p3 processing",
    "SETTLE p3 OK",
    "CREATE p4 IGNORED",
    "CONFIRM p4 ignored",
    "BALANCE m1 130",
]


# ============================================================================== Part 1
@pytest.mark.part1
def test_example1_verbatim(impl):
    assert impl.part1(EX1.splitlines()) == EX1_OUT


@pytest.mark.part1
def test_card_confirm_is_synchronous_and_credits_immediately(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    assert e.create_intent("p1", "m1", 500, "card") is True
    assert e.get_status("p1") == "requires_payment_method"
    assert e.confirm("p1") == "succeeded"
    assert e.get_status("p1") == "succeeded"
    assert e.get_balance("m1") == 500


@pytest.mark.part1
def test_bank_debit_confirm_is_asynchronous_settle_credits_later(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 300, "bank_debit")
    assert e.confirm("p1") == "processing"
    assert e.get_balance("m1") == 0  # no credit yet
    assert e.settle("p1") is True
    assert e.get_balance("m1") == 300
    assert e.get_status("p1") == "succeeded"


@pytest.mark.part1
def test_settle_on_card_intent_or_wrong_state_is_ignored(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "card")
    e.confirm("p1")  # already succeeded
    assert e.settle("p1") is False
    e.create_intent("p2", "m1", 100, "bank_debit")
    assert e.settle("p2") is False  # still requires_payment_method, never confirmed


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_merchant_init_does_not_reset_balance(impl):
    e = impl.PaymentIntentEngine()
    assert e.init_merchant("m1", 100) is True
    assert e.init_merchant("m1", 999) is False
    assert e.get_balance("m1") == 100


@pytest.mark.part1
@pytest.mark.edge
def test_create_intent_ignore_cases(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    assert e.create_intent("p1", "m1", 10, "card") is True
    assert e.create_intent("p1", "m1", 20, "card") is False  # duplicate id
    assert e.create_intent("p2", "ghost", 10, "card") is False  # unknown merchant
    assert e.create_intent("p3", "m1", -1, "card") is False  # negative amount
    assert e.create_intent("p4", "m1", 10, "wire") is False  # bad method
    assert e.create_intent("p5", "m1", 0, "card") is True  # zero amount is valid


@pytest.mark.part1
@pytest.mark.edge
def test_confirm_unknown_or_wrong_state_is_ignored(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    assert e.confirm("ghost") == "ignored"
    e.create_intent("p1", "m1", 10, "card")
    e.confirm("p1")
    assert e.confirm("p1") == "ignored"  # already succeeded


@pytest.mark.part1
def test_balances_sorted_and_zero_balance_listed(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m10", 0)
    e.init_merchant("m2", 5)
    assert e.balances() == [("m10", 0), ("m2", 5)]  # plain string order: "m10" < "m2"


# ============================================================================== Part 2
@pytest.mark.part2
def test_example2_verbatim(impl):
    assert impl.part2(EX2.splitlines()) == EX2_OUT


@pytest.mark.part2
def test_update_amount_only_while_requires_payment_method(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "card")
    assert e.update_amount("p1", 50) is True
    e.confirm("p1")  # -> succeeded, credits 50 (the updated amount)
    assert e.get_balance("m1") == 50
    assert e.update_amount("p1", 999) is False  # already succeeded
    assert e.get_balance("m1") == 50


@pytest.mark.part2
def test_change_method_reshapes_the_next_confirm_outcome(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "bank_debit")
    assert e.change_method("p1", "card") is True
    assert e.confirm("p1") == "succeeded"  # now synchronous
    assert e.get_balance("m1") == 100


@pytest.mark.part2
def test_change_method_ignored_after_confirm(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "bank_debit")
    e.confirm("p1")  # -> processing
    assert e.change_method("p1", "card") is False
    assert e.get_status("p1") == "processing"


@pytest.mark.part2
@pytest.mark.edge
def test_update_amount_negative_ignored_zero_allowed(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "card")
    assert e.update_amount("p1", -5) is False
    assert e.update_amount("p1", 0) is True


@pytest.mark.part2
@pytest.mark.edge
def test_change_method_invalid_value_ignored(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "card")
    assert e.change_method("p1", "paypal") is False
    assert e.get_status("p1") == "requires_payment_method"


# ============================================================================== Part 3
@pytest.mark.part3
def test_example3_verbatim(impl):
    assert impl.part3(EX3.splitlines()) == EX3_OUT


@pytest.mark.part3
def test_fail_returns_to_requires_payment_method_and_allows_retry(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "bank_debit")
    e.confirm("p1")
    assert e.fail("p1") is True
    assert e.get_status("p1") == "requires_payment_method"
    assert e.update_amount("p1", 40) is True  # editable again after fail
    assert e.confirm("p1") == "processing"
    assert e.settle("p1") is True
    assert e.get_balance("m1") == 40


@pytest.mark.part3
def test_auto_cancel_after_too_many_confirm_attempts(impl):
    e = impl.PaymentIntentEngine(max_confirm_attempts=2)
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "bank_debit")
    assert e.confirm("p1") == "processing"  # attempt 1
    e.fail("p1")
    assert e.confirm("p1") == "processing"  # attempt 2
    e.fail("p1")
    assert e.confirm("p1") == "canceled"  # attempt 3 > max(2) -> auto-cancel
    assert e.get_status("p1") == "canceled"
    assert e.get_balance("m1") == 0


@pytest.mark.part3
def test_manual_cancel_from_requires_payment_method_always_allowed(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 40, "card")
    assert e.cancel("p1") is True
    assert e.get_status("p1") == "canceled"


@pytest.mark.part3
def test_cancel_while_processing_allowed_only_for_bank_debit(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 20, "bank_debit")
    e.confirm("p1")
    assert e.cancel("p1") is True
    assert e.get_status("p1") == "canceled"


@pytest.mark.part3
@pytest.mark.edge
def test_cancel_terminal_states_are_idempotent_no_ops(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "card")
    e.confirm("p1")  # -> succeeded
    assert e.cancel("p1") is False
    assert e.cancel("p1") is False  # second cancel of an already-canceled/terminal intent: no-op


@pytest.mark.part3
@pytest.mark.edge
def test_fail_on_non_processing_is_ignored(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "card")
    assert e.fail("p1") is False  # still requires_payment_method
    e.confirm("p1")  # -> succeeded
    assert e.fail("p1") is False


@pytest.mark.part3
@pytest.mark.edge
def test_confirm_attempts_not_reset_by_fail(impl):
    e = impl.PaymentIntentEngine(max_confirm_attempts=1)
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "bank_debit")
    e.confirm("p1")  # attempt 1, ok
    e.fail("p1")
    assert e.confirm("p1") == "canceled"  # attempt 2 > max(1): fail did not reset the counter


# ============================================================================== Part 4
@pytest.mark.part4
def test_example4_verbatim(impl):
    assert impl.part4(EX4.splitlines()) == EX4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_settle_window_boundary_inclusive_one_tick_over_refused(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 100, "bank_debit", settle_window=5)
    e.confirm("p1", ts=10)
    assert e.settle("p1", ts=15) is True  # 15-10=5 <= 5: exact boundary
    e2 = impl.PaymentIntentEngine()
    e2.init_merchant("m1", 0)
    e2.create_intent("p1", "m1", 100, "bank_debit", settle_window=5)
    e2.confirm("p1", ts=10)
    assert e2.settle("p1", ts=16) is False  # 16-10=6 > 5: one tick too late
    assert e2.get_status("p1") == "processing"  # stays stuck, not auto-resolved


@pytest.mark.part4
@pytest.mark.edge
def test_zero_settle_window_allows_only_the_same_tick(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 30, "bank_debit", settle_window=0)
    e.confirm("p1", ts=3)
    assert e.settle("p1", ts=3) is True  # same tick as confirm: allowed
    e2 = impl.PaymentIntentEngine()
    e2.init_merchant("m1", 0)
    e2.create_intent("p1", "m1", 30, "bank_debit", settle_window=0)
    e2.confirm("p1", ts=3)
    assert e2.settle("p1", ts=4) is False  # one tick later: refused (but not "never" like q10's 0)


@pytest.mark.part4
@pytest.mark.edge
def test_negative_settle_window_rejects_create_entirely(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    assert e.create_intent("p1", "m1", 10, "bank_debit", settle_window=-1) is False
    assert e.get_status("p1") is None  # never created


@pytest.mark.part4
def test_expire_only_fires_once_window_has_strictly_elapsed(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "bank_debit", settle_window=5)
    e.confirm("p1", ts=0)
    assert e.expire("p1", 4) is False  # 4 <= 5: not overdue yet
    assert e.expire("p1", 5) is False  # exactly on the boundary: still not overdue (strict >)
    assert e.expire("p1", 6) is True  # 6 > 5: now expires
    assert e.get_status("p1") == "canceled"


@pytest.mark.part4
@pytest.mark.edge
def test_settle_window_none_never_auto_expires(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "bank_debit")  # settle_window=None
    e.confirm("p1", ts=0)
    assert e.expire("p1", 10_000_000) is False
    assert e.get_status("p1") == "processing"


@pytest.mark.part4
def test_cancel_while_processing_also_bounded_by_window(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "bank_debit", settle_window=2)
    e.confirm("p1", ts=0)
    assert e.cancel("p1", ts=3) is False  # 3 > 2: too late to cancel
    assert e.cancel("p1", ts=2) is True  # 2 <= 2: still allowed


@pytest.mark.part4
def test_requires_payment_method_cancel_is_never_time_bounded(impl):
    e = impl.PaymentIntentEngine()
    e.init_merchant("m1", 0)
    e.create_intent("p1", "m1", 10, "bank_debit", settle_window=0)
    assert e.cancel("p1", ts=999_999) is True  # never confirmed -> the unrestricted branch


# ============================================================================== fmt / io / perf
@pytest.mark.part1
@pytest.mark.fmt
def test_confirm_status_text_is_lowercase_others_are_ok_ignored(impl):
    out = impl.run_commands(EX1.splitlines(), part=1)
    assert out == EX1_OUT
    # spot-check the two distinct output vocabularies side by side
    assert "CONFIRM p1 succeeded" in out
    assert "CREATE p1 OK" in out


@pytest.mark.part3
@pytest.mark.fmt
def test_unlocked_command_in_earlier_part_produces_no_line(impl):
    lines = ["INIT m1 0", "CREATE p1 m1 10 card", "FAIL p1", "CONFIRM p1", "BALANCE m1"]
    out = impl.run_commands(lines, part=1)  # FAIL not unlocked in part 1: silently skipped
    assert out == ["CREATE p1 OK", "CONFIRM p1 succeeded", "BALANCE m1 10"]


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact_with_part_header(run_script):
    r = run_script("PART 4\n" + EX4 + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_default_part_is_4_without_header(run_script):
    r = run_script(EX4 + "\n")  # no "PART n" header at all -> default PART 4
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.io
def test_part1_header_stdio(run_script):
    r = run_script("PART 1\n" + EX1 + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_confirm_settle_cycles(run_script):
    rng = random.Random(0)
    lines = ["0 INIT m1 0"]
    t = 1
    for i in range(50_000):
        method = "bank_debit" if i % 2 == 0 else "card"
        window = rng.randrange(1, 20)
        lines.append(f"{t} CREATE p{i} m1 {rng.randrange(1, 1000)} {method} {window}")
        t += 1
        lines.append(f"{t} CONFIRM p{i}")
        t += 1
        if method == "bank_debit":
            lines.append(f"{t} SETTLE p{i}")
            t += 1
    lines.append(f"{t} BALANCE m1")
    r = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out = r.stdout.splitlines()
    assert out[-1].startswith("BALANCE m1 ")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
