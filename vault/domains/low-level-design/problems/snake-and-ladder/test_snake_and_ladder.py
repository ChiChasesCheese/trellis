"""蛇梯棋参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。

一道掷骰子的题最容易写出会偶发失败的测试。这里的做法只有两条：要么把骰子换成定死的序列
（`SequenceDie`），要么固定随机种子并断言**与种子无关的不变量**（谁都不会跑出棋盘、
一轮之内位置变化首尾相接）。没有一处断言依赖"大概会怎样"。
"""

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def board(last_square=20, jumps=()):
    """一块小棋盘，默认 20 格、没有跳跃。"""
    return impl.Board(last_square, [impl.Jump(a, b) for a, b in jumps])


def game(pips, *, players=("Alice", "Bob"), last_square=20, jumps=(), **kwargs):
    """用定死的点数序列开一局：`pips` 按掷骰顺序给出，和回合无关。"""
    return impl.Game(board(last_square, jumps), list(players), die=impl.SequenceDie(pips), **kwargs)


def reasons(record):
    """一轮之内发生的变化原因序列，测试按它断言"发生了什么"。"""
    return [c.reason for c in record.changes]


# ---- 第 1 关：棋盘校验 -----------------------------------------------------


def test_a_jump_whose_end_is_another_jumps_start_is_rejected():
    """甲的终点是乙的起点，一次掷骰就会连跳——这是这道题存在的理由，必须在构造时就炸。"""
    with pytest.raises(impl.InvalidBoardError):
        board(jumps=[(3, 12), (12, 5)])


def test_two_jumps_may_not_share_a_start_square():
    with pytest.raises(impl.InvalidBoardError):
        board(jumps=[(3, 12), (3, 7)])


def test_a_jump_may_not_start_on_the_first_or_the_last_square():
    """起点格上的跳跃开局前就触发，终点格上的跳跃永远踩不到——两者都是坏配置。"""
    with pytest.raises(impl.InvalidBoardError):
        board(jumps=[(0, 12)])
    with pytest.raises(impl.InvalidBoardError):
        board(jumps=[(20, 3)])
    with pytest.raises(impl.InvalidBoardError):
        board(jumps=[(12, 0)])


def test_a_jump_may_end_on_the_last_square():
    """直通终点的梯子（经典棋盘上的 80→100）完全合法。"""
    assert board(jumps=[(8, 20)]).jump_count == 1
    assert impl.classic_board().jump_from(80).end == 100


def test_a_zero_length_jump_is_rejected_by_the_value_itself():
    with pytest.raises(impl.InvalidBoardError):
        impl.Jump(7, 7)


def test_direction_decides_snake_or_ladder_and_the_table_is_readable():
    b = board(jumps=[(3, 12), (15, 5)])
    assert b.jump_count == 2
    assert b.jump_from(3).kind is impl.JumpKind.LADDER
    assert b.jump_from(15).is_snake is True
    assert b.jump_from(7) is None
    with pytest.raises(TypeError):
        b.jumps[4] = impl.Jump(4, 9)


# ---- 第 1 关：回合循环 -----------------------------------------------------


def test_players_take_turns_and_a_roll_moves_exactly_that_many_squares():
    g = game([3, 4])
    first = g.play_turn()
    assert first.player == "Alice"
    assert g.position_of("Alice") == 3
    assert g.current_player == "Bob"
    second = g.play_turn()
    assert second.player == "Bob"
    assert g.position_of("Bob") == 4
    assert g.turns_played == 2


def test_a_ladder_climbs_and_a_snake_slides_and_both_are_in_the_log():
    g = game([3, 16], jumps=[(3, 12), (16, 5)], players=("A", "B"))
    up = g.play_turn()
    assert g.position_of("A") == 12
    assert reasons(up) == [impl.ChangeReason.ROLL, impl.ChangeReason.LADDER]
    assert up.landed_on == 12
    down = g.play_turn()
    assert g.position_of("B") == 5
    assert reasons(down) == [impl.ChangeReason.ROLL, impl.ChangeReason.SNAKE]
    assert [c.to for c in down.changes] == [16, 5]


def test_landing_on_a_jumps_end_square_does_nothing():
    """12 是梯子的终点而不是起点，踩上去不该再动——这正是校验保证的"最多跳一次"。"""
    g = game([12], jumps=[(3, 12)])
    record = g.play_turn()
    assert g.position_of("Alice") == 12
    assert reasons(record) == [impl.ChangeReason.ROLL]


def test_exact_landing_is_required_and_an_overshoot_wastes_the_turn():
    g = game([6, 1, 6, 1, 6, 1, 5, 1, 2])
    for _ in range(6):
        g.play_turn()
    assert g.position_of("Alice") == 18
    blocked = g.play_turn()
    assert g.position_of("Alice") == 18
    assert reasons(blocked) == [impl.ChangeReason.BLOCKED]
    assert g.winner is None
    g.play_turn()
    won = g.play_turn()
    assert won.finishers == ("Alice",)
    assert g.winner == "Alice"
    assert g.is_over is True


