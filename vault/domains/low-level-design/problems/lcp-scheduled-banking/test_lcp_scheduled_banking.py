import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def make(*accounts, start=0):
    """开好若干账户，返回 (bank, 下一个可用时间戳)。"""
    bank = impl.Bank()
    t = start
    for name in accounts:
        assert bank.create_account(t, name) is True
        t += 1
    return bank, t


# ---------- 第 1 关：账户、存款、转账 ----------
def test_readme_example():
    bank = impl.Bank()
    assert bank.create_account(0, "a") is True
    assert bank.create_account(1, "b") is True
    assert bank.deposit(2, "a", 100) == 100
    assert bank.transfer_batch(3, [("a", "b", 70), ("b", "a", 20)]) == [30, 50]
    assert bank.transfer_batch(4, [("a", "b", 10), ("b", "a", 100)]) is None
    assert bank.get_balance(5, "a", 4) == 50


def test_create_account_rules():
    bank = impl.Bank()
    assert bank.create_account(0, "a") is True
    assert bank.create_account(1, "a") is False
    assert bank.create_account(2, "A") is True  # 区分大小写
    assert impl.Bank().create_account(0, "a") is True  # 各个银行互相独立


def test_deposit_and_missing_account():
    bank, t = make("a")
    assert bank.deposit(t, "a", 5) == 5
    assert bank.deposit(t + 1, "a", 7) == 12
    assert bank.deposit(t + 2, "ghost", 7) is None


def test_transfer_rules():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    assert bank.transfer(t + 1, "a", "b", 40) == 60
    assert bank.transfer(t + 2, "a", "a", 1) is None  # 同一个账户
    assert bank.transfer(t + 3, "a", "ghost", 1) is None
    assert bank.transfer(t + 4, "ghost", "b", 1) is None
    assert bank.transfer(t + 5, "a", "b", 61) is None  # 余额不足
    assert bank.get_balance(t + 6, "a", t + 6) == 60
    assert bank.get_balance(t + 7, "b", t + 7) == 40
    assert bank.transfer(t + 8, "a", "b", 60) == 0  # 恰好花光是合法的
    assert bank.top_spenders(t + 9, 5) == ["a(100)", "b(0)"]


# ---------- 第 2 关：支出排名 ----------
def test_top_spenders_order_and_format():
    bank, t = make("b", "a", "C", "d")
    bank.deposit(t, "b", 100)
    bank.deposit(t + 1, "a", 100)
    bank.transfer(t + 2, "b", "d", 30)
    bank.transfer(t + 3, "a", "d", 30)  # 与 b 同额，按 ID 升序
    assert bank.top_spenders(t + 4, 10) == ["a(30)", "b(30)", "C(0)", "d(0)"]
    assert bank.top_spenders(t + 5, 1) == ["a(30)"]


def test_top_spenders_string_order_not_case_folded():
    bank, t = make("a", "B")
    assert bank.top_spenders(t, 2) == ["B(0)", "a(0)"]  # "B" < "a"


def test_top_spenders_n_zero_and_large():
    bank, t = make("a")
    assert bank.top_spenders(t, 0) == []
    assert bank.top_spenders(t + 1, 99) == ["a(0)"]
    assert impl.Bank().top_spenders(0, 3) == []


def test_top_spenders_ignores_incoming_deposit_and_failures():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 50)
    bank.transfer(t + 1, "a", "b", 20)
    bank.transfer(t + 2, "b", "a", 999)  # 失败
    bank.schedule_payment(t + 3, "b", 500, 1)  # 付不起，永久失败
    assert bank.top_spenders(t + 10, 2) == ["a(20)", "b(0)"]


def test_keyword_call_matches_workspace_style():
    bank, t = make("a")
    assert bank.top_spenders(timestamp=t, n=1) == ["a(0)"]


# ---------- 第 3 关：定时付款的结算 ----------
def test_due_payment_runs_before_next_call():
    bank, t = make("a")
    bank.deposit(t, "a", 100)
    assert bank.schedule_payment(t + 1, "a", 30, 2) == "payment1"  # 到期 t+3
    assert bank.deposit(t + 3, "a", 10) == 80  # 到期那一刻先付款，再存款
    assert bank.top_spenders(t + 4, 1) == ["a(30)"]


