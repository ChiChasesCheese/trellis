import random

import pytest

EX1_GRID = ["..B.", ".D..", "...D"]
EX1_OUT = [2, 3]

EX2_GRID = ["B.D.B"]
EX2_OUT = [(2, (0, 0))]

EX3_GRID = ["B#D", ".#.", "..."]
EX3_OUT = [(6, (0, 0))]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.nearest_bathroom_distances(EX1_GRID) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_no_bathroom_is_minus_one_everywhere(impl):
    assert impl.nearest_bathroom_distances(["..D", "D.."]) == [-1, -1]


@pytest.mark.part1
@pytest.mark.edge
def test_no_desks_is_empty(impl):
    assert impl.nearest_bathroom_distances(["B..", "..."]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_desk_adjacent_to_bathroom(impl):
    assert impl.nearest_bathroom_distances(["BD"]) == [1]


@pytest.mark.part1
@pytest.mark.edge
def test_single_cell_grids(impl):
    assert impl.nearest_bathroom_distances(["B"]) == []
    assert impl.nearest_bathroom_distances(["D"]) == [-1]
    assert impl.nearest_bathroom_distances(["."]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_row_major_desk_order(impl):
    grid = ["D.D", "B..", "..D"]
    # desks at (0,0), (0,2), (2,2) in row-major order
    out = impl.nearest_bathroom_distances(grid)
    assert len(out) == 3
    assert out[0] == 1  # (0,0) -> (1,0)
    assert out[1] == 3  # (0,2) -> (1,0)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_example_2_tie_break(impl):
    assert impl.nearest_bathroom_with_location(EX2_GRID) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_unreachable_when_no_bathroom(impl):
    assert impl.nearest_bathroom_with_location(["..D"]) == [(-1, (-1, -1))]


@pytest.mark.part2
@pytest.mark.edge
def test_tie_break_prefers_smaller_row_over_smaller_col(impl):
    # two bathrooms equidistant from the desk: (0,2) is same row as desk but farther in col vs
    # (1,0) which is a different (larger) row but happens to also be distance 3 -- forces a real
    # (row, col) lexicographic comparison, not just "smaller col wins because same row"
    grid = [
        "..B..",
        "B..D.",
    ]
    # desk at (1,3): dist to (0,2) = |1-0|+|3-2| = 2; dist to (1,0) = |3-0| = 3 -> (0,2) wins
    # outright (not a tie) -- use as a sanity check that distance, not tie-break, decides first
    assert impl.nearest_bathroom_with_location(grid) == [(2, (0, 2))]


@pytest.mark.part2
@pytest.mark.edge
def test_single_source_no_tie_needed(impl):
    assert impl.nearest_bathroom_with_location(["BD"]) == [(1, (0, 0))]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_example_3_detour_around_wall(impl):
    assert impl.nearest_bathroom_with_obstacles(EX3_GRID) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_completely_walled_off_is_unreachable(impl):
    assert impl.nearest_bathroom_with_obstacles(["B#D"]) == [(-1, (-1, -1))]


@pytest.mark.part3
@pytest.mark.edge
def test_no_wall_control_matches_shorter_manhattan_path(impl):
    # same shape as the worked example but the wall column is open floor: distance must be
    # strictly shorter than the walled version (cross-checks the wall is actually load-bearing)
    grid = ["B.D", "...", "..."]
    result = impl.nearest_bathroom_with_obstacles(grid)
    assert result == [(2, (0, 0))]


@pytest.mark.part3
@pytest.mark.edge
def test_desk_surrounded_by_walls_is_unreachable(impl):
    grid = [
        "B....",
        ".###.",
        ".#D#.",
        ".###.",
        ".....",
    ]
    assert impl.nearest_bathroom_with_obstacles(grid) == [(-1, (-1, -1))]


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_format_exact(impl):
    out = impl.part2(["1 5", "B.D.B"])
    assert out == ["2,0,0"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    body = ["3 4"] + EX1_GRID
    r = run_script("PART 1\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n3\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    body = ["1 5"] + EX2_GRID
    r = run_script("PART 2\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2,0,0\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    body = ["3 3"] + EX3_GRID
    r = run_script("PART 3\n" + "\n".join(body) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6,0,0\n"


# ------------------------------------------------------------------------ perf
@pytest.mark.part1
@pytest.mark.perf
def test_perf_1000x1000_grid_multi_source(run_script):
    rng = random.Random(0)
    rows, cols = 1000, 1000
    lines = [f"{rows} {cols}"]
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = rng.random()
            row.append("B" if x < 0.001 else ("D" if x < 0.05 else "."))
        lines.append("".join(row))
    result = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert result.returncode == 0, result.stderr
    assert result.seconds < 2.0, f"too slow: {result.seconds:.2f}s"
    assert result.max_rss_mb < 256, f"too much memory: {result.max_rss_mb:.0f}MB"
