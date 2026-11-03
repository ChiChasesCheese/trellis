"""四子棋（Connect Four）：棋盘规则、撤销与回放、多局对战服务、搜索型机器人。

分三层，各管一件事，下一层只用上一层公开的接口：
1. `Game`：纯规则。棋盘按列存成栈（`list[list[str]]`，每列从下往上），落子只是往某一列的栈顶压一个子，
   "重力"因此不需要任何计算；输赢只检查刚落下的那一个子的四条线，不扫整个棋盘。
2. `GameService`：很多局同时进行。每局一把锁，轮次、认输、超时都在这一层，规则层完全不知道"谁是谁"。
3. `best_move`：用 `Game` 的 `drop / undo` 做带剪枝的搜索，不需要碰棋盘的内部结构。

行号从下往上数，第 0 行是最底下一行；列号从左往右，从 0 开始。
"""

from __future__ import annotations

import itertools
import threading
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum, StrEnum

Cell = tuple[int, int]  # (行, 列)


class Status(Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    DRAW = "draw"


class GameError(Exception):
    """所有失败路径的公共基类。"""


class InvalidColumn(GameError, ValueError):
    """列号不是 [0, cols) 里的整数。"""


class ColumnFull(GameError):
    """这一列已经放满了。落子失败不消耗回合。"""


class GameOver(GameError):
    """对局已经结束，不能再落子。"""


class NothingToUndo(GameError):
    """还没有落过任何子。"""


# 四个方向各取一边（另一边是反方向）：横、竖、斜、反斜
_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class Game:
    def __init__(self, rows: int = 6, cols: int = 7, connect: int = 4,
                 players: Sequence[str] = ("X", "O")) -> None:
        """一局棋。`players` 是各玩家的棋子标记（单个字符，互不相同），按顺序轮流落子。

        参数不合法抛 ValueError：行列数小于 1，`connect` 小于 2 或大于行列数中较大的一个（永远连不成），
        玩家少于 2 个、标记重复或不是单个字符。
        """
        marks = tuple(players)
        if (rows < 1 or cols < 1 or not 2 <= connect <= max(rows, cols) or len(marks) < 2
                or len(set(marks)) != len(marks) or any(len(m) != 1 for m in marks)):
            raise ValueError("棋局参数不合法")
        self.rows, self.cols, self.connect, self.players = rows, cols, connect, marks
        self._cols: list[list[str]] = [[] for _ in range(cols)]   # 每列一个栈，从下往上
        self._moves: list[int] = []
        self._result: tuple[str, tuple[Cell, ...]] | None = None  # (赢家, 连成的那条线)

    # ---- 第 1 关：落子、轮流、输赢、平局 ---------------------------------------

    def drop(self, column: int) -> int:
        """当前玩家在 `column` 列落子，返回棋子落到的行号（0 是最底下一行）。

        对局已结束抛 GameOver（先于其他检查）；列号不是范围内的整数抛 InvalidColumn；
        这一列已满抛 ColumnFull。失败的调用不改变棋盘，也不消耗回合。
        """
        if self.status is not Status.IN_PROGRESS:
            raise GameOver("对局已经结束")
        if type(column) is not int or not 0 <= column < self.cols:
            raise InvalidColumn(f"列号必须是 0 到 {self.cols - 1} 的整数")
        stack = self._cols[column]
        if len(stack) >= self.rows:
            raise ColumnFull(f"第 {column} 列已满")
        who = self.current_player
        stack.append(who)
        self._moves.append(column)
        line = self._line_through(len(stack) - 1, column)   # 只检查刚落下的这个子
        if len(line) >= self.connect:
            self._result = (who, line)
        return len(stack) - 1

    @property
    def current_player(self) -> str | None:
        """轮到谁落子；对局结束后是 None。"""
        if self._result is not None or len(self._moves) == self.rows * self.cols:
            return None
        return self.players[len(self._moves) % len(self.players)]

    @property
    def status(self) -> Status:
        if self._result is not None:
            return Status.WON
        return Status.DRAW if len(self._moves) == self.rows * self.cols else Status.IN_PROGRESS

    @property
    def winner(self) -> str | None:
        return self._result[0] if self._result else None

    def cell(self, row: int, col: int) -> str | None:
        """某一格上的棋子标记，空格是 None；越出棋盘抛 IndexError。"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(f"({row}, {col}) 不在棋盘上")
        stack = self._cols[col]
        return stack[row] if row < len(stack) else None

    def render(self) -> str:
        """画出棋盘：最上面一行在最前，空格是 `.`，行与行之间用换行连接，没有末尾换行。"""
        return "\n".join("".join(self.cell(r, c) or "." for c in range(self.cols))
                         for r in range(self.rows - 1, -1, -1))

    def _at(self, row: int, col: int) -> str | None:
        return self.cell(row, col) if 0 <= row < self.rows and 0 <= col < self.cols else None

    def _line_through(self, row: int, col: int) -> tuple[Cell, ...]:
        """经过 (row, col) 的、同色连续的最长一条线（四个方向里最长的），按 (行, 列) 排序。"""
        who = self.cell(row, col)
        best: list[Cell] = []
        for dr, dc in _DIRECTIONS:
            run = [(row, col)]
            for sign in (1, -1):                       # 向两边各延伸到不同色或出界为止
                r, c = row + sign * dr, col + sign * dc
                while self._at(r, c) == who:
                    run.append((r, c))
                    r, c = r + sign * dr, c + sign * dc
            if len(run) > len(best):
                best = run
        return tuple(sorted(best))

    # ---- 第 2 关：撤销、回放、复制 ---------------------------------------------

    @property
    def moves(self) -> tuple[int, ...]:
        """到目前为止落子的列号序列（只读快照）。"""
        return tuple(self._moves)

    def undo(self) -> int:
        """撤销最近一步，返回被撤销的那一步的列号。没有落过子抛 NothingToUndo。

        对局结束后也可以撤销：撤销最后一步，对局回到进行中。
        """
        if not self._moves:
            raise NothingToUndo("还没有落过任何子")
        column = self._moves.pop()
        self._cols[column].pop()
        self._result = None          # 对局只会在最后一步结束，撤销之后必然回到进行中
        return column

    def legal_moves(self) -> tuple[int, ...]:
        """现在还能落子的列，从小到大；对局结束后为空。"""
        if self.status is not Status.IN_PROGRESS:
            return ()
        return tuple(c for c in range(self.cols) if len(self._cols[c]) < self.rows)

    @property
    def winning_line(self) -> tuple[Cell, ...]:
        """赢的那条线上的所有格子 (行, 列)，按 (行, 列) 排序；没有赢家时为空。可能比 `connect` 更长。"""
        return self._result[1] if self._result else ()

    def copy(self) -> Game:
        """一份互不影响的副本（同样的规则、同样的落子历史）。"""
        return Game.from_moves(self._moves, self.rows, self.cols, self.connect, self.players)

    @classmethod
    def from_moves(cls, moves: Sequence[int], rows: int = 6, cols: int = 7, connect: int = 4,
                   players: Sequence[str] = ("X", "O")) -> Game:
        """按列号序列回放出一局棋。序列中任何一步不合法，抛出与 `drop` 相同的异常。"""
        game = cls(rows, cols, connect, players)
        for column in moves:
            game.drop(column)
        return game


# ---- 第 3 关：多局对战服务 ----------------------------------------------------


class UnknownGame(GameError):
    """没有这个对局。"""


class NotAPlayer(GameError):
    """这个玩家不在这局里。"""


class NotYourTurn(GameError):
    """现在不是这个玩家的回合。"""


class Reason(StrEnum):
    CONNECT = "connect"
    DRAW = "draw"
    RESIGN = "resign"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class MoveResult:
    row: int
    status: Status
    winner: str | None      # 玩家 ID


@dataclass(frozen=True, slots=True)
class GameView:
    """一局棋在某一时刻的只读快照，里面没有任何指向内部对象的引用。"""

    status: Status
    winner: str | None              # 玩家 ID
    current_player: str | None      # 玩家 ID；对局结束后是 None
    board: tuple[str, ...]          # 最上面一行在最前，棋子用 X / O，空格是 `.`
    moves: tuple[int, ...]
    reason: Reason | None           # 对局结束的原因；进行中是 None


@dataclass(slots=True)
class _Match:
    game: Game
    players: tuple[str, str]
    lock: threading.Lock
    turn_started: float
    forfeited: Reason | None = None     # 认输或超时时的原因；此时 winner 记在下一个字段
    forfeit_winner: str | None = None


class GameService:
    def __init__(self, clock: Callable[[], float] = time.monotonic, move_seconds: float | None = None) -> None:
        """`move_seconds` 不为空时，每一步限时这么多秒（从上一步落下或对局创建算起，到点即超时）。"""
        self._clock, self._move_seconds = clock, move_seconds
        self._matches: dict[str, _Match] = {}
        self._ids = itertools.count(1)
        self._mu = threading.Lock()                  # 只保护"登记新对局"和"按 ID 查对局"

    def create_game(self, first: str, second: str, rows: int = 6, cols: int = 7, connect: int = 4) -> str:
        """新建一局，`first` 先手（棋子 X），返回对局 ID。两个玩家 ID 必须是互不相同的非空字符串，否则 ValueError。"""
        if not first or not second or first == second:
            raise ValueError("需要两个不同的玩家 ID")
        game = Game(rows, cols, connect)
        with self._mu:
            gid = f"g{next(self._ids)}"
            self._matches[gid] = _Match(game, (first, second), threading.Lock(), self._clock())
        return gid

    def move(self, game_id: str, player: str, column: int) -> MoveResult:
        """`player` 在 `column` 列落子。

        对局不存在抛 UnknownGame；玩家不在这局里抛 NotAPlayer；对局已结束（含认输、超时）抛 GameOver；
        没轮到抛 NotYourTurn；列号不合法或列已满抛 InvalidColumn / ColumnFull（不消耗回合）。
        同一时刻多个线程以同一个玩家身份落子，恰好一个成功，其余抛 NotYourTurn。
        """
        with self._locked(game_id) as m:
            self._check_player(m, player)
            self._settle(m)
            if self._finished(m):
                raise GameOver("对局已经结束")
            if m.players[len(m.game.moves) % 2] != player:
                raise NotYourTurn(f"现在轮到 {m.players[len(m.game.moves) % 2]}")
            row = m.game.drop(column)
            m.turn_started = self._clock()
            return MoveResult(row, m.game.status, self._id_of(m, m.game.winner))

    def resign(self, game_id: str, player: str) -> None:
        """认输：对手获胜，原因是 RESIGN。随时可以，不必轮到自己；对局已结束抛 GameOver。"""
        with self._locked(game_id) as m:
            self._check_player(m, player)
            self._settle(m)
            if self._finished(m):
                raise GameOver("对局已经结束")
            m.forfeited, m.forfeit_winner = Reason.RESIGN, m.players[1 - m.players.index(player)]

    def view(self, game_id: str) -> GameView:
        """对局的只读快照。会先处理已经到点的超时。"""
        with self._locked(game_id) as m:
            self._settle(m)
            g = m.game
            if m.forfeited is not None:
                status, winner, current, reason = Status.WON, m.forfeit_winner, None, m.forfeited
            else:
                winner = self._id_of(m, g.winner)
                current = self._id_of(m, g.current_player)
                reason = {Status.WON: Reason.CONNECT, Status.DRAW: Reason.DRAW}.get(g.status)
                status = g.status
            return GameView(status, winner, current, tuple(g.render().split("\n")), g.moves, reason)

    @contextmanager
    def _locked(self, game_id: str) -> Iterator[_Match]:
        """找到对局并持有它自己的锁：不同对局互不阻塞，全局锁只在查字典的一瞬间持有。"""
        with self._mu:
            match = self._matches.get(game_id)
        if match is None:
            raise UnknownGame(game_id)
        with match.lock:
            yield match

    @staticmethod
    def _check_player(m: _Match, player: str) -> None:
        if player not in m.players:
            raise NotAPlayer(player)

    @staticmethod
    def _id_of(m: _Match, mark: str | None) -> str | None:
        return None if mark is None else m.players[m.game.players.index(mark)]

    @staticmethod
    def _finished(m: _Match) -> bool:
        return m.forfeited is not None or m.game.status is not Status.IN_PROGRESS

    def _settle(self, m: _Match) -> None:
        """惰性处理超时：没有后台线程，任何一次访问都先看一眼该回合是不是已经超时。"""
        if (self._move_seconds is not None and not self._finished(m)
                and self._clock() - m.turn_started >= self._move_seconds):
            mover = len(m.game.moves) % 2
            m.forfeited, m.forfeit_winner = Reason.TIMEOUT, m.players[1 - mover]


# ---- 第 4 关（选做）：搜索型机器人 ----------------------------------------------


def best_move(game: Game, depth: int = 4) -> int:
    """为当前玩家选一列：向前看 `depth` 步的带剪枝搜索（negamax + alpha-beta）。

    只支持两个玩家的对局，否则 ValueError；对局已结束抛 GameOver。不修改传入的 `game`。
    选择顺序固定，所以结果是确定的：先赢，再堵对手的必胜，其余同分时靠近中间的列优先，再小列号优先。
    """
    if len(game.players) != 2:
        raise ValueError("机器人只支持两个玩家")
    if game.status is not Status.IN_PROGRESS:
        raise GameOver("对局已经结束")
    work = game.copy()                                       # 在副本上搜索，调用方的棋局原样不动
    middle = (work.cols - 1) / 2
    order = sorted(work.legal_moves(), key=lambda c: (abs(c - middle), c))
    best_col, best, alpha = order[0], -_INF, -_INF
    for column in order:
        work.drop(column)
        score = -_negamax(work, depth - 1, -_INF, -alpha)
        work.undo()
        if score > best:                                     # 严格大于：同分保留排在前面的列
            best, best_col = score, column
        alpha = max(alpha, best)
    return best_col


_INF = float("inf")
_WIN = 10_000


def _negamax(game: Game, depth: int, alpha: float, beta: float) -> float:
    """从"轮到落子的一方"的角度打分：越大越好。"""
    if game.status is Status.WON:
        return -(_WIN + depth)           # 上一步的人赢了；剩余深度越大说明赢得越早，对输家扣得越多
    if game.status is Status.DRAW:
        return 0
    if depth == 0:
        return _centre_bias(game)
    best = -_INF
    for column in game.legal_moves():
        game.drop(column)
        best = max(best, -_negamax(game, depth - 1, -beta, -alpha))
        game.undo()
        alpha = max(alpha, best)
        if alpha >= beta:                # 剪枝：对手有更好的选择，这条分支不会被走到
            break
    return best


def _centre_bias(game: Game) -> int:
    """叶子的估值：靠近中间的棋子更有价值（中间的格子参与更多条线）。轮到谁落子，就从谁的角度算。"""
    me = game.current_player
    middle = (game.cols - 1) / 2
    total = 0
    for r in range(game.rows):
        for c in range(game.cols):
            mark = game.cell(r, c)
            if mark is not None:
                weight = int(middle - abs(c - middle)) + 1
                total += weight if mark == me else -weight
    return total
