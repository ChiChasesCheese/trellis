"""幂等转账服务的测试：`-k part1` 选第 1 关，依此类推。线程测试用事件和屏障排顺序，不靠 sleep 估时间。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T = 5.0  # 线程测试里所有等待的上限，只在实现出错时才会用满


def make_service(alice=10000, **kw):
    return impl.TransferService({("alice", "USD"): alice}, **kw)


def pay(svc, key="k1", amount=3000, client="c1", src="alice", dst="bob", ccy="USD"):
    return svc.transfer(client, key, src, dst, amount, ccy)


class FakeClock:
    def __init__(self, now=0.0):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class Hook:
    """可控的 on_execute：第 n 次调用时可以阻塞（等 release[n]）或抛异常。"""

    def __init__(self, block=(), fail=()):
        self.block, self.fail = set(block), set(fail)
        self.calls = 0
        self.entered = [threading.Event() for _ in range(8)]
        self.release = [threading.Event() for _ in range(8)]
        self._mu = threading.Lock()

    def __call__(self, client, key):
        with self._mu:
            n = self.calls
            self.calls += 1
        self.entered[n].set()
        if n in self.block:
            assert self.release[n].wait(T), "测试里的闸门没有被打开"
        if n in self.fail:
            raise RuntimeError("risk service down")


def in_thread(fn):
    """在线程里跑 fn，返回 (线程, 结果字典)；结果字典里是 value 或 error。"""
    box = {}

    def run():
        try:
            box["value"] = fn()
        except BaseException as e:  # noqa: BLE001 - 测试要原样拿到异常
            box["error"] = e

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t, box


# ---- 第 1 关：同键只转一次 -----------------------------------------------------


def test_part1_transfer_moves_money_and_returns_a_result():
    svc = make_service()
    r = pay(svc)
    assert r == impl.TransferResult("succeeded", None, 1)
    assert svc.balance("alice", "USD") == 7000 and svc.balance("bob", "USD") == 3000
    assert svc.balance("nobody", "USD") == 0
    (rec,) = svc.transfers()
    assert (rec.seq, rec.client, rec.key, rec.src, rec.dst, rec.amount, rec.currency) == \
        (1, "c1", "k1", "alice", "bob", 3000, "USD")


def test_part1_retry_with_the_same_key_returns_the_first_result_without_moving_money_again():
    svc = make_service()
    first = pay(svc)
    for _ in range(3):
        assert pay(svc) == first
    assert svc.balance("alice", "USD") == 7000 and len(svc.transfers()) == 1


def test_part1_same_key_with_a_different_request_is_rejected():
    svc = make_service()
    pay(svc)
    for bad in (dict(amount=3001), dict(dst="carol"), dict(src="carol"), dict(ccy="EUR")):
        with pytest.raises(impl.KeyReuse):
            pay(svc, **bad)
    assert svc.balance("alice", "USD") == 7000 and len(svc.transfers()) == 1
    assert pay(svc).status == "succeeded"                      # 原来的请求仍然可以重放


def test_part1_insufficient_funds_is_a_remembered_result_not_an_exception():
    svc = impl.TransferService({("alice", "USD"): 1000, ("bob", "USD"): 5000})
    r = svc.transfer("c1", "k1", "alice", "carol", 2000, "USD")
    assert r == impl.TransferResult("rejected", "insufficient_funds", None)
    assert svc.balance("alice", "USD") == 1000 and svc.transfers() == ()
    svc.transfer("c1", "topup", "bob", "alice", 5000, "USD")                     # alice 现在有 6000
    assert svc.transfer("c1", "k1", "alice", "carol", 2000, "USD") == r           # 同一个键：还是那个拒绝
    assert svc.transfer("c1", "k2", "alice", "carol", 2000, "USD").status == "succeeded"   # 新键：新的业务意图


def test_part1_spending_exactly_the_whole_balance_is_allowed():
    svc = make_service(alice=3000)
    assert pay(svc, amount=3000).status == "succeeded"
    assert svc.balance("alice", "USD") == 0
    assert pay(svc, key="k2", amount=1).status == "rejected"


def test_part1_keys_are_scoped_per_client():
    svc = make_service()
    a = pay(svc, key="same", client="c1", amount=1000)
    b = pay(svc, key="same", client="c2", amount=2000)         # 不同客户端的同名键互不相干
    assert (a.seq, b.seq) == (1, 2)
    assert svc.balance("bob", "USD") == 3000


@pytest.mark.parametrize("kw", [
    dict(amount=0), dict(amount=-5), dict(amount=10.5), dict(dst="alice"), dict(key=""), dict(client=""),
])
def test_part1_invalid_requests_raise_and_do_not_claim_the_key(kw):
    svc = make_service()
    with pytest.raises(impl.InvalidRequest):
        pay(svc, **kw)
    assert svc.balance("alice", "USD") == 10000 and svc.transfers() == ()
    if "key" not in kw and "client" not in kw:
        assert pay(svc, amount=100).status == "succeeded"       # 同一个键随后用合法请求，照常执行


def test_part1_failures_share_one_base_class_and_bad_input_is_a_value_error():
    svc = make_service()
    with pytest.raises(ValueError):
        pay(svc, amount=0)
    with pytest.raises(impl.TransferError):
        pay(svc, amount=-1)
    pay(svc)
    with pytest.raises(impl.TransferError):
        pay(svc, amount=1)                                     # KeyReuse


def test_part1_sequence_numbers_count_only_successful_transfers():
    svc = make_service(alice=5000)
    assert pay(svc, key="a", amount=1000).seq == 1
    assert pay(svc, key="b", amount=9000).status == "rejected"
    assert pay(svc, key="c", amount=1000).seq == 2
    assert pay(svc, key="a", amount=1000).seq == 1


# ---- 第 2 关：并发的重复请求合并 ------------------------------------------------


def test_part2_eight_threads_with_the_same_key_transfer_once():
    svc = make_service()
    barrier = threading.Barrier(8)
    results = []

    def worker():
        barrier.wait(T)
        results.append(pay(svc))

    threads = [threading.Thread(target=worker) for _ in range(8)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert len(results) == 8 and len(set(results)) == 1 and results[0].status == "succeeded"
    assert svc.balance("alice", "USD") == 7000 and svc.balance("bob", "USD") == 3000
    assert len(svc.transfers()) == 1


def test_part2_a_duplicate_waits_for_the_first_request_and_gets_its_result():
    hook = Hook(block={0})
    svc = make_service(on_execute=hook)
    t1, first = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    t2, second = in_thread(lambda: pay(svc))                   # 第一个还在外部步骤里
    hook.release[0].set()
    t1.join(T), t2.join(T)
    assert first["value"] == second["value"] and first["value"].status == "succeeded"
    assert hook.calls == 1                                     # 外部步骤只跑了一次
    assert svc.balance("alice", "USD") == 7000


def test_part2_duplicate_gets_still_running_when_the_first_takes_too_long():
    hook = Hook(block={0})
    svc = make_service(wait=0.05, on_execute=hook)
    t1, first = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    with pytest.raises(impl.StillRunning):
        pay(svc)
    assert svc.balance("alice", "USD") == 10000                # 等待者没有自己去执行
    hook.release[0].set()
    t1.join(T)
    assert pay(svc) == first["value"]                          # 之后的重试拿到完成的结果
    assert len(svc.transfers()) == 1


def test_part2_same_key_different_request_fails_fast_even_while_running():
    hook = Hook(block={0})
    svc = make_service(wait=T, on_execute=hook)
    t1, _ = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    with pytest.raises(impl.KeyReuse):                         # 不用等第一个请求结束就能判定
        pay(svc, amount=1)
    hook.release[0].set()
    t1.join(T)


def test_part2_a_slow_external_step_does_not_block_other_keys():
    hook = Hook(block={0})
    svc = make_service(on_execute=hook)
    slow, _ = in_thread(lambda: pay(svc, key="slow"))
    assert hook.entered[0].wait(T)
    fast, box = in_thread(lambda: pay(svc, key="fast", amount=1000))
    fast.join(T)
    assert not fast.is_alive() and box["value"].status == "succeeded"   # 慢请求没有持有全局锁
    hook.release[0].set()
    slow.join(T)
    assert svc.balance("alice", "USD") == 10000 - 3000 - 1000


def test_part2_different_keys_on_one_source_never_overdraw():
    svc = make_service(alice=100)
    n = 16
    barrier = threading.Barrier(n)
    results = []

    def worker(i):
        barrier.wait(T)
        results.append(pay(svc, key=f"k{i}", amount=10))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert sorted(r.status for r in results).count("succeeded") == 10
    assert svc.balance("alice", "USD") == 0 and svc.balance("bob", "USD") == 100
    assert sorted(r.seq for r in svc.transfers()) == list(range(1, 11))


def test_part2_a_rejected_result_is_also_shared_by_concurrent_duplicates():
    svc = make_service(alice=10)
    barrier = threading.Barrier(4)
    results = []

    def worker():
        barrier.wait(T)
        results.append(pay(svc))

    threads = [threading.Thread(target=worker) for _ in range(4)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert results == [impl.TransferResult("rejected", "insufficient_funds", None)] * 4


# ---- 第 3 关：失败要释放键、结果保留期 ------------------------------------------


def test_part3_a_failure_before_the_money_moves_releases_the_key():
    hook = Hook(fail={0})
    svc = make_service(on_execute=hook)
    with pytest.raises(RuntimeError):
        pay(svc)
    assert svc.balance("alice", "USD") == 10000 and svc.transfers() == ()
    r = pay(svc)                                               # 同一个键再来：当作从没见过
    assert r.status == "succeeded" and svc.balance("alice", "USD") == 7000
    assert pay(svc) == r and hook.calls == 2


def test_part3_waiters_recompete_when_the_owner_fails():
    hook = Hook(block={0}, fail={0})
    svc = make_service(on_execute=hook)
    t1, first = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    t2, second = in_thread(lambda: pay(svc))
    hook.release[0].set()
    t1.join(T), t2.join(T)
    assert isinstance(first["error"], RuntimeError)
    assert second["value"].status == "succeeded"               # 等待者成了新的拥有者
    assert len(svc.transfers()) == 1 and svc.balance("alice", "USD") == 7000


def test_part3_a_failed_request_with_a_different_fingerprint_does_not_poison_the_key():
    hook = Hook(fail={0})
    svc = make_service(on_execute=hook)
    with pytest.raises(RuntimeError):
        pay(svc, amount=3000)
    assert pay(svc, amount=500).status == "succeeded"          # 键已释放，换个金额也可以


def test_part3_results_are_kept_for_ttl_then_the_key_is_a_new_request():
    clock = FakeClock()
    svc = make_service(ttl=100, clock=clock)
    first = pay(svc)
    clock.advance(99.9)
    assert pay(svc) == first and len(svc.transfers()) == 1
    clock.advance(0.1)                                         # 正好 100 秒：已过期
    again = pay(svc)
    assert again.status == "succeeded" and again.seq == 2      # 保留期之外重试会再转一次，这是 ttl 的代价
    assert svc.balance("alice", "USD") == 4000


def test_part3_a_rejected_result_also_expires():
    clock = FakeClock()
    svc = impl.TransferService({("alice", "USD"): 10, ("bob", "USD"): 5000}, ttl=50, clock=clock)
    rejected = pay(svc)
    assert rejected.status == "rejected"
    svc.transfer("c2", "topup", "bob", "alice", 5000, "USD")
    clock.advance(49)
    assert pay(svc) == rejected                                # 保留期内：仍是同一个拒绝
    clock.advance(1)
    assert pay(svc).status == "succeeded"                      # 过期后是新请求，这次余额够了


def test_part3_purge_removes_only_expired_results():
    clock = FakeClock()
    svc = make_service(ttl=100, clock=clock)
    pay(svc, key="old")
    clock.advance(60)
    pay(svc, key="new")
    clock.advance(50)                                          # old 已 110 秒，new 只有 50 秒
    assert svc.purge() == 1
    assert svc.purge() == 0
    assert pay(svc, key="new").seq == 2                        # new 还在，重放
    assert pay(svc, key="old").seq == 3                        # old 没了，重新执行


def test_part3_without_ttl_nothing_expires():
    clock = FakeClock()
    svc = make_service(clock=clock)
    pay(svc)
    clock.advance(10 ** 9)
    assert svc.purge() == 0
    assert pay(svc).seq == 1


def test_part3_ttl_never_expires_a_request_that_is_still_running():
    clock = FakeClock()
    hook = Hook(block={0})
    svc = make_service(ttl=10, wait=0.05, clock=clock, on_execute=hook)
    t1, _ = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    clock.advance(1000)
    assert svc.purge() == 0
    with pytest.raises(impl.StillRunning):                     # 仍然是同一个执行中的请求，不会被当成新请求
        pay(svc)
    hook.release[0].set()
    t1.join(T)
    assert len(svc.transfers()) == 1


# ---- 第 4 关（选做）：租约，接手失联的拥有者 ------------------------------------


def test_part4_before_the_lease_expires_a_duplicate_still_waits():
    clock = FakeClock()
    hook = Hook(block={0})
    svc = make_service(lease=30, wait=0.05, clock=clock, on_execute=hook)
    t1, _ = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    clock.advance(29.9)
    with pytest.raises(impl.StillRunning):
        pay(svc)
    hook.release[0].set()
    t1.join(T)


def test_part4_after_the_lease_expires_a_duplicate_takes_over_and_money_moves_once():
    clock = FakeClock()
    hook = Hook(block={0})
    svc = make_service(lease=30, clock=clock, on_execute=hook)
    t1, old = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    clock.advance(30)
    taken = pay(svc)                                           # 第二个请求接手并完成
    assert taken.status == "succeeded"
    hook.release[0].set()                                      # 旧的拥有者醒来，继续往下走
    t1.join(T)
    assert old["value"] == taken                               # 旧拥有者拿到同样的结果，没有再动钱
    assert svc.balance("alice", "USD") == 7000 and len(svc.transfers()) == 1


def test_part4_the_old_owner_may_commit_first_and_the_new_owner_reuses_its_result():
    clock = FakeClock()
    hook = Hook(block={0, 1})
    svc = make_service(lease=30, clock=clock, on_execute=hook)
    t1, old = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    clock.advance(30)
    t2, new = in_thread(lambda: pay(svc))
    assert hook.entered[1].wait(T)
    hook.release[0].set()
    t1.join(T)                                                 # 旧的先提交
    hook.release[1].set()
    t2.join(T)
    assert old["value"] == new["value"] and old["value"].status == "succeeded"
    assert svc.balance("alice", "USD") == 7000 and len(svc.transfers()) == 1


def test_part4_if_the_new_owner_fails_the_old_one_must_not_move_money_later():
    clock = FakeClock()
    hook = Hook(block={0}, fail={1})
    svc = make_service(lease=30, clock=clock, on_execute=hook)
    t1, old = in_thread(lambda: pay(svc))
    assert hook.entered[0].wait(T)
    clock.advance(30)
    with pytest.raises(RuntimeError):                          # 接手的这一轮失败，键被释放
        pay(svc)
    hook.release[0].set()
    t1.join(T)
    assert isinstance(old["error"], impl.LeaseLost)            # 旧拥有者不能在键已释放后再动钱
    assert svc.balance("alice", "USD") == 10000 and svc.transfers() == ()
    assert pay(svc).status == "succeeded" and svc.balance("alice", "USD") == 7000   # 重试照常成功
