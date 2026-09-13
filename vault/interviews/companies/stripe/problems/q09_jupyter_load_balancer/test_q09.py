import random

import pytest

EX1 = ["CONNECT c1 u1", "CONNECT c2 u2", "CONNECT c3 u3", "CONNECT c4 u4", "DISCONNECT c2",
       "CONNECT c5 u5", "DISCONNECT nope", "CONNECT c6 u6"]
EX1_OUT = ["c1,u1,1", "c2,u2,2", "c3,u3,3", "c4,u4,1", "c5,u5,2", "c6,u6,2"]

EX2 = ["CONNECT c1 u1 nb1", "CONNECT c2 u2", "CONNECT c3 u3 nb1", "CONNECT c4 u4 nb1",
       "CONNECT c5 u5", "CONNECT c6 u6", "DISCONNECT c2", "CONNECT c7 u7 nb1", "CONNECT c8 u8"]
EX2_OUT = ["c1,u1,1", "c2,u2,2", "c3,u3,1", "c5,u5,2", "c8,u8,2"]

EX3 = ["CONNECT c1 u1 nbA", "CONNECT c2 u2", "CONNECT c3 u3 nbA", "CONNECT c4 u4", "SHUTDOWN 1",
       "CONNECT c5 u5", "CONNECT c6 u6 nbA", "DISCONNECT c1", "CONNECT c7 u7 nbA"]
EX3_OUT = ["c1,u1,1", "c2,u2,2", "c3,u3,1", "c4,u4,3", "c1,u1,2", "c5,u5,1", "c7,u7,2"]
EX3_PERMANENT_OUT = ["c1,u1,1", "c2,u2,2", "c3,u3,1", "c4,u4,3", "c1,u1,2", "c5,u5,3", "c7,u7,2"]


def route(impl, n, cap, reqs, **kw):
    return impl.route_requests(n, cap, reqs, **kw)


