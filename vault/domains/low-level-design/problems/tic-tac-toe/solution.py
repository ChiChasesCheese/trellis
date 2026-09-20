"""井字棋（Tic-Tac-Toe）——N×N 棋盘、K 子连珠、可悔棋、可插机器人的参考实现。

核心思路：胜负判定是这道题唯一有技术含量的地方，本设计把它抽成 `WinRule` 这个seam——
`FullLineRule` 用"每行、每列、两条对角线各一个计数器"做 O(1) 的增量判定（只在 K == N 时
成立），`KInARowRule` 从刚落的那一格向四个方向各走两侧，O(K) 地判 K 子连珠；两者都不需要
扫全盘。`Board` 只管"格子里有什么"和"落子/撤子时通知规则"，它不知道谁该走、也不知道谁赢了；
`Game` 管回合、终局（IN_PROGRESS / WIN / DRAW，平局靠已落子数而不是扫盘得出）和悔棋重做——
一手棋由 `Move` 这条不可变记录完整描述，撤销就是把它反着做一遍，不需要命令对象。机器人是
注入 `Player` 的一个普通函数 `(BoardView, mark) -> Cell`，因此第 4 关加机器人不碰 `Board`
和 `Game` 的任何一行。
"""

from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


# --------------------------------------------------------------------------
# 基本类型与失败路径


class TicTacToeError(Exception):
    """本设计里所有失败路径的公共基类，调用方可以一次性捕获。"""


class OutOfBoardError(TicTacToeError):
    """落子位置不在棋盘范围内。"""


class CellTakenError(TicTacToeError):
    """落子位置已经有子了。"""


class EmptyCellError(TicTacToeError):
    """要撤掉的格子本来就是空的。"""


class NotYourTurnError(TicTacToeError):
    """不是这位玩家的回合。"""


class GameOverError(TicTacToeError):
    """棋局已经结束（有人获胜或和棋），不能再落子。"""


class NothingToUndoError(TicTacToeError):
    """没有可悔的棋。"""


class NothingToRedoError(TicTacToeError):
    """没有可重做的棋。"""


class NoStrategyError(TicTacToeError):
    """当前玩家没有落子策略（是人类），这一手必须由外部用 `play(cell)` 给出。"""


@dataclass(frozen=True, slots=True, order=True)
class Cell:
    """棋盘上的一个格子，行列都从 0 开始；不可变，可以直接做字典键和集合元素。"""

    row: int
    col: int


class GameState(Enum):
    """棋局的三种状态；显式建模，而不是用 `winner is None` 之类的隐含判断。"""

    IN_PROGRESS = "in_progress"
    WIN = "win"
    DRAW = "draw"


# --------------------------------------------------------------------------
# 盘面的只读视图：机器人和判定规则只需要"看"，不需要"改"


class BoardView(Protocol):
    """盘面的只读契约。`Board` 天然满足它，机器人只按这份契约编写。"""

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
    """假设 `cell` 上落的是 `mark`，判断它是否连成了 k 子。

    关键在"假设"两个字：`cell` 本身无条件算作 1 子，因此这个函数**落子前后都能问**——
    落子后问的是"刚才这一手赢了吗"，落子前问的是"我要是走这里会不会赢"。机器人需要的
    正是后者，而增量计数器答不了这种假设句（一问就得改计数器）。复杂度 O(k)。
    """
    k = view.k if k is None else k
    for dr, dc in DIRECTIONS:
        run = 1
        for sign in (1, -1):
            r, c = cell.row + dr * sign, cell.col + dc * sign
            while 0 <= r < view.size and 0 <= c < view.size and view.mark_at(Cell(r, c)) == mark:
                run += 1
                r += dr * sign
                c += dc * sign
        if run >= k:
            return True
    return False


# --------------------------------------------------------------------------
# 胜负判定：两种算法，同一个接口


class WinRule(Protocol):
    """胜负判定规则。`record` 在棋子写进棋盘**之后**被调用，返回这一手是否成线。

    `view` 参数对增量实现是多余的（它靠自己的计数器就够了），但需要看盘面的实现离不开它，
    所以放进协议；这是"接口迁就最需要信息的那个实现"的一个例子。
    """

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        """记下这一手，返回它是否连成一条线。"""

    def forget(self, cell: Cell, mark: str) -> None:
        """撤掉这一手，把规则内部的状态退回去。"""


