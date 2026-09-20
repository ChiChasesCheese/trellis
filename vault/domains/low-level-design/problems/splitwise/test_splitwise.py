"""分账（Splitwise）的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import UTC, datetime
from decimal import Decimal

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

FIXED_NOW = datetime(2026, 3, 1, 12, 0, tzinfo=UTC)


def clock() -> datetime:
    """注入的时钟：固定时间，测试不依赖机器上真实的现在几点。"""
    return FIXED_NOW


@pytest.fixture
def people() -> tuple:
    return (impl.User("u1", "Alice"), impl.User("u2", "Bob"), impl.User("u3", "Carol"),
            impl.User("u4", "Dan"), impl.User("u5", "Erin"))


@pytest.fixture
def manager(people):
    m = impl.ExpenseManager(clock=clock)
    for person in people:
        m.add_user(person)
    return m


# --------------------------------------------------------------------------
# 第 1 关：用户、小组、均分、谁欠谁
# --------------------------------------------------------------------------

def test_equal_split_who_owes_whom(manager, people):
    alice, bob, carol, *_ = people
    manager.add_expense(payer=alice, amount=9000, description="晚餐",
                        participants=[alice, bob, carol], split=impl.EqualSplit())
    assert manager.balance_between(bob, alice) == 3000
    assert manager.balance_between(alice, bob) == -3000
    assert manager.balance_between(alice, alice) == 0
    owed = {(d.debtor, d.creditor): d.amount for d in manager.debts()}
    assert owed == {(bob, alice): 3000, (carol, alice): 3000}


def test_payer_need_not_be_a_participant(manager, people):
    alice, bob, carol, *_ = people
    manager.add_expense(payer=alice, amount=5000, description="替他们付的",
                        participants=[bob, carol], split=impl.EqualSplit())
    assert manager.balance_between(bob, alice) == 2500
    assert manager.net_balance(alice) == 5000


def test_group_members_are_a_snapshot(manager, people):
    alice, bob, *_ = people
    group = manager.create_group("g1", "室友", [alice, alice, bob])
    assert group.members == (alice, bob)          # 重复成员被去重
    snapshot = group.members
    group.add_member(people[2])
    assert snapshot == (alice, bob)               # 旧快照不会被后来的改动追认
    assert len(group.members) == 3


def test_unknown_user_is_rejected(manager, people):
    stranger = impl.User("u9", "Mallory")
    with pytest.raises(impl.UnknownUserError):
        manager.add_expense(payer=stranger, amount=100, description="x",
                            participants=[stranger], split=impl.EqualSplit())
    with pytest.raises(impl.UnknownUserError):
        manager.create_group("g2", "陌生人组", [stranger])


# --------------------------------------------------------------------------
# 第 2 关：四种拆分，份额之和必须精确等于总额
# --------------------------------------------------------------------------

def test_equal_split_remainder_goes_to_the_first_participants(people):
    alice, bob, carol, *_ = people
    shares = impl.EqualSplit().compute(100, [alice, bob, carol])
    assert shares == {alice: 34, bob: 33, carol: 33}
    assert sum(shares.values()) == 100


@pytest.mark.parametrize("amount", [1, 2, 7, 99, 100, 1001, 123457])
@pytest.mark.parametrize("n", [1, 2, 3, 7])
def test_equal_split_always_sums_to_the_total(amount, n):
    users = [impl.User(f"x{i}", f"X{i}") for i in range(n)]
    shares = impl.EqualSplit().compute(amount, users)
    assert sum(shares.values()) == amount
    assert max(shares.values()) - min(shares.values()) <= 1


def test_exact_split_must_sum_to_the_total(people):
    alice, bob, *_ = people
    good = impl.ExactSplit({alice: 700, bob: 300})
    assert good.compute(1000, [alice, bob]) == {alice: 700, bob: 300}
    with pytest.raises(impl.SplitError):
        impl.ExactSplit({alice: 700, bob: 400}).compute(1000, [alice, bob])
    with pytest.raises(impl.SplitError):
        impl.ExactSplit({alice: 1100, bob: -100}).compute(1000, [alice, bob])


def test_percentage_split_is_validated_at_construction(people):
    alice, bob, *_ = people
    with pytest.raises(impl.SplitError):
        impl.PercentageSplit({alice: Decimal("60"), bob: Decimal("30")})
    split = impl.PercentageSplit({alice: Decimal("33.33"), bob: Decimal("66.67")})
    shares = split.compute(1000, [alice, bob])
    assert sum(shares.values()) == 1000
    assert shares == {alice: 333, bob: 667}


def test_share_split_weights_and_validation(people):
    alice, bob, carol, *_ = people
    shares = impl.ShareSplit({alice: 2, bob: 1, carol: 1}).compute(100, [alice, bob, carol])
    assert shares == {alice: 50, bob: 25, carol: 25}
    with pytest.raises(impl.SplitError):
        impl.ShareSplit({alice: 0, bob: 1})


def test_split_participants_must_match(people):
    alice, bob, carol, *_ = people
    with pytest.raises(impl.SplitError):
        impl.ExactSplit({alice: 1000}).compute(1000, [alice, bob])
    with pytest.raises(impl.SplitError):
        impl.ShareSplit({alice: 1, bob: 1}).compute(1000, [alice, carol])
    with pytest.raises(impl.SplitError):
        impl.EqualSplit().compute(1000, [])


def test_recorded_shares_are_frozen_against_later_mutation(manager, people):
    alice, bob, *_ = people
    amounts = {alice: 400, bob: 600}
    expense = manager.add_expense(payer=alice, amount=1000, description="机票",
                                  participants=[alice, bob], split=impl.ExactSplit(amounts))
    amounts[bob] = 999_999                     # 事后改传进去的字典
    assert expense.shares[bob] == 600          # 已经记好的账不跟着变
    with pytest.raises(TypeError):             # 也改不动快照本身
        expense.shares[bob] = 1


# --------------------------------------------------------------------------
# 第 3 关：净额与贪心债务化简
# --------------------------------------------------------------------------

def test_simplify_points_the_money_the_right_way(manager, people):
    """回归测试：净额的符号和账本行的符号必须严格对偶。写反时 `debts()` 仍然正确，
    只有 `simplify()` 会把付款方和收款方整个对调——所以这里断言方向，不只断言金额。"""
    alice, bob, carol, *_ = people
    manager.add_expense(payer=alice, amount=9000, description="晚餐",
                        participants=[alice, bob, carol], split=impl.EqualSplit())
    manager.add_expense(payer=bob, amount=6000, description="出租车",
                        participants=[alice, bob], split=impl.ExactSplit({alice: 4000, bob: 2000}))
    assert manager.net_balance(alice) == 2000
    assert manager.net_balance(bob) == 1000
    assert manager.net_balance(carol) == -3000
    transfers = {(p.payer, p.payee): p.amount for p in manager.simplify()}
    assert transfers == {(carol, alice): 2000, (carol, bob): 1000}


def test_simplify_settles_everyone_in_at_most_n_minus_one_transfers(people):
    balances = {people[0]: 5000, people[1]: -2000, people[2]: -1000,
                people[3]: 1000, people[4]: -3000}
    payments = impl.simplify_debts(balances)
    assert len(payments) <= len(balances) - 1
    assert all(p.amount > 0 for p in payments)
    after = dict(balances)
    for p in payments:
        after[p.payer] += p.amount
        after[p.payee] -= p.amount
    assert all(v == 0 for v in after.values())


def test_greedy_simplify_is_not_always_optimal(people):
    """贪心的诚实边界：这组净额最优是 3 笔（+3/-3 对冲，+2/+2/-4 三人配平），
    贪心一定先拿最大应付 -4 去配最大应收 +3，结果是 4 笔。"""
    a, b, c, d, e = people
    balances = {a: 3, b: 2, c: -3, d: 2, e: -4}
    payments = impl.simplify_debts(balances)
    assert len(payments) == 4
    assert len(payments) <= len(balances) - 1


def test_simplify_of_a_settled_group_is_empty(manager, people):
    alice, bob, *_ = people
    manager.add_expense(payer=alice, amount=1000, description="咖啡",
                        participants=[alice, bob], split=impl.EqualSplit())
    manager.settle(payer=bob, payee=alice, amount=500)
    assert manager.simplify() == []
    assert manager.debts() == ()


# --------------------------------------------------------------------------
# 第 4 关：结算、活动日志、账本会缩小
# --------------------------------------------------------------------------

def test_settlement_reduces_and_can_flip_the_debt(manager, people):
    alice, bob, *_ = people
    manager.add_expense(payer=alice, amount=1000, description="咖啡",
                        participants=[alice, bob], split=impl.EqualSplit())
    manager.settle(payer=bob, payee=alice, amount=200)
    assert manager.balance_between(bob, alice) == 300
    manager.settle(payer=bob, payee=alice, amount=400)      # 多还了 100
    assert manager.balance_between(bob, alice) == -100
    assert manager.debts() == (impl.Debt(debtor=alice, creditor=bob, amount=100),)
    with pytest.raises(impl.SettlementError):
        manager.settle(payer=bob, payee=alice, amount=0)


def test_the_ledger_shrinks_when_a_pair_settles_up(manager, people):
    """“容器必须会缩小”：结清的那一对用户不能在账本里留下一行零余额。"""
    alice, bob, *_ = people
    ledger = impl.Ledger()
    ledger.record_debt(debtor=bob, creditor=alice, delta=500)
    assert len(ledger.debts()) == 1
    ledger.record_debt(debtor=bob, creditor=alice, delta=-500)
    assert ledger.debts() == ()
    assert ledger.net_balance(alice) == 0
    assert ledger.row_count == 0                            # 不是“留一行 0”，是整行删掉


def test_activity_log_is_fed_by_events_only(manager, people):
    alice, bob, *_ = people
    log = impl.ActivityLog()
    manager.subscribe(log)
    manager.add_expense(payer=alice, amount=1000, description="咖啡",
                        participants=[alice, bob], split=impl.EqualSplit())
    manager.settle(payer=bob, payee=alice, amount=500)
    recent = log.recent(5)
    assert [e.kind for e in recent] == [impl.SplitwiseEventKind.SETTLED,
                                        impl.SplitwiseEventKind.EXPENSE_ADDED]
    assert recent[0].amount == 500 and recent[0].users == (bob, alice)
    assert recent[1].at == FIXED_NOW and "咖啡" in recent[1].summary
    assert log.recent(1) == (recent[0],)


def test_concurrent_expenses_keep_the_ledger_consistent(manager, people):
    """真线程 + 屏障：断言的是不变式（总额守恒、笔数正确），不是时序。"""
    alice, bob, *_ = people
    threads_n, per_thread = 8, 25
    barrier = threading.Barrier(threads_n)

    def worker() -> None:
        barrier.wait()
        for _ in range(per_thread):
            manager.add_expense(payer=alice, amount=100, description="并发",
                                participants=[alice, bob], split=impl.EqualSplit())

    threads = [threading.Thread(target=worker) for _ in range(threads_n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert manager.expense_count == threads_n * per_thread
    assert manager.balance_between(bob, alice) == threads_n * per_thread * 50
    assert sum(manager.net_balance(p) for p in people) == 0
