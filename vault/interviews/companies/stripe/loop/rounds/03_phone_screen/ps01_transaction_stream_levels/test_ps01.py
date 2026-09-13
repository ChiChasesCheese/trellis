import random

import pytest

P1_LINES = ["1,10,100", "2,5,101", "1,7,102"]
P1_OUT = ["1: 17", "2: 5"]

P3_LINES = ["1,50,10", "1,60,40", "2,80,30", "3,30,40", "2,50,90"]
P3_PARAMS = "t=90 K=2"
P3_OUT = ["2: 130", "1: 60"]

P2_LINES = ["u1,40,0", "u1,40,30", "u1,40,60", "u2,200,5"]
P2_PARAMS = "T=100 W=60"
P2_OUT = ["u1: 120", "u2: 200"]

P4_LINES = ["u1,10,1", "u1,60,2", "u1,20,3", "u1,70,4", "u1,5,5"]
P4_PARAMS = "S=50"
P4_OUT = ["u1: 1,3"]


def run(impl, part, body_lines):
    return {1: impl.part1, 2: impl.part2, 3: impl.part3, 4: impl.part4}[part](body_lines)


# ---------------------------------------------------------------- Part 1: totals
@pytest.mark.part1
def test_example_totals(impl):
    assert impl.part1(P1_LINES) == P1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_single_and_duplicate_and_zero(impl):
    assert impl.part1(["u,0,0"]) == ["u: 0"]
    assert impl.part1(["u,5,0", "u,5,1", "u,5,2"]) == ["u: 15"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input(impl):
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_is_plain_string_order(impl):
    out = impl.part1(["user2,1,0", "user10,1,0", "B,1,0", "a,1,0"])
    assert out == ["B: 1", "a: 1", "user10: 1", "user2: 1"]


@pytest.mark.part1
def test_order_independent_out_of_order_timestamps(impl):
    # sum doesn't care about timestamp order for part 1
    a = impl.part1(["u,3,50", "u,2,10", "u,1,90"])
    b = impl.part1(["u,1,90", "u,2,10", "u,3,50"])
    assert a == b == ["u: 6"]


@pytest.mark.part1
def test_whitespace_tolerance(impl):
    assert impl.part1(["  1 , 10 , 100  ", "", "  2,5,101"]) == ["1: 10", "2: 5"]


# ---------------------------------------------------------------- Part 2: sliding-window flag
@pytest.mark.part2
def test_example_threshold_flag(impl):
    assert impl.part2([P2_PARAMS] + P2_LINES) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_p2_window_boundary_closed_inclusive(impl):
    # exactly W seconds old is still inside the window
    assert impl.part2(["T=10 W=60", "u,5,0", "u,5,60"]) == ["u: 10"]
    # one second older falls outside
    assert impl.part2(["T=10 W=60", "u,5,0", "u,5,61"]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_never_flagged_user_is_omitted(impl):
    assert impl.part2(["T=1000 W=60", "u,5,0", "u,5,10"]) == []


@pytest.mark.part2
def test_w_defaults_to_60_when_omitted(impl):
    assert impl.part2(["T=10", "u,5,0", "u,5,60"]) == ["u: 10"]


@pytest.mark.part2
def test_multiple_users_independent_windows(impl):
    out = impl.part2(["T=100 W=60", "a,100,0", "b,50,0", "b,50,10"])
    assert out == ["a: 100", "b: 100"]


@pytest.mark.part2
@pytest.mark.edge
def test_out_of_order_input_lines_still_windows_correctly(impl):
    # same events as the example but shuffled in the input; must still flag at first crossing
    shuffled = ["u1,40,60", "u2,200,5", "u1,40,0", "u1,40,30"]
    assert impl.part2(["T=100 W=60"] + shuffled) == P2_OUT


# ---------------------------------------------------------------- Part 3: top-K
@pytest.mark.part3
def test_example_topk(impl):
    assert impl.part3([P3_PARAMS] + P3_LINES) == P3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_p3_window_boundary_closed_inclusive(impl):
    assert impl.part3(["t=100 K=5", "u,5,40"]) == ["u: 5"]  # 40 == t-60, included
    assert impl.part3(["t=100 K=5", "u,5,39"]) == []  # 39 < t-60, excluded


@pytest.mark.part3
@pytest.mark.edge
def test_fewer_qualifying_users_than_k_no_padding(impl):
    assert impl.part3(["t=100 K=5", "a,1,100"]) == ["a: 1"]


@pytest.mark.part3
@pytest.mark.edge
def test_k_zero_is_empty(impl):
    assert impl.part3(["t=100 K=0", "a,1,100"]) == []


@pytest.mark.part3
@pytest.mark.fmt
def test_tie_broken_by_user_id_ascending(impl):
    out = impl.part3(["t=10 K=3", "z,5,10", "a,5,10", "m,5,10"])
    assert out == ["a: 5", "m: 5", "z: 5"]


@pytest.mark.part3
def test_inactive_user_never_a_candidate(impl):
    out = impl.part3(["t=1000 K=5", "u,5,10"])
    assert out == []


# ---------------------------------------------------------------- Part 4: pattern detection
@pytest.mark.part4
def test_example_pattern(impl):
    assert impl.part4([P4_PARAMS] + P4_LINES) == P4_OUT


@pytest.mark.part4
@pytest.mark.edge
def test_overlapping_matches_both_counted(impl):
    # small,large,small,large,small -> matches at index 0 and index 2, not 1 combined match
    lines = ["u,10,1", "u,60,2", "u,10,3", "u,60,4", "u,10,5"]
    assert impl.part4(["S=50"] + lines) == ["u: 1,3"]


@pytest.mark.part4
@pytest.mark.edge
def test_fewer_than_three_transactions_no_match(impl):
    assert impl.part4(["S=50", "u,10,1", "u,60,2"]) == []


@pytest.mark.part4
@pytest.mark.edge
def test_amount_equal_to_s_counts_as_large(impl):
    # S=50, amounts 10,50,10 -> large boundary is amount >= S, so 50 is 'large' -> pattern matches
    assert impl.part4(["S=50", "u,10,1", "u,50,2", "u,10,3"]) == ["u: 1"]


@pytest.mark.part4
def test_all_large_no_match(impl):
    assert impl.part4(["S=50", "u,60,1", "u,70,2", "u,80,3"]) == []


@pytest.mark.part4
@pytest.mark.fmt
def test_users_sorted_string_order_matches_only_reported(impl):
    lines = ["z,10,1", "z,60,2", "z,10,3", "a,60,1", "a,60,2", "a,60,3"]
    assert impl.part4(["S=50"] + lines) == ["z: 1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    r = run_script("PART 3\n" + P3_PARAMS + "\n" + "\n".join(P3_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_OUT) + "\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact_part4_with_params_line(run_script):
    r = run_script("PART 4\n" + P4_PARAMS + "\n" + "\n".join(P4_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P4_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_lines(run_script):
    rng = random.Random(0)
    body = [
        f"user{rng.randrange(3000)},{rng.randrange(0, 500)},{rng.randrange(0, 100000)}"
        for _ in range(100_000)
    ]
    stdin_text = "PART 2\nT=100000 W=60\n" + "\n".join(body) + "\n"
    r = run_script(stdin_text, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
