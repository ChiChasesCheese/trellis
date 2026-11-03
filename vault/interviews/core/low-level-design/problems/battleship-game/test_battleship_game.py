"""海战棋的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

# 5x5 棋盘，舰队 (3, 2)。
#   玩家 0 的船：(0,0)(0,1)(0,2) 和 (2,0)(2,1)
#   玩家 1 的船：(1,1)(2,1)(3,1) 和 (4,3)(4,4)
P0_SHIPS = {(0, 0), (0, 1), (0, 2), (2, 0), (2, 1)}
P1_SHIPS = {(1, 1), (2, 1), (3, 1), (4, 3), (4, 4)}
# 玩家 1 用来"陪打"的空格，它们都不是玩家 0 的船位。
FILLER = [(3, 0), (3, 2), (3, 3), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 3)]


def new_game(rules=None, place=True):
    g = impl.Game(size=5, fleet=(3, 2), rules=rules or impl.Rules())
    if place:
        g.place_ship(0, 0, 0, 3, True)
        g.place_ship(0, 2, 0, 2, True)
        g.place_ship(1, 1, 1, 3, False)
        g.place_ship(1, 4, 3, 2, True)
    return g


def p0_fires(g, cells, start=0):
    """玩家 0 依次打 cells，玩家 1 每次陪打 FILLER 里的一个空格（从 start 起），返回玩家 0 的结果列表。"""
    out = []
    for i, cell in enumerate(cells):
        out.append(g.fire(0, *cell))
        if g.phase is impl.Phase.PLAYING and g.current_player == 1:
            g.fire(1, *FILLER[start + i])
    return out


# ---- 第 1 关：摆放与开火 ----------------------------------------------------------


def test_part1_valid_placement_and_bad_constructor():
    g = new_game()
    assert isinstance(g, impl.Game)
    for kwargs in ({"size": 0}, {"fleet": ()}, {"fleet": (6,)}, {"fleet": (0,)}):
        with pytest.raises(ValueError):
            impl.Game(**{"size": 5, "fleet": (3, 2), **kwargs})


@pytest.mark.parametrize("row,col,length,horizontal", [
    (0, 3, 3, True),    # 横放从右边出界
    (3, 0, 3, False),   # 竖放从下边出界
    (-1, 0, 3, True),
    (0, -1, 2, False),
    (5, 0, 2, True),
])
def test_part1_out_of_bounds_placement(row, col, length, horizontal):
    g = new_game(place=False)
    with pytest.raises(impl.InvalidPlacementError):
        g.place_ship(0, row, col, length, horizontal)


def test_part1_overlap_and_quota():
    g = new_game(place=False)
    g.place_ship(0, 0, 0, 3, True)
    with pytest.raises(impl.InvalidPlacementError):
        g.place_ship(0, 0, 2, 2, False)   # 与 (0,2) 重叠
    with pytest.raises(impl.InvalidPlacementError):
        g.place_ship(0, 3, 0, 3, True)    # 长度 3 的额度已用完
    with pytest.raises(impl.InvalidPlacementError):
        g.place_ship(0, 3, 0, 4, True)    # 舰队里没有长度 4
    g.place_ship(0, 2, 0, 2, True)        # 失败的尝试没有吃掉额度，正确的船还能摆


def test_part1_two_players_are_independent_and_bad_player():
    g = new_game(place=False)
    g.place_ship(0, 0, 0, 3, True)
    g.place_ship(1, 0, 0, 3, True)        # 同一位置，不同玩家，不冲突
    with pytest.raises(ValueError):
        g.place_ship(2, 0, 0, 2, True)


def test_part1_fire_before_both_fleets_are_placed_and_placing_after():
    g = new_game(place=False)
    with pytest.raises(impl.GameStateError):
        g.fire(0, 0, 0)
    g.place_ship(0, 0, 0, 3, True)
    g.place_ship(0, 2, 0, 2, True)
    with pytest.raises(impl.GameStateError):
        g.fire(0, 0, 0)                   # 玩家 1 还没摆完
    g = new_game()
    with pytest.raises(impl.GameStateError):
        g.place_ship(0, 3, 3, 2, True)


def test_part1_miss_hit_and_sunk():
    g = new_game()
    res = p0_fires(g, [(0, 0), (4, 3), (4, 4)])
    assert res == [impl.ShotResult.MISS, impl.ShotResult.HIT, impl.ShotResult.SUNK]


def test_part1_long_ship_only_sinks_on_its_last_cell():
    g = new_game()
    res = p0_fires(g, [(1, 1), (2, 1), (3, 1)])
    assert res == [impl.ShotResult.HIT, impl.ShotResult.HIT, impl.ShotResult.SUNK]


def test_part1_repeated_and_out_of_bounds_shots():
    g = new_game()
    g.fire(0, 0, 0)
    g.fire(1, 3, 0)
    with pytest.raises(impl.AlreadyFiredError):
        g.fire(0, 0, 0)
    for cell in [(5, 0), (0, 5), (-1, 0)]:
        with pytest.raises(impl.InvalidShotError):
            g.fire(0, *cell)


def test_part1_a_hit_cell_cannot_be_hit_twice():
    g = new_game()
    g.fire(0, 1, 1)
    g.fire(1, 3, 0)
    with pytest.raises(impl.AlreadyFiredError):
        g.fire(0, 1, 1)


# ---- 第 2 关：回合与胜负 ----------------------------------------------------------


def test_part2_phase_and_first_player():
    g = new_game(place=False)
    assert g.phase is impl.Phase.PLACING and g.current_player is None and g.winner is None
    g = new_game()
    assert g.phase is impl.Phase.PLAYING and g.current_player == 0


def test_part2_turns_alternate_and_out_of_turn_is_rejected():
    g = new_game()
    with pytest.raises(impl.NotYourTurnError):
        g.fire(1, 3, 0)
    g.fire(0, 0, 0)
    assert g.current_player == 1
    with pytest.raises(impl.NotYourTurnError):
        g.fire(0, 0, 1)
    g.fire(1, 3, 0)
    assert g.current_player == 0


def test_part2_failed_shots_do_not_consume_the_turn():
    g = new_game()
    g.fire(0, 0, 0)
    g.fire(1, 3, 0)
    with pytest.raises(impl.AlreadyFiredError):
        g.fire(0, 0, 0)
    with pytest.raises(impl.InvalidShotError):
        g.fire(0, 9, 9)
    assert g.current_player == 0
    g.fire(0, 0, 1)


def test_part2_remaining_ships_and_winner():
    g = new_game()
    assert g.remaining_ships(0) == 2 and g.remaining_ships(1) == 2
    p0_fires(g, [(4, 3), (4, 4)])
    assert g.remaining_ships(1) == 1 and g.remaining_ships(0) == 2
    res = p0_fires(g, [(1, 1), (2, 1), (3, 1)], start=2)
    assert res[-1] is impl.ShotResult.SUNK
    assert g.phase is impl.Phase.OVER and g.winner == 0 and g.current_player is None
    assert g.remaining_ships(1) == 0


def test_part2_nothing_can_be_fired_after_the_game_is_over():
    g = new_game()
    p0_fires(g, sorted(P1_SHIPS))
    for player in (0, 1):
        with pytest.raises(impl.GameStateError):
            g.fire(player, 0, 4)


def test_part2_second_player_can_win_too():
    g = new_game()
    g.fire(0, 0, 4)
    for i, cell in enumerate(sorted(P0_SHIPS)):
        g.fire(1, *cell)
        if i < 4:
            g.fire(0, *FILLER[i])
    assert g.winner == 1 and g.phase is impl.Phase.OVER


# ---- 第 3 关：规则变体与视图 ------------------------------------------------------


def test_part3_no_touching_rejects_side_end_and_diagonal_contact():
    g = impl.Game(size=5, fleet=(3, 2, 2), rules=impl.Rules(touching_allowed=False))
    g.place_ship(0, 0, 0, 3, True)
    for row, col, horizontal in [(1, 0, True), (0, 3, False), (1, 3, True), (1, 2, False)]:
        with pytest.raises(impl.InvalidPlacementError):
            g.place_ship(0, row, col, 2, horizontal)
    g.place_ship(0, 2, 0, 2, True)        # 隔一行就可以
    g.place_ship(0, 0, 4, 2, False)       # 隔一列也可以


def test_part3_touching_is_allowed_by_default_and_only_own_ships_count():
    g = impl.Game(size=5, fleet=(3, 2))
    g.place_ship(0, 0, 0, 3, True)
    g.place_ship(0, 1, 0, 2, True)
    strict = impl.Game(size=5, fleet=(3, 2), rules=impl.Rules(touching_allowed=False))
    strict.place_ship(0, 0, 0, 3, True)
    strict.place_ship(1, 1, 0, 2, True)   # 对手的船不影响我


def test_part3_extra_turn_on_hit():
    g = new_game(rules=impl.Rules(extra_turn_on_hit=True))
    g.fire(0, 4, 3)                        # HIT：继续
    assert g.current_player == 0
    g.fire(0, 4, 4)                        # SUNK：继续
    assert g.current_player == 0
    g.fire(0, 0, 0)                        # MISS：换人
    assert g.current_player == 1
    g.fire(1, 3, 0)
    assert g.current_player == 0


def test_part3_winning_shot_ends_the_game_even_with_extra_turns():
    g = new_game(rules=impl.Rules(extra_turn_on_hit=True))
    for cell in sorted(P1_SHIPS):
        g.fire(0, *cell)
    assert g.phase is impl.Phase.OVER and g.winner == 0


def test_part3_board_view_hides_the_opponents_ships():
    g = new_game()
    assert g.board_view(0, 1) == ["....."] * 5
    g.fire(0, 1, 1)
    g.fire(1, 3, 0)
    g.fire(0, 0, 0)
    assert g.board_view(0, 1) == ["o....", ".X...", ".....", ".....", "....."]
    assert g.board_view(1, 1) == ["o....", ".X...", ".#...", ".#...", "...##"]
    assert g.board_view(0, 0) == ["###..", ".....", "##...", "o....", "....."]


def test_part3_board_view_marks_own_hits_and_misses_and_returns_a_copy():
    g = new_game()
    g.fire(0, 0, 4)
    g.fire(1, 0, 1)    # 命中玩家 0 的船
    g.fire(0, 0, 3)
    g.fire(1, 3, 0)    # 落空
    view = g.board_view(0, 0)
    assert view == ["#X#..", ".....", "##...", "o....", "....."]
    view[0] = "ZZZZZ"
    assert g.board_view(0, 0)[0] == "#X#.."
    assert len(view) == 5 and all(len(row) == 5 for row in view)


def test_part3_rejected_placement_changes_nothing():
    g = impl.Game(size=5, fleet=(3, 2), rules=impl.Rules(touching_allowed=False))
    g.place_ship(0, 0, 0, 3, True)
    with pytest.raises(impl.InvalidPlacementError):
        g.place_ship(0, 1, 0, 2, True)
    assert g.board_view(0, 0)[1] == "....."
    g.place_ship(0, 2, 0, 2, True)


# ---- 第 4 关：齐射 ----------------------------------------------------------------


def salvo_game():
    return new_game(rules=impl.Rules(salvo=True))


def test_part4_salvo_fires_one_shot_per_surviving_ship_and_passes_the_turn():
    g = salvo_game()
    res = g.fire_salvo(0, [(4, 3), (0, 0)])
    assert res == [impl.ShotResult.HIT, impl.ShotResult.MISS]
    assert g.current_player == 1
    assert g.board_view(0, 1)[4] == "...X."


def test_part4_wrong_shot_count_is_rejected():
    g = salvo_game()
    for cells in ([(0, 0)], [(0, 0), (0, 1), (0, 2)], []):
        with pytest.raises(impl.InvalidShotError):
            g.fire_salvo(0, cells)
    assert g.current_player == 0


def test_part4_an_illegal_shot_cancels_the_whole_salvo():
    g = salvo_game()
    g.fire_salvo(0, [(0, 0), (4, 3)])
    g.fire_salvo(1, [(3, 0), (4, 0)])
    with pytest.raises(impl.AlreadyFiredError):
        g.fire_salvo(0, [(1, 1), (0, 0)])      # 第二发打过了：第一发 (1,1) 也不能生效
    with pytest.raises(impl.AlreadyFiredError):
        g.fire_salvo(0, [(1, 1), (1, 1)])      # 同一齐射里重复
    with pytest.raises(impl.InvalidShotError):
        g.fire_salvo(0, [(1, 1), (9, 9)])
    assert g.board_view(0, 1)[1] == "....."
    assert g.current_player == 0


def test_part4_salvo_size_shrinks_when_your_ships_sink():
    g = salvo_game()
    g.fire_salvo(0, [(0, 4), (1, 4)])
    g.fire_salvo(1, [(2, 0), (2, 1)])          # 打沉玩家 0 的 2 格船
    assert g.remaining_ships(0) == 1
    with pytest.raises(impl.InvalidShotError):
        g.fire_salvo(0, [(3, 0), (3, 1)])
    g.fire_salvo(0, [(3, 0)])


def test_part4_modes_do_not_mix():
    g = salvo_game()
    with pytest.raises(impl.GameStateError):
        g.fire(0, 0, 0)
    h = new_game()
    with pytest.raises(impl.GameStateError):
        h.fire_salvo(0, [(0, 0), (0, 1)])


def test_part4_salvo_can_win_and_turn_rules_still_apply():
    g = salvo_game()
    with pytest.raises(impl.NotYourTurnError):
        g.fire_salvo(1, [(0, 0), (0, 1)])
    cells = sorted(P1_SHIPS)
    g.fire_salvo(0, cells[:2])
    g.fire_salvo(1, [(3, 0), (3, 2)])
    g.fire_salvo(0, cells[2:4])
    g.fire_salvo(1, [(3, 3)])
    res = g.fire_salvo(0, [cells[4], (0, 4)])
    assert res[0] is impl.ShotResult.SUNK
    assert g.phase is impl.Phase.OVER and g.winner == 0
