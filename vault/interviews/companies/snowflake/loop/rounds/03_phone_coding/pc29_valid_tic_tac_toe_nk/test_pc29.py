import itertools
import random

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_examples_part1(impl):
    assert impl.valid_tic_tac_toe(["O  ", "   ", "   "]) is False
    assert impl.valid_tic_tac_toe(["XOX", " X ", "  O"]) is True


@pytest.mark.part1
@pytest.mark.edge
def test_empty_board_is_valid(impl):
    assert impl.valid_tic_tac_toe(["   ", "   ", "   "]) is True


@pytest.mark.part1
@pytest.mark.edge
def test_both_win_invalid(impl):
    assert impl.valid_tic_tac_toe(["XXX", "   ", "OOO"]) is False


@pytest.mark.part1
@pytest.mark.edge
def test_two_lines_sharing_a_cell_valid(impl):
    assert impl.valid_tic_tac_toe(["XXX", "XOO", "XOO"]) is True


@pytest.mark.part1
def test_part1_exhaustive_against_brute_force(impl):
    """Every one of the 3^9 possible 3x3 boards, checked against a full BFS over the game tree
    (LC 794's known reachable-state count is 5478)."""
    reachable = impl.enumerate_reachable_boards(3, 3)
    reachable_spaces = {tuple(row.replace(".", " ") for row in b) for b in reachable}
    assert len(reachable_spaces) == 5478
    mismatches = 0
    for cells in itertools.product("XO ", repeat=9):
        board = ["".join(cells[r * 3 : r * 3 + 3]) for r in range(3)]
        expected = tuple(board) in reachable_spaces
        if impl.valid_tic_tac_toe(board) != expected:
            mismatches += 1
    assert mismatches == 0


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_examples_part2(impl):
    assert impl.valid_tic_tac_toe_nk(["O  ", "   ", "   "], 3, 3) is False
    assert impl.valid_tic_tac_toe_nk(["XOX", " X ", "  O"], 3, 3) is True


@pytest.mark.part2
@pytest.mark.edge
def test_three_lines_pairwise_intersecting_but_no_common_cell_is_invalid(impl):
    """The key subtlety documented in problem.md: X has three winning lines (row, column,
    diagonal) that pairwise intersect but share NO single common cell -- unreachable, even
    though every pair of lines does share a cell."""
    board = ["XO  ", "OXOO", " XXX", "OX  "]
    assert impl.valid_tic_tac_toe_nk(board, 4, 3) is False


@pytest.mark.part2
@pytest.mark.edge
def test_two_lines_with_common_cell_on_bigger_board(impl):
    board = ["XXX ", "XOO ", "XOO ", "    "]
    assert impl.valid_tic_tac_toe_nk(board, 4, 3) is True


@pytest.mark.part2
def test_part2_random_against_brute_force_n4(impl):
    n, k, max_moves = 4, 3, 6
    reachable = impl.enumerate_reachable_boards(n, k, max_moves=max_moves)
    reachable_spaces = {tuple(row.replace(".", " ") for row in b) for b in reachable}
    rng = random.Random(0)
    mismatches = 0
    for _ in range(500):
        m = rng.randint(0, max_moves)
        cells = rng.sample(range(n * n), m)
        grid = [[" "] * n for _ in range(n)]
        for idx in cells:
            r, c = divmod(idx, n)
            grid[r][c] = rng.choice("XO")
        board = ["".join(row) for row in grid]
        expected = tuple(board) in reachable_spaces
        if impl.valid_tic_tac_toe_nk(board, n, k) != expected:
            mismatches += 1
    assert mismatches == 0


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_worked_examples_part3(impl):
    assert impl.valid_tic_tac_toe_reason(["O  ", "   ", "   "], 3, 3) == "COUNT"
    assert impl.valid_tic_tac_toe_reason(["XXX", "   ", "OOO"], 3, 3) == "BOTH_WIN"
    assert impl.valid_tic_tac_toe_reason(["XOX", " X ", "  O"], 3, 3) == "OK"
    assert impl.valid_tic_tac_toe_reason(["XXX", "XOO", "XOO"], 3, 3) == "OK"


@pytest.mark.part3
@pytest.mark.edge
def test_double_win_impossible_reason(impl):
    board = ["XO  ", "OXOO", " XXX", "OX  "]
    assert impl.valid_tic_tac_toe_reason(board, 4, 3) == "DOUBLE_WIN_IMPOSSIBLE"


@pytest.mark.part3
@pytest.mark.edge
def test_x_win_bad_count_reason(impl):
    # #X == #O (passes the general alternating-turns check), but X has a winning line, which
    # requires #X - #O == 1 specifically (X's winning move must be the very last move).
    board = ["XXX", "OO ", "  O"]
    assert impl.valid_tic_tac_toe_reason(board, 3, 3) == "X_WIN_BAD_COUNT"


@pytest.mark.part3
@pytest.mark.edge
def test_o_win_bad_count_reason(impl):
    # #O == #X - 1 (passes the general alternating-turns check), but O has a winning line, which
    # requires #X == #O exactly (O's winning move must be the very last move).
    board = ["OOO", "XX ", "XX "]
    assert impl.valid_tic_tac_toe_reason(board, 3, 3) == "O_WIN_BAD_COUNT"


@pytest.mark.part3
def test_reason_ok_iff_bool_true(impl):
    rng = random.Random(3)
    n, k = 3, 3
    for cells in list(itertools.product("XO ", repeat=9))[::37]:  # sample every 37th of 19683
        board = ["".join(cells[r * 3 : r * 3 + 3]) for r in range(3)]
        reason = impl.valid_tic_tac_toe_reason(board, n, k)
        expected_bool = impl.valid_tic_tac_toe_nk(board, n, k)
        assert (reason == "OK") == expected_bool, (board, reason, expected_bool)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_large_board_many_queries(run_script):
    rng = random.Random(0)
    n, k = 30, 5
    boards = []
    for _ in range(300):
        grid = [[rng.choice(" XO") for _ in range(n)] for _ in range(n)]
        boards.append(["".join(row).replace(" ", "_") for row in grid])
    # PART 2 format expects one "SIZE n k" line followed by n board rows, per board.
    blocks = []
    for b in boards:
        blocks.append(f"SIZE {n} {k}")
        blocks.extend(b)
    stdin = f"PART 2\nN {len(boards)}\n" + "\n".join(blocks) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 300
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = "PART 1\nN 2\nO__\n___\n___\nXOX\n_X_\n__O\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\ntrue\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = "PART 2\nN 1\nSIZE 4 3\nXO__\nOXOO\n_XXX\nOX__\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    stdin = "PART 3\nN 1\nSIZE 4 3\nXO__\nOXOO\n_XXX\nOX__\n"
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "DOUBLE_WIN_IMPOSSIBLE\n"
