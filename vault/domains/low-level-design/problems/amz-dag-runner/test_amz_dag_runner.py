import importlib
import os
import threading

import pytest

import buggy_runner

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def valid(order, deps):
    pos = {n: i for i, n in enumerate(order)}
    nodes = set(deps) | {d for ds in deps.values() for d in ds}
    return set(order) == nodes and len(order) == len(nodes) and all(
        pos[d] < pos[n] for n, ds in deps.items() for d in ds
    )


# ---- 第 1 关：安装顺序与环 ----

def test_dependencies_come_before_dependents():
    deps = {"app": ["web", "db"], "web": ["lib"], "db": ["lib"], "lib": []}
    assert valid(impl.install_order(deps), deps)


def test_order_is_deterministic_by_first_appearance():
    assert impl.install_order({"app": ["web", "db"], "web": ["lib"], "db": ["lib"]}) == [
        "lib", "web", "db", "app"]


def test_package_only_named_as_dependency_is_installed():
    assert impl.install_order({"a": ["b"]}) == ["b", "a"]


def test_duplicate_dependency_counts_once():
    assert impl.install_order({"a": ["b", "b"], "b": []}) == ["b", "a"]


def test_empty_and_independent_nodes():
    assert impl.install_order({}) == []
    assert impl.install_order({"x": [], "y": []}) == ["x", "y"]


def test_cycle_raises_and_names_the_cycle():
    with pytest.raises(impl.CycleError) as info:
        impl.install_order({"a": ["b"], "b": ["c"], "c": ["a"]})
    assert info.value.cycle == ("a", "b", "c")
    assert str(info.value) == "a -> b -> c -> a"


def test_cycle_report_excludes_nodes_that_merely_hang_off_it():
    deps = {"app": ["x"], "x": ["y"], "y": ["x"], "ok": []}
    with pytest.raises(impl.CycleError) as info:
        impl.install_order(deps)
    assert set(info.value.cycle) == {"x", "y"}


def test_self_dependency_is_a_cycle():
    with pytest.raises(impl.CycleError) as info:
        impl.install_order({"a": ["a"]})
    assert info.value.cycle == ("a",)


def test_input_is_not_mutated():
    deps = {"a": ["b"], "b": []}
    impl.install_order(deps)
    assert deps == {"a": ["b"], "b": []}


def test_graph_descendants():
    g = impl.Graph({"c": ["b"], "b": ["a"], "d": ["a"], "e": []})
    assert g.descendants("a") == {"b", "c", "d"}
    assert g.descendants("e") == frozenset()
    assert g.prerequisites("c") == ("b",)


# ---- 第 2 关：代码评审，三个 bug ----

BUG_INPUTS = {
    "dependency_only_node_dropped": ({"a": ["b"]}, ["b", "a"]),
    "duplicate_edge_miscounted": ({"a": ["b", "b"], "b": []}, ["b", "a"]),
}


@pytest.mark.parametrize("name", BUG_INPUTS)
def test_buggy_runner_is_wrong_on_each_bug_input(name):
    deps, expected = BUG_INPUTS[name]
    assert buggy_runner.install_order(deps) != expected
    assert impl.install_order(deps) == expected


def test_buggy_runner_swallows_a_cycle_but_the_fix_raises():
    deps = {"a": ["b"], "b": ["a"]}
    assert buggy_runner.install_order(deps) == []  # 悄悄返回空，调用方以为"没东西要装"
    with pytest.raises(impl.CycleError):
        impl.install_order(deps)


def test_buggy_runner_is_right_on_the_happy_path():
    deps = {"app": ["lib"], "lib": []}
    assert buggy_runner.install_order(deps) == ["lib", "app"]


# ---- 第 3 关：按序执行，结果传递 ----

def test_results_flow_to_dependents():
    wf = impl.Workflow()
    wf.add("load", lambda _: 10)
    wf.add("double", lambda r: r["load"] * 2, needs=["load"])
    wf.add("shift", lambda r: r["load"] + 1, needs=["load"])
    wf.add("join", lambda r: r["double"] + r["shift"], needs=["double", "shift"])
    assert wf.run() == {"load": 10, "double": 20, "shift": 11, "join": 31}


def test_steps_run_in_dependency_order_even_when_added_out_of_order():
    seen = []
    wf = impl.Workflow()
    wf.add("b", lambda r: seen.append("b"), needs=["a"])
    wf.add("a", lambda r: seen.append("a"))
    wf.run()
    assert seen == ["a", "b"]


def test_step_gets_only_its_declared_dependencies():
    got = {}
    wf = impl.Workflow()
    wf.add("a", lambda r: 1)
    wf.add("b", lambda r: 2)
    wf.add("c", lambda r: got.update(r), needs=["a"])
    wf.run()
    assert got == {"a": 1}


