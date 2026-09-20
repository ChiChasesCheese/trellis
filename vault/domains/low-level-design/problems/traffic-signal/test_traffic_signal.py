"""交通信号灯的验收测试：相位序列、两种配时方案、抢占与恢复、第 4 关的新相位，
以及一个随机演练的性质测试——几千个 tick 里冲突不变式一次都不许破，也不许有流向被饿死。

全程没有 `sleep`、没有真实时间：时钟注入，随机数固定种子，所以每一次失败都能原样复现。
"""

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

from datetime import datetime, timedelta  # noqa: E402

START = datetime(2026, 4, 1, 8, 0)


class FakeClock:
    """每被读一次就前进两秒；时间只用于时间戳，不参与任何判断。"""

    def __init__(self):
        self.now = START

    def __call__(self):
        self.now = self.now + timedelta(seconds=2)
        return self.now


def make(plan=None, **kwargs):
    junction, ring = impl.four_way_intersection()
    kwargs.setdefault("clearance_ticks", 2)
    kwargs.setdefault("all_red_ticks", 1)
    plan = plan or impl.FixedTimePlan(default=4)
    return impl.SignalController(junction, ring, plan, FakeClock(), **kwargs), junction


def permissive(report):
    return {m.name for m, a in report.aspects.items() if a.permissive}


# ---- 第 1 关：相位序列与安全不变式 -----------------------------------------------


def test_the_first_phase_is_green_and_the_conflicting_one_is_red():
    controller, _ = make()
    assert controller.current_phase.name == "north-south"
    assert controller.aspect_of(impl.NORTH) is impl.Aspect.GREEN
    assert controller.aspect_of(impl.EAST) is impl.Aspect.RED
    assert controller.conflicting_permissive() == ()


def test_a_phase_change_goes_green_then_clearance_then_all_red_then_the_next_green():
    controller, _ = make(plan=impl.FixedTimePlan(default=4))
    stages = [r.stage for r in controller.run(7)]
    assert stages == [impl.Stage.GREEN] * 3 + [impl.Stage.CLEARANCE] * 2 + \
        [impl.Stage.ALL_RED, impl.Stage.GREEN]
    assert controller.current_phase.name == "east-west"
    assert controller.aspect_of(impl.EAST) is impl.Aspect.GREEN


def test_nothing_is_permissive_during_clearance_or_all_red():
    controller, _ = make(plan=impl.FixedTimePlan(default=4))
    reports = controller.run(7)
    for report in reports:
        if report.stage is not impl.Stage.GREEN:
            assert permissive(report) == set()
    # 两个方向的绿之间隔着 3 个 tick 谁都不许走——这就是相位间隔。
    assert [r.stage for r in reports].count(impl.Stage.GREEN) == 4


def test_conflicting_approaches_are_never_green_together_over_many_cycles():
    controller, junction = make(plan=impl.FixedTimePlan(default=6))
    for report in controller.run(200):
        live = permissive(report)
        assert not ({"north", "south"} & live and {"east", "west"} & live)
        assert controller.conflicting_permissive() == ()


def test_aspects_is_a_snapshot_not_a_live_view():
    controller, _ = make(plan=impl.FixedTimePlan(default=4))
    before = controller.aspects
    controller.run(7)
    assert before[impl.NORTH] is impl.Aspect.GREEN     # 快照没被后来的切换改写
    assert controller.aspect_of(impl.NORTH) is impl.Aspect.RED


# ---- 第 2 关：可换的配时方案 -----------------------------------------------------


def test_fixed_time_green_lasts_exactly_as_configured_regardless_of_traffic():
    controller, _ = make(plan=impl.FixedTimePlan({"north-south": 7}, default=3))
    controller.report_arrival(impl.NORTH, 50)          # 车再多也不延长
    stages = [r.stage for r in controller.run(8)]
    # 绿灯从第 0 个 tick（构造完成的那一刻）就亮着，所以配置的 7 个 tick 里只有 6 个由 step 报告。
    assert stages[:6] == [impl.Stage.GREEN] * 6
    assert stages[6] is impl.Stage.CLEARANCE


