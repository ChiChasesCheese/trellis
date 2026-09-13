import random

import pytest

EXAMPLE = [
    "alice,250,120,payg",
    "bob,99,99,payg",
    "carol,30000,15000,fixed",
    "dave,1000,1000,fixed",
    "dave,1000,1000,payg",
]
EXAMPLE_OUT = ["alice: $0.10", "bob: $0.00", "carol: $17.00", "dave: $8.20"]


def bill(impl, lines):
    return impl.calculate_monthly_billing(lines)


# ---------------------------------------------------------------- Part 1: payg
@pytest.mark.part1
def test_example_payg_lines(impl):
    assert bill(impl, ["alice,250,120,payg"]) == ["alice: $0.10"]
    assert bill(impl, ["bob,99,99,payg"]) == ["bob: $0.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_remainders_never_pool_across_sessions(impl):
    # 99 + 99 = 198 tokens but zero complete blocks
    assert bill(impl, ["u,99,0,payg", "u,99,0,payg"]) == ["u: $0.00"]
    assert bill(impl, ["u,100,0,payg", "u,100,0,payg"]) == ["u: $0.06"]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_tokens_and_empty_input(impl):
    assert bill(impl, ["u,0,0,payg"]) == ["u: $0.00"]
    assert bill(impl, []) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_is_plain_string_order(impl):
    out = bill(impl, ["user2,100,0,payg", "user10,100,0,payg", "B,100,0,payg", "a,100,0,payg"])
    assert out == ["B: $0.03", "a: $0.03", "user10: $0.03", "user2: $0.03"]


@pytest.mark.part1
@pytest.mark.edge
def test_huge_token_counts_stay_exact(impl):
    # 10^9 input tokens = 10^7 blocks × $0.03 = $300,000.00 ; float accumulation would drift
    assert bill(impl, ["u,1000000000,1000000000,payg"]) == ["u: $700000.00"]


@pytest.mark.part1
def test_whitespace_tolerance(impl):
    assert bill(impl, ["  alice , 250 , 120 , payg  ", ""]) == ["alice: $0.10"]


# ---------------------------------------------------------------- Part 2: fixed
@pytest.mark.part2
def test_example_fixed_overage(impl):
    assert bill(impl, ["carol,30000,15000,fixed"]) == ["carol: $17.00"]


@pytest.mark.part2
@pytest.mark.edge
def test_fixed_inside_allowance_is_flat_fee(impl):
    assert bill(impl, ["u,0,0,fixed"]) == ["u: $15.00"]
    assert bill(impl, ["u,20000,20000,fixed"]) == ["u: $15.00"]  # exactly 40,000


@pytest.mark.part2
@pytest.mark.edge
def test_fixed_one_block_over(impl):
    assert bill(impl, ["u,20000,20100,fixed"]) == ["u: $15.04"]
    assert bill(impl, ["u,20100,20000,fixed"]) == ["u: $15.04"]  # input consumed first, so the overage is output


@pytest.mark.part2
@pytest.mark.edge
def test_fixed_rounds_down_before_allowance(impl):
    # 39,999 + 99 -> billable 39,900 + 0 -> no overage
    assert bill(impl, ["u,39999,99,fixed"]) == ["u: $15.00"]
    # 40,099 -> billable 40,000 -> still no overage
    assert bill(impl, ["u,40099,0,fixed"]) == ["u: $15.00"]
    assert bill(impl, ["u,40100,0,fixed"]) == ["u: $15.03"]


@pytest.mark.part2
@pytest.mark.edge
def test_allowance_runs_out_mid_session_input_before_output(impl):
    # session1 uses 30,000 input; session2 has 15,000 input + 10,000 output
    # remaining allowance 10,000 -> covers 10,000 of the input; 5,000 input over (50 × .03 = 1.50)
    # + 10,000 output over (100 × .04 = 4.00) -> 15 + 5.50
    assert bill(impl, ["u,30000,0,fixed", "u,15000,10000,fixed"]) == ["u: $20.50"]


# ---------------------------------------------------------------- Part 3: switching
@pytest.mark.part3
def test_example_switching(impl):
    assert bill(impl, ["dave,1000,1000,fixed", "dave,1000,1000,payg"]) == ["dave: $8.20"]


@pytest.mark.part3
def test_full_example_all_users(impl):
    assert bill(impl, EXAMPLE) == EXAMPLE_OUT


@pytest.mark.part3
@pytest.mark.fmt
def test_prorated_fee_half_up_rounding(impl):
    # r = 1/3 -> 5.00 ; r = 1/6 -> 2.50 ; r = 1/7 -> 2.142857 -> 2.14 ; r = 3/7 -> 6.428571 -> 6.43
    def mk(fixed, payg):
        return [f"u,0,0,fixed"] * fixed + ["u,0,0,payg"] * payg
    assert bill(impl, mk(1, 2)) == ["u: $5.00"]
    assert bill(impl, mk(1, 5)) == ["u: $2.50"]
    assert bill(impl, mk(1, 6)) == ["u: $2.14"]
    assert bill(impl, mk(3, 4)) == ["u: $6.43"]
    # r = 1/8 -> 1.875 -> 1.88 (half-up, NOT banker's 1.87 — python round() would give 1.88 here
    # but round(0.125, 2) style cases are why we do it in integers)
    assert bill(impl, mk(1, 7)) == ["u: $1.88"]
    # r = 1/16 -> 0.9375 -> 0.94 ; r = 1/32 -> 0.46875 -> 0.47 ; r = 3/8 -> 5.625 -> 5.63
    assert bill(impl, mk(1, 15)) == ["u: $0.94"]
    assert bill(impl, mk(1, 31)) == ["u: $0.47"]
    assert bill(impl, mk(3, 5)) == ["u: $5.63"]


@pytest.mark.part3
@pytest.mark.edge
def test_prorated_allowance_floors_and_payg_ignores_allowance(impl):
    # r = 1/3: allowance floor(13333.33) = 13333 tokens, fee 5.00
    # fixed session 13,400 input -> billable 13,400 -> 67 tokens over -> 0 complete blocks over
    assert bill(impl, ["u,13400,0,fixed", "u,0,0,payg", "u,0,0,payg"]) == ["u: $5.00"]
    # 13,500 -> 167 over -> 1 block -> +0.03 ; payg session 100 tokens -> 0.03 regardless
    assert bill(impl, ["u,13500,0,fixed", "u,100,0,payg", "u,0,0,payg"]) == ["u: $5.06"]


@pytest.mark.part3
@pytest.mark.edge
def test_switching_order_independent_for_counts(impl):
    a = bill(impl, ["u,1000,1000,payg", "u,1000,1000,fixed"])
    b = bill(impl, ["u,1000,1000,fixed", "u,1000,1000,payg"])
    assert a == b == ["u: $8.20"]


@pytest.mark.part3
def test_multiple_users_independent(impl):
    out = bill(impl, ["b,0,0,fixed", "a,100,100,payg", "b,0,0,payg", "c,0,0,payg"])
    assert out == ["a: $0.07", "b: $7.50", "c: $0.00"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EXAMPLE_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_sessions(run_script):
    rng = random.Random(0)
    lines = [
        f"user{rng.randrange(5000)},{rng.randrange(0, 200000)},{rng.randrange(0, 200000)},{rng.choice(['payg', 'fixed'])}"
        for _ in range(100_000)
    ]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == len({ln.split(",")[0] for ln in lines})
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
