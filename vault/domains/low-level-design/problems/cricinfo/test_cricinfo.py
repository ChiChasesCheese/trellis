import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

BATTING = ["opener1", "opener2", "no3", "no4", "no5"]
BOWLING = ["bowlerA", "bowlerB", "bowlerC"]


def make_innings(overs_limit=None, batting=BATTING, bowling=BOWLING):
    return impl.Innings("I1", batting, bowling, overs_limit)


# ---- 第 1 关：一个球就是一条事件，统计现算 ------------------------------------


def test_normal_delivery_updates_runs_and_balls_faced():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=4))
    state = innings.state()
    assert state.total_runs == 4
    assert state.legal_balls == 1
    assert state.batters["opener1"].runs == 4
    assert state.batters["opener1"].balls_faced == 1
    assert state.batters["opener1"].fours == 1


def test_scorecard_is_recomputed_not_stored_across_multiple_balls():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=1))
    innings.record("bowlerA", impl.BallOutcome(bat_runs=6))
    first = innings.state()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=2))
    second = innings.state()
    assert first.total_runs == 7
    assert second.total_runs == 9
    assert second.batters["opener2"].sixes == 1  # 奇数跑动后 opener2 接了第二球


# ---- 第 2 关：额外球、出局、轮转 ------------------------------------------------


def test_wide_is_illegal_and_does_not_credit_the_batter():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(extra=impl.Extra.WIDE))
    state = innings.state()
    assert state.total_runs == 1          # 判罚的那一分
    assert state.legal_balls == 0         # 不算一颗合法球
    assert state.batters["opener1"].runs == 0
    assert state.batters["opener1"].balls_faced == 0   # 面对了，但不计入"面对球数"


def test_wide_with_extra_runs_adds_penalty_plus_the_runs_run():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(extra=impl.Extra.WIDE, extra_runs=2))
    assert innings.state().total_runs == 3   # 1 分判罚 + 跑动的 2 分


def test_bye_is_legal_and_does_not_credit_the_batter():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(extra=impl.Extra.BYE, extra_runs=2))
    state = innings.state()
    assert state.total_runs == 2
    assert state.legal_balls == 1
    assert state.batters["opener1"].runs == 0
    assert state.batters["opener1"].balls_faced == 1   # 但确实面对了这一球


def test_bowler_runs_conceded_excludes_byes_but_includes_wides():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(extra=impl.Extra.BYE, extra_runs=4))
    innings.record("bowlerA", impl.BallOutcome(extra=impl.Extra.WIDE))
    stats = innings.state().bowlers["bowlerA"]
    assert stats.runs_conceded == 1   # 只有 wide 判罚的那一分算在投手头上


def test_four_off_a_no_ball_credits_the_batter_and_adds_the_penalty_to_the_team():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=4, extra=impl.Extra.NO_BALL))
    state = innings.state()
    assert state.batters["opener1"].runs == 4     # 打出去的分照记在击球手头上
    assert state.batters["opener1"].fours == 1
    assert state.total_runs == 5                  # 4 分击球手跑动 + 1 分判罚
    assert state.bowlers["bowlerA"].runs_conceded == 5   # 判罚和击球手打出的分都算投手头上


def test_no_ball_does_not_advance_the_over():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=1, extra=impl.Extra.NO_BALL))
    state = innings.state()
    assert state.legal_balls == 0
    assert state.balls_in_current_over == 0


def test_odd_runs_off_the_bat_on_a_no_ball_rotates_the_strike():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=1, extra=impl.Extra.NO_BALL))
    assert innings.state().striker_id == "opener2"


def test_invalid_delivery_combinations_are_rejected():
    with pytest.raises(impl.InvalidDeliveryError):
        impl.BallOutcome(bat_runs=1, extra=impl.Extra.BYE)   # bye 不该有击球手跑动
    with pytest.raises(impl.InvalidDeliveryError):
        impl.BallOutcome(extra=impl.Extra.NO_BALL, extra_runs=1)   # no ball 不建模额外跑动