class FullLineRule:
    """整行、整列或整条对角线连满才算赢（K == N）时的 O(1) 增量判定。

    只维护 2N+2 个计数器：每行一个、每列一个、主副对角线各一个，按棋子符号分开计数。
    一手棋最多命中 4 条线，所以每一手是常数时间，跟棋盘多大无关。
    计数器降到 0 时**删掉这个键**——悔棋到空盘时字典必须重新变空，否则一个本该有界的
    结构会随对局数无限增长。`line_count` 就是为了让这条不变式在外部可验证。
    """

    def __init__(self, size: int) -> None:
        self._size = size
        self._counts: dict[tuple[str, str, int], int] = {}

    def _lines_through(self, cell: Cell) -> tuple[tuple[str, int], ...]:
        """一个格子最多落在 4 条线上：它那一行、那一列，以及（如果在上面）两条对角线。"""
        lines: list[tuple[str, int]] = [("row", cell.row), ("col", cell.col)]
        if cell.row == cell.col:
            lines.append(("diag", 0))
        if cell.row + cell.col == self._size - 1:
            lines.append(("anti", 0))
        return tuple(lines)

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        won = False
        for kind, index in self._lines_through(cell):
            key = (mark, kind, index)
            count = self._counts.get(key, 0) + 1
            self._counts[key] = count
            won = won or count == self._size
        return won

    def forget(self, cell: Cell, mark: str) -> None:
        for kind, index in self._lines_through(cell):
            key = (mark, kind, index)
            remaining = self._counts[key] - 1
            if remaining:
                self._counts[key] = remaining
            else:
                del self._counts[key]

    @property
    def line_count(self) -> int:
        """当前还有多少条线上有子——空盘时必须是 0。"""
        return len(self._counts)


class KInARowRule:
    """K 子连珠（K < N，如五子棋）的判定：从刚落的那一格向四个方向各走两侧，O(K)。

    这种规则**没有**常数时间的增量做法：一条长度为 K 的线可以落在盘上任何位置，
    要预先给每条可能的线配计数器，数量是 O(N²) 而不是 O(N)，而且一手棋会命中其中的
    O(K) 条——省不下来。所以这里索性不留状态，`forget` 什么也不用做。
    """

    def __init__(self, k: int) -> None:
        self._k = k

    def record(self, view: BoardView, cell: Cell, mark: str) -> bool:
        return completes_line(view, cell, mark, self._k)

    def forget(self, cell: Cell, mark: str) -> None:
        return None


# --------------------------------------------------------------------------
# 棋盘：只管格子里有什么


class Board:
    """N×N 棋盘：持有格子，落子与撤子时通知 `WinRule`。

    它守的不变式是"格子内容和胜负规则的内部状态永远同步"——所以规则只能通过
    `place`/`remove` 被更新，没有别的入口。它不知道轮到谁、也不保存历史，那是 `Game` 的事。
    """

    def __init__(self, size: int = 3, k: int | None = None, rule: WinRule | None = None) -> None:
        if size < 1:
            raise ValueError("棋盘边长至少是 1")
        self._size = size
        self._k = size if k is None else k
        if not 1 <= self._k <= size:
            raise ValueError(f"连子数 k 必须落在 1..{size} 之间，收到 {self._k}")
        self._grid: list[list[str | None]] = [[None] * size for _ in range(size)]
        self._played = 0
        self._rule: WinRule = rule if rule is not None else (
            FullLineRule(size) if self._k == size else KInARowRule(self._k))

    @property
    def size(self) -> int:
        return self._size

    @property
    def k(self) -> int:
        return self._k

    @property
    def win_rule(self) -> WinRule:
        """当前使用的胜负规则；公开只读，便于外部检查它的不变式。"""
        return self._rule

    @property
    def moves_played(self) -> int:
        """盘上已有的棋子数——和棋就是靠它判定的，不用扫盘。"""
        return self._played

    @property
    def is_full(self) -> bool:
        return self._played == self._size * self._size

    def contains(self, cell: Cell) -> bool:
        return 0 <= cell.row < self._size and 0 <= cell.col < self._size

    def mark_at(self, cell: Cell) -> str | None:
        if not self.contains(cell):
            raise OutOfBoardError(f"{cell} 不在 {self._size}×{self._size} 的棋盘上")
        return self._grid[cell.row][cell.col]

    def free_cells(self) -> tuple[Cell, ...]:
        """空格的一份快照。返回元组而不是内部列表：外部拿到手的东西改不动棋盘。"""
        return tuple(Cell(r, c) for r in range(self._size) for c in range(self._size)
                     if self._grid[r][c] is None)

    def rows(self) -> tuple[tuple[str | None, ...], ...]:
        """整个盘面的不可变快照，用于展示或存档。"""
        return tuple(tuple(row) for row in self._grid)

    def place(self, cell: Cell, mark: str) -> bool:
        """落子，返回这一手是否连成一条线。位置非法或已被占用时抛异常。"""
        if not self.contains(cell):
            raise OutOfBoardError(f"{cell} 不在 {self._size}×{self._size} 的棋盘上")
        if self._grid[cell.row][cell.col] is not None:
            raise CellTakenError(f"{cell} 已经是 {self._grid[cell.row][cell.col]} 了")
        self._grid[cell.row][cell.col] = mark
        self._played += 1
        return self._rule.record(self, cell, mark)

    def remove(self, cell: Cell) -> str:
        """撤掉一个格子上的子并返回它；规则的内部状态同步回退。"""
        if not self.contains(cell):
            raise OutOfBoardError(f"{cell} 不在 {self._size}×{self._size} 的棋盘上")
        mark = self._grid[cell.row][cell.col]
        if mark is None:
            raise EmptyCellError(f"{cell} 本来就是空的")
        self._grid[cell.row][cell.col] = None
        self._played -= 1
        self._rule.forget(cell, mark)
        return mark


