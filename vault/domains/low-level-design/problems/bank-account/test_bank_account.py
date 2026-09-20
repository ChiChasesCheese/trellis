"""银行账户系统的测试：分关覆盖账户流水、排行、定时返现与账户合并。"""

from __future__ import annotations

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


@pytest.fixture
def bank():
    b = impl.Bank(cashback_rate=0.02)
    b.create_account(0, "alice")
    b.create_account(0, "bob")
    b.deposit(1, "alice", 10_000)
    return b


# --- 第 1 关：开户、存款、转账、查余额 ------------------------------------------


def test_deposit_increases_balance_and_returns_it(bank):
    assert bank.deposit(2, "alice", 500) == 10_500
    assert bank.get_balance(2, "alice") == 10_500


def test_duplicate_account_id_is_rejected_even_after_it_would_be_merged_away(bank):
    with pytest.raises(impl.DuplicateAccountError):
        bank.create_account(3, "alice")


def test_transfer_moves_money_and_returns_the_source_balance(bank):
    result = bank.transfer(3, "alice", "bob", 4_000)
    assert result == 6_000
    assert bank.get_balance(3, "alice") == 6_000
    assert bank.get_balance(3, "bob") == 4_000


def test_transfer_more_than_available_raises_and_changes_neither_side(bank):
    with pytest.raises(impl.InsufficientFundsError) as excinfo:
        bank.transfer(3, "alice", "bob", 10_001)
    assert excinfo.value.shortfall == 1
    assert bank.get_balance(3, "alice") == 10_000
    assert bank.get_balance(3, "bob") == 0


def test_transfer_to_the_same_account_is_rejected(bank):
    with pytest.raises(impl.SameAccountError):
        bank.transfer(3, "alice", "alice", 100)


def test_unknown_account_is_rejected_for_deposit_transfer_and_balance(bank):
    with pytest.raises(impl.UnknownAccountError):
        bank.deposit(3, "carol", 100)
    with pytest.raises(impl.UnknownAccountError):
        bank.transfer(3, "alice", "carol", 100)
    with pytest.raises(impl.UnknownAccountError):
        bank.get_balance(3, "carol")


# --- 第 2 关：按支出排行 ---------------------------------------------------------


def test_top_spenders_ranks_by_outgoing_descending_ties_broken_by_id(bank):
    bank.create_account(4, "carol")
    bank.deposit(4, "bob", 5_000)
    bank.deposit(4, "carol", 5_000)
    bank.transfer(5, "alice", "bob", 3_000)   # alice 支出 3000
    bank.transfer(6, "bob", "carol", 3_000)   # bob 支出 3000（与 alice 打平，按 id 排）
    bank.transfer(7, "carol", "alice", 1_000)  # carol 支出 1000

    ranking = bank.top_spenders(7, 3)
    assert ranking == [("alice", 3_000), ("bob", 3_000), ("carol", 1_000)]


def test_top_spenders_excludes_accounts_with_zero_outgoing(bank):
    bank.transfer(3, "alice", "bob", 1_000)
    ranking = bank.top_spenders(3, 5)
    assert ranking == [("alice", 1_000)]  # bob 只收不发，不上榜


# --- 第 3 关：定时支付与返现 ------------------------------------------------------


def test_schedule_payment_deducts_immediately(bank):
    bank.schedule_payment(3, "alice", 2_000, cashback_delay=100)
    assert bank.get_balance(3, "alice") == 8_000


def test_cashback_settles_lazily_on_the_next_call_after_maturity(bank):
    payment_id = bank.schedule_payment(3, "alice", 2_000, cashback_delay=100)
    assert bank.payment_status(3, payment_id) is impl.PaymentStatus.IN_PROGRESS
    assert bank.get_balance(50, "alice") == 8_000  # 还没到期（matures_at = 103）
    assert bank.get_balance(200, "alice") == 8_000 + 40  # 到期后再查，返现已经落账（2% of 2000）
    assert bank.payment_status(200, payment_id) is impl.PaymentStatus.CASHBACK_RECEIVED


def test_cashback_is_recorded_at_maturity_time_not_at_the_triggering_call(bank):
    """结算是懒惰触发的，但落账的时间点必须是真正到期的那一刻，不是触发它的那次调用的
    时间——否则一次查询"到期和触发之间某个时刻"的历史余额会漏掉这笔早就该到账的钱。
    """
    payment_id = bank.schedule_payment(3, "alice", 2_000, cashback_delay=100)  # matures_at = 103
    bank.get_balance(500, "alice")  # 触发结算，但发生在很晚之后
    assert bank.get_balance(150, "alice") == 8_000 + 40  # 150 > 103，理应已经到账
    assert bank.get_balance(100, "alice") == 8_000  # 100 < 103，理应还没到账