def test_a_ladder_onto_the_last_square_wins_but_an_overshoot_still_wastes_the_turn():
    """两条规则各管各的：梯子负责移动，"怎么算赢"只由终点规则说了算，两者不打架。"""
    climbed = game([8], jumps=[(8, 20)])
    record = climbed.play_turn()
    assert reasons(record) == [impl.ChangeReason.ROLL, impl.ChangeReason.LADDER]
    assert climbed.position_of("Alice") == 20
    assert record.finishers == ("Alice",)
    assert climbed.winner == "Alice" and climbed.is_over is True

    missed = game([6, 1, 6, 1, 6, 1, 5], jumps=[(8, 20)])
    for _ in range(6):
        missed.play_turn()
    assert missed.position_of("Alice") == 18
    blocked = missed.play_turn()
    assert reasons(blocked) == [impl.ChangeReason.BLOCKED]
    assert missed.position_of("Alice") == 18 and missed.winner is None


def test_no_more_turns_once_the_game_is_over():
    g = game([6, 1, 6, 1, 6, 1, 2])
    for _ in range(7):
        g.play_turn()
    assert g.is_over
    with pytest.raises(impl.GameOverError):
        g.play_turn()


def test_a_broken_die_is_caught_by_the_game_not_by_the_caller():
    g = impl.Game(board(), ["Alice", "Bob"], die=lambda: 0)
    with pytest.raises(impl.InvalidRollError):
        g.play_turn()


def test_a_game_needs_at_least_two_distinct_players():
    with pytest.raises(impl.InvalidPlayersError):
        impl.Game(board(), ["Alice"])
    with pytest.raises(impl.InvalidPlayersError):
        impl.Game(board(), ["Alice", "Alice"])
    with pytest.raises(impl.InvalidPlayersError):
        impl.Game(board(), ["Alice", "Bob"]).position_of("Zoe")


# ---- 第 2 关：可替换的骰子与玩法 -------------------------------------------


def test_the_same_seed_replays_the_same_game():
    def run():
        g = impl.Game(impl.classic_board(), ["A", "B", "C"], rng=random.Random(2024))
        g.play()
        return [(r.player, r.rolls, r.changes) for r in g.log]

    assert run() == run()


def test_six_to_start_keeps_a_player_at_the_start_square():
    rules = impl.RuleSet(may_start=impl.six_to_start)
    g = game([3, 3, 6, 1], rules=rules)
    stuck = g.play_turn()
    assert g.position_of("Alice") == 0
    assert reasons(stuck) == [impl.ChangeReason.NOT_STARTED]
    g.play_turn()
    g.play_turn()
    assert g.position_of("Alice") == 6


def test_an_extra_turn_on_six_moves_twice_instead_of_summing_the_pips():
    """6 之后再掷 2：必须先踩到 6（触发梯子）再走 2，而不是一步走 8 把梯子跨过去。"""
    rules = impl.RuleSet(roll_again=impl.extra_turn_on_six)
    g = game([6, 2], last_square=40, jumps=[(6, 30)], rules=rules)
    record = g.play_turn()
    assert record.rolls == (6, 2)
    assert reasons(record) == [impl.ChangeReason.ROLL, impl.ChangeReason.LADDER, impl.ChangeReason.ROLL]
    assert g.position_of("Alice") == 32
    assert g.current_player == "Bob"


def test_three_sixes_void_the_whole_turn_including_the_two_steps_already_taken():
    rules = impl.RuleSet(roll_again=impl.three_sixes_cancel)
    g = game([6, 6, 6], last_square=40, rules=rules)
    record = g.play_turn()
    assert record.cancelled is True
    assert record.rolls == (6, 6, 6)
    assert record.changes == ()
    assert record.landed_on is None
    assert g.position_of("Alice") == 0
    assert g.turns_played == 1
    assert g.current_player == "Bob"


def test_a_bouncing_finish_rule_replaces_the_exact_one_without_touching_the_game():
    rules = impl.RuleSet(destination=impl.overshoot_bounces)
    g = game([6, 1, 6, 1, 6, 1, 5], rules=rules)
    for _ in range(6):
        g.play_turn()
    assert g.position_of("Alice") == 18
    g.play_turn()
    assert g.position_of("Alice") == 17


def test_a_rule_that_never_stops_rolling_fails_loudly_instead_of_hanging():
    rules = impl.RuleSet(roll_again=lambda rolls: impl.RollAgain.AGAIN)
    g = game([1] * 100, last_square=1000, rules=rules, max_rolls_per_turn=8)
    with pytest.raises(impl.RuleLoopError):
        g.play_turn()


# ---- 第 3 关：多人、名次与走子日志 -----------------------------------------


def test_many_players_get_a_full_ranking_not_just_a_winner():
    g = impl.Game(impl.classic_board(), ["A", "B", "C", "D"], rng=random.Random(5))
    result = g.play()
    assert result.outcome is impl.Outcome.WON
    assert [s.rank for s in result.standings] == [1, 2, 3, 4]
    assert result.winner == result.standings[0].player
    assert result.standings[0].finished_on_turn is not None
    assert all(s.finished_on_turn is None for s in result.standings[1:])
    assert [s.position for s in result.standings[1:]] == sorted(
        (s.position for s in result.standings[1:]), reverse=True
    )


