"""蛇梯棋（Snake and Ladder）——可配置棋盘、可替换骰子、多人名次、可组合规则的参考实现。

核心思路：棋盘在构造时就把自己校验干净（跳跃不能首尾相接、起点不能落在起点格或终点格、终点
不能回起点格、蛇向下梯向上），所以"一次移动最多触发一次跳跃"是结构上成立的，走子代码里不
需要 `while` 去追跳跃链；终点允许落在终点格，所以 80→100 这种直通终点的梯子照常存在。
骰子只是 `Callable[[], int]`，`fair_die()` 返回闭包、测试注入定死的序列，不需要策略类层次。
玩法变体（六点才出发、掷六加掷一次、连续三个六作废整轮、必须精确踩到终点、格子特效）是若干互相
独立的纯函数，装在 `RuleSet` 里由回合循环在五个固定决策点调用；`Game` 只拥有"谁在哪一格"这一件
事实，并保证一轮要么整体生效要么整体作废；棋局以 `GameResult` 给出完整名次，回合循环带显式上限。
"""

from __future__ import annotations

import random
from collections import deque
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType

# --------------------------------------------------------------------------
# 失败路径：一族有名字的异常，调用方既能分别处理，也能一把兜住


class SnakeLadderError(Exception):
    """本设计里所有失败路径的公共基类。"""


class InvalidBoardError(SnakeLadderError):
    """棋盘配置不合法：跳跃首尾相接、方向不对、或者两端落在起点格／终点格上。"""


class InvalidPlayersError(SnakeLadderError):
    """玩家不合法：人数不足两人、有重名，或者问了一个不在本局里的人。"""


class InvalidRollError(SnakeLadderError):
    """骰子给出的不是正整数点数——注入进来的骰子坏了。"""


class RuleLoopError(SnakeLadderError):
    """一轮之内掷骰次数超过上限：规则组合出现了不收敛的"再掷一次"。"""


class GameOverError(SnakeLadderError):
    """棋局已经结束，不能再掷。"""


# --------------------------------------------------------------------------
# 值对象


class JumpKind(Enum):
    """跳跃的两种方向；它是算出来的，不是存进去的。"""

    SNAKE = "snake"
    LADDER = "ladder"


class ChangeReason(Enum):
    """一次位置变化因何而起——日志和测试都按这个断言。"""

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
    """一次 `Game.play()` 的收场方式：有人赢了，还是轮数耗尽被放弃。"""

    WON = "won"
    ABANDONED = "abandoned"


@dataclass(frozen=True, slots=True, order=True)
class Jump:
    """棋盘上的一次跳跃：踩到 `start` 就被送到 `end`。

    蛇和梯子在这里**不是两个子类**——它们只差一个方向和一个称呼，`kind` 由两端大小算出来。
    """

    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start == self.end:
            raise InvalidBoardError(f"跳跃 {self.start}→{self.end} 的两端相同")

    @property
    def kind(self) -> JumpKind:
        """向下是蛇，向上是梯子。"""
        return JumpKind.SNAKE if self.end < self.start else JumpKind.LADDER

    @property
    def is_snake(self) -> bool:
        """是不是一条蛇。"""
        return self.end < self.start

    def __str__(self) -> str:
        return f"{self.start}{'↓' if self.is_snake else '↑'}{self.end}"


@dataclass(frozen=True, slots=True)
class PositionChange:
    """一次位置变化：谁、从哪到哪、为什么。整局的走子日志由它拼成。"""

    player: str
    frm: int
    to: int
    reason: ChangeReason


@dataclass(frozen=True, slots=True)
class TurnRecord:
    """一轮的完整记录，同时也是推给订阅者的事件：订阅者从事件本身更新自己，不用回头翻棋局的状态。"""

    turn: int
    player: str
    rolls: tuple[int, ...]
    changes: tuple[PositionChange, ...]
    cancelled: bool
    finishers: tuple[str, ...]

    @property
    def landed_on(self) -> int | None:
        """本轮玩家停在哪一格；整轮作废时是 `None`。"""
        mine = [c for c in self.changes if c.player == self.player]
        return mine[-1].to if mine else None


