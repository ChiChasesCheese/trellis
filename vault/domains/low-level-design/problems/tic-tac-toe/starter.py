"""井字棋（Tic-Tac-Toe）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass`、`Protocol` 和异常都和 `solution.py` 一致；
把标了 `raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/tic-tac-toe -q
"""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class TicTacToeError(Exception):
    """本设计里所有失败路径的公共基类。"""


class OutOfBoardError(TicTacToeError):
    """落子位置不在棋盘范围内。"""


class CellTakenError(TicTacToeError):
    """落子位置已经有子了。"""


class EmptyCellError(TicTacToeError):
    """要撤掉的格子本来就是空的。"""


class NotYourTurnError(TicTacToeError):
    """不是这位玩家的回合。"""


class GameOverError(TicTacToeError):
    """棋局已经结束，不能再落子。"""


class NothingToUndoError(TicTacToeError):
    """没有可悔的棋。"""


class NothingToRedoError(TicTacToeError):
    """没有可重做的棋。"""


class NoStrategyError(TicTacToeError):
    """当前玩家没有落子策略（是人类）。"""


@dataclass(frozen=True, slots=True, order=True)
class Cell:
    row: int
    col: int


class GameState(Enum):
    IN_PROGRESS = "in_progress"
    WIN = "win"
    DRAW = "draw"


class BoardView(Protocol):
    """盘面的只读契约。"""

    @property
    def size(self) -> int:
        """棋盘边长 N。"""

    @property
    def k(self) -> int:
        """连成多少子算赢。"""

    def mark_at(self, cell: Cell) -> str | None:
        """格子里的棋子符号；空格返回 `None`。"""

    def free_cells(self) -> tuple[Cell, ...]:
        """当前所有空格的一份快照，按行优先顺序。"""


DIRECTIONS: tuple[tuple[int, int], ...] = ((0, 1), (1, 0), (1, 1), (1, -1))


def completes_line(view: BoardView, cell: Cell, mark: str, k: int | None = None) -> bool:
    """假设 `cell` 上落的是 `mark`，判断它是否连成了 k 子（落子前后都能问）。"""
    raise NotImplementedError


class WinRule(Protocol):
    """胜负判定规则；`record` 在棋子写进棋盘之后被调用。"""

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        """记下这一手，返回它是否连成一条线。"""

    def forget(self, cell: Cell, mark: str) -> None:
        """撤掉这一手，把规则内部的状态退回去。"""


class FullLineRule:
    """K == N 时的 O(1) 增量判定：每行、每列、两条对角线各一个计数器。"""

    def __init__(self, size: int) -> None:
        raise NotImplementedError

    def _lines_through(self, cell: Cell) -> tuple[tuple[str, int], ...]:
        raise NotImplementedError

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        raise NotImplementedError

    def forget(self, cell: Cell, mark: str) -> None:
        raise NotImplementedError

    @property
    def line_count(self) -> int:
        """当前还有多少条线上有子——空盘时必须是 0。"""
        raise NotImplementedError


class KInARowRule:
    """K 子连珠（K < N）的判定：从刚落的那一格向四个方向各走两侧，O(K)，无内部状态。"""

    def __init__(self, k: int) -> None:
        raise NotImplementedError

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        raise NotImplementedError

    def forget(self, cell: Cell, mark: str) -> None:
        raise NotImplementedError


class Board:
    """N×N 棋盘：持有格子，落子与撤子时通知 `WinRule`。"""

    def __init__(self, size: int = 3, k: int | None = None, rule: WinRule | None = None) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    @property
    def k(self) -> int:
        raise NotImplementedError

    @property
    def win_rule(self) -> WinRule:
        """当前使用的胜负规则；公开只读，便于外部检查它的不变式。"""
        raise NotImplementedError

    @property
    def moves_played(self) -> int:
        """盘上已有的棋子数——和棋靠它判定，不用扫盘。"""
        raise NotImplementedError

    @property
    def is_full(self) -> bool:
        raise NotImplementedError

    def contains(self, cell: Cell) -> bool:
        raise NotImplementedError

    def mark_at(self, cell: Cell) -> str | None:
        raise NotImplementedError

    def free_cells(self) -> tuple[Cell, ...]:
        """空格的一份快照，外部改不动棋盘。"""
        raise NotImplementedError

    def rows(self) -> tuple[tuple[str | None, ...], ...]:
        """整个盘面的不可变快照。"""
        raise NotImplementedError

    def place(self, cell: Cell, mark: str) -> bool:
        """落子，返回这一手是否连成一条线。"""
        raise NotImplementedError

    def remove(self, cell: Cell) -> str:
        """撤掉一个格子上的子并返回它；规则的内部状态同步回退。"""
        raise NotImplementedError


MoveChooser = Callable[[BoardView, str], Cell]


@dataclass(frozen=True, slots=True)
class Player:
    name: str
    mark: str
    strategy: MoveChooser | None = None

    @property
    def is_bot(self) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Move:
    number: int
    cell: Cell
    mark: str


def random_bot(rng: random.Random) -> MoveChooser:
    """在空格里随机挑一个。"""
    raise NotImplementedError


def _rival_marks(view: BoardView, mark: str) -> frozenset[str]:
    """盘上除自己之外还出现过的棋子符号。"""
    raise NotImplementedError


def heuristic_bot(rng: random.Random) -> MoveChooser:
    """一步启发式：能赢就赢，不能赢就堵，都不是就往中心靠，同分随机。"""
    raise NotImplementedError


class Game:
    """一局棋：谁该走、棋局是什么状态、走过哪些手，以及悔棋与重做。"""

    def __init__(self, board: Board, players: Sequence[Player]) -> None:
        raise NotImplementedError

    @property
    def board(self) -> Board:
        raise NotImplementedError

    @property
    def players(self) -> tuple[Player, ...]:
        raise NotImplementedError

    @property
    def state(self) -> GameState:
        raise NotImplementedError

    @property
    def winner(self) -> Player | None:
        raise NotImplementedError

    @property
    def current_player(self) -> Player:
        """轮到谁，由已走手数推出来。"""
        raise NotImplementedError

    @property
    def moves(self) -> tuple[Move, ...]:
        raise NotImplementedError

    @property
    def undo_depth(self) -> int:
        raise NotImplementedError

    @property
    def redo_depth(self) -> int:
        """重做栈的深度——新走一手之后必须归零。"""
        raise NotImplementedError

    def _apply(self, cell: Cell, player: Player) -> Move:
        raise NotImplementedError

    def play(self, cell: Cell, by: Player | None = None) -> Move:
        """走一手；`by` 给出时会校验确实轮到他。"""
        raise NotImplementedError

    def play_turn(self) -> Move:
        """让当前玩家自己决定这一手。"""
        raise NotImplementedError

    def undo(self) -> Move:
        """悔一手。"""
        raise NotImplementedError

    def redo(self) -> Move:
        """重做一手。"""
        raise NotImplementedError


def play_out(game: Game) -> Game:
    """让全是机器人的一局自己下完。"""
    raise NotImplementedError
