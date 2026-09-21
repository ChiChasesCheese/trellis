import random
from collections import deque

import pytest


def _brute_container(h):
    best = 0
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            best = max(best, min(h[i], h[j]) * (j - i))
    return best


def _brute_trap_1d(h):
    n = len(h)
    total = 0
    for i in range(n):
        lm = max(h[: i + 1])
        rm = max(h[i:])
        total += max(0, min(lm, rm) - h[i])
    return total


def _brute_trap_2d(grid):
    """Raise the water level one unit at a time; at each level, flood-fill from the border
    through cells still below that level -- anything below the level that flooding cannot
    reach is trapped water at that level."""
    m, n = len(grid), len(grid[0])
    max_h = max(max(row) for row in grid)
    total = 0
    for level in range(1, max_h + 1):
        visited = [[False] * n for _ in range(m)]
        dq = deque()
        for i in range(m):
            for j in range(n):
                if (i in (0, m - 1) or j in (0, n - 1)) and grid[i][j] < level:
                    visited[i][j] = True
                    dq.append((i, j))
        while dq:
            i, j = dq.popleft()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj] and grid[ni][nj] < level:
                    visited[ni][nj] = True
                    dq.append((ni, nj))
        for i in range(m):
            for j in range(n):
                if grid[i][j] < level and not visited[i][j]:
                    total += 1
    return total


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.max_container_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49


@pytest.mark.part1
def test_worked_example_2(impl):
    assert impl.max_container_area([1, 1]) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_single(impl):
    assert impl.max_container_area([]) == 0
    assert impl.max_container_area([5]) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_duplicates(impl):
    assert impl.max_container_area([3, 3, 3, 3]) == 9


@pytest.mark.part1
@pytest.mark.edge
def test_negative_height_raises(impl):
    with pytest.raises(ValueError):
        impl.max_container_area([1, -2, 3])


@pytest.mark.part1
@pytest.mark.edge
def test_non_int_raises(impl):
    with pytest.raises(ValueError):
        impl.max_container_area([1, 2.5, 3])
    with pytest.raises(ValueError):
        impl.max_container_area("not a list")


@pytest.mark.part1
@pytest.mark.edge
def test_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 12)
        h = [rng.randint(0, 9) for _ in range(n)]
        assert impl.max_container_area(h) == _brute_container(h), h


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_1_two_pointer(impl):
    assert impl.trap_two_pointer([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6


@pytest.mark.part2
def test_worked_example_1_prefix_suffix(impl):
    assert impl.trap_prefix_suffix([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6


@pytest.mark.part2
def test_worked_example_2_both_impls(impl):
    assert impl.trap_two_pointer([4, 2, 0, 3, 2, 5]) == 9
    assert impl.trap_prefix_suffix([4, 2, 0, 3, 2, 5]) == 9


@pytest.mark.part2
@pytest.mark.edge
def test_fewer_than_three_bars(impl):
    assert impl.trap_two_pointer([]) == 0
    assert impl.trap_two_pointer([5]) == 0
    assert impl.trap_two_pointer([5, 3]) == 0
    assert impl.trap_prefix_suffix([5, 3]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_monotonic_traps_nothing(impl):
    assert impl.trap_two_pointer([1, 2, 3, 4, 5]) == 0
    assert impl.trap_two_pointer([5, 4, 3, 2, 1]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_negative_height_raises_part2(impl):
    with pytest.raises(ValueError):
        impl.trap_two_pointer([1, -1, 2])
    with pytest.raises(ValueError):
        impl.trap_prefix_suffix([1, -1, 2])


@pytest.mark.part2
@pytest.mark.edge
def test_two_impls_agree_random(impl):
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 12)
        h = [rng.randint(0, 9) for _ in range(n)]
        two_p = impl.trap_two_pointer(h)
        assert two_p == impl.trap_prefix_suffix(h) == _brute_trap_1d(h), h


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_1_grid(impl):
    grid = [[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]
    assert impl.trap_2d(grid) == 4


@pytest.mark.part3
def test_worked_example_2_moat(impl):
    grid = [
        [3, 3, 3, 3, 3],
        [3, 2, 2, 2, 3],
        [3, 2, 1, 2, 3],
        [3, 2, 2, 2, 3],
        [3, 3, 3, 3, 3],
    ]
    assert impl.trap_2d(grid) == 10


@pytest.mark.part3
@pytest.mark.edge
def test_flat_grid_traps_nothing(impl):
    grid = [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]
    assert impl.trap_2d(grid) == 0


@pytest.mark.part3
@pytest.mark.edge
def test_too_small_grid_traps_nothing(impl):
    assert impl.trap_2d([[1, 2], [3, 4]]) == 0
    assert impl.trap_2d([[1, 2, 3]]) == 0


@pytest.mark.part3
@pytest.mark.edge
def test_ragged_or_empty_grid_raises(impl):
    with pytest.raises(ValueError):
        impl.trap_2d([])
    with pytest.raises(ValueError):
        impl.trap_2d([[1, 2, 3], [4, 5]])
    with pytest.raises(ValueError):
        impl.trap_2d([[1, -2, 3], [4, 5, 6], [7, 8, 9]])


@pytest.mark.part3
@pytest.mark.edge
def test_against_brute_force_2d(impl):
    rng = random.Random(2)
    for _ in range(60):
        m = rng.randint(3, 6)
        n = rng.randint(3, 6)
        grid = [[rng.randint(0, 4) for _ in range(n)] for _ in range(m)]
        assert impl.trap_2d(grid) == _brute_trap_2d(grid), grid


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_bars(run_script):
    rng = random.Random(0)
    heights = [rng.randint(0, 1000) for _ in range(100_000)]
    body = " ".join(map(str, heights)) + "\n"
    r = run_script("PART 2\n" + body, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n1 8 6 2 5 4 8 3 7\n1 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "49\n1\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n0 1 0 2 1 0 1 3 2 1 2 1\n4 2 0 3 2 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n9\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n3\n1 4 3 1 3 2\n3 2 1 3 2 4\n2 3 3 2 3 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "4\n"
