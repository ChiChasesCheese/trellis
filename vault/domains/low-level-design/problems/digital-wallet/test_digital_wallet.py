"""数字钱包的测试：分关覆盖账户流水、双分录守恒、加锁顺序与幂等重试。"""

from __future__ import annotations

import importlib
import os
import random
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)


class FakeClock:
    """注入的时钟：测试里绝不 `sleep`，时间只在我们说它走的时候走。"""

    def __init__(self, now: datetime = START) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs: float) -> None:
        self.now = self.now + timedelta(**kwargs)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def wallet(clock: FakeClock):
    w = impl.Wallet(clock=clock)
    w.open_account("alice", opening_balance=10_000)
    w.open_account("bob", opening_balance=5_000)
    return w


# --- 第 1 关：账户、充值、提现、转账 ------------------------------------------


def test_top_up_increases_balance_and_leaves_two_balanced_entries(wallet):
    receipt = wallet.top_up("bob", 2_000)
    assert wallet.balance("bob") == 7_000
    debit, credit = wallet.transfer_entries(receipt.transfer_id)
    assert debit.delta + credit.delta == 0
    assert {debit.account_id, credit.account_id} == {"bob", impl.EXTERNAL_ACCOUNT_ID}


def test_withdraw_more_than_balance_is_rejected_and_changes_nothing(wallet):
    with pytest.raises(impl.InsufficientFundsError) as excinfo:
        wallet.withdraw("bob", 5_001)
    assert excinfo.value.shortfall == 1
    assert wallet.balance("bob") == 5_000


def test_transfer_moves_money_atomically_between_two_accounts(wallet):
    wallet.transfer("alice", "bob", 3_000)
    assert wallet.balance("alice") == 7_000
    assert wallet.balance("bob") == 8_000


def test_transfer_more_than_available_raises_and_changes_neither_side(wallet):
    with pytest.raises(impl.InsufficientFundsError):
        wallet.transfer("bob", "alice", 5_001)
    assert wallet.balance("alice") == 10_000
    assert wallet.balance("bob") == 5_000


def test_balance_never_negative_holds_across_a_chain_of_transfers(wallet):
    wallet.transfer("alice", "bob", 10_000)
    assert wallet.balance("alice") == 0
    with pytest.raises(impl.InsufficientFundsError):
        wallet.transfer("alice", "bob", 1)
    assert wallet.balance("alice") == 0


def test_transfer_to_the_same_account_is_rejected(wallet):
    with pytest.raises(impl.SameAccountTransferError):
        wallet.transfer("alice", "alice", 100)


def test_zero_or_negative_amount_is_rejected(wallet):
    with pytest.raises(impl.InvalidAmountError):
        wallet.top_up("bob", 0)
    with pytest.raises(impl.InvalidAmountError):
        wallet.transfer("alice", "bob", -1)


def test_unknown_account_is_rejected_everywhere(wallet):
    with pytest.raises(impl.UnknownAccountError):
        wallet.balance("carol")
    with pytest.raises(impl.UnknownAccountError):
        wallet.transfer("alice", "carol", 100)


def test_opening_the_same_account_twice_is_rejected(wallet):
    with pytest.raises(impl.WalletError):
        wallet.open_account("alice")


def test_external_account_cannot_be_used_as_a_transfer_endpoint(wallet):
    with pytest.raises(impl.UnknownAccountError):
        wallet.transfer("alice", impl.EXTERNAL_ACCOUNT_ID, 100)
    with pytest.raises(impl.UnknownAccountError):
        wallet.transfer(impl.EXTERNAL_ACCOUNT_ID, "bob", 100)


# --- 第 2 关：双分录账本与核对 --------------------------------------------------