def test_strike_rotates_on_odd_runs():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=1))
    assert innings.state().striker_id == "opener2"
    innings.record("bowlerA", impl.BallOutcome(bat_runs=2))
    assert innings.state().striker_id == "opener2"   # 偶数跑动不轮转


def test_strike_rotates_at_the_end_of_an_over():
    innings = make_innings()
    for _ in range(6):
        innings.record("bowlerA", impl.BallOutcome())
    assert innings.state().striker_id == "opener2"   # over 结束单独触发一次轮转


def test_wicket_brings_in_the_next_batter_without_touching_the_non_striker():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(dismissed=impl.Dismissal.BOWLED))
    state = innings.state()
    assert state.wickets == 1
    assert state.batters["opener1"].out is True
    assert state.striker_id == "no3"
    assert state.non_striker_id == "opener2"


# ---- 第 3 关：赛制、投手轮换 ---------------------------------------------------


def test_overs_limit_ends_the_innings_after_the_last_legal_ball():
    innings = make_innings(overs_limit=1, bowling=["bowlerA"])
    for _ in range(6):
        innings.record("bowlerA", impl.BallOutcome())
    assert innings.state().is_overs_complete is True
    with pytest.raises(impl.InningsCompleteError):
        innings.record("bowlerA", impl.BallOutcome())


def test_test_format_innings_never_auto_completes_on_overs():
    innings = make_innings(overs_limit=None)
    for _ in range(12):
        innings.record(["bowlerA", "bowlerB"][(0 if _ < 6 else 1)], impl.BallOutcome())
    assert innings.state().is_overs_complete is False


def test_all_out_completes_the_innings():
    innings = make_innings(batting=["b1", "b2", "b3"])
    innings.record("bowlerA", impl.BallOutcome(dismissed=impl.Dismissal.BOWLED))
    innings.record("bowlerA", impl.BallOutcome(dismissed=impl.Dismissal.BOWLED))
    assert innings.state().is_all_out is True
    assert innings.state().striker_id is None
    with pytest.raises(impl.InningsCompleteError):
        innings.record("bowlerA", impl.BallOutcome(bat_runs=1))


def test_bowler_cannot_bowl_two_overs_back_to_back():
    innings = make_innings()
    for _ in range(6):
        innings.record("bowlerA", impl.BallOutcome())
    with pytest.raises(impl.ConsecutiveOverError):
        innings.record("bowlerA", impl.BallOutcome())
    innings.record("bowlerB", impl.BallOutcome())   # 换个人就没问题


def test_bowler_cannot_change_mid_over():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome())
    with pytest.raises(impl.MidOverBowlerChangeError):
        innings.record("bowlerB", impl.BallOutcome())


def test_unknown_bowler_is_rejected_when_a_bowling_side_is_registered():
    innings = make_innings()
    with pytest.raises(impl.UnknownBowlerError):
        innings.record("not-on-the-team", impl.BallOutcome())


# ---- 第 3/4 关：改判——这才是不存总分的全部意义 ---------------------------------


def test_amending_the_last_ball_reverses_a_wicket_and_every_derived_figure_follows():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(dismissed=impl.Dismissal.BOWLED))
    assert innings.state().wickets == 1
    innings.amend_last_ball(impl.BallOutcome(bat_runs=1))   # 第三裁判：其实没出局，跑了一分
    state = innings.state()
    assert state.wickets == 0
    assert "no3" not in state.batters           # 换人的批次从来没真的发生过
    assert state.striker_id == "opener2"        # 奇数跑动让原来的击球手轮转，而不是被替换


def test_amend_only_touches_the_most_recent_ball():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=1))
    innings.record("bowlerA", impl.BallOutcome(bat_runs=4))
    innings.amend_last_ball(impl.BallOutcome(bat_runs=6))
    state = innings.state()
    assert state.total_runs == 7        # 1 + 6，第一球没被碰过


def test_amend_with_no_deliveries_raises():
    innings = make_innings()
    with pytest.raises(impl.NoDeliveryToAmendError):
        innings.amend_last_ball(impl.BallOutcome(bat_runs=1))


