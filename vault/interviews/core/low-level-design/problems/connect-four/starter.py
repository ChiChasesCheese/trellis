"""四子棋——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
from __future__ import annotations
import itertools
import threading
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum, StrEnum
Cell = tuple[int, int]

class Status(Enum):
    IN_PROGRESS = 'in_progress'
    WON = 'won'
    DRAW = 'draw'

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

class Game:

    def __init__(self, rows: int=6, cols: int=7, connect: int=4, players: Sequence[str]=('X', 'O')) -> None:
        """一局棋。`players` 是各玩家的棋子标记（单个字符，互不相同），按顺序轮流落子。

参数不合法抛 ValueError：行列数小于 1，`connect` 小于 2 或大于行列数中较大的一个（永远连不成），
玩家少于 2 个、标记重复或不是单个字符。"""
        raise NotImplementedError

    def drop(self, column: int) -> int:
        """当前玩家在 `column` 列落子，返回棋子落到的行号（0 是最底下一行）。

对局已结束抛 GameOver（先于其他检查）；列号不是范围内的整数抛 InvalidColumn；
这一列已满抛 ColumnFull。失败的调用不改变棋盘，也不消耗回合。"""
        raise NotImplementedError

    @property
    def current_player(self) -> str | None:
        """轮到谁落子；对局结束后是 None。"""
        raise NotImplementedError

    @property
    def status(self) -> Status:
        raise NotImplementedError

    @property
    def winner(self) -> str | None:
        raise NotImplementedError

    def cell(self, row: int, col: int) -> str | None:
        """某一格上的棋子标记，空格是 None；越出棋盘抛 IndexError。"""
        raise NotImplementedError

    def render(self) -> str:
        """画出棋盘：最上面一行在最前，空格是 `.`，行与行之间用换行连接，没有末尾换行。"""
        raise NotImplementedError

    @property
    def moves(self) -> tuple[int, ...]:
        """到目前为止落子的列号序列（只读快照）。"""
        raise NotImplementedError

    def undo(self) -> int:
        """撤销最近一步，返回被撤销的那一步的列号。没有落过子抛 NothingToUndo。

对局结束后也可以撤销：撤销最后一步，对局回到进行中。"""
        raise NotImplementedError

    def legal_moves(self) -> tuple[int, ...]:
        """现在还能落子的列，从小到大；对局结束后为空。"""
        raise NotImplementedError

    @property
    def winning_line(self) -> tuple[Cell, ...]:
        """赢的那条线上的所有格子 (行, 列)，按 (行, 列) 排序；没有赢家时为空。可能比 `connect` 更长。"""
        raise NotImplementedError

    def copy(self) -> Game:
        """一份互不影响的副本（同样的规则、同样的落子历史）。"""
        raise NotImplementedError

    @classmethod
    def from_moves(cls, moves: Sequence[int], rows: int=6, cols: int=7, connect: int=4, players: Sequence[str]=('X', 'O')) -> Game:
        """按列号序列回放出一局棋。序列中任何一步不合法，抛出与 `drop` 相同的异常。"""
        raise NotImplementedError

class UnknownGame(GameError):
    """没有这个对局。"""

class NotAPlayer(GameError):
    """这个玩家不在这局里。"""

class NotYourTurn(GameError):
    """现在不是这个玩家的回合。"""

class Reason(StrEnum):
    CONNECT = 'connect'
    DRAW = 'draw'
    RESIGN = 'resign'
    TIMEOUT = 'timeout'

@dataclass(frozen=True, slots=True)
class MoveResult:
    row: int
    status: Status
    winner: str | None

@dataclass(frozen=True, slots=True)
class GameView:
    """一局棋在某一时刻的只读快照，里面没有任何指向内部对象的引用。"""
    status: Status
    winner: str | None
    current_player: str | None
    board: tuple[str, ...]
    moves: tuple[int, ...]
    reason: Reason | None

class GameService:

    def __init__(self, clock: Callable[[], float]=time.monotonic, move_seconds: float | None=None) -> None:
        """`move_seconds` 不为空时，每一步限时这么多秒（从上一步落下或对局创建算起，到点即超时）。"""
        raise NotImplementedError

    def create_game(self, first: str, second: str, rows: int=6, cols: int=7, connect: int=4) -> str:
        """新建一局，`first` 先手（棋子 X），返回对局 ID。两个玩家 ID 必须是互不相同的非空字符串，否则 ValueError。"""
        raise NotImplementedError

    def move(self, game_id: str, player: str, column: int) -> MoveResult:
        """`player` 在 `column` 列落子。

对局不存在抛 UnknownGame；玩家不在这局里抛 NotAPlayer；对局已结束（含认输、超时）抛 GameOver；
没轮到抛 NotYourTurn；列号不合法或列已满抛 InvalidColumn / ColumnFull（不消耗回合）。
同一时刻多个线程以同一个玩家身份落子，恰好一个成功，其余抛 NotYourTurn。"""
        raise NotImplementedError

    def resign(self, game_id: str, player: str) -> None:
        """认输：对手获胜，原因是 RESIGN。随时可以，不必轮到自己；对局已结束抛 GameOver。"""
        raise NotImplementedError

    def view(self, game_id: str) -> GameView:
        """对局的只读快照。会先处理已经到点的超时。"""
        raise NotImplementedError

def best_move(game: Game, depth: int=4) -> int:
    """为当前玩家选一列：向前看 `depth` 步的带剪枝搜索（negamax + alpha-beta）。

只支持两个玩家的对局，否则 ValueError；对局已结束抛 GameOver。不修改传入的 `game`。
选择顺序固定，所以结果是确定的：先赢，再堵对手的必胜，其余同分时靠近中间的列优先，再小列号优先。"""
    raise NotImplementedError