@dataclass(frozen=True, slots=True)
class Standing:
    """名次表里的一行。`finished_on_turn` 为 `None` 表示还没到终点。"""

    rank: int
    player: str
    position: int
    finished_on_turn: int | None


@dataclass(frozen=True, slots=True)
class GameResult:
    """一次 `Game.play()` 的结果：怎么收的场、走了多少轮、完整名次。"""

    outcome: Outcome
    turns: int
    standings: tuple[Standing, ...]

    @property
    def winner(self) -> str | None:
        """第一名——只有真的有人到终点时才算赢家，轮数耗尽时是 `None`。"""
        first = self.standings[0] if self.standings else None
        return first.player if first is not None and first.finished_on_turn is not None else None


@dataclass(frozen=True, slots=True)
class TurnContext:
    """交给格子效果的只读快照：看得见全局，改不动任何人的位置。

    效果不写 `Game` 的状态，而是**返回**一串 `PositionChange` 让回合循环统一提交，
    "连续三个六作废整轮"才能把效果造成的位移一起退掉。`positions` 里没有已经退场的人。
    """

    player: str
    square: int
    positions: Mapping[str, int]
    rolls: tuple[int, ...]
    last_square: int
    rng: random.Random


# --------------------------------------------------------------------------
# 棋盘：构造即校验


class Board:
    """从 `start_square`（起点格，还没上路）到 `last_square` 的一串格子，外加一张跳跃表。

    它的不变量全部在构造函数里立起来，没有一个需要调用方记得去调的 `validate()`：跳跃的
    **起点**不能是起点格（那架梯子在开局前就触发了）也不能是终点格（踩到就已经赢了，跳去
    哪里都没意义）、起点唯一、终点必须在棋盘上且不能把人送回起点格、不同跳跃不首尾相接。
    最后一条最要命——允许"甲的终点是乙的起点"，一次掷骰就会连跳；而蛇梯首尾互指时，追链的
    循环会当场转不出来。注意终点**可以**是终点格：一架直通 100 的梯子踩到就赢，完全合法。
    """

    def __init__(self, last_square: int, jumps: Iterable[Jump] = (), *, start_square: int = 0) -> None:
        if last_square <= start_square + 1:
            raise InvalidBoardError(f"终点格 {last_square} 至少要比起点格 {start_square} 大 2")
        table: dict[int, Jump] = {}
        for jump in jumps:
            if not start_square < jump.start < last_square:
                raise InvalidBoardError(f"{jump} 的起点在 {jump.start}：起点格和终点格上不能有跳跃的起点")
            if not start_square < jump.end <= last_square:
                raise InvalidBoardError(f"{jump} 的终点在 {jump.end}：必须在棋盘上，且不能把人送回起点格")
            if jump.start in table:
                raise InvalidBoardError(f"{jump} 和 {table[jump.start]} 的起点都是 {jump.start}")
            table[jump.start] = jump
        chained = {j.end for j in table.values()} & set(table)
        if chained:
            raise InvalidBoardError(f"格子 {sorted(chained)} 既是某跳跃的终点又是另一跳跃的起点：一次掷骰会连跳")
        self._start_square = start_square
        self._last_square = last_square
        self._jumps = table

    @property
    def start_square(self) -> int:
        """起点格：开局所有人站在这里，它不算"已经上路"。"""
        return self._start_square

    @property
    def last_square(self) -> int:
        """终点格：踩到它就到达终点。"""
        return self._last_square

    @property
    def jumps(self) -> Mapping[int, Jump]:
        """按起点索引的跳跃表。棋盘构造完就不再变，所以交出只读视图而不是拷贝是安全的。"""
        return MappingProxyType(self._jumps)

    @property
    def jump_count(self) -> int:
        """跳跃总数——测试和自检用得上的只读计数。"""
        return len(self._jumps)

    def jump_from(self, square: int) -> Jump | None:
        """这一格上有没有跳跃。一次查表就够了：校验保证不会有链。"""
        return self._jumps.get(square)