def test_actuated_gaps_out_right_after_the_minimum_green_when_nobody_arrives():
    controller, _ = make(plan=impl.ActuatedPlan(gap=2))
    stages = [r.stage for r in controller.run(6)]
    # 最短绿 4 个 tick（含构造时那一刻）一走完、又没有新到达，立刻断流切相位。
    assert stages[:3] == [impl.Stage.GREEN] * 3
    assert stages[3] is impl.Stage.CLEARANCE


def test_actuated_extends_the_green_while_cars_keep_arriving_but_never_past_the_maximum():
    controller, _ = make(plan=impl.ActuatedPlan(gap=2))
    stages = []
    for _ in range(20):
        controller.report_arrival(impl.NORTH, 2)       # 每个 tick 都有新车
        stages.append(controller.step().stage)
    # 最长绿 12：延长得再久也必须让路，否则东西向永远等不到。
    assert stages[:11] == [impl.Stage.GREEN] * 11
    assert stages[11] is impl.Stage.CLEARANCE


def test_the_two_plans_disagree_on_the_same_demand():
    fixed, _ = make(plan=impl.FixedTimePlan(default=10))
    actuated, _ = make(plan=impl.ActuatedPlan(gap=2))
    fixed_green = [r.stage for r in fixed.run(12)].count(impl.Stage.GREEN)
    actuated_green = [r.stage for r in actuated.run(12)].count(impl.Stage.GREEN)
    # 没有任何到达时，定周期照样放满 10 个 tick，感应式最短绿一到就走。
    assert fixed_green > actuated_green


def test_queues_drain_while_green_and_the_queue_table_shrinks_to_nothing():
    controller, _ = make(plan=impl.FixedTimePlan(default=8))
    controller.report_arrival(impl.NORTH, 5)
    controller.report_arrival(impl.SOUTH, 1)
    assert controller.queue_count == 2
    controller.run(6)
    assert controller.waiting(impl.NORTH) == 0
    assert controller.queue_count == 0          # 排空的流向必须离开排队表


# ---- 第 3 关：紧急车辆抢占 -------------------------------------------------------


def test_preemption_still_passes_through_clearance_and_all_red():
    controller, _ = make(plan=impl.FixedTimePlan(default=30), max_preempt_ticks=30)
    controller.request_preemption(impl.EAST)
    reports = controller.run(8)
    stages = [r.stage for r in reports]
    # 最短绿 4 走完才让路，然后照常黄 2 + 全红 1，绝不直接从南北绿跳到东西绿。
    assert stages == [impl.Stage.GREEN] * 3 + [impl.Stage.CLEARANCE] * 2 + \
        [impl.Stage.ALL_RED, impl.Stage.GREEN, impl.Stage.GREEN]
    assert impl.Stage.ALL_RED in stages
    assert controller.aspect_of(impl.EAST) is impl.Aspect.GREEN
    assert all(r.preempted_for is impl.EAST for r in reports)


def test_preemption_on_the_current_phase_holds_the_green_until_the_cap():
    controller, _ = make(plan=impl.FixedTimePlan(default=4), max_preempt_ticks=8)
    controller.request_preemption(impl.NORTH)
    stages = [r.stage for r in controller.run(9)]
    assert stages[:8] == [impl.Stage.GREEN] * 8     # 定周期方案只给 4，抢占把它按住
    assert stages[8] is impl.Stage.CLEARANCE        # 上限一到，立刻回到方案
    assert controller.preempted_for is None


def test_after_the_emergency_the_controller_resumes_its_ring():
    controller, _ = make(plan=impl.FixedTimePlan(default=4), max_preempt_ticks=30)
    controller.request_preemption(impl.EAST)
    controller.run(7)
    assert controller.current_phase.name == "east-west"
    controller.release_preemption()
    controller.run(7)
    # 恢复的方式是从被抢占的相位继续环，而不是跳回被打断的那一个。
    assert controller.current_phase.name == "north-south"
    assert controller.preempted_for is None


def test_preemption_for_a_movement_no_phase_serves_is_refused():
    controller, _ = make()
    with pytest.raises(impl.UnknownMovementError):
        controller.request_preemption(impl.Movement("bike-lane"))


# ---- 第 4 关：新相位不许动引擎 ---------------------------------------------------


