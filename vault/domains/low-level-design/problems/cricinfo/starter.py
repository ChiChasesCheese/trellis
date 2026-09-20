"""体育比分系统（Cricinfo）——起始模板：把每个方法体补完。"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from enum import Enum


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


class Extra(Enum):
    WIDE = "wide"
    NO_BALL = "no_ball"
    BYE = "bye"
    LEG_BYE = "leg_bye"


class Dismissal(Enum):
    BOWLED = "bowled"
    CAUGHT = "caught"
    LBW = "lbw"
    RUN_OUT = "run_out"
    STUMPED = "stumped"


ILLEGAL_EXTRAS = frozenset({Extra.WIDE, Extra.NO_BALL})
NO_BAT_EXTRAS = frozenset({Extra.BYE, Extra.LEG_BYE})
BAT_RUN_EXTRAS = frozenset({None, Extra.NO_BALL})
EXTRA_RUN_EXTRAS = frozenset({Extra.WIDE, Extra.BYE, Extra.LEG_BYE})


@dataclass(frozen=True, slots=True)
class BallOutcome:
    """一次投球的结果：击球手跑了几分、额外跑了几分、是不是额外球、有没有人出局。"""

    bat_runs: int = 0
    extra: Extra | None = None
    extra_runs: int = 0
    dismissed: Dismissal | None = None

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def is_legal(self) -> bool:
        raise NotImplementedError

    @property
    def counts_as_ball_faced(self) -> bool:
        raise NotImplementedError

    @property
    def batter_runs(self) -> int:
        raise NotImplementedError

    @property
    def team_runs(self) -> int:
        raise NotImplementedError

    @property
    def bowler_runs(self) -> int:
        raise NotImplementedError

    @property
    def rotates_strike(self) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class BallEvent:
    seq: int
    bowler_id: str
    striker_id: str | None
    non_striker_id: str | None
    outcome: BallOutcome


@dataclass(frozen=True, slots=True)
class BatterStats:
    runs: int
    balls_faced: int
    fours: int
    sixes: int
    out: bool

    @property
    def strike_rate(self) -> float:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class BowlerStats:
    legal_balls: int
    runs_conceded: int
    wickets: int

    @property
    def overs(self) -> str:
        raise NotImplementedError

    @property
    def economy(self) -> float:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class InningsState:
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
        raise NotImplementedError

    @property
    def balls_in_current_over(self) -> int:
        raise NotImplementedError

    @property
    def is_overs_complete(self) -> bool:
        raise NotImplementedError

    @property
    def is_complete(self) -> bool:
        raise NotImplementedError

    @property
    def run_rate(self) -> float:
        raise NotImplementedError


def derive_innings_state(events: Sequence[BallEvent], batting_order: Sequence[str],
                         overs_limit: int | None) -> InningsState:
    raise NotImplementedError


class Innings:
    """一局：击球方的出场顺序、（可选的）投球方名单、限定球数，以及一条只增不改的事件日志。"""

    def __init__(self, innings_id: str, batting_order: Sequence[str],
                bowling_order: Sequence[str] = (), overs_limit: int | None = None) -> None:
        raise NotImplementedError

    @property
    def events(self) -> tuple[BallEvent, ...]:
        raise NotImplementedError

    def state(self) -> InningsState:
        raise NotImplementedError

    def record(self, bowler_id: str, outcome: BallOutcome) -> BallEvent:
        raise NotImplementedError

    def amend_last_ball(self, outcome: BallOutcome) -> BallEvent:
        raise NotImplementedError


class MatchFormat(Enum):
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
        raise NotImplementedError

    def start_innings(self, batting_order: Sequence[str],
                      bowling_order: Sequence[str] = ()) -> Innings:
        raise NotImplementedError

    def innings(self, innings_id: str) -> Innings:
        raise NotImplementedError

    @property
    def innings_ids(self) -> tuple[str, ...]:
        raise NotImplementedError

    def scoreboard(self) -> tuple[InningsState, ...]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class BallRecorded:
    innings_id: str
    event: BallEvent
    state: InningsState
    corrected: bool = False


Subscriber = Callable[[BallRecorded], None]


class CommentaryFeed:
    """包在一局外面的直播层：记球、改判都先转给被包的 `Innings`，成功后再通知订阅者。"""

    def __init__(self, innings: Innings) -> None:
        raise NotImplementedError

    def subscribe(self, subscriber: Subscriber) -> None:
        raise NotImplementedError

    def unsubscribe(self, subscriber: Subscriber) -> None:
        raise NotImplementedError

    def record(self, bowler_id: str, outcome: BallOutcome) -> BallEvent:
        raise NotImplementedError

    def amend_last_ball(self, outcome: BallOutcome) -> BallEvent:
        raise NotImplementedError