# ---- 派生统计的公式 -----------------------------------------------------------


def test_strike_rate_and_economy_formulas():
    innings = make_innings()
    innings.record("bowlerA", impl.BallOutcome(bat_runs=4))
    innings.record("bowlerA", impl.BallOutcome(bat_runs=2))
    state = innings.state()
    assert state.batters["opener1"].strike_rate == pytest.approx(300.0)   # 6 分 / 2 球 * 100
    assert state.bowlers["bowlerA"].economy == pytest.approx(18.0)        # 6 分 / (2/6) over


# ---- 第 4 关：直播订阅（Observer），不碰 Innings --------------------------------


def test_commentary_feed_notifies_subscribers_on_record_and_amend():
    innings = make_innings()
    feed = impl.CommentaryFeed(innings)
    updates = []
    feed.subscribe(lambda u: updates.append(u))
    feed.record("bowlerA", impl.BallOutcome(bat_runs=4))
    feed.amend_last_ball(impl.BallOutcome(bat_runs=6))
    assert len(updates) == 2
    assert updates[0].corrected is False
    assert updates[1].corrected is True
    assert updates[1].state.total_runs == 6


def test_unsubscribe_stops_further_notifications():
    innings = make_innings()
    feed = impl.CommentaryFeed(innings)
    updates = []

    def subscriber(update):
        updates.append(update)

    feed.subscribe(subscriber)
    feed.record("bowlerA", impl.BallOutcome(bat_runs=1))
    feed.unsubscribe(subscriber)
    feed.record("bowlerA", impl.BallOutcome(bat_runs=2))
    assert len(updates) == 1


def test_recording_directly_on_innings_never_reaches_a_feeds_subscribers():
    innings = make_innings()
    feed = impl.CommentaryFeed(innings)
    updates = []
    feed.subscribe(lambda u: updates.append(u))
    innings.record("bowlerA", impl.BallOutcome(bat_runs=4))   # 绕开 feed，直接记到 Innings 上
    assert updates == []
    assert innings.state().total_runs == 4                # 但记分本身完全正常


# ---- Match：若干局按顺序进行 ---------------------------------------------------


def test_match_scoreboard_reports_each_innings_in_order():
    match = impl.Match("M1", impl.MatchFormat.T20)
    first = match.start_innings(BATTING, BOWLING)
    second = match.start_innings(list(reversed(BATTING)), BOWLING)
    first.record("bowlerA", impl.BallOutcome(bat_runs=4))
    second.record("bowlerA", impl.BallOutcome(bat_runs=1))
    board = match.scoreboard()
    assert [s.total_runs for s in board] == [4, 1]


def test_unknown_innings_raises():
    match = impl.Match("M1", impl.MatchFormat.ODI)
    with pytest.raises(impl.UnknownInningsError):
        match.innings("does-not-exist")


def test_t20_and_odi_have_different_overs_limits_with_no_code_change():
    t20 = impl.Match("M1", impl.MatchFormat.T20).start_innings(BATTING, BOWLING)
    odi = impl.Match("M2", impl.MatchFormat.ODI).start_innings(BATTING, BOWLING)
    assert t20.overs_limit == 20
    assert odi.overs_limit == 50


# ---- 并发：多个读者在一个写者记分时，不变量始终成立 -----------------------------


def test_concurrent_readers_never_observe_a_state_past_the_format_limits():
    innings = make_innings(overs_limit=2, bowling=["bowlerA", "bowlerB"])
    stop = threading.Event()
    violations = []

    def reader():
        while not stop.is_set():
            state = innings.state()
            if state.wickets > 4 or state.legal_balls > 12:
                violations.append(state)

    readers = [threading.Thread(target=reader) for _ in range(4)]
    for t in readers:
        t.start()
    for i in range(12):
        bowler = "bowlerA" if i < 6 else "bowlerB"
        innings.record(bowler, impl.BallOutcome(bat_runs=1))
    stop.set()
    for t in readers:
        t.join()
    assert violations == []
    assert innings.state().legal_balls == 12
