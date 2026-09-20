"""井字棋参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def make_game(size: int = 3, k=None, marks: str = "XO"):
    players = [impl.Player(name=f"P{i}", mark=m) for i, m in enumerate(marks)]
    return impl.Game(impl.Board(size=size, k=k), players)


def play(game, *cells):
    """按 (row, col) 元组序列依次落子，返回最后一手。"""
    move = None
    for row, col in cells:
        move = game.play(impl.Cell(row, col))
    return move


# ---- 第 1 关：3×3 两个人类 --------------------------------------------------


def test_new_game_is_in_progress_and_first_player_moves_first():
    game = make_game()
    assert game.state is impl.GameState.IN_PROGRESS
    assert game.winner is None
    assert game.current_player.mark == "X"
    assert game.board.moves_played == 0


def test_players_alternate_and_marks_land_where_asked():
    game = make_game()
    play(game, (0, 0), (1, 1))
    assert game.board.mark_at(impl.Cell(0, 0)) == "X"
    assert game.board.mark_at(impl.Cell(1, 1)) == "O"
    assert game.current_player.mark == "X"


def test_a_full_row_wins():
    game = make_game()
    play(game, (0, 0), (1, 0), (0, 1), (1, 1), (0, 2))
    assert game.state is impl.GameState.WIN
    assert game.winner.mark == "X"


def test_a_full_column_wins():
    game = make_game()
    play(game, (0, 2), (0, 0), (1, 2), (1, 1), (2, 2))
    assert game.state is impl.GameState.WIN
    assert game.winner.mark == "X"


def test_both_diagonals_win():
    main = make_game()
    play(main, (0, 0), (0, 1), (1, 1), (0, 2), (2, 2))
    assert main.winner.mark == "X"
    anti = make_game()
    play(anti, (0, 2), (0, 0), (1, 1), (0, 1), (2, 0))
    assert anti.winner.mark == "X"


def test_draw_is_decided_by_moves_played_not_by_a_scan():
    game = make_game()
    # X O X / X O O / O X X —— 满盘无线
    play(game, (0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2))
    assert game.state is impl.GameState.DRAW
    assert game.winner is None
    assert game.board.moves_played == 9
    assert game.board.is_full


# ---- 非法着法：都是有名字的异常，不是返回 False ------------------------------


def test_playing_on_a_taken_cell_raises_and_does_not_consume_the_turn():
    game = make_game()
    play(game, (1, 1))
    with pytest.raises(impl.CellTakenError):
        game.play(impl.Cell(1, 1))
    assert game.current_player.mark == "O"
    assert game.board.moves_played == 1


def test_playing_off_the_board_raises():
    game = make_game()
    with pytest.raises(impl.OutOfBoardError):
        game.play(impl.Cell(3, 0))
    with pytest.raises(impl.OutOfBoardError):
        game.play(impl.Cell(-1, 0))
    assert game.board.moves_played == 0


def test_playing_out_of_turn_raises():
    game = make_game()
    second = game.players[1]
    with pytest.raises(impl.NotYourTurnError):
        game.play(impl.Cell(0, 0), by=second)
    assert game.board.moves_played == 0
    game.play(impl.Cell(0, 0), by=game.players[0])
    assert game.board.moves_played == 1


def test_playing_after_the_game_is_over_raises():
    game = make_game()
    play(game, (0, 0), (1, 0), (0, 1), (1, 1), (0, 2))
    with pytest.raises(impl.GameOverError):
        game.play(impl.Cell(2, 2))


def test_free_cells_is_a_snapshot_that_cannot_change_the_board():
    game = make_game()
    before = game.board.free_cells()
    play(game, (0, 0))
    assert len(before) == 9 and len(game.board.free_cells()) == 8
    assert isinstance(before, tuple)


# ---- 第 2 关：N×N 与 K 子连珠 ----------------------------------------------


def test_five_by_five_needs_a_full_line_by_default():
    game = make_game(size=5)
    assert game.board.k == 5
    play(game, (0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3))
    assert game.state is impl.GameState.IN_PROGRESS   # 四子还不够
    play(game, (0, 4))
    assert game.winner.mark == "X"


def test_k_in_a_row_wins_without_filling_the_line():
    game = make_game(size=5, k=4)
    play(game, (0, 0), (4, 0), (1, 1), (4, 1), (2, 2), (4, 2), (3, 3))
    assert game.state is impl.GameState.WIN
    assert game.winner.mark == "X"


def test_k_in_a_row_counts_both_sides_of_the_last_stone():
    # 中间补上的一子把左右两段接起来，只往一侧走的实现会漏掉它
    game = make_game(size=5, k=4)
    play(game, (2, 0), (4, 0), (2, 1), (4, 1), (2, 3), (4, 2))
    assert game.state is impl.GameState.IN_PROGRESS
    game.play(impl.Cell(2, 2))
    assert game.winner.mark == "X"


def test_completes_line_answers_the_hypothetical_before_the_move():
    game = make_game(size=3)
    play(game, (0, 0), (2, 0), (0, 1), (2, 1))
    board = game.board
    assert impl.completes_line(board, impl.Cell(0, 2), "X", 3) is True
    assert impl.completes_line(board, impl.Cell(1, 2), "X", 3) is False
    assert board.moves_played == 4     # 问一句不该改变盘面


def test_the_incremental_rule_and_the_predicate_agree_on_random_games():
    rng = random.Random(20260920)
    for _ in range(30):
        board = impl.Board(size=4)
        marks, expected_by_rule = ("A", "B"), []
        for i, cell in enumerate(rng.sample(board.free_cells(), 16)):
            mark = marks[i % 2]
            predicted = impl.completes_line(board, cell, mark, board.k)
            assert board.place(cell, mark) is predicted
            expected_by_rule.append(predicted)
            if predicted:
                break
        assert expected_by_rule


# ---- 第 3 关：悔棋与重做 ----------------------------------------------------


def test_undo_takes_back_the_winning_move_and_reopens_the_game():
    game = make_game()
    play(game, (0, 0), (1, 0), (0, 1), (1, 1), (0, 2))
    assert game.state is impl.GameState.WIN
    move = game.undo()
    assert move.cell == impl.Cell(0, 2)
    assert game.state is impl.GameState.IN_PROGRESS
    assert game.winner is None
    assert game.board.mark_at(impl.Cell(0, 2)) is None
    assert game.current_player.mark == "X"


def test_redo_replays_the_undone_move_and_a_new_move_clears_the_redo_stack():
    game = make_game()
    play(game, (0, 0), (1, 1))
    game.undo()
    game.undo()
    assert (game.undo_depth, game.redo_depth) == (0, 2)
    game.redo()
    assert game.board.mark_at(impl.Cell(0, 0)) == "X"
    assert (game.undo_depth, game.redo_depth) == (1, 1)
    game.play(impl.Cell(2, 2))                      # 走出新的分支
    assert game.redo_depth == 0
    with pytest.raises(impl.NothingToRedoError):
        game.redo()


def test_undo_on_an_empty_history_raises():
    game = make_game()
    with pytest.raises(impl.NothingToUndoError):
        game.undo()


def test_undoing_every_move_empties_the_rule_counters():
    game = make_game()
    play(game, (0, 0), (1, 1), (0, 1), (2, 2))
    assert game.board.win_rule.line_count > 0
    while game.undo_depth:
        game.undo()
    assert game.board.win_rule.line_count == 0      # 有界的结构必须能缩回去
    assert game.board.moves_played == 0


# ---- 第 4 关：机器人，不碰 Board 和 Game ------------------------------------


def test_random_bot_only_ever_picks_a_free_cell_and_is_reproducible():
    def finished(seed):
        game = impl.Game(impl.Board(size=3), [
            impl.Player("R1", "X", impl.random_bot(random.Random(seed))),
            impl.Player("R2", "O", impl.random_bot(random.Random(seed + 1)))])
        impl.play_out(game)
        return [m.cell for m in game.moves]

    first = finished(11)
    assert finished(11) == first
    assert len(set(first)) == len(first)            # 没有重复落点
    assert len(first) <= 9


def test_heuristic_bot_takes_the_win_when_it_has_one():
    game = make_game()
    play(game, (0, 0), (2, 0), (0, 1), (2, 1))
    bot = impl.heuristic_bot(random.Random(1))
    assert bot(game.board, "X") == impl.Cell(0, 2)


def test_heuristic_bot_blocks_the_opponent_when_it_cannot_win():
    game = make_game()
    play(game, (1, 1), (0, 0), (2, 2), (0, 1))
    bot = impl.heuristic_bot(random.Random(1))
    assert bot(game.board, "X") == impl.Cell(0, 2)  # 自己没有立即胜着，只能堵 O


def test_heuristic_bot_opens_in_the_centre():
    game = make_game()
    bot = impl.heuristic_bot(random.Random(3))
    assert bot(game.board, "X") == impl.Cell(1, 1)


def test_a_heuristic_bot_never_loses_to_a_random_bot_on_three_by_three():
    for seed in range(12):
        game = impl.Game(impl.Board(size=3), [
            impl.Player("bot", "X", impl.heuristic_bot(random.Random(seed))),
            impl.Player("rnd", "O", impl.random_bot(random.Random(seed + 100)))])
        impl.play_out(game)
        assert game.state in (impl.GameState.WIN, impl.GameState.DRAW)
        assert game.winner is None or game.winner.mark == "X"


def test_play_turn_refuses_a_human_player():
    game = make_game()
    with pytest.raises(impl.NoStrategyError):
        game.play_turn()
    assert game.players[0].is_bot is False


# ---- 扩展的证据：三个人、更大的盘，都不用改 Board 和 Game --------------------


def test_three_players_rotate_in_order_on_a_four_by_four_board():
    game = make_game(size=4, k=3, marks="XOZ")
    assert [game.current_player.mark for _ in range(1)] == ["X"]
    play(game, (0, 0), (3, 0), (3, 3))
    assert game.current_player.mark == "X"
    assert [m.mark for m in game.moves] == ["X", "O", "Z"]


def test_duplicate_marks_are_rejected_at_construction():
    with pytest.raises(ValueError):
        impl.Game(impl.Board(), [impl.Player("a", "X"), impl.Player("b", "X")])
    with pytest.raises(ValueError):
        impl.Game(impl.Board(), [impl.Player("a", "X")])
