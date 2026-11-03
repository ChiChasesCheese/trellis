"""额度账本的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
import random
from datetime import datetime, timedelta, UTC

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
A = impl.Allocation


def day(n: int, hour: int = 0) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=n, hours=hour)


# ---- 第 1 关：额度包、扣费、余额 ----------------------------------------------------


def test_part1_balance_counts_only_granted_and_unexpired_credits():
    led = impl.CreditLedger()
    led.grant("g1", 100, day(0), day(10))
    led.grant("g2", 50, day(5))
    assert led.balance(day(-1)) == 0        # 还没发放
    assert led.balance(day(0)) == 100       # 发放时刻含
    assert led.balance(day(5)) == 150
    assert led.balance(day(10)) == 50       # 到期时刻不含
    assert led.balance(day(99)) == 50


def test_part1_charge_takes_the_earliest_expiring_grant_first():
    led = impl.CreditLedger()
    led.grant("late", 100, day(0), day(30))
    led.grant("soon", 100, day(0), day(10))
    led.grant("never", 100, day(0))
    assert led.charge("c1", 60, day(1)) == (A("soon", 60),)
    assert led.charge("c2", 60, day(2)) == (A("soon", 40), A("late", 20))
    assert led.balance(day(3)) == 180


def test_part1_non_expiring_grants_are_used_last_and_ties_break_by_grant_time_then_id():
    led = impl.CreditLedger()
    led.grant("never", 10, day(0))
    led.grant("b", 10, day(1), day(20))
    led.grant("a", 10, day(1), day(20))
    led.grant("early", 10, day(0), day(20))
    assert led.charge("c", 35, day(2)) == (A("early", 10), A("a", 10), A("b", 10), A("never", 5))


def test_part1_charge_cannot_use_future_or_expired_grants():
    led = impl.CreditLedger()
    led.grant("g", 100, day(5), day(10))
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("c1", 1, day(4))         # 还没发放
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("c2", 1, day(10))        # 恰好到期
    assert led.charge("c3", 1, day(9, 23)) == (A("g", 1),)


def test_part1_insufficient_charge_changes_nothing():
    led = impl.CreditLedger()
    led.grant("g1", 30, day(0), day(10))
    led.grant("g2", 30, day(0))
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("big", 61, day(1))
    assert led.balance(day(1)) == 60
    assert led.charge("exact", 60, day(1)) == (A("g1", 30), A("g2", 30))
    assert led.balance(day(1)) == 0


def test_part1_expired_credits_are_gone_even_if_unused():
    led = impl.CreditLedger()
    led.grant("g1", 100, day(0), day(10))
    led.grant("g2", 40, day(0))
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("c", 50, day(11))        # g1 的 100 已经过期，只剩 g2 的 40
    assert led.charge("c", 40, day(11)) == (A("g2", 40),)


def test_part1_validation():
    led = impl.CreditLedger()
    for args in ((0, day(0)), (-5, day(0)), (10, day(0), day(0)), (10, day(1), day(0))):
        with pytest.raises(ValueError):
            led.grant("g", *args)
    led.grant("g", 10, day(0))
    for amount in (0, -1):
        with pytest.raises(ValueError):
            led.charge("c", amount, day(1))


# ---- 第 2 关：幂等 ----------------------------------------------------------------------


def test_part2_retrying_a_charge_does_not_debit_twice():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0))
    first = led.charge("c", 30, day(1))
    again = led.charge("c", 30, day(1))
    assert first == again == (A("g", 30),)
    assert led.balance(day(2)) == 70


def test_part2_same_charge_id_with_different_terms_is_a_conflict():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0))
    led.charge("c", 30, day(1))
    for amount, when in ((31, day(1)), (30, day(2))):
        with pytest.raises(impl.ConflictError):
            led.charge("c", amount, when)
    assert led.balance(day(3)) == 70


def test_part2_a_rejected_charge_is_not_remembered_so_it_can_be_retried():
    led = impl.CreditLedger()
    led.grant("g", 10, day(0))
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("c", 25, day(1))
    led.grant("g2", 20, day(0))
    assert led.charge("c", 25, day(1)) == (A("g", 10), A("g2", 15))


def test_part2_grants_are_idempotent_and_conflicts_are_detected():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0), day(10))
    led.grant("g", 100, day(0), day(10))
    assert led.balance(day(1)) == 100
    for args in ((101, day(0), day(10)), (100, day(1), day(10)), (100, day(0), day(11)), (100, day(0), None)):
        with pytest.raises(impl.ConflictError):
            led.grant("g", *args)
    assert led.balance(day(1)) == 100


def test_part2_a_retry_after_other_activity_returns_the_original_split():
    led = impl.CreditLedger()
    led.grant("g1", 50, day(0), day(10))
    led.grant("g2", 50, day(0))
    first = led.charge("c1", 70, day(1))
    led.charge("c2", 10, day(2))
    assert led.charge("c1", 70, day(1)) == first == (A("g1", 50), A("g2", 20))


# ---- 第 3 关：乱序到达的事件 -------------------------------------------------------------


def test_part3_a_late_charge_takes_the_earlier_expiring_grant_and_pushes_the_other_one_over():
    led = impl.CreditLedger()
    led.grant("g1", 100, day(0), day(10))
    led.grant("g2", 100, day(0), day(20))
    assert led.charge("c2", 100, day(5)) == (A("g1", 100),)
    led.charge("c1", 100, day(3))                       # 迟到：时间上比 c2 早
    assert led.allocations("c1") == (A("g1", 100),)
    assert led.allocations("c2") == (A("g2", 100),)     # c2 的分配被重放改掉了，总额不变


def test_part3_a_late_charge_that_would_starve_an_accepted_one_is_rejected():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0), day(10))
    led.charge("late-day", 100, day(8))
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("early", 50, day(2))
    assert led.allocations("late-day") == (A("g", 100),)
    assert led.balance(day(9)) == 0
    with pytest.raises(impl.UnknownChargeError):
        led.allocations("early")


def test_part3_a_late_grant_can_change_who_pays():
    led = impl.CreditLedger()
    led.grant("g1", 100, day(0), day(10))
    led.charge("c", 100, day(5))
    assert led.allocations("c") == (A("g1", 100),)
    led.grant("g0", 100, day(1), day(6))                # 迟到，但到期更早
    assert led.allocations("c") == (A("g0", 100),)
    assert led.balance(day(5)) == 100                   # g1 还剩 100


def test_part3_a_late_grant_can_unblock_a_charge_that_was_rejected():
    led = impl.CreditLedger()
    with pytest.raises(impl.InsufficientCreditsError):
        led.charge("c", 10, day(5))
    led.grant("g", 10, day(1))
    assert led.charge("c", 10, day(5)) == (A("g", 10),)


def test_part3_balance_is_a_function_of_time_not_of_arrival():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0), day(10))
    led.charge("c1", 30, day(5))
    led.charge("c2", 20, day(2))                        # 迟到
    assert led.balance(day(1)) == 100
    assert led.balance(day(2)) == 80
    assert led.balance(day(4)) == 80
    assert led.balance(day(5)) == 50
    assert led.balance(day(10)) == 0


def test_part3_events_at_the_same_instant_apply_grants_first():
    led = impl.CreditLedger()
    led.grant("g", 10, day(1), day(2))
    assert led.charge("c", 10, day(1)) == (A("g", 10),)     # 发放时刻就能扣
    led.grant("late", 5, day(1))                            # 迟到、时刻相同的包：重放时排在扣费之前，但它永不过期
    assert led.allocations("c") == (A("g", 10),)            # g 先到期，仍然先扣


def test_part3_final_allocations_do_not_depend_on_arrival_order():
    grants = [("g1", 40, day(0), day(10)), ("g2", 40, day(1), day(8)), ("g3", 40, day(2), None)]
    charges = [("c1", 30, day(3)), ("c2", 50, day(5)), ("c3", 25, day(9)), ("c4", 10, day(4))]
    results = set()
    rng = random.Random(3)
    for _ in range(20):
        led = impl.CreditLedger()
        g, c = grants[:], charges[:]
        rng.shuffle(g)
        rng.shuffle(c)
        for args in g:
            led.grant(*args)
        for args in c:
            led.charge(*args)
        results.add(tuple(led.allocations(cid) for cid, *_ in sorted(charges)))
    assert len(results) == 1


# ---- 第 4 关：作废额度包 -----------------------------------------------------------------


def test_part4_revoke_voids_the_unused_remainder_from_that_moment():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0))
    led.charge("c", 30, day(5))
    led.revoke("g", day(10))
    assert led.balance(day(9)) == 70
    assert led.balance(day(10)) == 0
    assert led.allocations("c") == (A("g", 30),)        # 已扣的不追回


def test_part4_revoke_that_would_starve_a_charge_is_rejected():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0))
    led.charge("c", 10, day(12))
    with pytest.raises(impl.InsufficientCreditsError):
        led.revoke("g", day(10))
    assert led.balance(day(11)) == 100
    with pytest.raises(impl.InsufficientCreditsError):
        led.revoke("g", day(12))                        # 作废时刻含在失效里：day(12) 的扣费也用不到了
    led.revoke("g", day(13))
    assert led.allocations("c") == (A("g", 10),)


def test_part4_revoke_is_idempotent_only_moves_expiry_earlier_and_validates():
    led = impl.CreditLedger()
    led.grant("g", 100, day(0), day(10))
    led.revoke("g", day(20))                            # 本来就更早失效：无事发生
    assert led.balance(day(9)) == 100
    led.revoke("g", day(5))
    led.revoke("g", day(7))                             # 比现有的晚：无事发生
    assert led.balance(day(4)) == 100 and led.balance(day(5)) == 0
    with pytest.raises(impl.UnknownGrantError):
        led.revoke("nope", day(1))
    with pytest.raises(ValueError):
        led.revoke("g", day(0))


def test_part4_revoke_changes_who_pays_for_existing_charges():
    led = impl.CreditLedger()
    led.grant("g1", 100, day(0), day(30))
    led.grant("g2", 100, day(0), day(40))
    led.charge("c", 100, day(20))
    assert led.allocations("c") == (A("g1", 100),)
    led.revoke("g1", day(15))
    assert led.allocations("c") == (A("g2", 100),)