# --------------------------------------------------------------------------
# 玩家与机器人：一手棋的决策就是一个普通函数


MoveChooser = Callable[[BoardView, str], Cell]


@dataclass(frozen=True, slots=True)
class Player:
    """一位玩家：名字、棋子符号，以及（可选的）落子策略。

    人类玩家的 `strategy` 是 `None`——他的决策不在进程里，由外部调用 `play(cell)` 给出。
    机器人只是把一个函数塞进同一个字段，所以第 4 关加机器人不需要动 `Player` 以外的任何类。
    """

    name: str
    mark: str
    strategy: MoveChooser | None = None

    @property
    def is_bot(self) -> bool:
        return self.strategy is not None


@dataclass(frozen=True, slots=True)
class Move:
    """一手棋的完整记录：第几手、落在哪、落的是什么子。撤销它只需要这三样信息。"""

    number: int
    cell: Cell
    mark: str


def random_bot(rng: random.Random) -> MoveChooser:
    """最笨的机器人：在空格里随机挑一个。注入 `Random` 才能让测试可复现。"""

    def choose(view: BoardView, mark: str) -> Cell:
        return rng.choice(view.free_cells())

    return choose


def _rival_marks(view: BoardView, mark: str) -> frozenset[str]:
    """盘上除自己之外还出现过的棋子符号——不写死"对手是 O"，三人局照样能用。"""
    return frozenset(
        other for r in range(view.size) for c in range(view.size)
        if (other := view.mark_at(Cell(r, c))) is not None and other != mark)


def heuristic_bot(rng: random.Random) -> MoveChooser:
    """一步启发式：能赢就赢，不能赢就堵，都不是就往中心靠，同分随机。

    它只用 `BoardView` 上的只读方法和 `completes_line` 这个假设判定，一行棋盘或棋局的
    代码都没碰——这正是第 4 关想看到的证据。
    """

    def choose(view: BoardView, mark: str) -> Cell:
        free = view.free_cells()
        for cell in free:                       # 一、自己能连线就直接连
            if completes_line(view, cell, mark, view.k):
                return cell
        for rival in sorted(_rival_marks(view, mark)):
            for cell in free:                   # 二、对手下一手能连线就堵住
                if completes_line(view, cell, rival, view.k):
                    return cell
        center = (view.size - 1) / 2            # 三、越靠中心的格子在越多条线上
        best = min(abs(c.row - center) + abs(c.col - center) for c in free)
        tied = [c for c in free if abs(c.row - center) + abs(c.col - center) == best]
        return rng.choice(tied)

    return choose


# --------------------------------------------------------------------------
# 棋局：回合、终局与悔棋


