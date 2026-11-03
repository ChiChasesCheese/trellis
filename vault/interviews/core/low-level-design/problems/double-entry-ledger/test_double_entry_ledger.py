"""复式账本的测试：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

P = impl.Posting


# ---- 第 1 关：分录、借贷平衡、幂等提交、余额、冲正 ------------


def entry(eid, *legs, reverses=None):
    return impl.Entry(eid, tuple(P(*leg) for leg in legs), reverses)


def deposit(eid, user, amount, ccy="USD"):
    """充值：来源账户 psp 余额变负，用户钱包增加。"""
    return entry(eid, ("psp", ccy, -amount), (user, ccy, amount))


def transfer(eid, src, dst, amount, ccy="USD"):
    return entry(eid, (src, ccy, -amount), (dst, ccy, amount))


def test_part1_post_updates_balances_and_returns_increasing_seq():
    led = impl.Ledger()
    assert led.post(deposit("e1", "alice", 10000)) == 1
    assert led.post(transfer("e2", "alice", "bob", 3000)) == 2
    assert led.balance("alice", "USD") == 7000
    assert led.balance("bob", "USD") == 3000
    assert led.balance("psp", "USD") == -10000
    assert led.balance("nobody", "USD") == 0
    assert led.total("USD") == 0


def test_part1_balance_is_per_currency():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 500, "USD"))
    led.post(deposit("e2", "alice", 700, "MYR"))
    assert led.balance("alice", "USD") == 500
    assert led.balance("alice", "MYR") == 700
    assert led.total("USD") == led.total("MYR") == 0


@pytest.mark.parametrize("legs", [
    [("a", "USD", 100), ("b", "USD", -99)],                       # 不平
    [("a", "USD", 100)],                                          # 只有一条腿
    [],                                                           # 没有腿
    [("a", "USD", 100), ("b", "EUR", -100)],                      # 总和为 0 但各币种不平
    [("a", "USD", 100), ("b", "USD", -100), ("c", "EUR", 5), ("d", "EUR", -4)],
    [("a", "USD", 0), ("b", "USD", 0)],                           # 零金额的腿
])
def test_part1_invalid_entries_are_rejected_without_trace(legs):
    led = impl.Ledger()
    with pytest.raises(impl.InvalidEntry):
        led.post(entry("bad", *legs))
    assert led.total("USD") == 0 and led.balance("a", "USD") == 0
    assert led.post(deposit("good", "a", 5)) == 1                  # 失败的调用不占序号
    assert led.balance("a", "USD") == 5


def test_part1_entry_with_empty_id_is_invalid():
    with pytest.raises(impl.InvalidEntry):
        impl.Ledger().post(deposit("", "a", 5))


def test_part1_multi_leg_entries_and_same_account_legs():
    led = impl.Ledger()
    # 一笔充值同时扣手续费：三条腿
    led.post(entry("e1", ("psp", "USD", -1000), ("alice", "USD", 980), ("fees", "USD", 20)))
    assert (led.balance("alice", "USD"), led.balance("fees", "USD")) == (980, 20)
    # 同一账户出现在两条腿里，净额生效
    led.post(entry("e2", ("alice", "USD", -100), ("alice", "USD", 30), ("bob", "USD", 70)))
    assert led.balance("alice", "USD") == 910 and led.balance("bob", "USD") == 70


def test_part1_duplicate_submission_is_a_no_op_returning_first_seq():
    led = impl.Ledger()
    e = deposit("e1", "alice", 100)
    assert led.post(e) == 1
    led.post(deposit("e2", "alice", 50))
    assert led.post(deposit("e1", "alice", 100)) == 1              # 内容相同的新对象也算重复
    assert led.balance("alice", "USD") == 150
    assert led.post(deposit("e3", "alice", 1)) == 3                # 重复提交不占序号


def test_part1_same_id_with_different_content_is_a_conflict():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))
    with pytest.raises(impl.ConflictError):
        led.post(deposit("e1", "alice", 101))
    with pytest.raises(impl.ConflictError):
        led.post(deposit("e1", "bob", 100))
    assert led.balance("alice", "USD") == 100


def test_part1_every_failure_can_be_caught_as_ledger_error():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 1))
    for call in (lambda: led.post(entry("bad", ("a", "USD", 1))),                  # InvalidEntry
                 lambda: led.post(deposit("e1", "alice", 2)),                      # ConflictError
                 lambda: led.reverse("ghost", "r")):                               # UnknownEntry
        with pytest.raises(impl.LedgerError):
            call()
    led.reverse("e1", "r1")
    with pytest.raises(impl.LedgerError):
        led.reverse("e1", "r2")                                                    # AlreadyReversed


def test_part1_reverse_negates_every_leg_and_keeps_the_original():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 10000))
    led.post(transfer("e2", "alice", "bob", 3000))
    seq = led.reverse("e2", "e2-undo")
    assert seq == 3
    assert led.balance("alice", "USD") == 10000 and led.balance("bob", "USD") == 0
    j = led.journal()
    assert [e.id for e in j] == ["e1", "e2", "e2-undo"]
    assert j[1] == transfer("e2", "alice", "bob", 3000)            # 原分录原样保留
    assert j[2].reverses == "e2"
    assert led.total("USD") == 0


def test_part1_reverse_unknown_entry():
    with pytest.raises(impl.UnknownEntry):
        impl.Ledger().reverse("nope", "x")


def test_part1_reverse_is_idempotent_per_new_id_but_only_once_per_entry():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))
    assert led.reverse("e1", "r1") == 2
    assert led.reverse("e1", "r1") == 2                            # 同一个冲正 ID 重试：返回原序号
    with pytest.raises(impl.AlreadyReversed):
        led.reverse("e1", "r2")                                    # 换个 ID 再冲一次：不行
    assert led.balance("alice", "USD") == 0
    assert len(led.journal()) == 2


def test_part1_new_id_clashing_with_another_entry_is_a_conflict():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))
    led.post(deposit("e2", "alice", 100))
    with pytest.raises(impl.ConflictError):
        led.reverse("e1", "e2")
    assert led.balance("alice", "USD") == 200


def test_part1_a_reversal_can_itself_be_reversed():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))
    led.reverse("e1", "r1")
    led.reverse("r1", "r1-undo")
    assert led.balance("alice", "USD") == 100


def test_part1_posting_with_unknown_or_taken_reverses_is_rejected():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))
    with pytest.raises(impl.UnknownEntry):
        led.post(entry("x", ("psp", "USD", 100), ("alice", "USD", -100), reverses="ghost"))
    led.reverse("e1", "r1")
    with pytest.raises(impl.AlreadyReversed):
        led.post(entry("y", ("psp", "USD", 100), ("alice", "USD", -100), reverses="e1"))


def test_part1_journal_is_a_snapshot():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 1))
    snap = led.journal()
    led.post(deposit("e2", "alice", 1))
    assert len(snap) == 1 and len(led.journal()) == 2
    assert isinstance(snap, tuple)


# ---- 第 2 关：历史余额、账户下限、对账单 ------------


def funded(amount=10000):
    led = impl.Ledger()
    led.post(deposit("seed", "alice", amount))
    led.set_floor("alice", "USD", 0)
    return led


def test_part2_balance_at_walks_history():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 10000))                        # 1
    led.post(deposit("e2", "bob", 500))                            # 2：不涉及 alice
    led.post(transfer("e3", "alice", "bob", 3000))                 # 3
    led.reverse("e3", "r3")                                        # 4
    assert [led.balance_at("alice", "USD", s) for s in range(0, 7)] == [0, 10000, 10000, 7000, 10000, 10000, 10000]
    assert led.balance_at("bob", "USD", 2) == 500
    assert led.balance_at("bob", "USD", 3) == 3500
    assert led.balance_at("ghost", "USD", 4) == 0
    assert led.balance_at("alice", "USD", -5) == 0
    assert led.balance_at("alice", "EUR", 4) == 0


def test_part2_floor_rejects_overdraft_and_leaves_no_trace():
    assert issubclass(impl.InsufficientFunds, impl.LedgerError)
    led = funded(100)
    with pytest.raises(impl.InsufficientFunds):
        led.post(transfer("t1", "alice", "bob", 101))
    assert led.balance("alice", "USD") == 100 and led.balance("bob", "USD") == 0
    assert len(led.journal()) == 1
    assert led.post(transfer("t1", "alice", "bob", 100)) == 2      # 同一个 ID 在资金够的时候可以重新提交
    assert led.balance("alice", "USD") == 0                        # 正好到下限是允许的


def test_part2_floor_rejection_is_atomic_across_legs():
    led = funded(100)
    led.post(entry("ok", ("alice", "USD", -60), ("bob", "USD", 30), ("carol", "USD", 30)))
    with pytest.raises(impl.InsufficientFunds):
        led.post(entry("too-much", ("alice", "USD", -60), ("bob", "USD", 30), ("carol", "USD", 30)))
    assert [led.balance(a, "USD") for a in ("alice", "bob", "carol")] == [40, 30, 30]   # 失败的那条一条腿都没落


def test_part2_accounts_without_a_floor_may_go_negative():
    led = funded(100)
    assert led.balance("psp", "USD") == -100                       # 对手账户没有下限
    led.post(transfer("t1", "bob", "alice", 50))                   # bob 没设下限，可以先欠着
    assert led.balance("bob", "USD") == -50


def test_part2_floor_can_be_negative_for_a_credit_line():
    led = impl.Ledger()
    led.set_floor("alice", "USD", -500)
    led.post(transfer("t1", "alice", "bob", 500))
    with pytest.raises(impl.InsufficientFunds):
        led.post(transfer("t2", "alice", "bob", 1))


def test_part2_statement_pages_through_history():
    led = impl.Ledger()
    led.post(deposit("e1", "alice", 100))                          # 1
    led.post(deposit("e2", "bob", 5))                              # 2
    led.post(transfer("e3", "alice", "bob", 30))                   # 3
    led.post(entry("e4", ("alice", "USD", -10), ("alice", "USD", 4), ("bob", "USD", 6)))   # 4：同账户两条腿合并成一行
    lines = led.statement("alice", "USD")
    assert [(l.seq, l.entry_id, l.amount, l.balance_after) for l in lines] == [
        (1, "e1", 100, 100), (3, "e3", -30, 70), (4, "e4", -6, 64)]
    page1 = led.statement("alice", "USD", limit=2)
    page2 = led.statement("alice", "USD", after_seq=page1[-1].seq, limit=2)
    assert [l.seq for l in page1] == [1, 3] and [l.seq for l in page2] == [4]
    assert led.statement("alice", "USD", after_seq=99) == []
    assert led.statement("ghost", "USD") == []


def test_part2_statement_rejects_a_bad_limit():
    with pytest.raises(ValueError):
        impl.Ledger().statement("alice", "USD", limit=0)


# ---- 第 3 关：冻结、原子释放、并发 ------------


def test_part3_hold_reduces_available_but_not_balance():
    led = funded(100)
    led.hold("h1", "alice", "USD", 60)
    assert led.balance("alice", "USD") == 100
    assert led.available("alice", "USD") == 40
    with pytest.raises(impl.InsufficientFunds):
        led.post(transfer("t1", "alice", "bob", 41))
    led.post(transfer("t2", "alice", "bob", 40))
    assert led.available("alice", "USD") == 0
    with pytest.raises(impl.InsufficientFunds):
        led.hold("h2", "alice", "USD", 1)


def test_part3_hold_is_idempotent_and_conflicts_on_changed_content():
    led = funded(100)
    led.hold("h1", "alice", "USD", 60)
    led.hold("h1", "alice", "USD", 60)
    assert led.available("alice", "USD") == 40                     # 重复冻结不叠加
    with pytest.raises(impl.ConflictError):
        led.hold("h1", "alice", "USD", 61)
    for bad in (0, -5):
        with pytest.raises(impl.InvalidEntry):
            led.hold("h-bad", "alice", "USD", bad)


def test_part3_release_restores_available_and_is_idempotent():
    led = funded(100)
    led.hold("h1", "alice", "USD", 60)
    led.release("h1")
    led.release("h1")
    assert led.available("alice", "USD") == 100
    with pytest.raises(impl.UnknownEntry):
        led.release("ghost")
    led.hold("h1", "alice", "USD", 60)                             # 已释放过的同参数冻结，重放是无操作
    assert led.available("alice", "USD") == 100


def test_part3_post_can_release_its_own_hold_atomically():
    led = funded(100)
    led.hold("h1", "alice", "USD", 60)
    with pytest.raises(impl.InsufficientFunds):
        led.post(transfer("t1", "alice", "bob", 61))               # 可用余额只有 40
    led.post(transfer("t1", "alice", "bob", 61), release_hold="h1")   # 先释放 60 再写入，一步完成
    assert led.balance("alice", "USD") == 39 and led.available("alice", "USD") == 39


def test_part3_post_with_release_hold_failure_keeps_the_hold():
    led = funded(100)
    led.hold("h1", "alice", "USD", 60)
    with pytest.raises(impl.InsufficientFunds):
        led.post(transfer("t1", "alice", "bob", 101), release_hold="h1")
    assert led.available("alice", "USD") == 40                     # 失败：冻结还在
    with pytest.raises(impl.UnknownEntry):
        led.post(transfer("t2", "alice", "bob", 1), release_hold="ghost")
    led.post(transfer("t3", "alice", "bob", 100), release_hold="h1")
    assert led.balance("alice", "USD") == 0 and led.available("alice", "USD") == 0
    with pytest.raises(impl.ConflictError):
        led.post(transfer("t4", "psp", "bob", 1), release_hold="h1")   # 冻结已经用掉了
    assert led.post(transfer("t3", "alice", "bob", 100), release_hold="h1") == 2   # 重放同一条分录：幂等


def test_part3_concurrent_transfers_never_overdraw():
    led = funded(100)
    n_threads, per_thread = 8, 5
    barrier = threading.Barrier(n_threads)
    wins, lock = [], threading.Lock()

    def worker(t):
        barrier.wait()
        for i in range(per_thread):
            try:
                led.post(transfer(f"t{t}-{i}", "alice", "bob", 10))
                with lock:
                    wins.append(1)
            except impl.InsufficientFunds:
                pass

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(wins) == 10                                         # 40 次尝试，正好 100/10 次成功
    assert led.balance("alice", "USD") == 0 and led.balance("bob", "USD") == 100
    assert led.total("USD") == 0
    assert len(led.journal()) == 11


def test_part3_concurrent_duplicate_submissions_post_once():
    led = funded(1000)
    n = 8
    barrier = threading.Barrier(n)
    seqs = []

    def worker():
        barrier.wait()
        seqs.append(led.post(transfer("same", "alice", "bob", 300)))

    threads = [threading.Thread(target=worker) for _ in range(n)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert set(seqs) == {2}
    assert led.balance("alice", "USD") == 700 and led.balance("bob", "USD") == 300


def test_part3_concurrent_hold_and_post_do_not_both_spend_the_money():
    led = funded(100)
    barrier = threading.Barrier(2)
    outcome = {}

    def holder():
        barrier.wait()
        try:
            led.hold("h", "alice", "USD", 80)
            outcome["hold"] = True
        except impl.InsufficientFunds:
            outcome["hold"] = False

    def spender():
        barrier.wait()
        try:
            led.post(transfer("t", "alice", "bob", 80))
            outcome["post"] = True
        except impl.InsufficientFunds:
            outcome["post"] = False

    threads = [threading.Thread(target=holder), threading.Thread(target=spender)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert outcome["hold"] != outcome["post"]                      # 100 块只够其中一个 80
    assert led.available("alice", "USD") == 20


# ---- 第 4 关（选做）：换汇 ------------


def test_part4_exchange_is_one_balanced_entry():
    led = impl.Ledger()
    led.post(deposit("d1", "alice", 10000, "USD"))
    seq = led.exchange("x1", "alice", "USD", 1000, "MYR", 4650)
    assert seq == 2
    assert led.balance("alice", "USD") == 9000 and led.balance("alice", "MYR") == 4650
    assert led.balance("fx", "USD") == 1000 and led.balance("fx", "MYR") == -4650
    assert led.total("USD") == 0 and led.total("MYR") == 0
    assert len(led.journal()[1].postings) == 4


def test_part4_exchange_is_idempotent_and_validates():
    led = impl.Ledger()
    led.post(deposit("d1", "alice", 10000, "USD"))
    led.exchange("x1", "alice", "USD", 1000, "MYR", 4650)
    assert led.exchange("x1", "alice", "USD", 1000, "MYR", 4650) == 2
    with pytest.raises(impl.ConflictError):
        led.exchange("x1", "alice", "USD", 1000, "MYR", 4700)
    for args in [("x2", "alice", "USD", 5, "USD", 5), ("x3", "alice", "USD", 0, "MYR", 5),
                 ("x4", "alice", "USD", 5, "MYR", -1)]:
        with pytest.raises(impl.InvalidEntry):
            led.exchange(*args)


def test_part4_exchange_respects_the_floor():
    led = impl.Ledger()
    led.post(deposit("d1", "alice", 100, "USD"))
    led.set_floor("alice", "USD", 0)
    with pytest.raises(impl.InsufficientFunds):
        led.exchange("x1", "alice", "USD", 101, "MYR", 400)
    assert led.balance("alice", "MYR") == 0
