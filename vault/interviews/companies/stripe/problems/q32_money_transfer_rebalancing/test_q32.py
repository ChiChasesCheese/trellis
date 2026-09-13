import random
import time

import pytest

# ---- verbatim example from MoneyTransfer.java -------------------------------------------------
ACCTS = ["- AU: 80", "- US: 140", "- MX: 110", "- SG: 120", "- FR: 70"]
ACCTS_OUT = ["from: US, to: AU, amount: 20", "from: US, to: FR, amount: 20", "from: MX, to: FR, amount: 10"]


def check_valid(impl, lines, transfers, minimum=100):
    """Every transfer > 0, sources never dip below the minimum, all accounts end >= minimum."""
    accounts, _, m, _ = impl.parse(lines)
    bal = {a.name: a.balance for a in accounts}
    for t in transfers:
        assert t.amount > 0 and t.src != t.dst
        bal[t.src] -= t.amount
        bal[t.dst] += t.amount
        assert bal[t.src] >= minimum, f"{t} overdrew {t.src}"
    assert all(b >= minimum for b in bal.values()), bal


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_verbatim_example(impl):
    assert impl.part1(ACCTS) == ACCTS_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_feasibility_boundary(impl):
    assert impl.part1(["A: 150", "B: 50"]) == ["from: A, to: B, amount: 50"]      # sum == 200
    assert impl.part1(["A: 149", "B: 50"]) == ["IMPOSSIBLE"]                      # one below
    assert impl.part1(["A: 151", "B: 50"]) == ["from: A, to: B, amount: 50"]      # one above


