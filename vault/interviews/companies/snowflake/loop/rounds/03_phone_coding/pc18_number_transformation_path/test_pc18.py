import random
from collections import deque

import pytest


def _is_valid_path(path, a, b):
    """Independent checker for Part1: does NOT compare to any fixed answer, just verifies the
    returned sequence is a legal walk from a to b."""
    if not path:
        return False
    if path[0] != a or path[-1] != b:
        return False
    for x in path:
        if not isinstance(x, int) or x < 1:
            return False
    for x, y in zip(path, path[1:]):
        if y == x + 2:
            continue
        if y == x - 2 and y >= 1:
            continue
        if x % 2 == 0 and y == x // 2:
            continue
        return False
    return True


def _brute_bfs_shortest_length(a, b, bound):
    """Independent BFS (different bound formula from the solution's) used only to cross-check
    the LENGTH of Part2's answer, not its exact path."""
    if a == b:
        return 0
    seen = {a}
    dq = deque([(a, 0)])
    while dq:
        cur, dist = dq.popleft()
        neighbors = []
        if cur + 2 <= bound:
            neighbors.append(cur + 2)
        if cur - 2 >= 1:
            neighbors.append(cur - 2)
        if cur % 2 == 0 and cur // 2 >= 1:
            neighbors.append(cur // 2)
        for nxt in neighbors:
            if nxt == b:
                return dist + 1
            if nxt not in seen:
                seen.add(nxt)
                dq.append((nxt, dist + 1))
    return None


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_same_value(impl):
    assert impl.transform(5, 5) == [5]


@pytest.mark.part1
def test_same_parity_direct(impl):
    path = impl.transform(1, 7)
    assert _is_valid_path(path, 1, 7)


@pytest.mark.part1
def test_even_to_odd_needs_split(impl):
    path = impl.transform(4, 7)
    assert _is_valid_path(path, 4, 7)


@pytest.mark.part1
def test_odd_start_even_target_is_impossible(impl):
    assert impl.transform(7, 4) is None
    assert impl.transform(3, 4) is None
    assert impl.transform(1, 2) is None


@pytest.mark.part1
@pytest.mark.edge
def test_odd_start_odd_target_always_possible(impl):
    assert _is_valid_path(impl.transform(1, 999), 1, 999)
    assert _is_valid_path(impl.transform(999, 1), 999, 1)


@pytest.mark.part1
@pytest.mark.edge
def test_split_down_to_one(impl):
    assert _is_valid_path(impl.transform(2, 1), 2, 1)


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("a,b", [(0, 5), (-3, 5), (5, 0), (5, -1)])
def test_non_positive_raises(impl, a, b):
    with pytest.raises(ValueError):
        impl.transform(a, b)


@pytest.mark.part1
@pytest.mark.edge
def test_part1_random_reachable_pairs(impl):
    rng = random.Random(0)
    for _ in range(300):
        a = rng.randint(1, 500)
        b = rng.randint(1, 500)
        result = impl.transform(a, b)
        if a % 2 == 1 and b % 2 == 0:
            assert result is None, (a, b)
        else:
            assert _is_valid_path(result, a, b), (a, b, result)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_shortest_same_value(impl):
    assert impl.shortest_transform(5, 5) == [5]


@pytest.mark.part2
def test_shortest_impossible_matches_part1(impl):
    assert impl.shortest_transform(7, 4) is None
    assert impl.shortest_transform(3, 4) is None


@pytest.mark.part2
@pytest.mark.edge
def test_shortest_is_valid_and_no_longer_than_part1(impl):
    rng = random.Random(1)
    for _ in range(150):
        a = rng.randint(1, 200)
        b = rng.randint(1, 200)
        if a % 2 == 1 and b % 2 == 0:
            continue
        shortest = impl.shortest_transform(a, b)
        naive = impl.transform(a, b)
        assert _is_valid_path(shortest, a, b), (a, b, shortest)
        assert len(shortest) <= len(naive), (a, b, shortest, naive)


@pytest.mark.part2
@pytest.mark.edge
def test_shortest_length_matches_independent_bfs(impl):
    rng = random.Random(2)
    for _ in range(150):
        a = rng.randint(1, 120)
        b = rng.randint(1, 120)
        if a % 2 == 1 and b % 2 == 0:
            continue
        shortest = impl.shortest_transform(a, b)
        expected_len = _brute_bfs_shortest_length(a, b, bound=3 * max(a, b) + 20)
        assert expected_len is not None
        assert len(shortest) - 1 == expected_len, (a, b, shortest, expected_len)


@pytest.mark.part2
@pytest.mark.edge
@pytest.mark.parametrize("a,b", [(0, 5), (5, 0), (-1, 2)])
def test_shortest_non_positive_raises(impl, a, b):
    with pytest.raises(ValueError):
        impl.shortest_transform(a, b)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_shortest_large_values(run_script):
    body = "\n".join(f"{a} {a + 1}" for a in range(2, 2002, 2))  # 1000 even-to-odd queries
    r = run_script("PART 2\n" + body + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 1000
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n5 5\n7 4\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "5"
    assert lines[1] == "IMPOSSIBLE"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n1 7\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1 3 5 7\n"