def test_a_pedestrian_phase_is_just_another_movement():
    ped = impl.Movement("ped-ns", impl.MovementKind.PEDESTRIAN)
    movements = (impl.NORTH, impl.SOUTH, impl.EAST, impl.WEST, ped)
    conflicts = [(ns, ew) for ns in (impl.NORTH, impl.SOUTH) for ew in (impl.EAST, impl.WEST)]
    conflicts += [(ped, impl.NORTH), (ped, impl.SOUTH)]   # 人行横道横穿南北车道
    junction = impl.Intersection("x", movements, conflicts)
    phases = (impl.Phase("north-south", frozenset({impl.NORTH, impl.SOUTH})),
              impl.Phase("east-west", frozenset({impl.EAST, impl.WEST, ped})))
    controller = impl.SignalController(junction, phases, impl.FixedTimePlan(default=4),
                                       FakeClock(), clearance_ticks=2, all_red_ticks=1)
    seen = []
    for report in controller.run(14):
        seen.append(report.aspects[ped])
        assert controller.conflicting_permissive() == ()
    # 走 / 闪烁禁止通行 / 禁止通行 三段，和机动车的绿黄红走的是同一套引擎。
    assert impl.Aspect.WALK in seen
    assert impl.Aspect.FLASHING_DONT_WALK in seen
    assert impl.Aspect.DONT_WALK in seen


def test_a_protected_left_turn_arrow_is_a_new_phase_and_nothing_else():
    left = impl.Movement("north-left")
    movements = (impl.NORTH, impl.SOUTH, impl.EAST, impl.WEST, left)
    conflicts = [(ns, ew) for ns in (impl.NORTH, impl.SOUTH) for ew in (impl.EAST, impl.WEST)]
    conflicts += [(left, impl.SOUTH), (left, impl.EAST), (left, impl.WEST)]
    junction = impl.Intersection("x", movements, conflicts)
    phases = (impl.Phase("north-left", frozenset({impl.NORTH, left}), min_green=2, max_green=6),
              impl.Phase("north-south", frozenset({impl.NORTH, impl.SOUTH})),
              impl.Phase("east-west", frozenset({impl.EAST, impl.WEST})))
    controller = impl.SignalController(junction, phases, impl.FixedTimePlan(default=4),
                                       FakeClock(), clearance_ticks=2, all_red_ticks=1)
    names = []
    for report in controller.run(30):
        assert controller.conflicting_permissive() == ()
        if report.changed and report.stage is impl.Stage.GREEN:
            names.append(report.phase_name)
    assert names[:3] == ["north-south", "east-west", "north-left"]


def test_a_phase_that_mixes_conflicting_movements_is_rejected_at_build_time():
    junction, _ = impl.four_way_intersection()
    bad = impl.Phase("everything", frozenset({impl.NORTH, impl.EAST}))
    with pytest.raises(impl.ConflictingPhaseError):
        junction.validate_phase(bad)
    with pytest.raises(impl.ConflictingPhaseError):
        impl.SignalController(junction, [bad], impl.FixedTimePlan(), FakeClock())


def test_an_unknown_movement_is_refused():
    controller, _ = make()
    with pytest.raises(impl.UnknownMovementError):
        controller.report_arrival(impl.Movement("tram"))


# ---- 抢占叠加 -------------------------------------------------------------------


def test_a_second_preemption_during_the_first_ones_clearance_still_pays_the_intergreen():
    """第一辆紧急车还在清空途中，第二辆从另一个方向来了：谁先走都行，间隔一次都不许省。"""
    controller, _ = make(plan=impl.FixedTimePlan(default=6), max_preempt_ticks=6)
    controller.request_preemption(impl.EAST)
    first = list(controller.run(4))
    assert first[-1].stage is impl.Stage.CLEARANCE      # 正在为东西向清空
    controller.request_preemption(impl.NORTH)           # 清空途中改要南北
    reports = first + list(controller.run(20))

    stages = [r.stage for r in reports]
    for before, after in zip(stages, stages[1:]):
        # 清空之后只能是清空或全红，绝不能直接跳到下一个绿。
        assert not (before is impl.Stage.CLEARANCE and after is impl.Stage.GREEN)
    assert controller.conflicting_permissive() == ()

    # 只看第二次请求之后的放行：两股车流最终都被服务，而后来的那次抢占先走——
    # 控制器在切相位的那一刻看的是手上最新的需求，不是先到先得的队列。
    served = {}
    for report in reports:
        if report.tick <= 4:
            continue                                    # 第二次请求之前的绿不算数
        for movement, aspect in report.aspects.items():
            if aspect.permissive:
                served.setdefault(movement.name, report.tick)
    assert {"north", "east"} <= served.keys()
    assert served["north"] < served["east"]
    assert served["north"] > 4 and controller.preempted_for is None


