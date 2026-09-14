import random

import pytest

EX1 = ["REGISTER us-east-1 38 120 100", "REGISTER us-west-2 50 112 30",
       "SET_HEALTHZ us-west-2 false", "REGISTER eu-east-1 -10 15 0"]
EX1_OUT = ["OK", "OK", "OK", "ERROR"]

EX2 = ["REGISTER east 40 -74 10", "REGISTER west 34 -118 20", "SET_HEALTHZ east false", "ROUTE 41 -73"]
EX2_OUT = ["OK", "OK", "OK", "west 4000 west"]

EX3 = ["REGISTER us-east-1 0 0 1", "REGISTER ap-south-1 0 0 1", "ROUTE 0 0", "ROUTE 0 0", "ROUTE 0 0",
       "SET_HEALTHZ ap-south-1 false", "ROUTE 0 0", "RELEASE us-east-1", "ROUTE 0 0"]
EX3_OUT = ["OK", "OK", "ap-south-1 0 ap-south-1 us-east-1", "us-east-1 0 ap-south-1 us-east-1",
           "NONE 0 ap-south-1 us-east-1", "OK", "NONE 0 us-east-1", "OK", "us-east-1 0 us-east-1"]

EX4 = ["DISTANCE 0 0 0 0", "DISTANCE 0 0 0 180", "DISTANCE 0 0 1 0", "DISTANCE 0 0 0 90", "DISTANCE 38 120 50 112"]
EX4_OUT = ["0", "20015", "111", "10008", "1478"]


def run(impl, lines, **kw):
    return impl.process_commands(lines, **kw)