def test_payment_history_is_dated_at_due_time():
    bank, t = make("a")
    bank.deposit(t, "a", 100)  # t = 1
    bank.schedule_payment(2, "a", 30, 3)  # 到期 5
    assert bank.get_balance(20, "a", 4) == 100  # 由很晚的一次调用触发结算
    assert bank.get_balance(21, "a", 5) == 70
    assert bank.get_balance(22, "a", 19) == 70


def test_deposit_at_due_time_cannot_rescue_failed_payment():
    bank, t = make("a")
    bank.deposit(t, "a", 10)
    bank.schedule_payment(t + 1, "a", 50, 4)  # 到期 t+5
    assert bank.deposit(t + 5, "a", 100) == 110  # 付款先失败，存款后到
    assert bank.deposit(t + 6, "a", 1) == 111  # 失败是永久的，不会再重试
    assert bank.top_spenders(t + 7, 1) == ["a(0)"]


def test_failed_scheduled_call_still_settles_first():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 60)
    bank.schedule_payment(t + 1, "a", 50, 4)  # 到期 t+5
    assert bank.transfer(t + 5, "a", "b", 20) is None  # 付款先走，剩 10，转 20 不够
    assert bank.get_balance(t + 6, "a", t + 5) == 10


def test_queries_trigger_settlement():
    bank, t = make("a")
    bank.deposit(t, "a", 40)
    bank.schedule_payment(t + 1, "a", 15, 1)
    assert bank.top_spenders(t + 2, 1) == ["a(15)"]
    bank.schedule_payment(t + 3, "a", 5, 1)
    assert bank.get_balance(t + 4, "a", t + 4) == 20


def test_payment_order_is_numeric_not_lexicographic():
    bank, t = make("a")
    bank.deposit(t, "a", 10)
    for _ in range(9):
        bank.schedule_payment(t + 1, "a", 1, 100)  # payment1..payment9，同一到期时间
    assert bank.schedule_payment(t + 1, "a", 5, 100) == "payment10"
    # 数值顺序：前九笔花掉 9，payment10 要 5 只剩 1，失败；字符串顺序下它会排在第二位并成功
    assert bank.top_spenders(t + 200, 1) == ["a(9)"]
    assert bank.get_balance(t + 201, "a", t + 101) == 1


def test_orders_by_due_time_then_creation():
    bank, t = make("a")
    bank.deposit(t, "a", 10)
    bank.schedule_payment(2, "a", 8, 10)  # payment1 到期 12
    bank.schedule_payment(3, "a", 8, 2)  # payment2 到期 5，先走
    assert bank.get_balance(30, "a", 5) == 2
    assert bank.get_balance(31, "a", 12) == 2  # payment1 付不起
    assert bank.top_spenders(32, 1) == ["a(8)"]


# ---------- 第 4 关：安排与取消 ----------
def test_schedule_ids_and_failures():
    bank, t = make("a", "b")
    assert bank.schedule_payment(t, "ghost", 5, 1) is None  # 不消耗编号
    assert bank.schedule_payment(t + 1, "a", 5, 10) == "payment1"
    assert bank.schedule_payment(t + 2, "b", 5, 10) == "payment2"  # 编号在整个银行内全局
    other = impl.Bank()
    other.create_account(0, "a")
    assert other.schedule_payment(1, "a", 5, 10) == "payment1"  # 另一家银行从头编号


def test_schedule_does_not_reserve_funds():
    bank, t = make("a")
    bank.deposit(t, "a", 10)
    bank.schedule_payment(t + 1, "a", 10, 5)
    assert bank.deposit(t + 2, "a", 1) == 11  # 余额没有被冻结
    assert bank.get_balance(t + 3, "a", t + 3) == 11


def test_cancel_rules():
    bank, t = make("a", "b")
    pid = bank.schedule_payment(t, "a", 10, 10)
    assert bank.cancel_payment(t + 1, "b", pid) is False  # 不是它的付款
    assert bank.cancel_payment(t + 2, "a", "payment99") is False
    assert bank.cancel_payment(t + 3, "ghost", pid) is False
    assert bank.cancel_payment(t + 4, "a", pid) is True
    assert bank.cancel_payment(t + 5, "a", pid) is False  # 只能取消一次
    bank.deposit(t + 6, "a", 50)
    assert bank.get_balance(t + 30, "a", t + 30) == 50  # 取消后不再扣款


