"""蛇梯棋（Snake and Ladder）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass`、类型别名和异常都和 `solution.py` 一致；
把标了 `raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/snake-and-ladder -q
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum


class SnakeLadderError(Exception):
    """本设计里所有失败路径的公共基类。"""


class InvalidBoardError(SnakeLadderError):
    """棋盘配置不合法。"""


class InvalidPlayersError(SnakeLadderError):
    """玩家不合法：人数不足两人、有重名，或者不在本局里。"""


class InvalidRollError(SnakeLadderError):
    """骰子给出的不是正整数点数。"""


class RuleLoopError(SnakeLadderError):
    """一轮之内掷骰次数超过上限。"""


class GameOverError(SnakeLadderError):
    """棋局已经结束，不能再掷。"""


class JumpKind(Enum):
    """跳跃的两种方向。"""

    SNAKE = "snake"
    LADDER = "ladder"


class ChangeReason(Enum):
    """一次位置变化因何而起。"""

    ROLL = "roll"
    LADDER = "ladder"
    SNAKE = "snake"
    EFFECT = "effect"
    BLOCKED = "blocked"
    NOT_STARTED = "not_started"


class RollAgain(Enum):
    """掷完一次之后，回合循环该怎么办。"""

    STOP = "stop"
    AGAIN = "again"
    CANCEL = "cancel"


class Outcome(Enum):
    """一次 `Game.play()` 的收场方式。"""

    WON = "won"
    ABANDONED = "abandoned"


@dataclass(frozen=True, slots=True, order=True)
class Jump:
    """棋盘上的一次跳跃：踩到 `start` 就被送到 `end`。"""

    start: int
    end: int

    def __post_init__(self) -> None:
        """两端相同要抛 `InvalidBoardError`。"""
        raise NotImplementedError

    @property
    def kind(self) -> JumpKind:
        """向下是蛇，向上是梯子。"""
        raise NotImplementedError

    @property
    def is_snake(self) -> bool:
        """是不是一条蛇。"""
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class PositionChange:
    """一次位置变化：谁、从哪到哪、为什么。"""

    player: str
    frm: int
    to: int
    reason: ChangeReason


@dataclass(frozen=True, slots=True)
class TurnRecord:
    """一轮的完整记录，同时也是推给订阅者的事件。"""

    turn: int
    player: str
    rolls: tuple[int, ...]
    changes: tuple[PositionChange, ...]
    cancelled: bool
    finishers: tuple[str, ...]

    @property
    def landed_on(self) -> int | None:
        """本轮玩家停在哪一格；整轮作废时是 `None`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Standing:
    """名次表里的一行。"""

    rank: int
    player: str
    position: int
    finished_on_turn: int | None