# ---------------------------------------------------------------- Part 1: least loaded
@pytest.mark.part1
def test_example1_least_loaded_and_disconnect(impl):
    assert route(impl, 3, 10, EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.fmt
def test_one_based_index_and_tie_smallest(impl):
    out = route(impl, 12, 5, [f"CONNECT c{i} u{i}" for i in range(1, 13)] + ["CONNECT c13 u13"])
    assert out[9] == "c10,u10,10" and out[11] == "c12,u12,12" and out[12] == "c13,u13,1"


@pytest.mark.part1
@pytest.mark.edge
def test_single_target_and_empty_requests(impl):
    assert route(impl, 1, 3, ["CONNECT a u", "CONNECT b u"]) == ["a,u,1", "b,u,1"]
    assert route(impl, 5, 5, []) == []
    assert route(impl, 3, 3, ["", "   "]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_active_connect_id_ignored(impl):
    out = route(impl, 2, 10, ["CONNECT c1 u1", "CONNECT c1 u9", "CONNECT c2 u2"])
    assert out == ["c1,u1,1", "c2,u2,2"]  # c2 goes to 2, so the duplicate did not add load to 1


@pytest.mark.part1
def test_whitespace_noise(impl):
    assert route(impl, 2, 2, ["  CONNECT   c1   u1  "]) == ["c1,u1,1"]


# ---------------------------------------------------------------- Part 2: DISCONNECT
@pytest.mark.part2
def test_disconnect_frees_slot_and_unknown_ignored(impl):
    out = route(impl, 2, 10, ["CONNECT a u", "CONNECT b u", "DISCONNECT a", "DISCONNECT zzz",
                              "DISCONNECT a", "CONNECT c u"])
    assert out == ["a,u,1", "b,u,2", "c,u,1"]


@pytest.mark.part2
@pytest.mark.edge
def test_id_reusable_after_disconnect(impl):
    out = route(impl, 2, 10, ["CONNECT a u", "CONNECT b u", "DISCONNECT a", "CONNECT a u2"])
    assert out == ["a,u,1", "b,u,2", "a,u2,1"]


@pytest.mark.part2
@pytest.mark.edge
def test_many_disconnects_change_least_loaded(impl):
    reqs = [f"CONNECT c{i} u" for i in range(6)] + ["DISCONNECT c2", "DISCONNECT c5", "CONNECT x u"]
    # loads after: t1=2, t2=2, t3=0 -> x to 3
    assert route(impl, 3, 10, reqs)[-1] == "x,u,3"


# ---------------------------------------------------------------- Part 3: affinity
@pytest.mark.part3
def test_sticky_beats_load(impl):
    out = route(impl, 3, 10, ["CONNECT a u nb", "CONNECT b u nb", "CONNECT c u nb", "CONNECT d u"])
    assert out == ["a,u,1", "b,u,1", "c,u,1", "d,u,2"]


@pytest.mark.part3
@pytest.mark.edge
def test_pin_survives_disconnect(impl):
    out = route(impl, 2, 10, ["CONNECT a u nb", "DISCONNECT a", "CONNECT b u", "CONNECT c u nb"])
    assert out == ["a,u,1", "b,u,1", "c,u,1"]  # c still pinned to 1 although 2 is emptier


@pytest.mark.part3
def test_distinct_objects_spread(impl):
    out = route(impl, 2, 10, ["CONNECT a u o1", "CONNECT b u o2", "CONNECT c u o2", "CONNECT d u o1"])
    assert out == ["a,u,1", "b,u,2", "c,u,2", "d,u,1"]


# ---------------------------------------------------------------- Part 4: capacity
@pytest.mark.part4
def test_example2_sticky_and_capacity(impl):
    assert route(impl, 2, 2, EX2) == EX2_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_capacity_boundary(impl):
    reqs = [f"CONNECT c{i} u" for i in range(7)]
    out = route(impl, 2, 3, reqs)
    assert len(out) == 6 and out[-1] == "c5,u,2"          # 7th rejected, no log
    assert route(impl, 3, 0, ["CONNECT a u"]) == []          # cap 0 rejects everything
    assert route(impl, 1, 1, ["CONNECT a u", "CONNECT b u", "DISCONNECT a", "CONNECT b u"]) == ["a,u,1", "b,u,1"]


@pytest.mark.part4
@pytest.mark.edge
def test_rejected_connect_is_not_active(impl):
    out = route(impl, 1, 1, ["CONNECT a u", "CONNECT b u", "DISCONNECT b", "CONNECT c u", "DISCONNECT a", "CONNECT c u"])
    assert out == ["a,u,1", "c,u,1"]  # b was never active, so DISCONNECT b frees nothing


# ---------------------------------------------------------------- Part 5: SHUTDOWN
@pytest.mark.part5
def test_example3_shutdown(impl):
    assert route(impl, 3, 2, EX3) == EX3_OUT


@pytest.mark.part5
def test_example3_permanent_variant(impl):
    assert route(impl, 3, 2, EX3, shutdown_permanent=True) == EX3_PERMANENT_OUT


@pytest.mark.part5
@pytest.mark.edge
def test_reroute_in_arrival_order_and_target_returns_empty(impl):
    reqs = ["CONNECT a u", "CONNECT b u", "CONNECT c u", "CONNECT d u", "SHUTDOWN 1", "CONNECT e u"]
    # t1: a,c ; t2: b,d. Shutdown 1 -> a,c re-routed to 2 (only target) in order; t1 back at 0 -> e to 1
    assert route(impl, 2, 10, reqs) == ["a,u,1", "b,u,2", "c,u,1", "d,u,2", "a,u,2", "c,u,2", "e,u,1"]


@pytest.mark.part5
@pytest.mark.edge
def test_shutdown_reroute_keeps_objects_together_and_drops_overflow(impl):
    reqs = ["CONNECT a u o", "CONNECT b u o", "CONNECT c u", "SHUTDOWN 1", "CONNECT d u o"]
    # cap 2: t1={a,b} t2={c}; shutdown 1: a->2 (pins o to 2, full), b dropped; d sticky to 2 full -> rejected
    assert route(impl, 2, 2, reqs) == ["a,u,1", "b,u,1", "c,u,2", "a,u,2"]


@pytest.mark.part5
@pytest.mark.edge
def test_shutdown_noops_and_repeat(impl):
    reqs = ["SHUTDOWN 9", "SHUTDOWN 0", "SHUTDOWN 2", "CONNECT a u", "SHUTDOWN 1", "SHUTDOWN 1", "CONNECT b u"]
    # a on 1; shutdown 1 -> a to 2; second shutdown 1 is empty -> no-op; b -> 1 (load 0)
    assert route(impl, 2, 10, reqs) == ["a,u,1", "a,u,2", "b,u,1"]
    # permanent: target 2 is gone from the start, so a is dropped at SHUTDOWN 1 and b has no target
    assert route(impl, 2, 10, reqs, shutdown_permanent=True) == ["a,u,1"]
    # permanent, second SHUTDOWN of a removed target is a no-op; b lands on the survivor
    assert route(impl, 2, 10, reqs[:2] + reqs[3:], shutdown_permanent=True) == ["a,u,1", "a,u,2", "b,u,2"]


@pytest.mark.part5
@pytest.mark.edge
def test_permanent_shutdown_all_gone_rejects(impl):
    assert route(impl, 1, 5, ["CONNECT a u", "SHUTDOWN 1", "CONNECT b u"], shutdown_permanent=True) == ["a,u,1"]


@pytest.mark.part5
@pytest.mark.fmt
def test_variant_b_format(impl):
    reqs = ["CONNECT c1 objA", "CONNECT c2 objB", "CONNECT c3 objA", "SHUTDOWN 1"]
    assert route(impl, 2, 5, reqs, variant_b=True) == ["c1 1", "c2 2", "c3 1", "c1 2", "c3 2"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part5
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("3 2\n" + "\n".join(EX3) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX3_OUT) + "\n"


@pytest.mark.part5
@pytest.mark.io
def test_empty_and_header_only_stdin(run_script):
    assert run_script("").stdout == ""
    assert run_script("3 3\n").stdout == ""


@pytest.mark.part5
@pytest.mark.perf
def test_perf_1e5_targets_2e5_requests(run_script):
    rng = random.Random(0)
    n, cap = 100_000, 3
    reqs, active = [], []
    for i in range(200_000):
        r = rng.random()
        if r < 0.65 or not active:
            obj = f" nb{rng.randrange(20_000)}" if rng.random() < 0.3 else ""
            reqs.append(f"CONNECT c{i} u{rng.randrange(5000)}{obj}")
            active.append(f"c{i}")
        elif r < 0.9:
            reqs.append(f"DISCONNECT {active.pop(rng.randrange(len(active)))}")
        else:
            reqs.append(f"SHUTDOWN {rng.randrange(1, n + 1)}")
    r = run_script(f"{n} {cap}\n" + "\n".join(reqs) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
