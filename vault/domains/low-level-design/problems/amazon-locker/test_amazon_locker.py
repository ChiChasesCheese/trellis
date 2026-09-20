"""快递柜的验收测试：分配规则、一次性码的三种失败、过期回收、逆向投件、多网点与并发。

时间和取件码都被注入，所以整套测试没有任何 sleep、没有任何随机；断言全部落在公开行为和
只读计数上（`code_count`、`pending_expiry_count`、`free_count`、`state_of`），不碰私有属性。
"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

from datetime import datetime, timedelta  # noqa: E402

START = datetime(2026, 3, 1, 9, 0)


class FakeClock:
    """可手动推进的时钟；注入之后"过期"是一件能被精确复现的事。"""

    def __init__(self, now=START):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, **kwargs):
        self.now = self.now + timedelta(**kwargs)
        return self.now


def codes():
    """确定性的取件码生成器：CODE-0001、CODE-0002……"""
    counter = iter(range(1, 10_000))
    return lambda: f"CODE-{next(counter):04d}"


def make_site(sizes=("small", "small", "medium", "large"), clock=None, **kwargs):
    catalog = {"small": impl.SMALL, "medium": impl.MEDIUM, "large": impl.LARGE}
    lockers = [impl.Locker(f"L{i}", catalog[name]) for i, name in enumerate(sizes, start=1)]
    clock = clock or FakeClock()
    kwargs.setdefault("code_factory", codes())
    kwargs.setdefault("ttl", timedelta(days=3))
    return impl.LockerLocation("site-1", lockers, clock, **kwargs), clock


# ---- 第 1 关：分配与取件码 -------------------------------------------------------


def test_deposit_picks_the_smallest_fitting_locker():
    site, _ = make_site()
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    assert grant.locker_id == "L1"
    assert site.state_of("L1") is impl.LockerState.OCCUPIED


def test_small_package_falls_back_to_a_bigger_locker_when_small_ones_are_full():
    site, _ = make_site(sizes=("small", "medium", "large"))
    site.deposit(impl.Package("P1", impl.SMALL))          # 占掉唯一的小柜
    grant = site.deposit(impl.Package("P2", impl.SMALL))  # 只能退而求其次
    assert grant.locker_id == "L2"
    # 但绝不会先拿最大的那个：中号能装下就不动大号。
    assert site.state_of("L3") is impl.LockerState.FREE


def test_large_package_never_fits_a_small_locker():
    site, _ = make_site(sizes=("small", "small"))
    with pytest.raises(impl.NoLockerAvailableError):
        site.deposit(impl.Package("P1", impl.LARGE))
    assert site.free_count() == 2  # 失败不吃掉任何柜格


def test_every_deposit_gets_its_own_code_and_the_index_grows():
    site, _ = make_site()
    g1 = site.deposit(impl.Package("P1", impl.SMALL))
    g2 = site.deposit(impl.Package("P2", impl.SMALL))
    assert g1.code != g2.code
    assert site.code_count == 2


# ---- 第 2 关：取件、错码、过期 ---------------------------------------------------


def test_collect_returns_the_package_frees_the_locker_and_burns_the_code():
    site, _ = make_site()
    package = impl.Package("P1", impl.SMALL)
    grant = site.deposit(package)
    assert site.collect(grant.code) is package
    assert package.status is impl.PackageStatus.COLLECTED
    assert site.state_of(grant.locker_id) is impl.LockerState.FREE
    assert site.code_count == 0          # 码表必须缩：用过的码立刻消失
    assert site.free_count(impl.SMALL) == 4


def test_a_code_works_exactly_once():
    site, _ = make_site()
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    site.collect(grant.code)
    with pytest.raises(impl.UnknownCodeError):
        site.collect(grant.code)


def test_a_wrong_code_changes_nothing():
    site, _ = make_site()
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    with pytest.raises(impl.UnknownCodeError):
        site.collect("CODE-9999")
    assert site.code_count == 1
    assert site.state_of(grant.locker_id) is impl.LockerState.OCCUPIED


def test_repeated_wrong_codes_lock_the_terminal_then_it_recovers():
    site, clock = make_site(max_failed_attempts=3, lockout=timedelta(minutes=10))
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    for _ in range(3):
        with pytest.raises(impl.UnknownCodeError):
            site.collect("NOPE")
    # 封锁的是这台柜机，不是这个包裹：正确的码在冷却期内也开不了门。
    with pytest.raises(impl.TerminalLockedError):
        site.collect(grant.code)
    clock.advance(minutes=11)
    assert site.collect(grant.code).package_id == "P1"


def test_a_correct_code_resets_the_failure_counter():
    site, _ = make_site(max_failed_attempts=3)
    first = site.deposit(impl.Package("P1", impl.SMALL))
    second = site.deposit(impl.Package("P2", impl.SMALL))
    for _ in range(2):
        with pytest.raises(impl.UnknownCodeError):
            site.collect("NOPE")
    site.collect(first.code)                       # 成功一次，计数清零
    for _ in range(2):
        with pytest.raises(impl.UnknownCodeError):
            site.collect("NOPE")
    assert site.collect(second.code).package_id == "P2"


def test_expiry_frees_the_locker_and_flags_the_package_for_return():
    site, clock = make_site(ttl=timedelta(days=3))
    package = impl.Package("P1", impl.SMALL)
    site.deposit(package)
    clock.advance(days=4)
    events = site.expire_due()
    assert [e.subject for e in events] == ["P1"]
    assert package.status is impl.PackageStatus.RETURN_TO_SENDER
    assert site.free_count() == 4
    assert site.code_count == 0
    assert site.pending_expiry_count == 0     # 到期堆也必须缩回去


def test_sweep_discards_stale_heap_entries_of_collected_codes():
    site, clock = make_site(ttl=timedelta(days=3))
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    site.collect(grant.code)
    assert site.pending_expiry_count == 1     # 惰性删除：条目还躺在堆里
    clock.advance(days=4)
    assert site.expire_due() == ()            # 不会把已取走的包裹再"回收"一次
    assert site.pending_expiry_count == 0     # 但弹出时必须被丢掉


def test_an_expired_code_presented_at_the_keypad_expires_it_on_the_spot():
    site, clock = make_site(ttl=timedelta(days=3), max_failed_attempts=2)
    package = impl.Package("P1", impl.SMALL)
    grant = site.deposit(package)
    clock.advance(days=4)
    with pytest.raises(impl.ExpiredCodeError):
        site.collect(grant.code)              # 还没扫过，键盘上这一次就要把状态收干净
    assert package.status is impl.PackageStatus.RETURN_TO_SENDER
    assert site.code_count == 0
    # 迟到的本人不是攻击者：过期不计入失败计数，键盘没有被封。
    with pytest.raises(impl.UnknownCodeError):
        site.collect("NOPE")
    assert site.free_count() == 4


def test_a_dropoff_code_cannot_be_used_to_collect_and_survives_the_attempt():
    site, _ = make_site()
    grant = site.reserve_return("RET-1", impl.SMALL)
    with pytest.raises(impl.WrongPurposeError):
        site.collect(grant.code)
    assert site.code_count == 1               # 码是真的，不能因为用错门就作废


# ---- 第 3 关：多网点与并发 -------------------------------------------------------


def test_network_skips_a_full_location_and_deposits_at_the_next_nearest():
    near = impl.LockerLocation("near", [impl.Locker("N1", impl.SMALL)], FakeClock(),
                               position=(0.0, 0.0), code_factory=codes())
    far = impl.LockerLocation("far", [impl.Locker("F1", impl.SMALL)], FakeClock(),
                              position=(10.0, 0.0), code_factory=codes())
    network = impl.LockerNetwork([near, far])
    assert network.nearest_with_space((1.0, 0.0), impl.SMALL).location_id == "near"
    first, _ = network.deposit_nearest((1.0, 0.0), impl.Package("P1", impl.SMALL))
    second, _ = network.deposit_nearest((1.0, 0.0), impl.Package("P2", impl.SMALL))
    assert (first, second) == ("near", "far")
    with pytest.raises(impl.NoLockerAvailableError):
        network.deposit_nearest((1.0, 0.0), impl.Package("P3", impl.SMALL))


def test_concurrent_couriers_never_share_a_locker():
    site, _ = make_site(sizes=("small",) * 5)
    barrier = threading.Barrier(12)
    granted: list = []
    rejected = []
    guard = threading.Lock()

    def courier(index: int) -> None:
        barrier.wait()
        try:
            grant = site.deposit(impl.Package(f"P{index}", impl.SMALL))
        except impl.NoLockerAvailableError:
            with guard:
                rejected.append(index)
        else:
            with guard:
                granted.append(grant)

    threads = [threading.Thread(target=courier, args=(i,)) for i in range(12)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(granted) == 5 and len(rejected) == 7
    assert len({g.locker_id for g in granted}) == 5     # 没有两个包裹进同一个柜格
    assert len({g.code for g in granted}) == 5
    assert site.free_count() == 0 and site.code_count == 5


# ---- 第 4 关：逆向流程与新尺寸 ---------------------------------------------------


def test_return_flow_reuses_the_same_locker_and_code_machinery():
    site, _ = make_site()
    drop = site.reserve_return("RET-1", impl.SMALL)
    assert drop.purpose is impl.GrantPurpose.DROP_OFF
    assert site.state_of(drop.locker_id) is impl.LockerState.RESERVED
    assert site.free_count(impl.SMALL) == 3            # 预留的柜格已经离开可用池

    parcel = impl.Package("RET-1-BOX", impl.SMALL)
    pickup = site.drop_off(drop.code, parcel)
    assert pickup.purpose is impl.GrantPurpose.COLLECT
    assert site.state_of(drop.locker_id) is impl.LockerState.OCCUPIED
    assert site.code_count == 1                        # 投件码作废，取件码顶上
    assert site.collect(pickup.code) is parcel


def test_an_unused_reservation_expires_and_returns_an_empty_locker():
    site, clock = make_site(ttl=timedelta(days=1))
    drop = site.reserve_return("RET-1", impl.SMALL)
    clock.advance(days=2)
    events = site.expire_due()
    assert [e.subject for e in events] == ["RET-1"]
    assert site.state_of(drop.locker_id) is impl.LockerState.FREE
    assert site.free_count() == 4


def test_a_brand_new_size_needs_no_change_to_the_allocator():
    site, _ = make_site(sizes=("small",))
    oversize = impl.Size("xl", 100, 120, 80)
    site.add_locker(impl.Locker("X1", oversize))
    grant = site.deposit(impl.Package("P1", oversize))
    assert grant.locker_id == "X1"
    # 而小包裹仍然优先拿小柜，新尺寸没有打乱"最小可容纳优先"。
    assert site.deposit(impl.Package("P2", impl.SMALL)).locker_id == "L1"


def test_events_describe_what_happened_and_never_carry_the_code():
    site, clock = make_site(ttl=timedelta(days=1))
    seen: list = []
    site.subscribe(seen.append)
    grant = site.deposit(impl.Package("P1", impl.SMALL))
    clock.advance(days=2)
    site.expire_due()
    kinds = [e.kind for e in seen]
    assert kinds == [impl.EventKind.DEPOSITED, impl.EventKind.EXPIRED]
    assert all(grant.code not in (e.subject, e.locker_id) for e in seen)
    assert seen[-1].at == clock.now and seen[-1].location_id == "site-1"


def test_a_return_that_does_not_fit_does_not_burn_the_drop_off_code():
    """回归：动作失败时不能顺手把码作废——顾客还得用它去开别的柜子。"""
    site, _ = make_site(sizes=("small", "large"))
    drop = site.reserve_return("RET-1", impl.SMALL)
    with pytest.raises(impl.LockerStateError):
        site.drop_off(drop.code, impl.Package("OOPS", impl.LARGE))
    assert site.code_count == 1
    assert site.state_of(drop.locker_id) is impl.LockerState.RESERVED
    assert site.drop_off(drop.code, impl.Package("RET-1-BOX", impl.SMALL)).purpose \
        is impl.GrantPurpose.COLLECT


def test_a_locker_is_given_back_when_no_unique_code_can_be_issued():
    """回归：发码失败时柜格必须回到可用池，否则它永远占着而且没有码能打开它。"""
    site, _ = make_site(sizes=("small", "small"), code_factory=lambda: "SAME")
    site.deposit(impl.Package("P1", impl.SMALL))
    with pytest.raises(impl.LockerError):
        site.deposit(impl.Package("P2", impl.SMALL))
    assert site.free_count() == 1
    assert site.code_count == 1


def test_a_locker_refuses_to_swallow_a_second_package():
    locker = impl.Locker("L1", impl.MEDIUM)
    locker.store(impl.Package("P1", impl.SMALL))
    with pytest.raises(impl.LockerStateError):
        locker.store(impl.Package("P2", impl.SMALL))
    assert locker.release().package_id == "P1"
    assert locker.state is impl.LockerState.FREE