def test_playing_to_the_end_skips_finished_players_and_ranks_everyone_who_arrived():
    g = impl.Game(impl.classic_board(), ["A", "B", "C"], rng=random.Random(9), play_to_the_end=True)
    result = g.play()
    finished = [s for s in result.standings if s.finished_on_turn is not None]
    assert len(finished) == 2
    assert finished[0].finished_on_turn < finished[1].finished_on_turn
    assert all(r.player != result.winner for r in g.log if r.turn > finished[0].finished_on_turn)


def test_the_log_is_a_snapshot_and_turn_count_survives_truncation():
    g = game([1] * 8, log_limit=3)
    for _ in range(8):
        g.play_turn()
    assert g.turns_played == 8
    assert len(g.log) == 3
    assert [r.turn for r in g.log] == [6, 7, 8]
    assert isinstance(g.log, tuple)


def test_positions_are_handed_out_as_a_read_only_snapshot():
    g = game([3])
    snapshot = g.positions
    with pytest.raises(TypeError):
        snapshot["Alice"] = 99
    g.play_turn()
    assert snapshot["Alice"] == 0
    assert g.positions["Alice"] == 3


def test_a_subscriber_is_fed_events_and_can_unsubscribe():
    seen = []
    g = game([1, 1, 1, 1])
    stop = g.subscribe(seen.append)
    g.play_turn()
    g.play_turn()
    stop()
    g.play_turn()
    assert [r.turn for r in seen] == [1, 2]
    assert seen[0].player == "Alice" and seen[0].rolls == (1,)


def test_the_scripted_die_reports_how_many_rolls_are_left():
    die = impl.SequenceDie([1, 2, 3])
    assert die.rolls_left == 3
    assert die() == 1
    assert die.rolls_left == 2
    die()
    die()
    with pytest.raises(impl.InvalidRollError):
        die()


# ---- 第 4 关：靠组合加规则，不碰回合循环 -----------------------------------


def test_a_teleport_square_is_added_by_composition():
    plain = game([4], jumps=[(3, 12)])
    plain.play_turn()
    assert plain.position_of("Alice") == 4

    rules = impl.RuleSet(effects=(impl.teleport(4, 17),))
    g = game([4], jumps=[(3, 12)], rules=rules)
    record = g.play_turn()
    assert g.position_of("Alice") == 17
    assert reasons(record) == [impl.ChangeReason.ROLL, impl.ChangeReason.EFFECT]


def test_a_double_move_square_uses_the_pips_that_brought_you_there():
    rules = impl.RuleSet(effects=(impl.double_move(5),))
    g = game([5], rules=rules)
    g.play_turn()
    assert g.position_of("Alice") == 10


def test_a_swap_square_moves_two_players_in_one_turn():
    rules = impl.RuleSet(effects=(impl.swap_with_leader(4),))
    g = game([9, 4], last_square=20, rules=rules)
    g.play_turn()
    assert g.position_of("Alice") == 9
    record = g.play_turn()
    assert g.position_of("Bob") == 9
    assert g.position_of("Alice") == 4
    assert [c.player for c in record.changes] == ["Bob", "Bob", "Alice"]


def test_an_effect_that_moves_a_stranger_or_leaves_the_board_is_refused():
    def rogue(ctx):
        return (impl.PositionChange("Zoe", ctx.square, ctx.square + 1, impl.ChangeReason.EFFECT),)

    def overboard(ctx):
        return (impl.PositionChange(ctx.player, ctx.square, 999, impl.ChangeReason.EFFECT),)

    for bad in (rogue, overboard):
        g = game([3], rules=impl.RuleSet(effects=(bad,)))
        with pytest.raises(impl.SnakeLadderError):
            g.play_turn()


# ---- 与种子无关的不变量：随机也不许让测试变飘 -------------------------------


def test_invariants_hold_for_every_seed():
    """跑三十局固定种子的完整棋局，断言的全是"任何一局都必须成立"的性质。"""
    for seed in range(30):
        g = impl.Game(
            impl.classic_board(),
            ["A", "B", "C"],
            rng=random.Random(seed),
            rules=impl.RuleSet(roll_again=impl.three_sixes_cancel, effects=(impl.swap_with_leader(42),)),
            play_to_the_end=True,
        )
        result = g.play()
        assert result.outcome is impl.Outcome.WON, f"种子 {seed} 没能在轮数上限内分出胜负"
        assert all(0 <= s.position <= 100 for s in result.standings)
        last = {p: 0 for p in g.players}
        for record in g.log:
            assert record.cancelled == (record.changes == ())
            for change in record.changes:
                assert change.frm == last[change.player], "一轮之内的位置变化必须首尾相接"
                assert 0 <= change.to <= 100
                last[change.player] = change.to
        assert {s.player: s.position for s in result.standings} == last
