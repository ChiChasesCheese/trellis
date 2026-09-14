import random

import pytest


def _brute_1d(arr):
    twos = [i for i, x in enumerate(arr) if x == 2]
    out = []
    for i, x in enumerate(arr):
        if x == 1:
            out.append(min((abs(i - t) for t in twos), default=-1))
    return out


def _brute_2d(grid):
    if not grid or not grid[0]:
        return []
    twos = [(r, c) for r, row in enumerate(grid) for c, x in enumerate(row) if x == 2]
    out = []
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if x == 1:
                out.append(min((abs(r - tr) + abs(c - tc) for tr, tc in twos), default=-1))
    return out


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example(impl):
    assert impl.nearest_two_distances([2, 0, 1, 0, 1, 0, 0, 2, 1]) == [2, 3, 1]


@pytest.mark.part1
@pytest.mark.edge
def test_no_twos_at_all(impl):
    assert impl.nearest_two_distances([1, 1, 0, 1]) == [-1, -1, -1]


@pytest.mark.part1
@pytest.mark.edge
def test_no_ones_blank_output(impl):
    assert impl.nearest_two_distances([2, 0, 0, 2]) == []
    assert impl.nearest_two_distances([]) == []
    assert impl.nearest_two_distances([0, 0, 0]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_two_adjacent_to_one(impl):
    assert impl.nearest_two_distances([1, 2]) == [1]


@pytest.mark.part1
@pytest.mark.edge
def test_one_is_itself_a_two_neighbor_on_both_sides(impl):
    assert impl.nearest_two_distances([2, 1, 2]) == [1]


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_values_raise(impl):
    with pytest.raises(ValueError):
        impl.nearest_two_distances([0, 1, 3])
    with pytest.raises(ValueError):
        impl.nearest_two_distances([-1])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 20)
        arr = [rng.choice([0, 1, 2]) for _ in range(n)]
        assert impl.nearest_two_distances(arr) == _brute_1d(arr), arr


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_1m(run_script):
    rng = random.Random(1)
    n = 1_000_000
    arr = [rng.choice([0, 0, 0, 1, 2]) for _ in range(n)]
    stdin = f"PART 1\n{n}\n" + " ".join(map(str, arr)) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert len(r.stdout.splitlines()) == arr.count(1)
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_grid(impl):
    grid = [[0, 1, 0], [1, 0, 2], [0, 1, 0]]
    assert impl.nearest_two_distances_grid(grid) == [2, 2, 2]


@pytest.mark.part2
@pytest.mark.edge
def test_grid_no_twos(impl):
    grid = [[1, 0], [0, 1]]
    assert impl.nearest_two_distances_grid(grid) == [-1, -1]


@pytest.mark.part2
@pytest.mark.edge
def test_grid_no_ones(impl):
    assert impl.nearest_two_distances_grid([[0, 2], [2, 0]]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_grid_empty(impl):
    assert impl.nearest_two_distances_grid([]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_grid_ragged_rows_raise(impl):
    with pytest.raises(ValueError):
        impl.nearest_two_distances_grid([[0, 1], [1]])


@pytest.mark.part2
@pytest.mark.edge
def test_grid_invalid_values_raise(impl):
    with pytest.raises(ValueError):
        impl.nearest_two_distances_grid([[0, 3]])


@pytest.mark.part2
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(2)
    for _ in range(150):
        rows = rng.randint(1, 6)
        cols = rng.randint(1, 6)
        grid = [[rng.choice([0, 1, 2]) for _ in range(cols)] for _ in range(rows)]
        assert impl.nearest_two_distances_grid(grid) == _brute_2d(grid), grid


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_large_grid(run_script):
    rng = random.Random(3)
    rows, cols = 500, 500
    grid = [[rng.choice([0, 0, 0, 1, 2]) for _ in range(cols)] for _ in range(rows)]
    lines = [f"PART 2", f"{rows} {cols}"] + [" ".join(map(str, row)) for row in grid]
    stdin = "\n".join(lines) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    expected_ones = sum(row.count(1) for row in grid)
    assert len(r.stdout.splitlines()) == expected_ones
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n9\n2 0 1 0 1 0 0 2 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n3\n1\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part1_blank_when_no_ones(run_script):
    r = run_script("PART 1\n3\n2 0 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == ""


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n3 3\n0 1 0\n1 0 2\n0 1 0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n2\n2\n"