def test_cancel_at_due_time_is_too_late():
    bank, t = make("a")
    bank.deposit(t, "a", 100)
    pid = bank.schedule_payment(t + 1, "a", 30, 5)  # 到期 t+6
    assert bank.cancel_payment(t + 6, "a", pid) is False
    assert bank.get_balance(t + 7, "a", t + 6) == 70


def test_cancel_processed_and_failed_payments():
    bank, t = make("a")
    ok = bank.schedule_payment(t, "a", 1, 1)  # 付不起，失败
    bank.deposit(t + 1, "a", 5)
    done = bank.schedule_payment(t + 2, "a", 1, 1)
    assert bank.cancel_payment(t + 10, "a", ok) is False
    assert bank.cancel_payment(t + 11, "a", done) is False


def test_cancelled_entries_do_not_pile_up():
    bank, t = make("a")
    ids = [bank.schedule_payment(t + i, "a", 1, 10**6) for i in range(500)]
    for i, pid in enumerate(ids):
        assert bank.cancel_payment(t + 600 + i, "a", pid) is True
    assert bank.pending_count == 0
    assert bank.queue_size <= 16


# ---------- 合并 ----------
def test_merge_moves_balance_spending_and_payments():
    bank, t = make("a", "b", "c")
    bank.deposit(t, "a", 20)
    bank.deposit(t + 1, "b", 100)
    bank.transfer(t + 2, "b", "c", 10)
    bank.transfer(t + 3, "a", "c", 5)
    pid = bank.schedule_payment(t + 4, "b", 60, 10)
    assert bank.merge_accounts(t + 5, "a", "b") is True
    assert bank.top_spenders(t + 6, 5) == ["a(15)", "c(0)"]
    assert bank.cancel_payment(t + 7, "b", pid) is False  # b 已退役
    assert bank.get_balance(t + 8, "a", t + 8) == 105
    assert bank.get_balance(t + 30, "a", t + 30) == 45  # 付款随合并归到 a，在 t+14 扣掉
    assert bank.top_spenders(t + 31, 1) == ["a(75)"]


def test_retired_ids_are_dead_everywhere():
    bank, t = make("a", "b")
    bank.deposit(t, "b", 10)
    assert bank.merge_accounts(t + 1, "a", "b") is True
    assert bank.create_account(t + 2, "b") is False  # 退役的 ID 也不能再用
    assert bank.deposit(t + 3, "b", 1) is None
    assert bank.transfer(t + 4, "b", "a", 1) is None
    assert bank.schedule_payment(t + 5, "b", 1, 1) is None
    assert bank.get_balance(t + 6, "b", t) is None  # 合并之前的时刻也是 None
    assert bank.get_balance(t + 7, "b", t + 7) is None


def test_merge_failures_change_nothing():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 10)
    assert bank.merge_accounts(t + 1, "a", "a") is False
    assert bank.merge_accounts(t + 2, "a", "ghost") is False
    assert bank.merge_accounts(t + 3, "ghost", "a") is False
    assert bank.get_balance(t + 4, "a", t + 4) == 10
    assert bank.top_spenders(t + 5, 5) == ["a(0)", "b(0)"]


def test_merged_payments_keep_ids_due_times_and_order():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 10)
    bank.deposit(t + 1, "b", 10)
    first = bank.schedule_payment(t + 2, "b", 8, 20)  # 先创建，到期相同
    second = bank.schedule_payment(t + 3, "a", 8, 19)
    assert (first, second) == ("payment1", "payment2")
    assert bank.merge_accounts(t + 4, "a", "b") is True  # 余额 20
    # 到期时间相同 (t+22)：先 payment1 成功（剩 12），再 payment2 成功（剩 4）
    assert bank.get_balance(t + 40, "a", t + 22) == 4
    assert bank.cancel_payment(t + 41, "a", first) is False


def test_cancel_merged_payment_by_survivor():
    bank, t = make("a", "b")
    pid = bank.schedule_payment(t, "b", 5, 50)
    bank.merge_accounts(t + 1, "a", "b")
    assert bank.cancel_payment(t + 2, "a", pid) is True


