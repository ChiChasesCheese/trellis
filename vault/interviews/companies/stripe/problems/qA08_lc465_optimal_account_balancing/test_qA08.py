import random
import time

import pytest

LC1 = [[0, 1, 10], [2, 0, 5]]
LC2 = [[0, 1, 10], [1, 0, 1], [1, 2, 5], [2, 0, 5]]


def _apply(transactions, transfers, impl):
    """Apply the transfers to the credits; each sender must currently owe exactly what it sends and
    each receiver must currently be owed. Return the remaining non-zero credits (must be empty)."""
    net = dict(impl.net_balances(transactions))
    for frm, to, amount in transfers:
        assert amount > 0 and frm != to
        assert net.get(frm, 0) < 0 < net.get(to, 0), (frm, to, amount, net)
        assert amount in (-net[frm], net[to])  # every transfer fully settles one of its two ends
        net[frm] += amount
        net[to] -= amount
    return {p: v for p, v in net.items() if v}


def _random_case(rng):
    k = rng.randint(1, 8)
    return [[a, b, rng.randint(1, 100)] for a, b in (rng.sample(range(12), 2) for _ in range(k))]


# ---------------------------------------------------------------- Part 1: LC 465
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.min_transfers(LC1) == 2
    assert impl.min_transfers(LC2) == 1
    assert impl.min_transfers_bitmask(LC1) == 2
    assert impl.min_transfers_bitmask(LC2) == 1


@pytest.mark.part1
def test_net_balances_drops_zero_and_sorts(impl):
    assert impl.net_balances(LC2) == {0: 4, 1: -4}  # party 2 is a pass-through -> dropped
    assert impl.net_balances([[5, 3, 2], [1, 3, 1]]) == {1: 1, 3: -3, 5: 2}
    assert impl.net_balances([]) == {}


@pytest.mark.part1
@pytest.mark.edge
def test_everything_cancels_and_single(impl):
    assert impl.min_transfers([[0, 1, 5], [1, 0, 5]]) == 0
    assert impl.min_transfers([]) == 0
    assert impl.min_transfers([[3, 7, 100]]) == 1
    assert impl.min_transfers_bitmask([[0, 1, 5], [1, 0, 5]]) == 0
    assert impl.min_transfers_bitmask([[3, 7, 100]]) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_zero_sum_subsets_not_n_minus_one(impl):
    # nets +5,-5,+3,-3 -> two groups -> 2 (not 3)
    assert impl.min_transfers([[0, 1, 5], [2, 3, 3]]) == 2
    # two 5-groups and two 3-groups -> 4 (not 7)
    assert impl.min_transfers([[0, 1, 5], [2, 3, 5], [4, 5, 3], [6, 7, 3]]) == 4
    # {3,4} cancels; 0 pays 1 and 2 -> 3
    assert impl.min_transfers([[0, 1, 3], [0, 2, 7], [3, 4, 10]]) == 3
    # 0:+5, 1:+5, 2:-10 : 2 must pay both -> 2
    assert impl.min_transfers([[2, 0, 5], [2, 1, 5]]) == 2


@pytest.mark.part1
@pytest.mark.edge
def test_hub_debtor_pays_everyone(impl):
    t = [[0, 1, 6], [0, 2, 2], [0, 3, 2], [0, 4, 2]]
    assert impl.min_transfers(t) == 4  # duplicate +2 nets: pruning must not lower the answer
    assert impl.min_transfers_bitmask(t) == 4


@pytest.mark.part1
@pytest.mark.edge
def test_boundaries_of_lc_domain(impl):
    # party ids up to 11, amount 100, 8 transactions
    t = [[11, 0, 100], [10, 1, 100], [9, 2, 100], [8, 3, 100], [7, 4, 100], [6, 5, 100], [0, 11, 100], [1, 10, 1]]
    assert impl.min_transfers(t) == 5  # (11,0) cancels; (10,1) net 99 pair; 4 more pairs
    assert impl.min_transfers_bitmask(t) == 5


@pytest.mark.part1
def test_dfs_matches_bitmask_on_random_instances(impl):
    rng = random.Random(0)
    for _ in range(300):
        t = _random_case(rng)
        assert impl.min_transfers(t) == impl.min_transfers_bitmask(t), t


# ---------------------------------------------------------------- Part 2: transfers
@pytest.mark.part2
def test_settle_examples(impl):
    T = impl.Transfer
    assert impl.settle(LC1) == [T(1, 0, 5), T(1, 2, 5)]
    assert impl.settle(LC2) == [T(1, 0, 4)]
    assert impl.settle([[0, 1, 3], [0, 2, 7], [3, 4, 10]]) == [T(1, 0, 10), T(2, 1, 7), T(4, 3, 10)]