@dataclass(frozen=True, slots=True)
class GameResult:
    """一次 `Game.play()` 的结果。"""

    outcome: Outcome
    turns: int
    standings: tuple[Standing, ...]

    @property
    def winner(self) -> str | None:
        """第一名——只有真的有人到终点时才算赢家。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TurnContext:
    """交给格子效果的只读快照。"""

    player: str
    square: int
    positions: Mapping[str, int]
    rolls: tuple[int, ...]
    last_square: int
    rng: random.Random


class Board:
    """棋盘：一串格子外加一张跳跃表，构造时就把自己校验干净。"""

    def __init__(self, last_square: int, jumps: Iterable[Jump] = (), *, start_square: int = 0) -> None:
        """校验：终点格够大；跳跃的**起点**不能是起点格或终点格、且唯一；终点必须在棋盘上、
        不能是起点格（终点格是允许的，直通终点的梯子踩到就赢）；不同跳跃不首尾相接。"""
        raise NotImplementedError

    @property
    def start_square(self) -> int:
        """起点格。"""
        raise NotImplementedError

    @property
    def last_square(self) -> int:
        """终点格。"""
        raise NotImplementedError

    @property
    def jumps(self) -> Mapping[int, Jump]:
        """按起点索引的跳跃表（只读）。"""
        raise NotImplementedError

    @property
    def jump_count(self) -> int:
        """跳跃总数。"""
        raise NotImplementedError

    def jump_from(self, square: int) -> Jump | None:
        """这一格上有没有跳跃。"""
        raise NotImplementedError


def classic_board() -> Board:
    """经典 100 格棋盘（9 梯 9 蛇），包括 80→100 那架直通终点的梯子。"""
    raise NotImplementedError


Die = Callable[[], int]


def fair_die(sides: int = 6, rng: random.Random | None = None) -> Die:
    """一枚公平的 `sides` 面骰子，随机源注入。"""
    raise NotImplementedError


class SequenceDie:
    """按给定序列依次出点的骰子：测试靠它把随机性拿掉。"""

    def __init__(self, pips: Sequence[int]) -> None:
        raise NotImplementedError

    def __call__(self) -> int:
        raise NotImplementedError

    @property
    def rolls_left(self) -> int:
        """还剩几个预设点数。"""
        raise NotImplementedError


EntryRule = Callable[[int], bool]
RollAgainRule = Callable[[tuple[int, ...]], RollAgain]
DestinationRule = Callable[[int, int, int], int]
SquareEffect = Callable[[TurnContext], tuple[PositionChange, ...]]


def always_start(pips: int) -> bool:
    """默认：第一次掷骰就能出发。"""
    raise NotImplementedError


def six_to_start(pips: int) -> bool:
    """变体：停在起点格的人必须掷到六才能上路。"""
    raise NotImplementedError


def one_roll_per_turn(rolls: tuple[int, ...]) -> RollAgain:
    """默认：一轮掷一次。"""
    raise NotImplementedError


def extra_turn_on_six(rolls: tuple[int, ...]) -> RollAgain:
    """变体：掷到六就再掷一次（再走一步，不是把点数加起来）。"""
    raise NotImplementedError


def three_sixes_cancel(rolls: tuple[int, ...]) -> RollAgain:
    """变体：掷六加掷一次，但连续三个六整轮作废。"""
    raise NotImplementedError


def exact_finish(square: int, pips: int, last_square: int) -> int:
    """默认：必须精确踩到终点格，超出就原地不动。"""
    raise NotImplementedError


def overshoot_bounces(square: int, pips: int, last_square: int) -> int:
    """变体：超出终点就从终点往回弹。"""
    raise NotImplementedError


def teleport(frm: int, to: int) -> SquareEffect:
    """第 4 关：踩到 `frm` 就被传送到 `to`。"""
    raise NotImplementedError


def double_move(square: int) -> SquareEffect:
    """第 4 关：踩到这一格，再按刚才的点数往前走一次。"""
    raise NotImplementedError


def swap_with_leader(square: int) -> SquareEffect:
    """第 4 关：踩到这一格，和当前领先者换位置。"""
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RuleSet:
    """一局棋的玩法：每个字段管一个决策点，可以任意组合。"""

    may_start: EntryRule = always_start
    roll_again: RollAgainRule = one_roll_per_turn
    destination: DestinationRule = exact_finish
    effects: tuple[SquareEffect, ...] = ()


class Game:
    """一局蛇梯棋：唯一拥有"谁在哪一格"的对象。"""

    def __init__(
        self,
        board: Board,
        players: Sequence[str],
        *,
        die: Die | None = None,
        rules: RuleSet | None = None,
        rng: random.Random | None = None,
        max_turns: int = 10_000,
        max_rolls_per_turn: int = 32,
        play_to_the_end: bool = False,
        log_limit: int | None = None,
    ) -> None:
        """人数不足两人或者重名要抛 `InvalidPlayersError`。"""
        raise NotImplementedError

    @property
    def players(self) -> tuple[str, ...]:
        """按出场顺序排列的玩家。"""
        raise NotImplementedError

    @property
    def positions(self) -> Mapping[str, int]:
        """所有人位置的快照。"""
        raise NotImplementedError

    @property
    def current_player(self) -> str:
        """该谁掷了；已经到终点的人会被跳过。"""
        raise NotImplementedError

    @property
    def turns_played(self) -> int:
        """已经走过的轮数（独立计数器，不是 `len(log)`）。"""
        raise NotImplementedError

    @property
    def log(self) -> tuple[TurnRecord, ...]:
        """走子日志快照。"""
        raise NotImplementedError

    @property
    def is_over(self) -> bool:
        """棋局是否已经结束。"""
        raise NotImplementedError

    @property
    def winner(self) -> str | None:
        """第一个到达终点的人。"""
        raise NotImplementedError

    def position_of(self, player: str) -> int:
        """某个玩家现在在哪一格。"""
        raise NotImplementedError

    def subscribe(self, listener: Callable[[TurnRecord], None]) -> Callable[[], None]:
        """订阅每轮事件，返回取消订阅的函数。"""
        raise NotImplementedError

    def play_turn(self) -> TurnRecord:
        """走一轮：掷骰（可能多次）、移动、结算，整体提交或整体作废。"""
        raise NotImplementedError

    def play(self, max_turns: int | None = None) -> GameResult:
        """一直走到棋局结束或轮数耗尽。"""
        raise NotImplementedError

    def standings(self) -> tuple[Standing, ...]:
        """当前名次。"""
        raise NotImplementedError