def classic_board() -> Board:
    """经典 100 格棋盘（9 梯 9 蛇），包括 80→100 那架直通终点的梯子。

    踩到第 80 格就赢——这是合法的：跳跃不能**起始**于终点格，但完全可以**结束**在那里。
    第 1 格上的那架 1→38 也一样：起点格是 0，第 1 格是普通格子。
    """
    ladders = [(1, 38), (4, 14), (9, 31), (21, 42), (28, 84), (36, 44), (51, 67), (71, 91), (80, 100)]
    snakes = [(16, 6), (47, 26), (49, 11), (56, 53), (62, 19), (64, 60), (87, 24), (93, 73), (95, 75)]
    return Board(100, [Jump(a, b) for a, b in ladders + snakes])


# --------------------------------------------------------------------------
# 骰子：一个可调用对象就够了，不需要策略类层次

Die = Callable[[], int]


def fair_die(sides: int = 6, rng: random.Random | None = None) -> Die:
    """一枚公平的 `sides` 面骰子。随机源是注入的：同一个种子必然重放出同一局棋。"""
    if sides < 1:
        raise InvalidRollError(f"骰子至少要有一面，给的是 {sides}")
    source = rng or random.Random()
    return lambda: source.randint(1, sides)


class SequenceDie:
    """按给定序列依次出点的骰子：测试靠它把随机性彻底拿掉。

    写成类而不是闭包，只因为多要了一个可断言的只读属性 `rolls_left`；
    两种写法同样满足 `Die`，调用方一行都不用改。
    """

    def __init__(self, pips: Sequence[int]) -> None:
        if not pips:
            raise InvalidRollError("脚本骰子至少要给一个点数")
        self._pips = tuple(pips)
        self._index = 0

    def __call__(self) -> int:
        if self._index >= len(self._pips):
            raise InvalidRollError("脚本骰子的点数用完了：这一局比预期掷得多")
        pip = self._pips[self._index]
        self._index += 1
        return pip

    @property
    def rolls_left(self) -> int:
        """还剩几个预设点数。"""
        return len(self._pips) - self._index


# --------------------------------------------------------------------------
# 规则：互相独立的纯函数，装在一个不可变的 RuleSet 里

EntryRule = Callable[[int], bool]
RollAgainRule = Callable[[tuple[int, ...]], RollAgain]
DestinationRule = Callable[[int, int, int], int]
SquareEffect = Callable[[TurnContext], tuple[PositionChange, ...]]


def always_start(pips: int) -> bool:
    """默认：第一次掷骰就能出发。"""
    return True


def six_to_start(pips: int) -> bool:
    """变体：停在起点格的人必须掷到六才能上路。"""
    return pips == 6


def one_roll_per_turn(rolls: tuple[int, ...]) -> RollAgain:
    """默认：一轮掷一次。"""
    return RollAgain.STOP


def extra_turn_on_six(rolls: tuple[int, ...]) -> RollAgain:
    """变体：掷到六就再掷一次——是"再走一步"，不是"把点数加起来"。"""
    return RollAgain.AGAIN if rolls[-1] == 6 else RollAgain.STOP


def three_sixes_cancel(rolls: tuple[int, ...]) -> RollAgain:
    """变体：掷六加掷一次，但连续三个六整轮作废——前两步走出去的也要退回来。"""
    if rolls[-3:] == (6, 6, 6):
        return RollAgain.CANCEL
    return RollAgain.AGAIN if rolls[-1] == 6 else RollAgain.STOP


def exact_finish(square: int, pips: int, last_square: int) -> int:
    """默认：必须精确踩到终点格，超出就原地不动。"""
    target = square + pips
    return target if target <= last_square else square


def overshoot_bounces(square: int, pips: int, last_square: int) -> int:
    """变体：超出终点就从终点往回弹。"""
    target = square + pips
    return target if target <= last_square else last_square - (target - last_square)