def test_chained_merges():
    bank, t = make("a", "b", "c")
    bank.deposit(t, "a", 1)
    bank.deposit(t + 1, "b", 2)
    bank.deposit(t + 2, "c", 4)
    assert bank.merge_accounts(t + 3, "b", "c") is True
    assert bank.merge_accounts(t + 4, "a", "b") is True
    assert bank.get_balance(t + 5, "a", t + 5) == 7
    assert bank.get_balance(t + 6, "a", t + 2) == 1  # 不追溯合并来的历史
    assert bank.get_balance(t + 7, "b", t + 7) is None
    assert bank.get_balance(t + 8, "c", t + 8) is None


def test_merge_settles_due_payments_first():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 10)
    bank.deposit(t + 1, "b", 10)
    bank.schedule_payment(t + 2, "b", 7, 3)  # 到期 t+5，付款人还是 b
    assert bank.merge_accounts(t + 5, "a", "b") is True
    assert bank.top_spenders(t + 6, 1) == ["a(7)"]  # b 的支出带进 a
    assert bank.get_balance(t + 7, "a", t + 5) == 13


# ---------- 历史查询 ----------
def test_history_basics_and_bounds():
    bank, t = make("a")  # 创建在 0
    bank.deposit(3, "a", 10)
    bank.deposit(7, "a", 5)
    assert bank.get_balance(8, "a", 0) == 0
    assert bank.get_balance(9, "a", 2) == 0
    assert bank.get_balance(10, "a", 3) == 10
    assert bank.get_balance(11, "a", 6) == 10
    assert bank.get_balance(12, "a", 7) == 15
    assert bank.get_balance(13, "a", 13) == 15
    assert bank.get_balance(14, "a", 15) is None  # 查询未来
    assert bank.get_balance(15, "ghost", 0) is None


def test_history_before_creation_is_none():
    bank = impl.Bank()
    bank.create_account(5, "a")
    assert bank.get_balance(6, "a", 4) is None
    assert bank.get_balance(7, "a", 5) == 0


def test_history_merge_boundary_is_not_retroactive():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 20)
    bank.deposit(t + 1, "b", 30)
    bank.merge_accounts(t + 2, "a", "b")
    assert bank.get_balance(t + 3, "a", t + 1) == 20
    assert bank.get_balance(t + 4, "a", t + 2) == 50


def test_same_timestamp_shows_payment_then_request():
    bank = impl.Bank()
    bank.create_account(0, "a")
    bank.deposit(1, "a", 100)
    bank.schedule_payment(2, "a", 30, 3)  # 到期 5
    assert bank.deposit(5, "a", 10) == 80
    assert bank.get_balance(6, "a", 5) == 80  # 付款与存款都在 5 时刻之内
    assert bank.get_balance(7, "a", 4) == 100


def test_history_replays_live_observations():
    """随机操作；每个时刻当场观察到的余额，事后按历史查询必须完全一致。"""
    rng = random.Random(7)
    bank = impl.Bank()
    ids = ["a", "b", "c", "d"]
    for i, name in enumerate(ids):
        bank.create_account(i, name)
    t, seen, retired = 4, [], set()
    for _ in range(400):
        op = rng.choice(["dep", "xfer", "sched", "cancel", "merge", "batch"])
        live = [x for x in ids if x not in retired]
        t += 1
        if op == "dep":
            bank.deposit(t, rng.choice(live), rng.randint(1, 50))
        elif op == "xfer":
            bank.transfer(t, rng.choice(live), rng.choice(live), rng.randint(1, 40))
        elif op == "sched":
            bank.schedule_payment(t, rng.choice(live), rng.randint(1, 30), rng.randint(1, 15))
        elif op == "cancel":
            bank.cancel_payment(t, rng.choice(live), f"payment{rng.randint(1, 40)}")
        elif op == "batch":
            moves = [(rng.choice(live), rng.choice(live), rng.randint(1, 20)) for _ in range(3)]
            bank.transfer_batch(t, moves)
        elif len(live) > 2 and rng.random() < 0.15:
            x, y = rng.sample(live, 2)
            if bank.merge_accounts(t, x, y):
                retired.add(y)
        t += 1
        for name in [x for x in ids if x not in retired]:
            seen.append((t, name, bank.get_balance(t, name, t)))
            t += 1
    for when, name, balance in seen:
        if name in retired:
            continue  # 已并掉的账户查什么时刻都是 None
        t += 1
        assert bank.get_balance(t, name, when) == balance