# ---------------------------------------------------------------- Part 1: registry + health
@pytest.mark.part1
def test_example_1_register_and_health(impl):
    assert run(impl, EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_register_keeps_original(impl):
    out = run(impl, ["REGISTER a 0 0 1", "REGISTER a 10 10 5", "ROUTE 10 10"])
    assert out == ["OK", "ERROR", "a 1569 a"]  # (10,10)->(0,0) = 1568.52 km: original coords kept


@pytest.mark.part1
@pytest.mark.edge
def test_coordinate_and_capacity_boundaries(impl):
    ok = ["REGISTER n 90 180 1", "REGISTER s -90 -180 1", "REGISTER c 0 0 1"]
    bad = ["REGISTER x 91 0 1", "REGISTER y -91 0 1", "REGISTER z 0 181 1", "REGISTER w 0 -181 1",
           "REGISTER v 0 0 0", "REGISTER u 0 0 -3"]
    assert run(impl, ok + bad) == ["OK"] * 3 + ["ERROR"] * 6


@pytest.mark.part1
@pytest.mark.edge
def test_arity_types_unknown_command(impl):
    out = run(impl, ["REGISTER a 1 2", "REGISTER a 1 2 3 4", "REGISTER a 1.5 2 3", "REGISTER a x 2 3",
                     "FOO a", "SET_HEALTHZ a true", "REGISTER a 1 2 3", "SET_HEALTHZ a maybe",
                     "SET_HEALTHZ a", "SET_HEALTHZ a FALSE", "SET_HEALTHZ a True", "SET_HEALTHZ ghost true"])
    assert out == ["ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "OK", "ERROR", "ERROR", "OK", "OK", "ERROR"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input_and_blank_lines(impl):
    assert run(impl, []) == []
    assert run(impl, ["", "   ", "REGISTER a 0 0 1", ""]) == ["OK"]


# ---------------------------------------------------------------- Part 2: distance
@pytest.mark.part2
def test_example_4_distances(impl):
    assert run(impl, EX4) == EX4_OUT


@pytest.mark.part2
def test_haversine_float_reference_values(impl):
    assert round(impl.haversine_km(0, 0, 0, 0), 2) == 0.00
    assert round(impl.haversine_km(0, 0, 0, 180), 2) == 20015.09   # antipodes
    assert round(impl.haversine_km(0, 0, 1, 0), 2) == 111.19       # one degree of latitude
    assert round(impl.haversine_km(30, 40, -30, -140), 2) == 20015.09
    assert round(impl.haversine_km(41, -73, 34, -118), 2) == 4000.08


@pytest.mark.part2
@pytest.mark.fmt
def test_distance_rounds_half_up_and_symmetric(impl):
    # (0,0)->(0,90) = 10007.54 -> 10008 ; (60,0)->(60,1) = 55.60 -> 56
    assert run(impl, ["DISTANCE 0 0 0 90", "DISTANCE 0 90 0 0", "DISTANCE 60 0 60 1"]) == ["10008", "10008", "56"]


@pytest.mark.part2
@pytest.mark.edge
def test_distance_needs_no_regions_and_validates_arity(impl):
    assert run(impl, ["DISTANCE 0 0 0", "DISTANCE 0 0 0 0 0", "DISTANCE 0 0 a 0", "DISTANCE -90 -180 90 180"]) == \
        ["ERROR", "ERROR", "ERROR", "20015"]


# ---------------------------------------------------------------- Part 3: routing
@pytest.mark.part3
def test_example_2_prachub_route(impl):
    assert run(impl, EX2) == EX2_OUT


@pytest.mark.part3
def test_example_3_capacity_and_ties(impl):
    assert run(impl, EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_route_no_regions_and_all_unhealthy(impl):
    out = run(impl, ["ROUTE 0 0", "REGISTER a 0 0 1", "SET_HEALTHZ a false", "ROUTE 0 0",
                     "SET_HEALTHZ a true", "ROUTE 0 0", "ROUTE 1 2"])
    assert out == ["NONE 0", "OK", "OK", "NONE 0", "OK", "a 0 a", "ERROR"] or out[:6] == \
        ["NONE 0", "OK", "OK", "NONE 0", "OK", "a 0 a"]


@pytest.mark.part3
@pytest.mark.edge
def test_nearest_healthy_with_capacity_skips_full_but_lists_it(impl):
    lines = ["REGISTER near 0 0 1", "REGISTER far 0 10 5", "ROUTE 0 0", "ROUTE 0 0", "ROUTE 0 0"]
    assert run(impl, lines) == ["OK", "OK", "near 0 near far", "far 1112 near far", "far 1112 near far"]


@pytest.mark.part3
@pytest.mark.edge
def test_unrounded_distance_decides_ranking(impl):
    # both ~4000 km from (41,-73): west at 4000.08; fake at (34,-117.999) is a hair closer
    lines = ["REGISTER west 34 -118 1", "REGISTER aaaa 34 -118 1", "ROUTE 41 -73"]
    assert run(impl, lines)[-1] == "aaaa 4000 aaaa west"  # exact tie -> name
    lines = ["REGISTER zzz 0 10 1", "REGISTER aaa 0 11 1", "ROUTE 0 0"]
    assert run(impl, lines)[-1] == "zzz 1112 zzz aaa"


@pytest.mark.part3
@pytest.mark.edge
def test_load_survives_health_flip_and_capacity_boundary(impl):
    lines = ["REGISTER a 0 0 2", "ROUTE 0 0", "SET_HEALTHZ a false", "SET_HEALTHZ a true", "ROUTE 0 0", "ROUTE 0 0"]
    assert run(impl, lines) == ["OK", "a 0 a", "OK", "OK", "a 0 a", "NONE 0 a"]


@pytest.mark.part3
@pytest.mark.edge
def test_invalid_commands_do_not_mutate(impl):
    lines = ["REGISTER a 0 0 1", "ROUTE 0", "ROUTE x y", "ROUTE 0 0", "ROUTE 0 0"]
    assert run(impl, lines) == ["OK", "ERROR", "ERROR", "a 0 a", "NONE 0 a"]


@pytest.mark.part3
def test_variant_tie_by_registration_order_matches_leetcode_sample(impl):
    lines = ["REGISTER us-east-1 0 0 1", "REGISTER ap-south-1 0 0 1", "ROUTE 0 0",
             "SET_HEALTHZ ap-south-1 false", "ROUTE 0 0"]
    assert run(impl, lines, tie="registration") == ["OK", "OK", "us-east-1 0 us-east-1 ap-south-1", "OK", "NONE 0 us-east-1"]


@pytest.mark.part3
def test_variant_allow_float(impl):
    assert run(impl, ["REGISTER a 51.5 -0.13 1", "ROUTE 48.85 2.35"], allow_float=True) == ["OK", "a 343 a"]
    assert run(impl, ["REGISTER a 51.5 -0.13 1"]) == ["ERROR"]


# ---------------------------------------------------------------- Part 4: release
@pytest.mark.part4
def test_release_frees_one_unit(impl):
    lines = ["REGISTER a 0 0 1", "ROUTE 0 0", "ROUTE 0 0", "RELEASE a", "ROUTE 0 0", "RELEASE a", "RELEASE a"]
    assert run(impl, lines) == ["OK", "a 0 a", "NONE 0 a", "OK", "a 0 a", "OK", "ERROR"]


@pytest.mark.part4
@pytest.mark.edge
def test_release_errors(impl):
    assert run(impl, ["RELEASE ghost", "REGISTER a 0 0 1", "RELEASE a", "RELEASE", "RELEASE a b"]) == \
        ["ERROR", "OK", "ERROR", "ERROR", "ERROR"]


@pytest.mark.part4
@pytest.mark.edge
def test_release_on_unhealthy_region(impl):
    lines = ["REGISTER a 0 0 1", "ROUTE 0 0", "SET_HEALTHZ a false", "RELEASE a", "SET_HEALTHZ a true", "ROUTE 0 0"]
    assert run(impl, lines) == ["OK", "a 0 a", "OK", "OK", "OK", "a 0 a"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX4 + EX2 + EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX4_OUT + EX2_OUT + EX1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_commands(run_script):
    rng = random.Random(0)
    lines = [f"REGISTER r{i} {rng.randint(-90, 90)} {rng.randint(-180, 180)} {rng.randint(1, 1000)}" for i in range(50)]
    for _ in range(100_000):
        k = rng.random()
        if k < 0.6:
            lines.append(f"ROUTE {rng.randint(-90, 90)} {rng.randint(-180, 180)}")
        elif k < 0.8:
            lines.append(f"DISTANCE {rng.randint(-90, 90)} {rng.randint(-180, 180)} {rng.randint(-90, 90)} {rng.randint(-180, 180)}")
        elif k < 0.9:
            lines.append(f"SET_HEALTHZ r{rng.randrange(50)} {rng.choice(['true', 'false'])}")
        else:
            lines.append(f"RELEASE r{rng.randrange(50)}")
    r = run_script("\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == len(lines)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
