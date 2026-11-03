"""四子棋的测试：`-k part1` 选第 1 关，依此类推。线程测试用屏障和有上限的等待，不靠 sleep 估时间。"""

import importlib
import itertools
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Status = impl.Status

T = 5.0

# 手工验证过的棋谱（列号序列，X 先手）
HORIZONTAL_X = (0, 5, 3, 6, 2, 5, 1)                       # X 在第 0 行占 0-3 列
VERTICAL_X = (0, 3, 0, 1, 0, 6, 0)                         # X 在第 0 列占 0-3 行
DIAGONAL_O = (2, 0, 1, 2, 3, 1, 3, 2, 3, 3)               # O 占 (0,0) (1,1) (2,2) (3,3)，最后一步赢
ANTI_DIAGONAL_X = (3, 2, 4, 2, 4, 2, 5, 3, 2, 0, 3)        # X 占 (0,5) (1,4) (2,3) (3,2)


def play(game, *columns):
    return [game.drop(c) for c in columns]


# ---- 第 1 关：落子、轮流、输赢、平局 ------------------------------------------


def test_part1_new_game_is_empty_and_x_moves_first():
    g = impl.Game()
    assert (g.rows, g.cols, g.connect, g.players) == (6, 7, 4, ("X", "O"))
    assert g.current_player == "X" and g.status is Status.IN_PROGRESS and g.winner is None
    assert all(g.cell(r, c) is None for r in range(6) for c in range(7))


def test_part1_drop_returns_the_landing_row_and_discs_stack_up():
    g = impl.Game()
    assert play(g, 3, 3, 3, 4) == [0, 1, 2, 0]
    assert [g.cell(r, 3) for r in range(4)] == ["X", "O", "X", None]
    assert g.cell(0, 4) == "O"


def test_part1_players_alternate_and_failed_drops_do_not_consume_the_turn():
    g = impl.Game(rows=2)
    play(g, 0, 0)
    assert g.current_player == "X"
    with pytest.raises(impl.ColumnFull):
        g.drop(0)
    assert g.current_player == "X"                            # 列满：回合不变
    for bad in (-1, 7, 100, "3", 2.0, None, True):
        with pytest.raises(impl.InvalidColumn):
            g.drop(bad)
    assert g.current_player == "X" and g.cell(0, 1) is None
    g.drop(1)
    assert g.current_player == "O"


def test_part1_render_draws_the_top_row_first():
    g = impl.Game(rows=3, cols=4)
    play(g, 1, 1, 3)
    assert g.render() == "....\n.O..\n.X.X"
    assert impl.Game(rows=1, cols=2, connect=2).render() == ".."


def test_part1_horizontal_win():
    g = impl.Game()
    play(g, *HORIZONTAL_X[:-1])
    assert g.status is Status.IN_PROGRESS
    g.drop(HORIZONTAL_X[-1])
    assert (g.status, g.winner, g.current_player) == (Status.WON, "X", None)


def test_part1_vertical_win():
    g = impl.Game()
    play(g, *VERTICAL_X)
    assert (g.status, g.winner) == (Status.WON, "X")


def test_part1_both_diagonals_win():
    g = impl.Game()
    play(g, *DIAGONAL_O)
    assert (g.status, g.winner) == (Status.WON, "O")
    g = impl.Game()
    play(g, *ANTI_DIAGONAL_X)
    assert (g.status, g.winner) == (Status.WON, "X")


def test_part1_three_in_a_row_is_not_a_win_and_a_gap_breaks_the_line():
    g = impl.Game()
    play(g, 0, 0, 1, 1, 2)                                    # X 在第 0 行占 0 1 2
    assert g.status is Status.IN_PROGRESS
    g = impl.Game()
    play(g, 0, 0, 1, 1, 3, 3, 4, 4)                           # X: 0 1 _ 3 4  中间空着
    assert g.status is Status.IN_PROGRESS
    g.drop(2)                                                 # 补上中间那一格：五连也算赢
    assert g.winner == "X"


def test_part1_no_moves_after_the_game_is_over():
    g = impl.Game()
    play(g, *VERTICAL_X)
    for column in (0, 1, 99):                                 # 对局结束的检查先于列号检查
        with pytest.raises(impl.GameOver):
            g.drop(column)
    assert g.render().count("X") == 4


