import random
import time

import pytest


def _brute(m, n, coords, k=2):
    """Reference: materialise the grid (small only)."""
    grid = [[0] * n for _ in range(m)]
    for x, y in coords:
        grid[x][y] = 1
    out = [0] * (k * k + 1)
    for bx in range(m - k + 1):
        for by in range(n - k + 1):
            out[sum(grid[bx + dx][by + dy] for dx in range(k) for dy in range(k))] += 1
    return out


# ---------------------------------------------------------------- Part 1: LC 2768
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.count_black_blocks(3, 3, [[0, 0]]) == [3, 1, 0, 0, 0]
    assert impl.count_black_blocks(3, 3, [[0, 0], [1, 1], [0, 2]]) == [0, 2, 2, 0, 0]


@pytest.mark.part1
@pytest.mark.edge
def test_corner_edge_interior(impl):
    assert impl.count_black_blocks(4, 4, [[1, 1]]) == [5, 4, 0, 0, 0]   # interior: 4 blocks
    assert impl.count_black_blocks(4, 4, [[0, 1]]) == [7, 2, 0, 0, 0]   # top edge: 2 blocks
    assert impl.count_black_blocks(4, 4, [[3, 3]]) == [8, 1, 0, 0, 0]   # bottom-right corner: 1 block
    assert impl.count_black_blocks(4, 4, [[3, 1]]) == [7, 2, 0, 0, 0]   # bottom edge: blocks above it
    assert impl.count_black_blocks(4, 4, [[1, 3]]) == [7, 2, 0, 0, 0]   # right edge: blocks left of it


@pytest.mark.part1
@pytest.mark.edge
def test_empty_full_and_thin_grids(impl):
    assert impl.count_black_blocks(3, 3, []) == [4, 0, 0, 0, 0]
    assert impl.count_black_blocks(2, 2, [[0, 0], [0, 1], [1, 0], [1, 1]]) == [0, 0, 0, 0, 1]
    assert impl.count_black_blocks(2, 5, [[0, 2]]) == [2, 2, 0, 0, 0]    # single row of blocks
    assert impl.count_black_blocks(5, 2, [[2, 0], [2, 1]]) == [2, 0, 2, 0, 0]


@pytest.mark.part1
@pytest.mark.edge
def test_huge_grid_never_materialised(impl):
    m = n = 10**5
    assert impl.count_black_blocks(m, n, []) == [(m - 1) * (n - 1), 0, 0, 0, 0]
    assert impl.count_black_blocks(m, n, [[m - 1, n - 1]]) == [(m - 1) * (n - 1) - 1, 1, 0, 0, 0]
    assert impl.count_black_blocks(m, n, [[50_000, 50_000]]) == [(m - 1) * (n - 1) - 4, 4, 0, 0, 0]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_coordinates_count_once(impl):
    assert impl.count_black_blocks(3, 3, [[0, 0], [0, 0]]) == [3, 1, 0, 0, 0]


@pytest.mark.part1
def test_matches_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        m, n = rng.randint(2, 7), rng.randint(2, 7)
        cells = rng.sample([(x, y) for x in range(m) for y in range(n)], rng.randint(0, m * n))
        coords = [list(c) for c in cells]
        assert impl.count_black_blocks(m, n, coords) == _brute(m, n, coords), (m, n, coords)