def test_cancel_payment_before_maturity_refunds_the_principal(bank):
    payment_id = bank.schedule_payment(3, "alice", 2_000, cashback_delay=100)
    bank.cancel_payment(10, payment_id)
    assert bank.get_balance(10, "alice") == 10_000
    assert bank.payment_status(10, payment_id) is impl.PaymentStatus.CANCELLED
    assert bank.get_balance(500, "alice") == 10_000  # 取消之后不会再返现


def test_cancelling_an_already_settled_payment_raises(bank):
    payment_id = bank.schedule_payment(3, "alice", 2_000, cashback_delay=100)
    bank.get_balance(200, "alice")  # 触发结算
    with pytest.raises(impl.InvalidPaymentStateError):
        bank.cancel_payment(201, payment_id)


def test_cancelling_the_same_payment_twice_raises(bank):
    payment_id = bank.schedule_payment(3, "alice", 100, cashback_delay=1_000)
    bank.cancel_payment(4, payment_id)
    with pytest.raises(impl.InvalidPaymentStateError):
        bank.cancel_payment(5, payment_id)


def test_unknown_payment_id_is_rejected(bank):
    with pytest.raises(impl.UnknownPaymentError):
        bank.cancel_payment(3, "does-not-exist")
    with pytest.raises(impl.UnknownPaymentError):
        bank.payment_status(3, "does-not-exist")


# --- 第 4 关：合并账户与历史时点查询 -----------------------------------------------


def test_merge_combines_balance_and_reassigns_a_pending_payment(bank):
    bank.deposit(3, "bob", 1_000)
    payment_id = bank.schedule_payment(4, "bob", 500, cashback_delay=100)  # matures_at = 104
    bank.merge_accounts(5, "alice", "bob")

    assert bank.get_balance(5, "alice") == 10_000 + (1_000 - 500)
    with pytest.raises(impl.UnknownAccountError):
        bank.deposit(6, "bob", 1)  # 合并掉的账户不再接受新操作
    assert bank.get_balance(200, "alice") == 10_000 + 500 + 10  # 返现落到了存活的账户


def test_merged_away_account_still_answers_historical_balance_queries(bank):
    bank.deposit(3, "bob", 1_000)
    bank.merge_accounts(4, "alice", "bob")
    assert bank.get_balance(3, "bob") == 1_000  # 合并之前那一刻的余额，随时可查
    assert bank.get_balance(999, "bob") == 1_000  # 合并之后余额被冻结，不会再变化


def test_merging_the_same_account_into_itself_is_rejected(bank):
    with pytest.raises(impl.SameAccountError):
        bank.merge_accounts(3, "alice", "alice")


def test_get_balance_accepts_a_past_timestamp_even_after_later_writes(bank):
    """写操作的时间戳必须不倒退，但只读的余额查询可以问任意历史时刻——这正是上面
    "合并后仍可查历史余额"必须成立的前提。"""
    bank.deposit(5, "alice", 100)
    with pytest.raises(impl.NonMonotonicTimestampError):
        bank.deposit(4, "alice", 100)  # 写操作倒退时间戳：拒绝
    assert bank.get_balance(2, "alice") == 10_000  # 读操作查一个更早的时刻：允许


# --- 综合：日志与规模 --------------------------------------------------------------


def test_history_records_every_step_in_order(bank):
    bank.transfer(3, "alice", "bob", 1_000)
    events = bank.history("alice")
    assert [e.kind for e in events] == [impl.EventKind.OPENED, impl.EventKind.DEPOSIT,
                                         impl.EventKind.TRANSFER_OUT]
    assert [e.delta for e in events] == [0, 10_000, -1_000]


def test_pending_payment_count_shrinks_as_payments_settle_or_cancel(bank):
    p1 = bank.schedule_payment(3, "alice", 100, cashback_delay=10)
    p2 = bank.schedule_payment(3, "alice", 100, cashback_delay=10)
    assert bank.pending_payment_count == 2
    bank.cancel_payment(4, p1)
    assert bank.pending_payment_count == 1
    bank.get_balance(20, "alice")  # 触发 p2 结算
    assert bank.pending_payment_count == 0
    assert bank.payment_count == 2  # 历史记录不清理


def test_total_balance_is_conserved_after_a_randomised_deposit_and_transfer_session():
    rng = random.Random(20260305)
    bank = impl.Bank()
    accounts = [f"acc{i}" for i in range(5)]
    t = 0
    total_deposited = 0
    for i, account_id in enumerate(accounts):
        bank.create_account(t, account_id)
        t += 1

    for _ in range(200):
        t += 1
        if rng.random() < 0.5:
            amount = rng.randint(1, 1_000)
            bank.deposit(t, rng.choice(accounts), amount)
            total_deposited += amount
        else:
            a, b = rng.sample(accounts, 2)
            try:
                bank.transfer(t, a, b, rng.randint(1, 500))
            except impl.InsufficientFundsError:
                pass

    total_balance = sum(bank.get_balance(t, account_id) for account_id in accounts)
    assert total_balance == total_deposited
