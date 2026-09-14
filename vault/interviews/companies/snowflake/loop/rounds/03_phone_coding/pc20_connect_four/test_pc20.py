import random

import pytest


def _brute_can_play_win(board, x, y, player):
    """Independent reference: scan the WHOLE board for any length-4 run of `player` that
    includes (x, y), instead of expanding outward from the point."""
    rows, cols = len(board), len(board[0])
    for dx, dy in ((0, 1), (1, 0), (1, 1), (1, -1)):
        for sx in range(rows):
            for sy in range(cols):
                cells = []
                for k in range(4):
                    cx, cy = sx + dx * k, sy + dy * k
                    if not (0 <= cx < rows and 0 <= cy < cols):
                        cells = None
                        break
                    cells.append((cx, cy))
                if cells is None:
                    continue
                if (x, y) in cells and all(board[cx][cy] == player for cx, cy in cells):
                    return True
    return False


def _empty_board(rows, cols):
    return [["" for _ in range(cols)] for _ in range(rows)]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_horizontal_win(impl):
    board = _empty_board(4, 5)
    for c in range(4):
        board[3][c] = "a"
    assert impl.can_play_win(board, 3, 3, "a") is True


@pytest.mark.part1
def test_vertical_win(impl):
    board = _empty_board(5, 4)
    for r in range(4):
        board[r][0] = "b"
    assert impl.can_play_win(board, 3, 0, "b") is True


@pytest.mark.part1
def test_diagonal_backslash_win(impl):
    board = _empty_board(4, 4)
    for i in range(4):
        board[i][i] = "a"
    assert impl.can_play_win(board, 0, 0, "a") is True
    assert impl.can_play_win(board, 3, 3, "a") is True


@pytest.mark.part1
def test_diagonal_slash_win(impl):
    board = _empty_board(4, 4)
    board[3][0] = board[2][1] = board[1][2] = board[0][3] = "a"
    assert impl.can_play_win(board, 3, 0, "a") is True


@pytest.mark.part1
@pytest.mark.edge
def test_only_three_in_a_row_is_not_a_win(impl):
    board = _empty_board(4, 5)
    for c in range(3):
        board[0][c] = "a"
    assert impl.can_play_win(board, 0, 2, "a") is False


@pytest.mark.part1
@pytest.mark.edge
def test_placed_cell_not_matching_player_raises(impl):
    board = _empty_board(3, 3)
    board[0][0] = "b"
    with pytest.raises(ValueError):
        impl.can_play_win(board, 0, 0, "a")


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_bounds_raises(impl):
    board = _empty_board(3, 3)
    with pytest.raises(ValueError):
        impl.can_play_win(board, 5, 5, "a")


@pytest.mark.part1
@pytest.mark.edge
def test_bad_player_raises(impl):
    board = _empty_board(3, 3)
    board[0][0] = "c"
    with pytest.raises(ValueError):
        impl.can_play_win(board, 0, 0, "c")


@pytest.mark.part1
@pytest.mark.edge
def test_against_brute_force_random_boards(impl):
    rng = random.Random(0)
    for _ in range(200):
        rows, cols = rng.randint(4, 7), rng.randint(4, 7)
        board = _empty_board(rows, cols)
        for r in range(rows):
            for c in range(cols):
                board[r][c] = rng.choice(["a", "b", "", "", ""])
        x, y = rng.randrange(rows), rng.randrange(cols)
        if board[x][y] == "":
            continue
        player = board[x][y]
        assert impl.can_play_win(board, x, y, player) == _brute_can_play_win(board, x, y, player), (board, x, y)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_drop_lands_on_bottom_of_empty_column(impl):
    board = _empty_board(4, 4)
    row, win = impl.drop_and_check(board, 2, "a")
    assert row == 3
    assert win is False
    assert board[3][2] == "a"


@pytest.mark.part2
def test_drop_stacks_on_existing_pieces(impl):
    board = _empty_board(4, 4)
    board[3][0] = "a"
    board[2][0] = "b"
    row, win = impl.drop_and_check(board, 0, "a")
    assert row == 1
    assert board[1][0] == "a"