# ---- 性质测试：随机演练下不变式与公平性 ------------------------------------------


def starvation_bound(phases, *, clearance_ticks, all_red_ticks, max_preempt_ticks):
    """从控制器自己的参数推出「一个流向最多等多少个 tick 才会再次拿到放行」。

    `intergreen = clearance + all_red`：每一段绿灯之后必付的相位间隔。
    `normal_slot = max_green + intergreen`：计划驱动下一个相位最多占多久。
    `preempt_slot = max_green + cap + intergreen`：被抢占按住的相位最多占多久——绿灯可以先
        按计划走满最长绿，再被抢占多按 `cap` 个 tick。
    `len(phases) - 1` 个普通相位：`_next_index` 在没有抢占时只沿环**向前**走，所以两次轮到
        同一个相位之间，其余每个相位最多各插进一次。
    额外的一个 `preempt_slot`：抢占会**改写**下一个相位的选择，它既可能跳过若干相位，也可能
        把当前相位再点一次（请求落在清空段时就会这样），所以要为它单独留出一个相位区间。
    末尾 `+ 1`：等待是从上一次放行的那一 tick 数起的。

    前提是一个等待窗口里最多发生一次抢占；演练靠 `cooldown = bound + 1` 的请求冷却保证——
    两次抢占之间至少隔着一整个上界，因此不可能双双落进同一个窗口。
    """
    intergreen = clearance_ticks + all_red_ticks
    longest_green = max(phase.max_green for phase in phases)
    normal_slot = longest_green + intergreen
    preempt_slot = longest_green + max_preempt_ticks + intergreen
    return intergreen + (len(phases) - 1) * normal_slot + preempt_slot + 1


def test_random_demand_never_breaks_safety_and_never_starves_an_approach():
    """二十四个种子、每个 600 个 tick 的随机演练：冲突不变式一次不破，等待不超过推导出的上界。

    上界由 `starvation_bound` 从控制器参数算出，不是跑一遍观察到的经验值——经验值换个种子
    就会翻车，而且它回答不了「你凭什么说它永远不会饿死」这个真正被考的问题。
    """
    junction, ring = impl.four_way_intersection()
    clearance, all_red, cap = 2, 1, 10
    bound = starvation_bound(ring, clearance_ticks=clearance, all_red_ticks=all_red,
                             max_preempt_ticks=cap)
    cooldown = bound + 1          # 两次抢占之间至少隔一个上界，保证窗口里最多一次
    worst_overall = 0

    for seed in range(24):
        rng = random.Random(20260920 + seed)
        controller = impl.SignalController(junction, ring, impl.ActuatedPlan(gap=2), FakeClock(),
                                           clearance_ticks=clearance, all_red_ticks=all_red,
                                           max_preempt_ticks=cap)
        last_go = {movement: 0 for movement in junction.movements}
        released_at = -cooldown
        preemptions = 0
        for tick in range(1, 601):
            for movement in junction.movements:
                if rng.random() < 0.25:
                    controller.report_arrival(movement, rng.randint(1, 3))
            if controller.preempted_for is None:
                if tick - released_at >= cooldown and rng.random() < 0.08:
                    controller.request_preemption(rng.choice(junction.movements))
                    preemptions += 1
            elif rng.random() < 0.25:
                controller.release_preemption()
                released_at = tick
            active = controller.preempted_for is not None
            report = controller.step()
            if active and controller.preempted_for is None:
                released_at = tick    # 达到上限自动释放，和手动释放一样要开始冷却
            assert controller.conflicting_permissive() == ()
            for movement, aspect in report.aspects.items():
                if aspect.permissive:
                    last_go[movement] = tick
            worst = max(tick - seen for seen in last_go.values())
            assert worst <= bound, (
                f"seed {seed}, tick {tick}: {worst} ticks without green, derived bound is {bound}")
            worst_overall = max(worst_overall, worst)
        assert preemptions > 0        # 这一轮真的演练过抢占，不是空转

    assert worst_overall <= bound
    # 上界不能宽松到毫无意义：实际最坏等待要落在它的一半以上。
    assert worst_overall * 2 >= bound