def test_part1_full_board_without_a_line_is_a_draw():
    g = impl.Game(rows=2, cols=3, connect=3)
    play(g, 0, 2, 0, 2, 1, 1)
    assert (g.status, g.winner, g.current_player) == (Status.DRAW, None, None)
    assert g.render() == "XOO\nXXO"
    with pytest.raises(impl.GameOver):
        g.drop(0)


def test_part1_a_winning_last_disc_beats_a_full_board():
    g = impl.Game(rows=1, cols=4, connect=2)
    play(g, 3, 1, 0, 2)                                       # O 的最后一子连成 1-2，棋盘同时放满
    assert (g.status, g.winner) == (Status.WON, "O")


@pytest.mark.parametrize("kw", [
    dict(rows=0), dict(cols=0), dict(connect=1), dict(connect=8), dict(players=("X",)),
    dict(players=("X", "X")), dict(players=("X", "OO")), dict(players=()),
])
def test_part1_invalid_configuration_is_rejected(kw):
    with pytest.raises(ValueError):
        impl.Game(**kw)


def test_part1_custom_connect_and_three_players():
    g = impl.Game(rows=3, cols=3, connect=3, players=("A", "B", "C"))
    play(g, 0, 1, 2)
    assert g.current_player == "A"
    play(g, 0, 1, 2)                                          # A B C 轮流叠两层
    assert g.status is Status.IN_PROGRESS
    g.drop(0)                                                 # A 第三个：第 0 列竖着三连
    assert (g.status, g.winner) == (Status.WON, "A")


def test_part1_cell_outside_the_board_is_an_index_error():
    g = impl.Game()
    for rc in ((-1, 0), (6, 0), (0, 7), (0, -1)):
        with pytest.raises(IndexError):
            g.cell(*rc)


# ---- 第 2 关：撤销、回放、复制 ------------------------------------------------


def test_part2_undo_restores_board_and_turn():
    g = impl.Game()
    play(g, 3, 3, 4)
    before = g.render()
    assert g.undo() == 4
    assert g.current_player == "X" and g.cell(0, 4) is None       # 又轮到撤销掉的那一步的主人
    assert g.moves == (3, 3)
    g.drop(4)
    assert g.render() == before and g.moves == (3, 3, 4)


def test_part2_undo_after_a_win_reopens_the_game():
    g = impl.Game()
    play(g, *VERTICAL_X)
    assert g.winner == "X" and g.winning_line
    assert g.undo() == 0
    assert (g.status, g.winner, g.winning_line, g.current_player) == (Status.IN_PROGRESS, None, (), "X")
    g.drop(5)                                                 # 可以换一步继续下
    assert g.status is Status.IN_PROGRESS


def test_part2_undo_after_a_draw_reopens_the_game():
    g = impl.Game(rows=2, cols=3, connect=3)
    play(g, 0, 2, 0, 2, 1, 1)
    assert g.status is Status.DRAW
    g.undo()
    assert g.status is Status.IN_PROGRESS and g.legal_moves() == (1,)


def test_part2_undo_on_an_empty_game_raises():
    g = impl.Game()
    with pytest.raises(impl.NothingToUndo):
        g.undo()
    g.drop(0)
    g.undo()
    with pytest.raises(impl.NothingToUndo):
        g.undo()


def test_part2_moves_is_an_immutable_snapshot():
    g = impl.Game()
    play(g, 1, 2)
    m = g.moves
    g.drop(3)
    assert m == (1, 2) and g.moves == (1, 2, 3) and isinstance(m, tuple)


def test_part2_legal_moves_skip_full_columns_and_vanish_when_over():
    g = impl.Game(rows=2, cols=3, connect=3)
    assert g.legal_moves() == (0, 1, 2)
    play(g, 0, 2, 0)
    assert g.legal_moves() == (1, 2)                          # 第 0 列满了
    play(g, 2, 1, 1)                                          # 平局收场
    assert g.status is Status.DRAW and g.legal_moves() == ()
    g2 = impl.Game()
    play(g2, *VERTICAL_X)
    assert g2.legal_moves() == ()