@pytest.mark.part2
@pytest.mark.edge
def test_settle_empty_and_fully_cancelled(impl):
    assert impl.settle([]) == []
    assert impl.settle([[0, 1, 5], [1, 0, 5]]) == []
    assert impl.settle([[3, 7, 100]]) == [impl.Transfer(7, 3, 100)]  # 7 received, so 7 pays back


@pytest.mark.part2
def test_settle_is_optimal_and_zeroes_every_net(impl):
    rng = random.Random(1)
    for _ in range(200):
        t = _random_case(rng)
        transfers = impl.settle(t)
        assert len(transfers) == impl.min_transfers_bitmask(t)
        assert _apply(t, transfers, impl) == {}
        assert all(a > 0 for _, _, a in transfers)


@pytest.mark.part2
@pytest.mark.fmt
def test_settle_chain_direction(impl):
    # 4 handed 9 to 2 and 1 to 3; 5 handed 8 to 3 -> nets 2:-9, 3:-9, 4:+10, 5:+8
    transfers = impl.settle([[4, 2, 9], [4, 3, 1], [5, 3, 8]])
    assert len(transfers) == 3
    assert transfers[0] == impl.Transfer(2, 4, 9)  # first-found: party 2 pays the first creditor, 4
    assert _apply([[4, 2, 9], [4, 3, 1], [5, 3, 8]], transfers, impl) == {}


# ---------------------------------------------------------------- Part 3: write-off
@pytest.mark.part3
def test_writeoff_examples(impl):
    T = impl.Transfer
    s = impl.settle_with_writeoff(LC1, 6)
    assert s.transfers == [T(1, impl.PLATFORM, 10)] and s.written_off == [(0, 5), (2, 5)]
    s = impl.settle_with_writeoff(LC2, 5)
    assert s.transfers == [] and s.written_off == [(0, 4), (1, -4)]  # residual 0 -> no PLATFORM


@pytest.mark.part3
@pytest.mark.edge
def test_writeoff_threshold_boundary(impl):
    assert impl.settle_with_writeoff(LC1, 5) == impl.Settlement(impl.settle(LC1), [])   # == threshold: settled
    assert impl.settle_with_writeoff(LC1, 0) == impl.Settlement(impl.settle(LC1), [])   # threshold 0 == Part 2
    s = impl.settle_with_writeoff(LC1, 11)  # everything written off, residual 0
    assert s.transfers == [] and s.written_off == [(0, 5), (1, -10), (2, 5)]


@pytest.mark.part3
@pytest.mark.edge
def test_writeoff_platform_can_be_debtor(impl):
    # nets 0:+10, 1:-3, 2:-7 ; threshold 4 forgives 1's debt -> the platform pays 0 the missing 3
    s = impl.settle_with_writeoff([[0, 1, 3], [0, 2, 7]], 4)
    assert s.written_off == [(1, -3)]
    assert s.transfers == [impl.Transfer(impl.PLATFORM, 0, 3), impl.Transfer(2, 0, 7)]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\n0,1,10\n2,0,5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"
    r = run_script("PART 2\n0,1,10\n\n2, 0, 5\n")
    assert r.stdout == "2\nfrom: 1, to: 0, amount: 5\nfrom: 1, to: 2, amount: 5\n"
    r = run_script("PART 3\nTHRESHOLD 6\n0,1,10\n2,0,5\n")
    assert r.stdout == "from: 1, to: PLATFORM, amount: 10\nwritten_off: 0=5,2=5\n"
    r = run_script("PART 3\nTHRESHOLD 5\n0,1,10\n2,0,5\n")
    assert r.stdout == "from: 1, to: 0, amount: 5\nfrom: 1, to: 2, amount: 5\nwritten_off: none\n"
    assert run_script("PART 2\n0,1,5\n1,0,5\n").stdout == "0\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max_twelve_nonzero_nets(impl, run_script):
    # LC max: 8 transactions, 12 non-zero nets, no pair cancels -> the DFS's worst shape
    worst = [[6, 0, 100], [7, 1, 98], [8, 2, 96], [9, 3, 94], [10, 4, 92], [11, 5, 90], [6, 7, 1], [8, 9, 3]]
    assert len(impl.net_balances(worst)) == 12
    # slowest of 3000 random LC-max instances (found offline with random.Random(0))
    slow = [[1, 5, 95], [0, 8, 36], [2, 3, 98], [7, 5, 79], [4, 10, 46], [9, 10, 80], [2, 4, 50], [11, 6, 84]]
    rng = random.Random(0)
    cases = [worst, slow] + [_random_case(rng) for _ in range(200)]
    t0 = time.perf_counter()
    for c in cases:
        assert impl.min_transfers(c) == impl.min_transfers_bitmask(c)
    assert time.perf_counter() - t0 < 2.0
    text = "PART 2\n" + "\n".join(f"{a},{b},{c}" for a, b, c in worst) + "\n"
    r = run_script(text)
    assert r.returncode == 0 and r.stdout.startswith("8\n") and r.seconds < 2.0 and r.max_rss_mb < 256