def test_ledger_sums_to_zero_after_a_randomised_session(clock):
    """固定种子跑一批随机的充值/提现/转账，账本作为唯一真源必须全局守恒，缓存余额
    必须和账本重新推导出来的值完全一致——这正是"缓存并核对"这条设计承诺要证明的事。
    """
    rng = random.Random(20260120)
    w = impl.Wallet(clock=clock)
    accounts = [f"acc{i}" for i in range(5)]
    for account_id in accounts:
        w.open_account(account_id, opening_balance=rng.randint(0, 5_000))

    for _ in range(300):
        op = rng.choice(["top_up", "withdraw", "transfer"])
        amount = rng.randint(1, 500)
        try:
            if op == "top_up":
                w.top_up(rng.choice(accounts), amount)
            elif op == "withdraw":
                w.withdraw(rng.choice(accounts), amount)
            else:
                a, b = rng.sample(accounts, 2)
                w.transfer(a, b, amount)
        except impl.InsufficientFundsError:
            pass  # 随机金额偶尔超过余额，属于预期中的失败路径，不影响后面的断言

    assert w.ledger_total() == 0
    for account_id in accounts:
        assert w.balance(account_id) == w.derived_balance(account_id)
        assert w.reconcile(account_id) is False  # 缓存没有漂移，核对不需要纠正


def test_history_is_most_recent_first_and_respects_offset_and_limit(wallet):
    # bob 开户时带了 5_000 起始余额，它本身也是一笔"外部注入"、也落在账本里（见
    # `Wallet.open_account`），所以这里一共有 4 条分录，不是只有下面这三笔充值。
    for amount in (100, 200, 300):
        wallet.top_up("bob", amount)
    page = wallet.history("bob", offset=0, limit=2)
    assert [e.delta for e in page] == [300, 200]
    rest = wallet.history("bob", offset=2, limit=2)
    assert [e.delta for e in rest] == [100, 5_000]
    assert wallet.history_count("bob") == 4


def test_reconcile_reports_no_correction_when_cache_already_matches(wallet):
    wallet.transfer("alice", "bob", 1_000)
    assert wallet.reconcile("alice") is False
    assert wallet.reconcile("bob") is False


# --- 第 3 关：并发与加锁顺序 ----------------------------------------------------