@pytest.mark.part2
def test_drop_detects_win(impl):
    board = _empty_board(4, 4)
    board[3][0] = board[3][1] = board[3][2] = "a"
    row, win = impl.drop_and_check(board, 3, "a")
    assert row == 3
    assert win is True


@pytest.mark.part2
@pytest.mark.edge
def test_drop_full_column_raises(impl):
    board = _empty_board(2, 2)
    board[0][0] = "a"
    board[1][0] = "b"
    with pytest.raises(ValueError):
        impl.drop_and_check(board, 0, "a")


@pytest.mark.part2
@pytest.mark.edge
def test_drop_out_of_range_column_raises(impl):
    board = _empty_board(3, 3)
    with pytest.raises(ValueError):
        impl.drop_and_check(board, 3, "a")


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_game_starts_with_player_a(impl):
    game = impl.ConnectFour(4, 4)
    assert game.current_player() == "a"
    assert game.winner() is None
    assert game.is_draw() is False


@pytest.mark.part3
def test_turns_alternate(impl):
    game = impl.ConnectFour(4, 4)
    game.drop(0)
    assert game.current_player() == "b"
    game.drop(1)
    assert game.current_player() == "a"


@pytest.mark.part3
def test_vertical_win_ends_game(impl):
    game = impl.ConnectFour(4, 4)
    for col in (0, 1, 0, 1, 0, 1, 0):
        game.drop(col)
    assert game.winner() == "a"
    assert game.is_draw() is False
    with pytest.raises(ValueError):
        game.drop(2)


@pytest.mark.part3
@pytest.mark.edge
def test_draw_when_board_fills_without_a_winner(impl):
    game = impl.ConnectFour(4, 4)
    # a drop sequence (found by brute search over shuffles of the full 16-move multiset) that
    # fills the whole 4x4 board with no 4-in-a-row anywhere -- a genuine draw.
    moves = [0, 2, 1, 3, 3, 0, 2, 3, 1, 2, 1, 2, 0, 1, 3, 0]
    for col in moves:
        game.drop(col)
    assert game.winner() is None
    assert game.is_draw() is True
    with pytest.raises(ValueError):
        game.drop(0)


@pytest.mark.part3
@pytest.mark.edge
def test_invalid_column_raises(impl):
    game = impl.ConnectFour(4, 4)
    with pytest.raises(ValueError):
        game.drop(4)
    with pytest.raises(ValueError):
        game.drop(-1)


@pytest.mark.part3
@pytest.mark.edge
def test_full_column_raises_but_game_continues(impl):
    game = impl.ConnectFour(4, 4)
    for col in (0, 0, 0, 0):  # fills col0 with a,b,a,b (turns alternate globally) -- no win
        game.drop(col)
    assert game.winner() is None
    with pytest.raises(ValueError):
        game.drop(0)  # col0 is full
    assert game.winner() is None  # the failed drop must not have mutated game state
    # game is not over -- a different column still works
    game.drop(1)


@pytest.mark.part3
def test_tiny_board_minimum_size(impl):
    game = impl.ConnectFour(4, 4)
    assert game.current_player() == "a"
    with pytest.raises(ValueError):
        impl.ConnectFour(3, 4)
    with pytest.raises(ValueError):
        impl.ConnectFour(4, 3)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_board_scan(run_script):
    rows, cols = 500, 500
    row_str = ",".join(["a"] * cols)
    board_str = ";".join([row_str] * rows)
    line = f"{board_str} | {rows - 1} {cols - 1} a"
    r = run_script("PART 1\n" + line + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "true"
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    board = "a,a,a,_;_,_,_,_;_,_,_,_;_,_,_,_"
    r = run_script(f"PART 1\n{board} | 0 2 a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "false\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    board = "_,_,_,_;_,_,_,_;_,_,_,_;_,_,_,_"
    r = run_script(f"PART 2\n{board} | 2 a\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "3 false\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n4 4\n0\n1\n0\n1\n0\n1\n0\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[-1] == "0 b a false"
