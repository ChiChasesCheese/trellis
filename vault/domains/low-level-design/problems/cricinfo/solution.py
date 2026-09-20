"""体育比分系统（Cricinfo）——把一场板球比赛建模成一条球事件日志，统计全部现算的参考实现。

核心思路：这道题是事件溯源（event sourcing）的教科书场景，只是没人在题面里这么叫它。**一个球
（ball）就是一条不可再分的事件**——谁投的、谁打的、跑了几分、算不算合法球、有没有人出局；
局面（总分、击球手个人得分、投手的经济率、轮到谁击球、轮到谁投球）**没有一个是被存下来再累加
更新的字段，全部是对事件日志的一次重放（replay）**。`derive_innings_state` 是全文唯一改数字
的地方，`Innings.record` 只管往日志末尾追加一条事件。这样一来，"第三裁判改判"这个全题最有
意思的需求几乎不需要专门的代码：只要把最近一条事件换成修正后的版本，重新跑一遍
`derive_innings_state`，所有派生出来的数字——总分、少了几个 wicket、轮到谁击球——自动跟着对。
直播订阅（Observer）被做成一层薄薄的外壳 `CommentaryFeed`，包住 `Innings` 而不改它一行代码。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径。


class CricketError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownInningsError(CricketError):
    """局号不存在。"""

class UnknownBowlerError(CricketError):
    """这名投手不在这一局登记的投球方名单里。"""

class NoDeliveryToAmendError(CricketError):
    """这一局还没有任何一球，没有可改判的对象。"""

class InningsCompleteError(CricketError):
    """这一局已经结束（全部出局或用完球数），不能再记球。"""

class ConsecutiveOverError(CricketError):
    """同一名投手不能连续投两个 over。"""

class MidOverBowlerChangeError(CricketError):
    """一个 over 还没投完，中途换了投手。"""

class InvalidDeliveryError(CricketError):
    """一次投球的结果自相矛盾——比如给一次 bye 记上了击球手跑动。"""


# --------------------------------------------------------------------------
# 一个球：额外球的种类、出局的方式，以及一次投球的结果。


class Extra(Enum):
    """额外球的四种：wide、no ball 不算合法球；bye、leg bye 算合法球。"""

    WIDE = "wide"
    NO_BALL = "no_ball"
    BYE = "bye"
    LEG_BYE = "leg_bye"


class Dismissal(Enum):
    """出局方式；本设计不限制哪种出局能发生在哪种额外球上，见题解的取舍说明。"""

    BOWLED = "bowled"
    CAUGHT = "caught"
    LBW = "lbw"
    RUN_OUT = "run_out"
    STUMPED = "stumped"


ILLEGAL_EXTRAS = frozenset({Extra.WIDE, Extra.NO_BALL})
NO_BAT_EXTRAS = frozenset({Extra.BYE, Extra.LEG_BYE})
BAT_RUN_EXTRAS = frozenset({None, Extra.NO_BALL})       # 允许击球手个人得分非零的两种场景
EXTRA_RUN_EXTRAS = frozenset({Extra.WIDE, Extra.BYE, Extra.LEG_BYE})  # 允许"额外跑动"非零的场景


@dataclass(frozen=True, slots=True)
class BallOutcome:
    """一次投球的结果。这是唯一会被"改判"的部分，也是四条额外球规则唯一的落点。

    `bat_runs` 和 `extra_runs`是两个含义完全不同的数字，分开存而不是共用一个字段：前者是
    "打到球棒上跑了几分"（只有正常球和 no ball 才可能非零——no ball 上打出去的分照样记
    在击球手头上，这是本设计和一份更早、错误的版本之间唯一的差别）；后者是"跟球棒无关、
    但要记进队伍总分的额外跑动"（bye／leg bye 的跑动、wide 上的超跑）。两者的合法组合由
    `__post_init__` 校验，写错场景（比如给一次 bye 塞了击球手跑动）会立刻报错，而不是
    悄悄算出一个错误的总分。
    """

    bat_runs: int = 0
    extra: Extra | None = None
    extra_runs: int = 0
    dismissed: Dismissal | None = None

    def __post_init__(self) -> None:
        if self.bat_runs and self.extra not in BAT_RUN_EXTRAS:
            raise InvalidDeliveryError(f"{self.extra} deliveries cannot credit the batter")
        if self.extra_runs and self.extra not in EXTRA_RUN_EXTRAS:
            raise InvalidDeliveryError(f"{self.extra} deliveries cannot carry extra team runs")

    @property
    def is_legal(self) -> bool:
        """算不算一颗合法球——wide 和 no ball 都要重投，不计入这个 over 的球数。"""
        return self.extra not in ILLEGAL_EXTRAS

    @property
    def counts_as_ball_faced(self) -> bool:
        """简化模型：除了 wide，击球手都算"面对了"这一球——包括 no ball，因为他确实有机会
        把它打出去，这正是 no ball 和 wide 唯一不该被同等对待的地方。
        """
        return self.extra is not Extra.WIDE

    @property
    def batter_runs(self) -> int:
        """记到击球手个人得分上的跑动。`__post_init__` 已经保证了它只在合法的场景下非零。"""
        return self.bat_runs

    @property
    def team_runs(self) -> int:
        """记到球队总分上的跑动：击球手跑的 + 额外跑的 + 非法球那一分自动判罚。"""
        return self.bat_runs + self.extra_runs + (1 if not self.is_legal else 0)

    @property
    def bowler_runs(self) -> int:
        """记到投手失分上的跑动：bye／leg bye 不是投手的责任；no ball 的判罚分和击球手
        打出去的分都要算进投手的经济率——那两分本来就是他投出这颗坏球才产生的。
        """
        return 0 if self.extra in NO_BAT_EXTRAS else self.team_runs

    @property
    def rotates_strike(self) -> bool:
        """这一球单独触发一次击球手轮转吗：正常球和 no ball 看击球手跑动的奇偶，bye／leg
        bye 看额外跑动的奇偶，wide 维持不触发——wide 上会不会有人跑动本题不建模，保留
        原有行为，不在这次修正的范围内。
        """
        if self.extra is Extra.WIDE:
            return False
        if self.extra in NO_BAT_EXTRAS:
            return self.extra_runs % 2 == 1
        return self.bat_runs % 2 == 1


@dataclass(frozen=True, slots=True)
class BallEvent:
    """一条球事件：谁投的、谁在击球（两端都记，换人时才用得上）、结果是什么。"""

    seq: int
    bowler_id: str
    striker_id: str | None
    non_striker_id: str | None
    outcome: BallOutcome


# --------------------------------------------------------------------------
# 派生状态：现算的击球手/投手统计与整局局面。


@dataclass(frozen=True, slots=True)
class BatterStats:
    """一名击球手此刻的统计，全部由 `derive_innings_state` 重放算出。"""

    runs: int
    balls_faced: int
    fours: int
    sixes: int
    out: bool

    @property
    def strike_rate(self) -> float:
        return (self.runs * 100 / self.balls_faced) if self.balls_faced else 0.0


@dataclass(frozen=True, slots=True)
class BowlerStats:
    """一名投手此刻的统计。"""

    legal_balls: int
    runs_conceded: int
    wickets: int

    @property
    def overs(self) -> str:
        return f"{self.legal_balls // 6}.{self.legal_balls % 6}"

    @property
    def economy(self) -> float:
        bowled = self.legal_balls / 6
        return (self.runs_conceded / bowled) if bowled else 0.0


@dataclass(frozen=True, slots=True)
class InningsState:
    """一局此刻的全部局面：从球事件日志重放出来的一份不可变快照，从不被写入。"""

    total_runs: int
    wickets: int
    legal_balls: int
    striker_id: str | None
    non_striker_id: str | None
    over_bowler_id: str | None
    last_over_bowler_id: str | None
    batters: Mapping[str, BatterStats]
    bowlers: Mapping[str, BowlerStats]
    is_all_out: bool
    overs_limit: int | None

    @property
    def overs_completed(self) -> int:
        return self.legal_balls // 6

    @property
    def balls_in_current_over(self) -> int:
        return self.legal_balls % 6

    @property
    def is_overs_complete(self) -> bool:
        return self.overs_limit is not None and self.legal_balls >= self.overs_limit * 6

    @property
    def is_complete(self) -> bool:
        """这一局结束了吗：全部出局，或者（限定球数赛制下）球数用完。"""
        return self.is_all_out or self.is_overs_complete

    @property
    def run_rate(self) -> float:
        bowled = self.legal_balls / 6
        return (self.total_runs / bowled) if bowled else 0.0


def _add_batter(existing: BatterStats | None, outcome: BallOutcome) -> BatterStats:
    base = existing or BatterStats(0, 0, 0, 0, False)
    runs = outcome.batter_runs
    return replace(base, runs=base.runs + runs,
                   balls_faced=base.balls_faced + (1 if outcome.counts_as_ball_faced else 0),
                   fours=base.fours + (1 if runs == 4 else 0),
                   sixes=base.sixes + (1 if runs == 6 else 0))


def _add_bowler(existing: BowlerStats | None, outcome: BallOutcome) -> BowlerStats:
    base = existing or BowlerStats(0, 0, 0)
    return replace(base, legal_balls=base.legal_balls + (1 if outcome.is_legal else 0),
                   runs_conceded=base.runs_conceded + outcome.bowler_runs,
                   wickets=base.wickets + (1 if outcome.dismissed is not None else 0))


def derive_innings_state(events: Sequence[BallEvent], batting_order: Sequence[str],
                         overs_limit: int | None) -> InningsState:
    """把整条球事件日志重放一遍，算出这一局此刻的全部状态——本设计唯一"计算"发生的地方。"""
    batters: dict[str, BatterStats] = {}
    bowlers: dict[str, BowlerStats] = {}
    striker = batting_order[0] if batting_order else None
    non_striker = batting_order[1] if len(batting_order) > 1 else None
    next_index = 2
    total_runs = wickets = legal_balls = balls_this_over = 0
    over_bowler: str | None = None
    last_over_bowler: str | None = None

    for event in events:
        outcome = event.outcome
        total_runs += outcome.team_runs
        if over_bowler is None:
            over_bowler = event.bowler_id
        bowlers[event.bowler_id] = _add_bowler(bowlers.get(event.bowler_id), outcome)
        if striker is not None:
            batters[striker] = _add_batter(batters.get(striker), outcome)
        if outcome.is_legal:
            legal_balls += 1
            balls_this_over += 1
        if outcome.dismissed is not None and striker is not None:
            wickets += 1
            batters[striker] = replace(batters[striker], out=True)
            striker = batting_order[next_index] if next_index < len(batting_order) else None
            next_index += 1
        elif outcome.rotates_strike:
            striker, non_striker = non_striker, striker
        if outcome.is_legal and balls_this_over == 6:
            last_over_bowler, over_bowler = over_bowler, None
            balls_this_over = 0
            if striker is not None and non_striker is not None:
                striker, non_striker = non_striker, striker

    is_all_out = wickets >= max(len(batting_order) - 1, 0)
    return InningsState(total_runs=total_runs, wickets=wickets, legal_balls=legal_balls,
                        striker_id=striker, non_striker_id=non_striker,
                        over_bowler_id=over_bowler, last_over_bowler_id=last_over_bowler,
                        batters=batters, bowlers=bowlers, is_all_out=is_all_out,
                        overs_limit=overs_limit)


# --------------------------------------------------------------------------
# Innings：只持有一条按顺序追加的球事件日志。


class Innings:
    """一局：击球方的出场顺序、（可选的）投球方名单、限定球数，以及一条只增不改的事件日志。

    唯一的例外是 `amend_last_ball`——现实里第三裁判的裁决发生在下一球开始之前，所以能改的
    永远只有最后一条记录；改掉更早的一球会让它之后已经发生的一切都变得不自洽。
    """

    def __init__(self, innings_id: str, batting_order: Sequence[str],
                bowling_order: Sequence[str] = (), overs_limit: int | None = None) -> None:
        self.id = innings_id
        self.batting_order = tuple(batting_order)
        self.bowling_order = tuple(bowling_order)
        self.overs_limit = overs_limit
        self._events: list[BallEvent] = []
        self._lock = threading.Lock()
        self._ids = itertools.count(1)

    @property
    def events(self) -> tuple[BallEvent, ...]:
        """事件日志的不可变快照。"""
        with self._lock:
            return tuple(self._events)

    def state(self) -> InningsState:
        """此刻的局面——对日志的一次重放，读多少次都不会改变日志本身。"""
        with self._lock:
            return derive_innings_state(self._events, self.batting_order, self.overs_limit)

    def record(self, bowler_id: str, outcome: BallOutcome) -> BallEvent:
        """记一球：谁在击球由当前状态决定，调用方只需要给出谁在投、投出了什么结果。"""
        with self._lock:
            state = derive_innings_state(self._events, self.batting_order, self.overs_limit)
            if state.is_complete:
                raise InningsCompleteError(f"innings {self.id} is already complete")
            self._validate_bowler(state, bowler_id)
            event = BallEvent(next(self._ids), bowler_id, state.striker_id,
                              state.non_striker_id, outcome)
            self._events.append(event)
            return event

    def amend_last_ball(self, outcome: BallOutcome) -> BallEvent:
        """第三裁判改判：只能改最近记的那一球，结果换掉，谁投谁打的事实不变。"""
        with self._lock:
            if not self._events:
                raise NoDeliveryToAmendError(f"innings {self.id} has no delivery to amend")
            last = self._events[-1]
            amended = BallEvent(last.seq, last.bowler_id, last.striker_id,
                                last.non_striker_id, outcome)
            self._events[-1] = amended
            return amended

    def _validate_bowler(self, state: InningsState, bowler_id: str) -> None:
        if self.bowling_order and bowler_id not in self.bowling_order:
            raise UnknownBowlerError(f"{bowler_id!r} is not in this innings' bowling side")
        if state.over_bowler_id is not None and bowler_id != state.over_bowler_id:
            raise MidOverBowlerChangeError(
                f"the over in progress is being bowled by {state.over_bowler_id!r}")
        if state.over_bowler_id is None and bowler_id == state.last_over_bowler_id:
            raise ConsecutiveOverError(f"{bowler_id!r} cannot bowl two overs back to back")


# --------------------------------------------------------------------------
# Match：若干局按顺序进行。赛制只决定"每局限定几球"，不改局内任何规则。


class MatchFormat(Enum):
    """三种常见赛制；一局限定几个 over 由赛制决定，TEST 不限（本文不实现follow-on等规则）。"""

    T20 = "t20"
    ODI = "odi"
    TEST = "test"


OVERS_PER_INNINGS: Mapping[MatchFormat, int | None] = {
    MatchFormat.T20: 20,
    MatchFormat.ODI: 50,
    MatchFormat.TEST: None,
}


class Match:
    """一场比赛：按顺序进行的若干局，`format` 唯一决定每一局限定几个 over。"""

    def __init__(self, match_id: str, fmt: MatchFormat) -> None:
        self.id = match_id
        self.format = fmt
        self._innings: dict[str, Innings] = {}
        self._order: list[str] = []
        self._lock = threading.Lock()
        self._ids = itertools.count(1)

    def start_innings(self, batting_order: Sequence[str],
                      bowling_order: Sequence[str] = ()) -> Innings:
        """开一局：不管这是第几局，限定球数只看 `self.format`——两局制的赛制不用改这一行。"""
        with self._lock:
            innings = Innings(f"{self.id}-I{next(self._ids)}", batting_order, bowling_order,
                              OVERS_PER_INNINGS[self.format])
            self._innings[innings.id] = innings
            self._order.append(innings.id)
            return innings

    def innings(self, innings_id: str) -> Innings:
        with self._lock:
            found = self._innings.get(innings_id)
        if found is None:
            raise UnknownInningsError(f"unknown innings {innings_id!r}")
        return found

    @property
    def innings_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._order)

    def scoreboard(self) -> tuple[InningsState, ...]:
        """全场比分：按开局顺序列出每一局此刻的状态，全部现算。"""
        return tuple(self.innings(i).state() for i in self.innings_ids)


# --------------------------------------------------------------------------
# CommentaryFeed：给一局比赛加直播订阅，一行都不碰 Innings。


@dataclass(frozen=True, slots=True)
class BallRecorded:
    """发给订阅者的通知：发生了什么，而不是让订阅者反过来翻 `Innings` 的内部状态。"""

    innings_id: str
    event: BallEvent
    state: InningsState
    corrected: bool = False


Subscriber = Callable[[BallRecorded], None]


class CommentaryFeed:
    """包在一局外面的直播层：记球、改判都先转给被包的 `Innings`，成功后再通知订阅者。"""

    def __init__(self, innings: Innings) -> None:
        self._innings = innings
        self._subscribers: list[Subscriber] = []
        self._lock = threading.Lock()

    def subscribe(self, subscriber: Subscriber) -> None:
        with self._lock:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber) -> None:
        with self._lock:
            if subscriber in self._subscribers:
                self._subscribers.remove(subscriber)

    def record(self, bowler_id: str, outcome: BallOutcome) -> BallEvent:
        event = self._innings.record(bowler_id, outcome)
        self._notify(event, corrected=False)
        return event

    def amend_last_ball(self, outcome: BallOutcome) -> BallEvent:
        event = self._innings.amend_last_ball(outcome)
        self._notify(event, corrected=True)
        return event

    def _notify(self, event: BallEvent, corrected: bool) -> None:
        update = BallRecorded(self._innings.id, event, self._innings.state(), corrected)
        with self._lock:
            subscribers = tuple(self._subscribers)
        for subscriber in subscribers:
            subscriber(update)


if __name__ == "__main__":
    match = Match("M1", MatchFormat.T20)
    innings = match.start_innings(["opener1", "opener2", "no3"], bowling_order=["bowlerA", "bowlerB"])
    feed = CommentaryFeed(innings)
    feed.subscribe(lambda u: print(f"ball {u.event.seq}: {u.state.total_runs}/{u.state.wickets}"))
    feed.record("bowlerA", BallOutcome(bat_runs=4))
    feed.record("bowlerA", BallOutcome(bat_runs=1))
    feed.record("bowlerA", BallOutcome(extra=Extra.WIDE))
    feed.record("bowlerA", BallOutcome(bat_runs=4, extra=Extra.NO_BALL))
    feed.record("bowlerA", BallOutcome(dismissed=Dismissal.BOWLED))
    print(f"striker now: {innings.state().striker_id}")