class Game:
    """一局棋：谁该走、棋局是什么状态、走过哪些手，以及悔棋与重做。

    它守的不变式是"`state`、`winner` 和 `moves` 永远互相自洽"：只有 `_apply` 能改这三样。
    棋盘规则（怎么算赢）和玩家决策（走哪）都不在这里，`Game` 只做编排。
    """

    def __init__(self, board: Board, players: Sequence[Player]) -> None:
        if len(players) < 2:
            raise ValueError("至少要两位玩家")
        marks = [p.mark for p in players]
        if len(set(marks)) != len(marks):
            raise ValueError(f"玩家的棋子符号必须两两不同，收到 {marks}")
        self._board = board
        self._players = tuple(players)
        self._history: list[Move] = []
        self._redo: list[Move] = []
        self._state = GameState.IN_PROGRESS
        self._winner: Player | None = None

    @property
    def board(self) -> Board:
        return self._board

    @property
    def players(self) -> tuple[Player, ...]:
        return self._players

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def winner(self) -> Player | None:
        return self._winner

    @property
    def current_player(self) -> Player:
        """轮到谁，由已走手数推出来，因此悔棋之后自动回到正确的一方。"""
        return self._players[len(self._history) % len(self._players)]

    @property
    def moves(self) -> tuple[Move, ...]:
        """走子历史的快照。"""
        return tuple(self._history)

    @property
    def undo_depth(self) -> int:
        return len(self._history)

    @property
    def redo_depth(self) -> int:
        """重做栈的深度——新走一手之后必须归零，否则就会重做出一段不存在的历史。"""
        return len(self._redo)

    def _apply(self, cell: Cell, player: Player) -> Move:
        """把一手棋落到盘上并更新终局状态；`play` 和 `redo` 共用，避免两份判负逻辑。"""
        won = self._board.place(cell, player.mark)
        move = Move(number=len(self._history) + 1, cell=cell, mark=player.mark)
        self._history.append(move)
        if won:
            self._state, self._winner = GameState.WIN, player
        elif self._board.is_full:
            self._state = GameState.DRAW
        return move

    def play(self, cell: Cell, by: Player | None = None) -> Move:
        """走一手。`by` 给出时会校验确实轮到他；棋局已结束、位置非法都会抛异常。"""
        if self._state is not GameState.IN_PROGRESS:
            raise GameOverError(f"棋局已经结束（{self._state.value}），不能再落子")
        player = self.current_player
        if by is not None and by.mark != player.mark:
            raise NotYourTurnError(f"现在轮到 {player.name}（{player.mark}），不是 {by.name}")
        move = self._apply(cell, player)
        self._redo.clear()      # 走出新的一手，原来的重做分支就作废了
        return move

    def play_turn(self) -> Move:
        """让当前玩家自己决定这一手；人类玩家没有策略，会抛 `NoStrategyError`。"""
        if self._state is not GameState.IN_PROGRESS:
            raise GameOverError(f"棋局已经结束（{self._state.value}），不能再落子")
        player = self.current_player
        if player.strategy is None:
            raise NoStrategyError(f"{player.name} 没有落子策略，请用 play(cell) 给出这一手")
        return self.play(player.strategy(self._board, player.mark))

    def undo(self) -> Move:
        """悔一手：从盘上撤掉它，压进重做栈，棋局回到进行中。"""
        if not self._history:
            raise NothingToUndoError("还没有走过任何一手")
        move = self._history.pop()
        self._board.remove(move.cell)
        self._redo.append(move)
        self._state, self._winner = GameState.IN_PROGRESS, None
        return move

    def redo(self) -> Move:
        """重做一手：重放的正是刚才悔掉的那一手，轮到的人必然对得上。"""
        if not self._redo:
            raise NothingToRedoError("没有可重做的棋")
        move = self._redo.pop()
        return self._apply(move.cell, self.current_player)


def play_out(game: Game) -> Game:
    """让全是机器人的一局自己下完；人类在场时会抛 `NoStrategyError`。"""
    while game.state is GameState.IN_PROGRESS:
        game.play_turn()
    return game


if __name__ == "__main__":
    rng = random.Random(7)
    demo = play_out(Game(Board(size=3), [
        Player("启发式", "X", heuristic_bot(rng)),
        Player("随机", "O", random_bot(rng)),
    ]))
    for row in demo.board.rows():
        print(" ".join(m or "." for m in row))
    print(demo.state.value, demo.winner.name if demo.winner else "")