def test_part2_winning_line_lists_every_cell_of_the_run():
    g = impl.Game()
    assert g.winning_line == ()
    play(g, *HORIZONTAL_X)
    assert g.winning_line == ((0, 0), (0, 1), (0, 2), (0, 3))
    g = impl.Game()
    play(g, *ANTI_DIAGONAL_X)
    assert g.winning_line == ((0, 5), (1, 4), (2, 3), (3, 2))
    g = impl.Game()
    play(g, 0, 0, 1, 1, 3, 3, 4, 4, 2)                        # 五连：整条线都要列出来
    assert g.winning_line == ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))


def test_part2_from_moves_replays_a_game_and_rejects_illegal_histories():
    g = impl.Game.from_moves(DIAGONAL_O)
    assert (g.status, g.winner) == (Status.WON, "O") and g.moves == DIAGONAL_O
    h = impl.Game.from_moves([3, 3], rows=4, cols=5, connect=3)
    assert (h.rows, h.cols, h.connect) == (4, 5, 3) and h.current_player == "X"
    with pytest.raises(impl.InvalidColumn):
        impl.Game.from_moves([0, 9])
    with pytest.raises(impl.ColumnFull):
        impl.Game.from_moves([0] * 7, connect=7)
    with pytest.raises(impl.GameOver):
        impl.Game.from_moves(VERTICAL_X + (1,))


def test_part2_copy_is_independent():
    g = impl.Game()
    play(g, 3, 3)
    c = g.copy()
    c.drop(0)
    assert g.moves == (3, 3) and c.moves == (3, 3, 0)
    g.undo()
    assert c.moves == (3, 3, 0)
    assert (c.rows, c.cols, c.connect, c.players) == (6, 7, 4, ("X", "O"))


def test_part2_undoing_everything_returns_to_the_empty_board():
    rng = random.Random(7)
    for _ in range(20):
        g = impl.Game()
        while g.status is Status.IN_PROGRESS:
            g.drop(rng.choice(g.legal_moves()))
        replay = impl.Game.from_moves(g.moves)
        assert replay.render() == g.render() and replay.status == g.status and replay.winning_line == g.winning_line
        while g.moves:
            g.undo()
        assert g.render() == impl.Game().render() and g.status is Status.IN_PROGRESS and g.current_player == "X"


# ---- 第 3 关：多局对战服务 ----------------------------------------------------


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make_service(**kw):
    clock = FakeClock()
    return impl.GameService(clock=clock, **kw), clock


def test_part3_create_games_and_play_a_move():
    svc, _ = make_service()
    g1 = svc.create_game("alice", "bob")
    g2 = svc.create_game("alice", "carol", rows=4, cols=4, connect=3)
    assert g1 != g2
    r = svc.move(g1, "alice", 3)
    assert r == impl.MoveResult(0, Status.IN_PROGRESS, None)
    v = svc.view(g1)
    assert (v.status, v.winner, v.current_player, v.moves, v.reason) == (Status.IN_PROGRESS, None, "bob", (3,), None)
    assert v.board[-1] == "...X..." and len(v.board) == 6
    assert svc.view(g2).board == ("....",) * 4


def test_part3_only_the_player_whose_turn_it_is_may_move():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob")
    with pytest.raises(impl.NotYourTurn):
        svc.move(g, "bob", 0)
    svc.move(g, "alice", 0)
    with pytest.raises(impl.NotYourTurn):
        svc.move(g, "alice", 1)
    with pytest.raises(impl.NotAPlayer):
        svc.move(g, "mallory", 1)
    with pytest.raises(impl.UnknownGame):
        svc.move("nope", "alice", 1)
    with pytest.raises(impl.UnknownGame):
        svc.view("nope")


def test_part3_a_bad_move_does_not_consume_the_turn():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob", rows=1, cols=2, connect=2)
    with pytest.raises(impl.InvalidColumn):
        svc.move(g, "alice", 5)
    svc.move(g, "alice", 0)
    with pytest.raises(impl.ColumnFull):
        svc.move(g, "bob", 0)
    assert svc.view(g).current_player == "bob"