# ---------------------------------------------------------------- Part 2: k x k
@pytest.mark.part2
def test_k_examples(impl):
    c = [[0, 0], [1, 1], [0, 2]]
    assert impl.count_black_blocks_k(3, 3, c, 2) == impl.count_black_blocks(3, 3, c)
    assert impl.count_black_blocks_k(3, 3, c, 3) == [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert impl.count_black_blocks_k(3, 3, c, 1) == [6, 3]
    assert impl.count_black_blocks_k(4, 4, [[1, 1]], 3) == [0, 4, 0, 0, 0, 0, 0, 0, 0, 0]


@pytest.mark.part2
@pytest.mark.edge
def test_k_larger_than_grid_and_lengths(impl):
    assert impl.count_black_blocks_k(3, 3, [[0, 0]], 4) == [0] * 17
    assert impl.count_black_blocks_k(3, 5, [[0, 0]], 4) == [0] * 17     # k > m but k <= n
    assert len(impl.count_black_blocks_k(10, 10, [], 5)) == 26
    assert impl.count_black_blocks_k(10, 10, [], 10) == [1] + [0] * 100
    assert impl.count_black_blocks_k(10, 10, [[9, 9]], 10) == [0, 1] + [0] * 99


@pytest.mark.part2
def test_k_matches_brute_force(impl):
    rng = random.Random(1)
    for _ in range(150):
        m, n = rng.randint(2, 7), rng.randint(2, 7)
        k = rng.randint(1, 4)
        cells = rng.sample([(x, y) for x in range(m) for y in range(n)], rng.randint(0, m * n))
        coords = [list(c) for c in cells]
        assert impl.count_black_blocks_k(m, n, coords, k) == _brute(m, n, coords, k), (m, n, k, coords)


# ---------------------------------------------------------------- Part 3: streaming
@pytest.mark.part3
def test_streaming_example(impl):
    bc = impl.BlockCounter(3, 3)
    assert bc.counts() == [4, 0, 0, 0, 0]
    bc.paint(0, 0, True)
    assert bc.counts() == [3, 1, 0, 0, 0]
    bc.paint(1, 1, True)
    assert bc.counts() == [0, 3, 1, 0, 0]
    bc.paint(0, 2, True)
    assert bc.counts() == [0, 2, 2, 0, 0]
    bc.paint(1, 1, False)
    assert bc.counts() == [2, 2, 0, 0, 0]
    bc.paint(1, 1, False)  # idempotent
    assert bc.counts() == [2, 2, 0, 0, 0]


@pytest.mark.part3
@pytest.mark.edge
def test_streaming_idempotent_and_back_to_zero(impl):
    bc = impl.BlockCounter(2, 2)
    bc.paint(0, 0, True)
    bc.paint(0, 0, True)
    assert bc.counts() == [0, 1, 0, 0, 0]
    bc.paint(0, 0, False)
    assert bc.counts() == [1, 0, 0, 0, 0]   # block returns to bucket 0
    for x, y in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        bc.paint(x, y, True)
    assert bc.counts() == [0, 0, 0, 0, 1]
    bc.paint(1, 1, False)
    assert bc.counts() == [0, 0, 0, 1, 0]


@pytest.mark.part3
def test_streaming_matches_batch_after_random_paints(impl):
    rng = random.Random(2)
    for _ in range(60):
        m, n = rng.randint(2, 8), rng.randint(2, 8)
        bc = impl.BlockCounter(m, n)
        black = set()
        for _ in range(40):
            x, y, b = rng.randrange(m), rng.randrange(n), rng.random() < 0.6
            bc.paint(x, y, b)
            (black.add if b else black.discard)((x, y))
            assert bc.counts() == impl.count_black_blocks(m, n, [list(c) for c in black])


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\n3 3\n0,0\n1,1\n0,2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0 2 2 0 0\n"
    assert run_script("PART 1\n3 3\n").stdout == "4 0 0 0 0\n"
    assert run_script("PART 2\n3 3\nK 3\n0,0\n1, 1\n\n0,2\n").stdout == "0 0 0 1 0 0 0 0 0 0\n"
    r = run_script("PART 3\n3 3\nB 0,0\nQ\nB 1,1\nB 0,2\nQ\nW 1,1\nQ\n")
    assert r.stdout == "3 1 0 0 0\n0 2 2 0 0\n2 2 0 0 0\n"
    assert run_script("PART 3\n3 3\n").stdout == ""
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.fmt
def test_stdin_huge_bucket_zero_exact(run_script):
    assert run_script("PART 1\n100000 100000\n").stdout == "9999800001 0 0 0 0\n"
    assert run_script("PART 1\n100000 100000\n99999,99999\n").stdout == "9999800000 1 0 0 0\n"


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    m = n = 10**5
    cells = set()
    while len(cells) < 10_000:
        cells.add((rng.randrange(m), rng.randrange(n)))
    coords = [list(c) for c in cells]
    t0 = time.perf_counter()
    r1 = impl.count_black_blocks(m, n, coords)
    assert sum(r1) == (m - 1) * (n - 1)
    r5 = impl.count_black_blocks_k(m, n, coords, 5)
    assert sum(r5) == (m - 4) * (n - 4)
    bc = impl.BlockCounter(m, n)
    for x, y in coords:
        bc.paint(x, y, True)
    assert bc.counts() == r1
    for x, y in coords:
        bc.paint(x, y, False)
    assert bc.counts() == [(m - 1) * (n - 1), 0, 0, 0, 0]
    assert time.perf_counter() - t0 < 2.0
    text = f"PART 1\n{m} {n}\n" + "\n".join(f"{x},{y}" for x, y in coords) + "\n"
    r = run_script(text)
    assert r.returncode == 0 and r.stdout == " ".join(map(str, r1)) + "\n" and r.seconds < 2.0 and r.max_rss_mb < 256