@pytest.mark.part1
@pytest.mark.edge
def test_nothing_to_do_single_and_empty(impl):
    assert impl.part1(["A: 100", "B: 100"]) == []
    assert impl.part1(["A: 100"]) == []
    assert impl.part1(["A: 99"]) == ["IMPOSSIBLE"]
    assert impl.part1([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_negative_balance_and_custom_min(impl):
    assert impl.part1(["A: -50", "B: 300"]) == ["from: B, to: A, amount: 150"]
    assert impl.part1(["MIN 10", "A: 0", "B: 25"]) == ["from: B, to: A, amount: 10"]
    assert impl.part1(["MIN 0", "A: -5", "B: 5"]) == ["from: B, to: A, amount: 5"]


@pytest.mark.part1
def test_deficit_needs_several_sources_input_order(impl):
    out = impl.part1(["A: 110", "B: 110", "C: 110", "D: 70"])
    assert out == ["from: A, to: D, amount: 10", "from: B, to: D, amount: 10", "from: C, to: D, amount: 10"]


@pytest.mark.part1
def test_input_tolerates_bullets_and_spaces(impl):
    assert impl.part1(["-  AU : 80", "US:140 ", ""]) == ["from: US, to: AU, amount: 20"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_minimum_is_two_transfers(impl):
    out = impl.part2(ACCTS)
    assert out == ["from: US, to: FR, amount: 30", "from: SG, to: AU, amount: 20"]


@pytest.mark.part2
def test_greedy_is_a_heuristic_on_the_example(impl):
    accounts, _, _, _ = impl.parse(ACCTS)
    greedy = impl.rebalance_greedy(accounts)
    assert len(greedy) == 3 and len(impl.min_transfers_exact(accounts)) == 2
    check_valid(impl, ACCTS, greedy)


@pytest.mark.part2
@pytest.mark.edge
def test_exact_counts_hand_verified(impl):
    def count(balances):
        accounts = [impl.Account(f"a{i}", 100 + n) for i, n in enumerate(balances)]
        ts = impl.min_transfers_exact(accounts)
        check_valid(impl, [f"a{i}: {100 + n}" for i, n in enumerate(balances)], ts)
        return len(ts)
    assert count([10, 10, -10, -10]) == 2
    assert count([20, -10, -10]) == 2
    assert count([15, 5, -10, -10]) == 3          # 5 alone cannot cover a 10
    assert count([-4, 4, 0]) == 1                 # LC 465 example 2
    assert count([-5, 10, -5]) == 2               # LC 465 example 1
    assert count([30, -10, -10, -10]) == 3
    assert count([0, 0]) == 0
    assert count([5, 5, 5, -15, 100]) == 1        # the big surplus covers it in one transfer


@pytest.mark.part2
@pytest.mark.edge
def test_part2_impossible_and_noop(impl):
    assert impl.part2(["A: 90", "B: 100"]) == ["IMPOSSIBLE"]
    assert impl.part2(["A: 100", "B: 250"]) == []


@pytest.mark.part2
def test_part2_large_input_falls_back_to_greedy_and_is_valid(impl):
    rng = random.Random(1)
    lines = [f"acct{i}: {rng.randrange(0, 250)}" for i in range(500)]
    accounts, _, _, _ = impl.parse(lines)
    out = impl.part2(lines)
    if out == ["IMPOSSIBLE"]:
        assert sum(a.balance for a in accounts) < 100 * 500
    else:
        check_valid(impl, lines, impl.rebalance_greedy(accounts))
        assert out == [str(t) for t in impl.rebalance_greedy(accounts)]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_audit_verbatim_transfers_ok(impl):
    lines = ["AU: 80", "US: 140", "MX: 110", "SG: 120", "FR: 70"] + ACCTS_OUT
    assert impl.part3(lines) == ["AU: 100", "US: 100", "MX: 100", "SG: 120", "FR: 100", "OK"]


@pytest.mark.part3
def test_audit_best_effort_examples(impl):
    assert impl.part3(["AU: 50", "US: 120", "from: US, to: AU, amount: 20"]) == ["AU: 70", "US: 100", "BEST_EFFORT"]
    assert impl.part3(["AU: 50", "US: 120", "from: US, to: AU, amount: 10"]) == ["AU: 60", "US: 110", "NOT_BEST_EFFORT"]


@pytest.mark.part3
@pytest.mark.edge
def test_audit_incomplete_invalid_and_no_transfers(impl):
    assert impl.part3(["A: 80", "B: 140"]) == ["A: 80", "B: 140", "INCOMPLETE"]
    assert impl.part3(["A: 80", "B: 140", "from: B, to: A, amount: 20"]) == ["A: 100", "B: 120", "OK"]
    assert impl.part3(["A: 80", "B: 140", "from: B, to: Z, amount: 20"]) == ["A: 80", "B: 140", "INVALID"]
    assert impl.part3(["A: 80", "B: 140", "from: B, to: A, amount: 0"]) == ["A: 80", "B: 140", "INVALID"]
    assert impl.part3(["A: 80", "B: 140", "from: B, to: B, amount: 5"]) == ["A: 80", "B: 140", "INVALID"]
    # transfers before the invalid one are applied, the ones after are skipped
    lines = ["A: 80", "B: 140", "from: B, to: A, amount: 10", "from: Q, to: A, amount: 1", "from: B, to: A, amount: 10"]
    assert impl.part3(lines) == ["A: 90", "B: 130", "INVALID"]


@pytest.mark.part3
@pytest.mark.edge
def test_audit_boundaries(impl):
    assert impl.part3(["A: 100", "B: 100"]) == ["A: 100", "B: 100", "OK"]
    assert impl.part3(["A: 99", "B: 100"]) == ["A: 99", "B: 100", "BEST_EFFORT"]      # sum 199, nobody above
    assert impl.part3(["A: 98", "B: 101"]) == ["A: 98", "B: 101", "NOT_BEST_EFFORT"]
    assert impl.part3(["A: 100", "B: 100", "from: A, to: B, amount: 30"]) == ["A: 70", "B: 130", "INCOMPLETE"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_fee_example(impl):
    assert impl.part4(["FEE 5", "A: 140", "B: 80", "C: 95"]) == ["from: A, to: B, amount: 20", "from: A, to: C, amount: 5", "FEES: 10"]
    assert impl.part4(["FEE 5", "A: 130", "B: 80", "C: 95"]) == ["IMPOSSIBLE"]


@pytest.mark.part4
@pytest.mark.edge
def test_fee_zero_matches_greedy_and_fee_exhausts_source(impl):
    assert impl.part4(["FEE 0"] + ACCTS)[-1] == "FEES: 0"
    assert impl.part4(ACCTS)[:-1] == [str(t) for t in impl.rebalance_greedy(impl.parse(ACCTS)[0])]
    # source surplus 5 == fee -> nothing sendable; a second source pays
    assert impl.part4(["FEE 5", "A: 105", "B: 130", "C: 90"]) == ["from: B, to: C, amount: 10", "FEES: 5"]
    assert impl.part4(["FEE 5", "A: 100", "B: 100"]) == ["FEES: 0"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 1\n" + "\n".join(ACCTS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(ACCTS_OUT) + "\n"
    assert run_script("PART 2\nA: 100\n").stdout == ""
    assert run_script("A: 90\nB: 100\n").stdout == "IMPOSSIBLE\n"   # no PART header -> Part 1


@pytest.mark.part4
@pytest.mark.perf
def test_perf_500_accounts_100k_audit_and_exact_worst_case(run_script, impl):
    rng = random.Random(0)
    names = [f"acct{i}" for i in range(500)]
    lines = ["PART 3"] + [f"{n}: {rng.randrange(0, 300)}" for n in names]
    lines += [f"from: {rng.choice(names)}, to: {rng.choice(names)}, amount: {rng.randrange(1, 50)}" for _ in range(100_000)]
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 501
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    # exact search at its size limit: 6 distinct surpluses vs 6 distinct deficits
    accounts = [impl.Account(f"s{i}", 100 + v) for i, v in enumerate([97, 89, 83, 79, 73, 71])]
    accounts += [impl.Account(f"d{i}", 100 - v) for i, v in enumerate([61, 59, 53, 47, 43, 41])]
    t0 = time.perf_counter()
    ts = impl.min_transfers_exact(accounts)
    assert time.perf_counter() - t0 < 2.0
    check_valid(impl, [f"{a.name}: {a.balance}" for a in accounts], ts)
    assert len(ts) == 6