def test_sequential_failure_stops_and_names_the_step():
    ran = []
    wf = impl.Workflow()
    wf.add("a", lambda r: ran.append("a"))

    def boom(r):
        raise ValueError("bad")

    wf.add("b", boom, needs=["a"])
    wf.add("c", lambda r: ran.append("c"), needs=["b"])
    with pytest.raises(impl.StepError) as info:
        wf.run()
    assert info.value.step == "b" and isinstance(info.value.__cause__, ValueError)
    assert ran == ["a"]


def test_workflow_rejects_cycle_duplicate_and_unknown_step():
    wf = impl.Workflow()
    wf.add("a", lambda r: 1, needs=["b"])
    wf.add("b", lambda r: 1, needs=["a"])
    with pytest.raises(impl.CycleError):
        wf.run()
    with pytest.raises(impl.DuplicateStepError):
        wf.add("a", lambda r: 1)
    wf2 = impl.Workflow()
    wf2.add("x", lambda r: 1, needs=["ghost"])
    with pytest.raises(KeyError):
        wf2.order()


# ---- 第 4 关：并行执行与失败传播 ----

def test_independent_steps_really_run_at_the_same_time():
    barrier = threading.Barrier(3, timeout=10)  # 三个都进来才放行；串行执行会超时失败
    wf = impl.Workflow()
    for n in "abc":
        wf.add(n, lambda r, n=n: (barrier.wait(), n)[1])
    wf.add("join", lambda r: "".join(sorted(r.values())), needs=["a", "b", "c"])
    report = wf.run_parallel(max_workers=3)
    assert report.ok and report.results["join"] == "abc"


def test_parallel_results_flow_like_sequential():
    wf = impl.Workflow()
    wf.add("load", lambda _: 10)
    wf.add("double", lambda r: r["load"] * 2, needs=["load"])
    wf.add("shift", lambda r: r["load"] + 1, needs=["load"])
    wf.add("join", lambda r: r["double"] + r["shift"], needs=["double", "shift"])
    assert wf.run_parallel().results == wf.run()


def test_dependent_never_starts_before_its_prerequisite_finishes():
    release = threading.Event()
    started = []
    wf = impl.Workflow()

    def slow(r):
        release.wait(10)
        return 1

    wf.add("slow", slow)
    wf.add("after", lambda r: started.append("after"), needs=["slow"])
    wf.add("free", lambda r: release.set())  # 独立分支先完成并放行 slow
    report = wf.run_parallel(max_workers=2)
    assert report.ok and started == ["after"]


def test_failure_skips_only_descendants_and_other_branches_finish():
    def boom(r):
        raise RuntimeError("x")

    wf = impl.Workflow()
    wf.add("root", lambda r: 1)
    wf.add("bad", boom, needs=["root"])
    wf.add("child", lambda r: 2, needs=["bad"])
    wf.add("grandchild", lambda r: 3, needs=["child"])
    wf.add("good", lambda r: 4, needs=["root"])
    wf.add("good2", lambda r: r["good"] + 1, needs=["good"])
    wf.add("mixed", lambda r: 9, needs=["bad", "good2"])  # 一个依赖失败，另一个成功
    report = wf.run_parallel(max_workers=3)
    assert not report.ok
    assert set(report.failed) == {"bad"} and isinstance(report.failed["bad"], RuntimeError)
    assert report.skipped == {"child", "grandchild", "mixed"}
    assert report.results == {"root": 1, "good": 4, "good2": 5}


def test_every_step_lands_in_exactly_one_bucket():
    def boom(r):
        raise RuntimeError

    wf = impl.Workflow()
    wf.add("a", boom)
    wf.add("b", lambda r: 1, needs=["a"])
    wf.add("c", lambda r: 1)
    rep = wf.run_parallel()
    buckets = [set(rep.results), set(rep.failed), set(rep.skipped)]
    assert sorted(n for b in buckets for n in b) == ["a", "b", "c"]


def test_parallel_cycle_raises_before_running_anything():
    ran = []
    wf = impl.Workflow()
    wf.add("a", lambda r: ran.append("a"), needs=["b"])
    wf.add("b", lambda r: ran.append("b"), needs=["a"])
    with pytest.raises(impl.CycleError):
        wf.run_parallel()
    assert ran == []


def test_worker_limit_is_respected():
    lock = threading.Lock()
    active = peak = 0
    gate = threading.Barrier(2, timeout=10)

    def work(r):
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        gate.wait()  # 两个 worker 同时在场后才一起离开；第三个必须等位
        with lock:
            active -= 1

    wf = impl.Workflow()
    for n in "abcd":
        wf.add(n, work)
    assert wf.run_parallel(max_workers=2).ok
    assert peak == 2