def test_part3_winning_ends_the_game_with_ids_not_marks():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob")
    for column, who in zip(VERTICAL_X, itertools.cycle(("alice", "bob"))):
        last = svc.move(g, who, column)
    assert last == impl.MoveResult(3, Status.WON, "alice")
    v = svc.view(g)
    assert (v.status, v.winner, v.current_player, v.reason) == (Status.WON, "alice", None, "connect")
    with pytest.raises(impl.GameOver):
        svc.move(g, "bob", 0)
    with pytest.raises(impl.GameOver):
        svc.resign(g, "bob")


def test_part3_a_draw_is_reported():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob", rows=2, cols=3, connect=3)
    for column, who in zip((0, 2, 0, 2, 1, 1), itertools.cycle(("alice", "bob"))):
        svc.move(g, who, column)
    v = svc.view(g)
    assert (v.status, v.winner, v.current_player, v.reason) == (Status.DRAW, None, None, "draw")


def test_part3_resigning_hands_the_win_to_the_opponent_at_any_time():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob")
    svc.resign(g, "bob")                                       # 没轮到 bob 也可以认输
    v = svc.view(g)
    assert (v.status, v.winner, v.current_player, v.reason) == (Status.WON, "alice", None, "resign")
    with pytest.raises(impl.GameOver):
        svc.move(g, "alice", 0)
    with pytest.raises(impl.GameOver):
        svc.resign(g, "alice")
    g2 = svc.create_game("alice", "bob")
    with pytest.raises(impl.NotAPlayer):
        svc.resign(g2, "mallory")


def test_part3_timeouts_forfeit_the_player_who_is_too_slow():
    svc, clock = make_service(move_seconds=30)
    g = svc.create_game("alice", "bob")
    clock.advance(29.5)
    svc.move(g, "alice", 0)                                    # 29.5 秒：来得及
    clock.advance(29.5)
    svc.move(g, "bob", 1)                                      # 计时从上一步重新算
    clock.advance(30)                                          # 轮到 alice，已经满 30 秒
    with pytest.raises(impl.GameOver):
        svc.move(g, "alice", 2)
    v = svc.view(g)
    assert (v.status, v.winner, v.reason, v.moves) == (Status.WON, "bob", "timeout", (0, 1))


def test_part3_timeout_is_applied_to_views_and_resignations_too():
    svc, clock = make_service(move_seconds=10)
    g = svc.create_game("alice", "bob")
    clock.advance(10)
    assert svc.view(g).reason == "timeout" and svc.view(g).winner == "bob"
    with pytest.raises(impl.GameOver):
        svc.resign(g, "alice")                                 # 已经超时判负，不能再改成认输
    g2 = svc.create_game("alice", "bob")
    svc.move(g2, "alice", 0)
    clock.advance(10)
    with pytest.raises(impl.GameOver):
        svc.move(g2, "alice", 1)                               # 超时的是 bob；alice 试图连走两步，一样是对局已结束
    assert svc.view(g2).winner == "alice"


def test_part3_without_a_limit_nobody_times_out():
    svc, clock = make_service()
    g = svc.create_game("alice", "bob")
    clock.advance(10 ** 9)
    assert svc.view(g).status is Status.IN_PROGRESS
    svc.move(g, "alice", 0)


def test_part3_create_game_validates_players_and_board():
    svc, _ = make_service()
    for args in (("a", "a"), ("", "b"), ("a", "")):
        with pytest.raises(ValueError):
            svc.create_game(*args)
    with pytest.raises(ValueError):
        svc.create_game("a", "b", connect=1)


def test_part3_view_is_a_snapshot_that_does_not_expose_the_game():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob")
    svc.move(g, "alice", 0)
    v = svc.view(g)
    svc.move(g, "bob", 0)
    assert v.moves == (0,) and svc.view(g).moves == (0, 0)
    assert isinstance(v.board, tuple) and isinstance(v.moves, tuple)


def test_part3_concurrent_moves_by_the_same_player_succeed_exactly_once():
    svc, _ = make_service()
    g = svc.create_game("alice", "bob")
    n = 8
    barrier = threading.Barrier(n)
    outcomes = []

    def worker(i):
        barrier.wait(T)
        try:
            svc.move(g, "alice", i % 7)
            outcomes.append("ok")
        except impl.NotYourTurn:
            outcomes.append("not-your-turn")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert sorted(outcomes) == ["not-your-turn"] * 7 + ["ok"]
    assert len(svc.view(g).moves) == 1 and svc.view(g).current_player == "bob"