def test_concurrent_transfers_in_both_directions_do_not_deadlock_and_conserve_money(clock):
    """A→B 和 B→A 两个方向同时高频转账：如果加锁顺序按参数（from, to）而不是按账户 id
    的稳定顺序，这两个线程会分别按相反的顺序抢两把锁，构成环形等待、直接死锁。稳定顺序
    下二者只会互相排队，函数必须在有限时间内返回——用 `join(timeout=...)` 断言的就是
    这一点，而不是账目本身（账目上还有 `total_before == total_after` 这条更强的断言）。
    """
    w = impl.Wallet(clock=clock)
    w.open_account("a", opening_balance=10_000)
    w.open_account("b", opening_balance=10_000)
    total_before = w.balance("a") + w.balance("b")
    barrier = threading.Barrier(2)
    rounds = 400

    def run(src: str, dst: str) -> None:
        barrier.wait()
        for _ in range(rounds):
            w.transfer(src, dst, 1)

    threads = [threading.Thread(target=run, args=("a", "b")),
               threading.Thread(target=run, args=("b", "a"))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert not any(t.is_alive() for t in threads), "线程没有在超时内结束，说明发生了死锁"
    assert w.balance("a") + w.balance("b") == total_before
    assert w.balance("a") >= 0 and w.balance("b") >= 0
    assert w.ledger_total() == 0


# --- 第 4 关：幂等与分页 --------------------------------------------------------


def test_retrying_a_transfer_with_the_same_client_key_moves_money_only_once(wallet):
    first = wallet.transfer("alice", "bob", 1_000, client_key="req-42")
    for _ in range(5):
        again = wallet.transfer("alice", "bob", 1_000, client_key="req-42")
        assert again == first
    assert wallet.balance("alice") == 9_000
    assert wallet.balance("bob") == 6_000
    # 一条开户入金 + 一条转账，重试的四次没有再各自追加分录。
    assert wallet.history_count("bob") == 2


def test_reusing_a_client_key_for_a_different_transfer_is_a_conflict(wallet):
    wallet.transfer("alice", "bob", 1_000, client_key="req-1")
    with pytest.raises(impl.IdempotencyConflictError):
        wallet.transfer("alice", "bob", 2_000, client_key="req-1")
    with pytest.raises(impl.IdempotencyConflictError):
        wallet.top_up("alice", 1_000, client_key="req-1")


def test_concurrent_retries_of_the_same_client_key_move_money_exactly_once(wallet):
    """幂等靠"重试必然竞争同一对账户锁"这个论证成立，而不是靠顺序调用侥幸没有撞上。
    16 个线程用同一个 client_key、同样的参数同时发起同一笔转账：账户锁的互斥性必须
    保证只有一个线程真正执行了记账，其余线程要么在锁上排队、要么在轮到自己时发现
    幂等缓存已经命中——不存在"两个线程都以为自己是第一个"的窗口，因为幂等检查和
    记账在同一段持锁的临界区里。
    """
    n = 16
    barrier = threading.Barrier(n)
    results: list[object] = [None] * n
    errors: list[BaseException | None] = [None] * n

    def run(i: int) -> None:
        barrier.wait()
        try:
            results[i] = wallet.transfer("alice", "bob", 1_000, client_key="race-same")
        except Exception as exc:  # 记录下来在主线程断言，不让子线程的异常悄悄消失
            errors[i] = exc

    threads = [threading.Thread(target=run, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert not any(t.is_alive() for t in threads), "线程没有在超时内结束，说明发生了死锁"
    # 资金充足、参数完全相同：每个线程要么拿到同一个回执，要么（理论上）遇到一个
    # 有名字的幂等冲突异常——不会出现"钱被移动了不止一次"这种既非成功、也不报错的结果。
    for error in errors:
        if error is not None:
            assert isinstance(error, impl.IdempotencyConflictError)
    receipts = [r for r in results if r is not None]
    assert receipts, "至少要有一个线程成功拿到回执"
    assert len(set(receipts)) == 1, "所有成功的线程必须拿到完全相同的回执"

    assert wallet.balance("alice") == 10_000 - 1_000  # 钱只搬动了一次
    assert wallet.balance("bob") == 5_000 + 1_000
    assert wallet.history_count("alice") == 2  # 开户入金一条 + 这一笔转账一条，没有被重复记账
    assert wallet.history_count("bob") == 2
    assert wallet.ledger_total() == 0


def test_concurrent_retries_of_the_same_client_key_with_different_params_conflict(wallet):
    """两个线程同时用同一个 client_key，但金额不同——这是调用方的 bug（幂等键被错误
    地复用到了两笔不同的移动上），必须恰好一个线程成功、另一个线程拿到一个有名字的
    冲突异常，而不是后到的线程静默覆盖先到的那笔、或者两笔都生效。
    """
    barrier = threading.Barrier(2)
    results: list[object] = [None, None]
    errors: list[BaseException | None] = [None, None]

    def run(i: int, amount: int) -> None:
        barrier.wait()
        try:
            results[i] = wallet.transfer("alice", "bob", amount, client_key="race-conflict")
        except Exception as exc:
            errors[i] = exc

    threads = [threading.Thread(target=run, args=(0, 1_000)),
               threading.Thread(target=run, args=(1, 2_000))]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert not any(t.is_alive() for t in threads), "线程没有在超时内结束，说明发生了死锁"
    winners = [r for r in results if r is not None]
    losers = [e for e in errors if e is not None]
    assert len(winners) == 1, "恰好一个线程应该真正执行了转账"
    assert len(losers) == 1 and isinstance(losers[0], impl.IdempotencyConflictError), (
        "另一个线程必须看到一个有名字的冲突异常，而不是静默被覆盖或者两边都生效")

    winning_amount = winners[0].amount
    assert wallet.balance("alice") == 10_000 - winning_amount
    assert wallet.balance("bob") == 5_000 + winning_amount
    assert wallet.ledger_total() == 0


def test_purge_idempotency_before_cutoff_removes_only_old_receipts(wallet, clock):
    wallet.transfer("alice", "bob", 100, client_key="old")
    clock.advance(days=2)
    wallet.transfer("alice", "bob", 100, client_key="new")
    removed = wallet.purge_idempotency_before(clock.now - timedelta(days=1))
    assert removed == 1
    # 旧回执被清掉后，同一个 key 会被当成一笔新的移动重新执行。
    wallet.transfer("alice", "bob", 100, client_key="old")
    assert wallet.balance("bob") == 5_000 + 100 + 100 + 100
