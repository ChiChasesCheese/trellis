"""国际象棋（Chess）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/chess -q
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

FILES = "abcdefgh"


class ChessError(Exception):
    """本设计里所有失败路径的公共基类。"""


class IllegalMoveError(ChessError):
    """这一手不在当前局面的合法着法里。"""


class PromotionRequiredError(ChessError):
    """兵走到底线必须声明升变成什么子。"""


class GameOverError(ChessError):
    """棋局已经结束，不能再走子。"""


class NothingToUndoError(ChessError):
    """没有可悔的棋。"""


class Color(Enum):
    WHITE = "w"
    BLACK = "b"

    @property
    def opponent(self) -> Color:
        raise NotImplementedError


@dataclass(frozen=True, slots=True, order=True)
class Square:
    """一个格子。`row` 0 是第 1 横线（白方底线），`col` 0 是 a 列。"""

    row: int
    col: int

    @property
    def name(self) -> str:
        """`"e4"` 这样的代数记号。"""
        raise NotImplementedError

    @classmethod
    def of(cls, value: Square | str) -> Square:
        """接受 `Square` 或 `"e4"` 这样的代数记号，统一成 `Square`。"""
        raise NotImplementedError

    def offset(self, rows: int, cols: int) -> Square:
        raise NotImplementedError


def on_board(square: Square) -> bool:
    raise NotImplementedError


class MoveKind(Enum):
    """普通着法之外只有两种特例，它们在落子时要做额外的动作。"""

    NORMAL = "normal"
    CASTLE = "castle"
    EN_PASSANT = "en_passant"


@dataclass(frozen=True)
class Piece(ABC):
    """一枚棋子。**不知道自己在哪一格**——位置只由棋盘的字典持有，不存第二份。"""

    color: Color
    letter: ClassVar[str] = "?"
    resets_clock: ClassVar[bool] = False    # 走这种子会不会让五十步计数归零（只有兵会）

    @property
    def symbol(self) -> str:
        """白子大写、黑子小写，用于记谱和局面指纹。"""
        raise NotImplementedError

    @abstractmethod
    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        """从 `origin` 出发、只按本棋子走法能到的格子（不考虑走完之后自己会不会被将）。"""

    def attacks(self, board: Board, origin: Square) -> Iterator[Square]:
        """本棋子**攻击**的格子。默认与落点相同；只有兵不一样。"""
        raise NotImplementedError

    def moves(self, board: Board, origin: Square) -> Iterator[Move]:
        """把落点包装成着法。默认每个落点就是一手普通着法；兵覆写它。"""
        raise NotImplementedError

    def en_passant_square(self, move: Move) -> Square | None:
        """走完之后对方可以吃过路兵的目标格；只有兵的双步会给出它。"""
        raise NotImplementedError


class SlidingPiece(Piece):
    """车、象、后：沿方向一直滑，撞到自己人停、撞到对方吃掉再停。"""

    directions: ClassVar[tuple[tuple[int, int], ...]] = ()

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        raise NotImplementedError


class SteppingPiece(Piece):
    """马和王：只跳固定的一步，落点空着或站着对方的子都行。"""

    steps: ClassVar[tuple[tuple[int, int], ...]] = ()

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        raise NotImplementedError


ORTHOGONAL = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAGONAL = ((1, 1), (1, -1), (-1, 1), (-1, -1))


@dataclass(frozen=True)
class Rook(SlidingPiece):
    letter: ClassVar[str] = "R"
    directions: ClassVar[tuple[tuple[int, int], ...]] = ORTHOGONAL


@dataclass(frozen=True)
class Bishop(SlidingPiece):
    letter: ClassVar[str] = "B"
    directions: ClassVar[tuple[tuple[int, int], ...]] = DIAGONAL


@dataclass(frozen=True)
class Queen(SlidingPiece):
    letter: ClassVar[str] = "Q"
    directions: ClassVar[tuple[tuple[int, int], ...]] = ORTHOGONAL + DIAGONAL


@dataclass(frozen=True)
class Knight(SteppingPiece):
    letter: ClassVar[str] = "N"
    steps: ClassVar[tuple[tuple[int, int], ...]] = (
        (2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))


@dataclass(frozen=True)
class King(SteppingPiece):
    """王只负责"走一步"；易位由 `Board` 生成。"""

    letter: ClassVar[str] = "K"
    steps: ClassVar[tuple[tuple[int, int], ...]] = ORTHOGONAL + DIAGONAL


@dataclass(frozen=True)
class Pawn(Piece):
    """兵是唯一"走法和吃法不同"的子，所以它同时覆写 `attacks` 和 `moves`。"""

    letter: ClassVar[str] = "P"
    resets_clock: ClassVar[bool] = True

    @property
    def forward(self) -> int:
        raise NotImplementedError

    @property
    def last_row(self) -> int:
        raise NotImplementedError

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        raise NotImplementedError

    def attacks(self, board: Board, origin: Square) -> Iterator[Square]:
        """斜前方两格——**不管有没有子**。"""
        raise NotImplementedError

    def moves(self, board: Board, origin: Square) -> Iterator[Move]:
        raise NotImplementedError

    def en_passant_square(self, move: Move) -> Square | None:
        raise NotImplementedError


PROMOTION_CLASSES: Mapping[str, type[Piece]] = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}


@dataclass(frozen=True, slots=True)
class Move:
    """一手棋的完整记录：纯数据，不引用棋盘。后三个字段是被这一手覆盖掉的旧棋盘状态。"""

    origin: Square
    target: Square
    piece: Piece
    kind: MoveKind = MoveKind.NORMAL
    captured: Piece | None = None
    captured_square: Square | None = None
    promotion: str | None = None
    rook_move: tuple[Square, Square] | None = None
    prev_en_passant: Square | None = None
    prev_rights: frozenset[str] = frozenset()
    prev_halfmove: int = 0

    def notation(self) -> str:
        """长代数记谱（long algebraic）：`Ng1-f3`、`e5xd6 e.p.`、`e7-e8=Q`、`O-O`。"""
        raise NotImplementedError


def _castle_plan(row: int, king_side: bool) -> tuple[Square, Square, Square, Square,
                                                     tuple[Square, ...], tuple[Square, ...]]:
    """(王起点, 王终点, 车起点, 车终点, 必须空着的格, 不能被攻击的格)。"""
    raise NotImplementedError


# 填完 `_castle_plan` 之后，把 "K"/"Q"/"k"/"q" 四个易位权的方案建进这张表。
CASTLE_PLANS: dict[str, tuple[Square, Square, Square, Square,
                              tuple[Square, ...], tuple[Square, ...]]] = {}
# 一旦这些格子被"离开"或"被吃"，对应的易位权就没了：王动丢两个，车动或车被吃丢一个。
RIGHT_SQUARES = {Square(0, 4): "KQ", Square(0, 0): "Q", Square(0, 7): "K",
                 Square(7, 4): "kq", Square(7, 0): "q", Square(7, 7): "k"}
BACK_RANK: tuple[type[Piece], ...] = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)


class Board:
    """棋盘：唯一知道"哪一格站着谁"的地方，外加易位权、吃过路兵目标格、五十步计数。"""

    def __init__(self, squares: Mapping[Square | str, Piece], rights: str = "",
                 en_passant: Square | str | None = None, halfmove: int = 0) -> None:
        raise NotImplementedError

    @classmethod
    def initial(cls) -> Board:
        """标准开局摆法。"""
        raise NotImplementedError

    @property
    def castling_rights(self) -> frozenset[str]:
        raise NotImplementedError

    @property
    def en_passant_target(self) -> Square | None:
        raise NotImplementedError

    @property
    def halfmove_clock(self) -> int:
        """距离上一次吃子或动兵过了多少个半回合；到 100 就够五十步和棋了。"""
        raise NotImplementedError

    @property
    def piece_count(self) -> int:
        """盘上还有多少子——悔棋时必须一个不少地回来。"""
        raise NotImplementedError

    def piece_at(self, square: Square) -> Piece | None:
        raise NotImplementedError

    def occupied(self) -> tuple[tuple[Square, Piece], ...]:
        """盘面快照，按格子排序；返回元组，外部拿到手改不动棋盘。"""
        raise NotImplementedError

    def king_square(self, color: Color) -> Square:
        raise NotImplementedError

    def is_attacked(self, square: Square, by: Color) -> bool:
        """`by` 方有没有任何一个子攻击到这一格。"""
        raise NotImplementedError

    def in_check(self, color: Color) -> bool:
        raise NotImplementedError

    def plain_move(self, piece: Piece, origin: Square, target: Square, *,
                   kind: MoveKind = MoveKind.NORMAL, captured_square: Square | None = None,
                   promotion: str | None = None,
                   rook_move: tuple[Square, Square] | None = None) -> Move:
        """把一个落点补全成 `Move`：查出被吃的子，并把当前会被覆盖的棋盘状态一并存进去。"""
        raise NotImplementedError

    def _castling_moves(self, color: Color) -> Iterator[Move]:
        """易位：权利还在、中间空着、且王的起点/经过点/终点都不被攻击。"""
        raise NotImplementedError

    def pseudo_moves(self, color: Color) -> Iterator[Move]:
        """伪合法着法：按棋子走法能走的一切，**不管走完自己的王会不会挨将**。"""
        raise NotImplementedError

    def legal_moves(self, color: Color) -> tuple[Move, ...]:
        """合法着法 = 伪合法着法里走完之后自己的王没有挨将的那些（make/unmake）。"""
        raise NotImplementedError

    def apply(self, move: Move) -> None:
        raise NotImplementedError

    def unapply(self, move: Move) -> None:
        """`apply` 的精确逆操作，包括被吃的子、车的位置和三项棋盘状态。"""
        raise NotImplementedError

    def position_key(self, to_move: Color) -> tuple[object, ...]:
        """局面指纹：子力摆放 + 该谁走 + 易位权 + 吃过路兵目标格。"""
        raise NotImplementedError

    def rows(self) -> tuple[str, ...]:
        """从第 8 横线到第 1 横线的字符画，空格用 `.`。"""
        raise NotImplementedError


class GameStatus(Enum):
    """终局的四种收场。"""

    IN_PROGRESS = "in_progress"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW_FIFTY_MOVE = "draw_fifty_move"
    DRAW_REPETITION = "draw_repetition"


class Game:
    """一局棋：谁该走、走过哪些手、局面重复了几次，以及悔棋。"""

    def __init__(self, board: Board | None = None, to_move: Color = Color.WHITE) -> None:
        raise NotImplementedError

    @property
    def board(self) -> Board:
        raise NotImplementedError

    @property
    def to_move(self) -> Color:
        raise NotImplementedError

    @property
    def history(self) -> tuple[Move, ...]:
        raise NotImplementedError

    @property
    def in_check(self) -> bool:
        raise NotImplementedError

    @property
    def repetition_count(self) -> int:
        """当前局面在本局里出现过几次。"""
        raise NotImplementedError

    @property
    def distinct_positions(self) -> int:
        """局面计数表里有多少条目——悔棋必须让它缩回去。"""
        raise NotImplementedError

    def legal_moves(self) -> tuple[Move, ...]:
        raise NotImplementedError

    @property
    def status(self) -> GameStatus:
        """终局判定的全部逻辑。将死/逼和优先于和棋规则。"""
        raise NotImplementedError

    @property
    def winner(self) -> Color | None:
        raise NotImplementedError

    def move(self, origin: Square | str, target: Square | str, promotion: str | None = None) -> Move:
        """走一手。升变必须显式声明成什么子，否则抛 `PromotionRequiredError`。"""
        raise NotImplementedError

    def undo(self) -> Move:
        """悔一手：局面计数先减（减到 0 就删键），再让棋盘精确回滚。"""
        raise NotImplementedError