def test_part3_many_games_progress_concurrently():
    svc, _ = make_service()
    games = [svc.create_game("alice", "bob") for _ in range(4)]
    barrier = threading.Barrier(len(games) * 2)

    def player(gid, name, column):
        barrier.wait(T)
        while True:
            try:
                svc.move(gid, name, column)
            except impl.NotYourTurn:
                continue                                       # 等对手走完
            except impl.GameOver:
                return

    threads = [threading.Thread(target=player, args=(gid, name, col), daemon=True)
               for gid in games for name, col in (("alice", 0), ("bob", 1))]
    [t.start() for t in threads]
    [t.join(T * 2) for t in threads]
    assert not any(t.is_alive() for t in threads)
    for gid in games:
        v = svc.view(gid)
        assert (v.status, v.winner, v.moves) == (Status.WON, "alice", (0, 1) * 3 + (0,))


# ---- 第 4 关（选做）：机器人 ---------------------------------------------------


def test_part4_takes_an_immediate_win():
    g = impl.Game.from_moves([0, 0, 1, 1, 2, 2])               # X 在第 0 行占 0 1 2，第 3 列能赢
    assert impl.best_move(g) == 3
    assert impl.best_move(g, depth=1) == 3


def test_part4_blocks_the_opponents_immediate_win():
    g = impl.Game.from_moves([0, 1, 0, 2, 5, 3])               # O 在第 0 行占 1 2 3，X 必须堵第 4 列
    assert g.current_player == "X"
    assert impl.best_move(g) == 4
    assert impl.best_move(g, depth=2) == 4


def test_part4_opens_in_the_centre_and_is_deterministic():
    g = impl.Game()
    assert impl.best_move(g) == 3
    assert impl.best_move(g) == impl.best_move(g)
    assert impl.best_move(impl.Game(cols=6), depth=2) in (2, 3)


def test_part4_never_changes_the_game_it_is_given():
    g = impl.Game.from_moves([3, 3, 2, 4])
    snapshot = (g.moves, g.render(), g.status)
    impl.best_move(g)
    assert (g.moves, g.render(), g.status) == snapshot
    g.drop(0)                                                  # 之后照常可以继续下


def test_part4_only_picks_legal_columns():
    g = impl.Game(rows=2, cols=3, connect=3)
    play(g, 0, 0, 1, 1)                                        # 0、1 两列已满，只剩第 2 列
    assert impl.best_move(g) == 2


def _wins(g, column):
    """当前玩家在 column 落子会不会立刻赢（不改变 g）。"""
    mover = g.current_player
    g.drop(column)
    won = g.winner == mover
    g.undo()
    return won


def _hands_over_a_win(g, column):
    """当前玩家在 column 落子后，对手是否有一步立刻获胜（不改变 g）。"""
    g.drop(column)
    bad = g.status is Status.IN_PROGRESS and any(_wins(g, d) for d in g.legal_moves())
    g.undo()
    return bad


def test_part4_never_hands_over_a_win_and_always_takes_one_when_it_can():
    rng = random.Random(11)
    checked = 0
    for _ in range(150):
        g = impl.Game(rows=5, cols=5, connect=4)
        for _ in range(rng.randint(4, 14)):
            if g.status is not Status.IN_PROGRESS:
                break
            g.drop(rng.choice(g.legal_moves()))
        if g.status is not Status.IN_PROGRESS:
            continue
        winning = [c for c in g.legal_moves() if _wins(g, c)]
        safe = [c for c in g.legal_moves() if not _hands_over_a_win(g, c)]
        choice = impl.best_move(g, depth=3)
        assert choice in g.legal_moves()
        if winning:
            assert choice in winning                           # 能赢就赢
        elif safe:
            assert choice in safe                              # 不能赢就别送对手一步杀
        checked += 1
    assert checked > 50


def test_part4_refuses_unsupported_games():
    g = impl.Game.from_moves(VERTICAL_X)
    with pytest.raises(impl.GameOver):
        impl.best_move(g)
    with pytest.raises(ValueError):
        impl.best_move(impl.Game(players=("A", "B", "C")))