# ---------- 第 5 关：原子批次 ----------
def test_batch_later_transfer_spends_earlier_receipts():
    bank, t = make("a", "b", "c")
    bank.deposit(t, "a", 50)
    assert bank.transfer_batch(t + 1, [("a", "b", 50), ("b", "c", 30), ("c", "a", 10)]) == [0, 20, 20]
    assert bank.get_balance(t + 2, "a", t + 2) == 10
    assert bank.get_balance(t + 3, "b", t + 3) == 20
    assert bank.get_balance(t + 4, "c", t + 4) == 20


def test_batch_failure_discards_everything():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    assert bank.transfer_batch(t + 1, [("a", "b", 50), ("b", "a", 60)]) is None
    assert bank.get_balance(t + 2, "a", t + 2) == 100
    assert bank.get_balance(t + 3, "b", t + 3) == 0
    assert bank.get_balance(t + 4, "a", t + 1) == 100  # 历史也没有留下痕迹
    assert bank.top_spenders(t + 5, 2) == ["a(0)", "b(0)"]  # 支出也没记


@pytest.mark.parametrize(
    "bad", [("a", "a", 1), ("a", "ghost", 1), ("ghost", "a", 1), ("a", "b", 101)]
)
def test_batch_each_failure_kind(bad):
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    assert bank.transfer_batch(t + 1, [("a", "b", 10), bad]) is None
    assert bank.get_balance(t + 2, "b", t + 2) == 0


def test_batch_keeps_due_payments_committed_even_when_it_fails():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    bank.schedule_payment(t + 1, "a", 40, 2)  # 到期 t+3
    assert bank.transfer_batch(t + 3, [("a", "b", 70)]) is None  # 付款先走，只剩 60
    assert bank.get_balance(t + 4, "a", t + 3) == 60
    assert bank.top_spenders(t + 5, 1) == ["a(40)"]


def test_empty_batch_returns_list_and_still_settles():
    bank, t = make("a")
    bank.deposit(t, "a", 10)
    bank.schedule_payment(t + 1, "a", 4, 1)
    result = bank.transfer_batch(t + 2, [])
    assert result == []
    assert bank.top_spenders(t + 3, 1) == ["a(4)"]
    result.append(99)  # 返回的是新列表，改它不影响银行
    assert bank.transfer_batch(t + 4, []) == []


def test_batch_net_zero_still_counts_spending_and_history_shows_final():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    moves = [("a", "b", 100), ("b", "a", 100)]
    snapshot = list(moves)
    assert bank.transfer_batch(t + 1, moves) == [0, 0]
    assert moves == snapshot  # 输入不被改动
    assert bank.get_balance(t + 2, "a", t + 1) == 100  # 看到的是批次结束后的余额
    assert bank.get_balance(t + 3, "b", t + 1) == 0
    assert bank.top_spenders(t + 4, 2) == ["a(100)", "b(100)"]


def test_batch_history_at_same_timestamp_is_final_balance():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 100)
    bank.transfer_batch(t + 1, [("a", "b", 70), ("b", "a", 20)])
    assert bank.get_balance(t + 2, "a", t + 1) == 50
    assert bank.get_balance(t + 3, "b", t + 1) == 50
    assert bank.get_balance(t + 4, "a", t) == 100


def test_batch_accepts_any_sequence_of_triples():
    bank, t = make("a", "b")
    bank.deposit(t, "a", 10)
    assert bank.transfer_batch(t + 1, (("a", "b", 3), ["b", "a", 1])) == [7, 2]


def test_payment_may_spend_exact_balance():
    bank, t = make("a")
    bank.deposit(t, "a", 30)
    bank.schedule_payment(t + 1, "a", 30, 1)
    assert bank.get_balance(t + 3, "a", t + 2) == 0
    assert bank.top_spenders(t + 4, 1) == ["a(30)"]