def teleport(frm: int, to: int) -> SquareEffect:
    """第 4 关：踩到 `frm` 就被传送到 `to`。它是规则不是跳跃，所以允许直达终点格。"""

    def effect(ctx: TurnContext) -> tuple[PositionChange, ...]:
        if ctx.square != frm:
            return ()
        return (PositionChange(ctx.player, frm, to, ChangeReason.EFFECT),)

    return effect


def double_move(square: int) -> SquareEffect:
    """第 4 关：踩到这一格，再按刚才的点数往前走一次（走不动就算了）。"""

    def effect(ctx: TurnContext) -> tuple[PositionChange, ...]:
        if ctx.square != square:
            return ()
        target = ctx.square + ctx.rolls[-1]
        if target > ctx.last_square:
            return ()
        return (PositionChange(ctx.player, ctx.square, target, ChangeReason.EFFECT),)

    return effect


def swap_with_leader(square: int) -> SquareEffect:
    """第 4 关：踩到这一格，和当前领先者换位置——一个效果同时改两个人的位置。"""

    def effect(ctx: TurnContext) -> tuple[PositionChange, ...]:
        if ctx.square != square:
            return ()
        rivals = [(pos, name) for name, pos in ctx.positions.items() if name != ctx.player]
        if not rivals:
            return ()
        best, leader = max(rivals)
        if best <= ctx.square:
            return ()
        return (
            PositionChange(ctx.player, ctx.square, best, ChangeReason.EFFECT),
            PositionChange(leader, best, ctx.square, ChangeReason.EFFECT),
        )

    return effect


@dataclass(frozen=True, slots=True)
class RuleSet:
    """一局棋的玩法。每个字段管一个决策点，互不知道对方存在，可以任意组合。

    字段里存的是普通函数：`slots=True` 让它们成为**实例属性**，
    `self.may_start(pips)` 不会把 `self` 偷偷塞成第一个参数——写成类属性就会。
    """

    may_start: EntryRule = always_start
    roll_again: RollAgainRule = one_roll_per_turn
    destination: DestinationRule = exact_finish
    effects: tuple[SquareEffect, ...] = ()


# --------------------------------------------------------------------------
# 棋局：唯一拥有"谁在哪一格"的对象


class Game:
    """一局蛇梯棋。它只拥有一件事实——每个玩家在哪一格——并保证一轮的位移要么全生效要么全作废。

    回合循环固定不变：掷骰 → 问出发规则 → 问终点规则 → 查跳跃表 → 跑格子效果 → 结算到达。
    玩法变体全部通过 `RuleSet` 挂在这五个决策点上，加新规则不动这个类的任何一行。
    """

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
        if len(players) < 2:
            raise InvalidPlayersError("至少要两个玩家")
        if len(set(players)) != len(players):
            raise InvalidPlayersError("玩家名字必须互不相同")
        self._board = board
        self._players = tuple(players)
        self._rng = rng or random.Random()
        self._die: Die = die or fair_die(6, self._rng)
        self._rules = rules or RuleSet()
        self._max_turns = max_turns
        self._max_rolls_per_turn = max_rolls_per_turn
        self._play_to_the_end = play_to_the_end
        self._positions: dict[str, int] = {p: board.start_square for p in self._players}
        self._finished: dict[str, int] = {}
        self._arrived: dict[str, int] = {p: 0 for p in self._players}
        self._log: deque[TurnRecord] = deque(maxlen=log_limit)
        self._listeners: list[Callable[[TurnRecord], None]] = []
        self._seat = 0
        self._turns = 0

    # ---- 只读状态：交出去的永远是快照或不可变值 --------------------------

    @property
    def players(self) -> tuple[str, ...]:
        """按出场顺序排列的玩家。"""
        return self._players

    @property
    def positions(self) -> Mapping[str, int]:
        """所有人位置的快照——调用方拿到的不是内部那本字典。"""
        return MappingProxyType(dict(self._positions))

    @property
    def current_player(self) -> str:
        """该谁掷了。已经到终点的人会被跳过。"""
        return self._players[self._seat]

    @property
    def turns_played(self) -> int:
        """已经走过的轮数。它是独立计数器，不是 `len(log)`——日志可以被截断，轮数不能。"""
        return self._turns

    @property
    def log(self) -> tuple[TurnRecord, ...]:
        """走子日志快照；`log_limit` 生效时只保留最近若干轮。"""
        return tuple(self._log)

    @property
    def is_over(self) -> bool:
        """棋局是否已经结束：默认第一个到终点就结束，`play_to_the_end` 时要排到只剩一人。"""
        if not self._finished:
            return False
        return len(self._finished) >= len(self._players) - 1 if self._play_to_the_end else True

    @property
    def winner(self) -> str | None:
        """第一个到达终点的人。"""
        if not self._finished:
            return None
        return min(self._finished, key=lambda p: (self._finished[p], self._players.index(p)))

    def position_of(self, player: str) -> int:
        """某个玩家现在在哪一格。"""
        if player not in self._positions:
            raise InvalidPlayersError(f"{player!r} 不在这局里")
        return self._positions[player]

    def subscribe(self, listener: Callable[[TurnRecord], None]) -> Callable[[], None]:
        """订阅每轮事件，返回一个取消订阅的函数——监听器表因此不会只进不出。"""
        self._listeners.append(listener)

        def unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return unsubscribe

    # ---- 回合循环 --------------------------------------------------------

    def play_turn(self) -> TurnRecord:
        """走一轮：掷骰（可能多次）、移动、结算，整体提交或整体作废。"""
        if self.is_over:
            raise GameOverError("棋局已经结束")
        player = self.current_player
        pending: dict[str, int] = {}
        changes: list[PositionChange] = []
        rolls: list[int] = []
        cancelled = False
        while True:
            rolls.append(self._roll())
            verdict = self._rules.roll_again(tuple(rolls))
            if verdict is RollAgain.CANCEL:
                cancelled, pending, changes = True, {}, []
                break
            changes.extend(self._one_leg(player, rolls[-1], pending, tuple(rolls)))
            if pending.get(player, self._positions[player]) == self._board.last_square:
                break
            if verdict is not RollAgain.AGAIN:
                break
            if len(rolls) >= self._max_rolls_per_turn:
                raise RuleLoopError(f"一轮之内掷了 {len(rolls)} 次：加轮规则不收敛")
        return self._commit(player, tuple(rolls), tuple(changes), cancelled, pending)

    def play(self, max_turns: int | None = None) -> GameResult:
        """一直走到棋局结束或轮数耗尽，返回收场方式与完整名次。"""
        budget = self._max_turns if max_turns is None else max_turns
        while not self.is_over and budget > 0:
            self.play_turn()
            budget -= 1
        return GameResult(
            outcome=Outcome.WON if self.is_over else Outcome.ABANDONED,
            turns=self._turns,
            standings=self.standings(),
        )

    def standings(self) -> tuple[Standing, ...]:
        """当前名次：到过终点的按到达早晚排，其余按格子由远到近；同格看谁先到，再看座次。"""
        order = sorted(self._players, key=self._rank_key)
        return tuple(
            Standing(rank=i + 1, player=p, position=self._positions[p], finished_on_turn=self._finished.get(p))
            for i, p in enumerate(order)
        )

    # ---- 内部 ------------------------------------------------------------

    def _roll(self) -> int:
        """掷一次并校验：注入进来的骰子也是外部输入，坏了要当场说清楚。"""
        pips = self._die()
        if isinstance(pips, bool) or not isinstance(pips, int) or pips < 1:
            raise InvalidRollError(f"骰子给出了 {pips!r}，必须是正整数")
        return pips

    def _one_leg(
        self, player: str, pips: int, pending: dict[str, int], rolls: tuple[int, ...]
    ) -> tuple[PositionChange, ...]:
        """一次掷骰引起的全部位置变化，只写进 `pending`，不碰真正的状态。"""
        square = pending.get(player, self._positions[player])
        if square == self._board.start_square and not self._rules.may_start(pips):
            return (PositionChange(player, square, square, ChangeReason.NOT_STARTED),)
        target = self._rules.destination(square, pips, self._board.last_square)
        if target == square:
            return (PositionChange(player, square, square, ChangeReason.BLOCKED),)
        out = [PositionChange(player, square, target, ChangeReason.ROLL)]
        pending[player] = target
        jump = self._board.jump_from(target)
        if jump is not None:
            reason = ChangeReason.SNAKE if jump.is_snake else ChangeReason.LADDER
            out.append(PositionChange(player, target, jump.end, reason))
            pending[player] = jump.end
        for effect in self._rules.effects:
            merged = {**self._positions, **pending}
            ctx = TurnContext(
                player=player,
                square=pending[player],
                positions=MappingProxyType({p: s for p, s in merged.items() if p not in self._finished}),
                rolls=rolls,
                last_square=self._board.last_square,
                rng=self._rng,
            )
            for change in effect(ctx):
                self._check_effect(change)
                pending[change.player] = change.to
                out.append(change)
        return tuple(out)

    def _check_effect(self, change: PositionChange) -> None:
        """格子效果也是外部代码：它不许移动退场的人，也不许把人推到棋盘外面。"""
        if change.player not in self._positions or change.player in self._finished:
            raise SnakeLadderError(f"格子效果想移动 {change.player!r}，但他不在场上")
        if not self._board.start_square <= change.to <= self._board.last_square:
            raise SnakeLadderError(f"格子效果想把 {change.player!r} 挪到 {change.to}，不在棋盘上")

    def _commit(
        self,
        player: str,
        rolls: tuple[int, ...],
        changes: tuple[PositionChange, ...],
        cancelled: bool,
        pending: Mapping[str, int],
    ) -> TurnRecord:
        """把一轮的结果整体写入状态、记日志、换人、通知订阅者。"""
        self._turns += 1
        finishers: list[str] = []
        if not cancelled:
            for name, square in pending.items():
                if square != self._positions[name]:
                    self._positions[name] = square
                    self._arrived[name] = self._turns
                if square == self._board.last_square and name not in self._finished:
                    self._finished[name] = self._turns
                    finishers.append(name)
        record = TurnRecord(
            turn=self._turns,
            player=player,
            rolls=rolls,
            changes=changes,
            cancelled=cancelled,
            finishers=tuple(finishers),
        )
        self._log.append(record)
        self._advance_seat()
        for listener in tuple(self._listeners):
            listener(record)
        return record

    def _advance_seat(self) -> None:
        """轮到下一个还没到终点的人；都到了就原地不动（棋局已经结束）。"""
        for step in range(1, len(self._players) + 1):
            seat = (self._seat + step) % len(self._players)
            if self._players[seat] not in self._finished:
                self._seat = seat
                return

    def _rank_key(self, player: str) -> tuple[int, int, int, int]:
        """名次排序键：到过终点的优先，然后按格子由远到近，同格看谁先到，最后按座次。"""
        finished = self._finished.get(player)
        return (
            0 if finished is not None else 1,
            finished if finished is not None else 0,
            -self._positions[player],
            self._arrived[player],
        )


if __name__ == "__main__":  # pragma: no cover - 演示用
    game = Game(
        classic_board(),
        ["Alice", "Bob", "Carol"],
        rules=RuleSet(roll_again=three_sixes_cancel, effects=(swap_with_leader(42),)),
        rng=random.Random(7),
        play_to_the_end=True,
    )
    result = game.play()
    for row in game.log:
        moves = "".join(f" {c.frm}→{c.to}({c.reason.value})" for c in row.changes)
        print(f"#{row.turn:>3} {row.player:<6} {row.rolls}{moves}{' 整轮作废' if row.cancelled else ''}")
    print(f"收场：{result.outcome.value}，共 {result.turns} 轮")
    for standing in result.standings:
        print(f"  第 {standing.rank} 名 {standing.player}（第 {standing.position} 格）")
