"""国际象棋（Chess）——走法生成、合法性过滤、特殊着法与悔棋的参考实现。

核心思路：棋子是**值**不是实体——不可变、只有颜色、不知道自己在哪，"谁在哪一格"只由 `Board`
的一张稀疏字典说了算，从根上杜绝两份真源。走法生成是多态的：车象后共用"沿方向一直走"，马王
共用"跳一步"，兵覆写 `moves()` 自己长出吃过路兵与升变，`Board` 里没有一处 `isinstance` 阶梯。
合法性不属于棋子而属于局面：先生成伪合法着法，再逐个 make/unmake，走完自己王还挨将的丢掉；
将死与逼和于是退化成同一句"没有合法着法，看王在不在将中"。易位权、吃过路兵目标格、五十步计数
放在 `Board` 上，被这一手覆盖掉的旧值随 `Move` 一起存下来，所以悔棋是精确回滚而非重新推演。
不做搜索、不做局面评估，那是引擎的事。
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
        return Color.BLACK if self is Color.WHITE else Color.WHITE

@dataclass(frozen=True, slots=True, order=True)
class Square:
    """一个格子。`row` 0 是第 1 横线（白方底线），`col` 0 是 a 列。"""
    row: int
    col: int

    @property
    def name(self) -> str:
        return f"{FILES[self.col]}{self.row + 1}"

    @classmethod
    def of(cls, value: Square | str) -> Square:
        """接受 `Square` 或 `"e4"` 这样的代数记号，统一成 `Square`。"""
        return value if isinstance(value, Square) else cls(int(value[1]) - 1, FILES.index(value[0]))

    def offset(self, rows: int, cols: int) -> Square:
        return Square(self.row + rows, self.col + cols)

def on_board(square: Square) -> bool:
    return 0 <= square.row < 8 and 0 <= square.col < 8

class MoveKind(Enum):
    """普通着法之外只有两种特例，它们在落子时要做额外的动作。"""
    NORMAL = "normal"
    CASTLE = "castle"
    EN_PASSANT = "en_passant"

@dataclass(frozen=True)
class Piece(ABC):
    """一枚棋子。**不知道自己在哪一格**——位置只由棋盘的字典持有，不存第二份；不可变且只有
    颜色，所以全局其实只需要 12 个实例。"""
    color: Color
    letter: ClassVar[str] = "?"
    resets_clock: ClassVar[bool] = False    # 走这种子会不会让五十步计数归零（只有兵会）

    @property
    def symbol(self) -> str:
        """白子大写、黑子小写，用于记谱和局面指纹。"""
        return self.letter if self.color is Color.WHITE else self.letter.lower()

    @abstractmethod
    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        """从 `origin` 出发、只按本棋子走法能到的格子（不考虑走完之后自己会不会被将）。"""

    def attacks(self, board: Board, origin: Square) -> Iterator[Square]:
        """本棋子**攻击**的格子。默认与落点相同；只有兵不一样，所以只有兵覆写它。"""
        return self.destinations(board, origin)

    def moves(self, board: Board, origin: Square) -> Iterator[Move]:
        """把落点包装成着法。默认每个落点就是一手普通着法；兵覆写它，长出吃过路兵与升变。"""
        for target in self.destinations(board, origin):
            yield board.plain_move(self, origin, target)

    def en_passant_square(self, move: Move) -> Square | None:
        """走完之后对方可以吃过路兵的目标格；只有兵的双步会给出它。"""
        return None

class SlidingPiece(Piece):
    """车、象、后：沿方向一直滑，撞到自己人停、撞到对方吃掉再停。三者唯一的差别是方向表，
    所以这段走法只写一次——这就是"多态代替类型阶梯"的本体。"""
    directions: ClassVar[tuple[tuple[int, int], ...]] = ()

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        for rows, cols in self.directions:
            square = origin.offset(rows, cols)
            while on_board(square):
                other = board.piece_at(square)
                if other is None:
                    yield square
                else:
                    if other.color is not self.color:
                        yield square
                    break
                square = square.offset(rows, cols)

class SteppingPiece(Piece):
    """马和王：只跳固定的一步，落点空着或站着对方的子都行。"""
    steps: ClassVar[tuple[tuple[int, int], ...]] = ()

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        for rows, cols in self.steps:
            square = origin.offset(rows, cols)
            if on_board(square):
                other = board.piece_at(square)
                if other is None or other.color is not self.color:
                    yield square

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
    """王只负责"走一步"。易位不在这里——它要用易位权和"不能经过被攻击的格"，那是局面的知识。"""
    letter: ClassVar[str] = "K"
    steps: ClassVar[tuple[tuple[int, int], ...]] = ORTHOGONAL + DIAGONAL

@dataclass(frozen=True)
class Pawn(Piece):
    """兵是唯一"走法和吃法不同"的子，所以它同时覆写 `attacks` 和 `moves`。"""
    letter: ClassVar[str] = "P"
    resets_clock: ClassVar[bool] = True

    @property
    def forward(self) -> int:
        return 1 if self.color is Color.WHITE else -1

    @property
    def last_row(self) -> int:
        return 7 if self.color is Color.WHITE else 0

    def destinations(self, board: Board, origin: Square) -> Iterator[Square]:
        one = origin.offset(self.forward, 0)
        if on_board(one) and board.piece_at(one) is None:
            yield one
            two = origin.offset(2 * self.forward, 0)
            if origin.row == (1 if self.color is Color.WHITE else 6) and board.piece_at(two) is None:
                yield two
        for square in self.attacks(board, origin):
            # 吃过路兵要吃的子不在目标格上，而在自己同一横线的那一格；把它一并当成"这手吃的子"
            # 参与下面的敌我判断，顺带挡掉"过路格是自己人双步留下的"这种假过路兵。
            other = board.piece_at(square) or (
                board.piece_at(Square(origin.row, square.col))
                if square == board.en_passant_target else None)
            if other is not None and other.color is not self.color:
                yield square

    def attacks(self, board: Board, origin: Square) -> Iterator[Square]:
        """斜前方两格——**不管有没有子**。正前方虽然能走，却从不攻击，判"王是否被将"靠的是这个。"""
        for cols in (-1, 1):
            square = origin.offset(self.forward, cols)
            if on_board(square):
                yield square

    def moves(self, board: Board, origin: Square) -> Iterator[Move]:
        for target in self.destinations(board, origin):
            if target == board.en_passant_target:
                yield board.plain_move(self, origin, target, kind=MoveKind.EN_PASSANT,
                                       captured_square=Square(origin.row, target.col))
            elif target.row == self.last_row:
                for letter in PROMOTION_CLASSES:
                    yield board.plain_move(self, origin, target, promotion=letter)
            else:
                yield board.plain_move(self, origin, target)

    def en_passant_square(self, move: Move) -> Square | None:
        if abs(move.target.row - move.origin.row) == 2:
            return Square((move.origin.row + move.target.row) // 2, move.origin.col)
        return None

PROMOTION_CLASSES: Mapping[str, type[Piece]] = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
@dataclass(frozen=True, slots=True)
class Move:
    """一手棋的完整记录：纯数据，不引用棋盘，可以存盘、传给别的进程、在别的盘上重放。后三个
    字段是被这一手**覆盖掉的旧棋盘状态**（备忘录 Memento），有了它们悔棋才是精确回滚。"""
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
        """长代数记谱：`Ng1-f3`、`e5xd6 e.p.`、`e7-e8=Q`、`O-O`。不用 SAN（`Nf3`）是因为它要靠
        "还有没有别的马也能到 f3"消歧，那要回头重新生成一遍合法着法，记谱就依赖了走法生成。"""
        if self.kind is MoveKind.CASTLE:
            return "O-O" if self.target.col == 6 else "O-O-O"
        head = "" if self.piece.letter == "P" else self.piece.letter
        text = f"{head}{self.origin.name}{'x' if self.captured else '-'}{self.target.name}"
        if self.promotion:
            text += f"={self.promotion}"
        return text + (" e.p." if self.kind is MoveKind.EN_PASSANT else "")

def _castle_plan(row: int, king_side: bool) -> tuple[Square, Square, Square, Square,
                                                     tuple[Square, ...], tuple[Square, ...]]:
    """(王起点, 王终点, 车起点, 车终点, 必须空着的格, 不能被攻击的格)。"""
    king = Square(row, 4)
    if king_side:
        return (king, Square(row, 6), Square(row, 7), Square(row, 5),
                (Square(row, 5), Square(row, 6)), (king, Square(row, 5), Square(row, 6)))
    return (king, Square(row, 2), Square(row, 0), Square(row, 3),
            (Square(row, 1), Square(row, 2), Square(row, 3)), (king, Square(row, 3), Square(row, 2)))

CASTLE_PLANS = {"K": _castle_plan(0, True), "Q": _castle_plan(0, False),
                "k": _castle_plan(7, True), "q": _castle_plan(7, False)}
# 一旦这些格子被"离开"或"被吃"，对应的易位权就没了：王动丢两个，车动或车被吃丢一个。
RIGHT_SQUARES = {Square(0, 4): "KQ", Square(0, 0): "Q", Square(0, 7): "K",
                 Square(7, 4): "kq", Square(7, 0): "q", Square(7, 7): "k"}
BACK_RANK: tuple[type[Piece], ...] = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

class Board:
    """棋盘：唯一知道"哪一格站着谁"的地方，外加易位权、吃过路兵目标格、五十步计数。它守的
    不变式是 `apply` 与 `unapply` 严格互逆；它不知道轮到谁走、也不保存历史，那是 `Game` 的事。"""

    def __init__(self, squares: Mapping[Square | str, Piece], rights: str = "",
                 en_passant: Square | str | None = None, halfmove: int = 0) -> None:
        self._squares: dict[Square, Piece] = {Square.of(k): v for k, v in squares.items()}
        self._rights = frozenset(rights)
        self._en_passant = None if en_passant is None else Square.of(en_passant)
        self._halfmove = halfmove

    @classmethod
    def initial(cls) -> Board:
        """标准开局摆法。"""
        squares: dict[Square | str, Piece] = {}
        for col, kind in enumerate(BACK_RANK):
            squares[Square(0, col)] = kind(Color.WHITE)
            squares[Square(7, col)] = kind(Color.BLACK)
            squares[Square(1, col)] = Pawn(Color.WHITE)
            squares[Square(6, col)] = Pawn(Color.BLACK)
        return cls(squares, rights="KQkq")

    @property
    def castling_rights(self) -> frozenset[str]:
        """还剩哪些易位权；`frozenset` 本身不可变，交出去也改不动棋盘。"""
        return self._rights

    @property
    def en_passant_target(self) -> Square | None:
        return self._en_passant

    @property
    def halfmove_clock(self) -> int:
        """距离上一次吃子或动兵过了多少个半回合；到 100 就够五十步和棋了。"""
        return self._halfmove

    @property
    def piece_count(self) -> int:
        """盘上还有多少子——被吃的子必须真的从字典里消失，悔棋时必须一个不少地回来。"""
        return len(self._squares)

    def piece_at(self, square: Square) -> Piece | None:
        return self._squares.get(square)

    def occupied(self) -> tuple[tuple[Square, Piece], ...]:
        """盘面快照，按格子排序；返回元组，外部改不动棋盘。"""
        return tuple(sorted(self._squares.items()))

    def king_square(self, color: Color) -> Square:
        for square, piece in self._squares.items():
            if piece.color is color and piece.letter == "K":
                return square
        raise LookupError(f"{color.value} 方没有王")

    def is_attacked(self, square: Square, by: Color) -> bool:
        """`by` 方有没有任何一个子攻击到这一格。判将、判易位能不能走，都只用这一个问句。"""
        return any(square in piece.attacks(self, origin)
                   for origin, piece in self._squares.items() if piece.color is by)

    def in_check(self, color: Color) -> bool:
        return self.is_attacked(self.king_square(color), color.opponent)

    def plain_move(self, piece: Piece, origin: Square, target: Square, *,
                   kind: MoveKind = MoveKind.NORMAL, captured_square: Square | None = None,
                   promotion: str | None = None, rook_move: "tuple[Square, Square] | None" = None) -> Move:
        """把一个落点补全成 `Move`：查出被吃的子，并把当前会被覆盖的棋盘状态一并存进去。"""
        victim_square = target if captured_square is None else captured_square
        captured = self._squares.get(victim_square)
        return Move(origin, target, piece, kind, captured,
                    victim_square if captured is not None else None, promotion, rook_move,
                    self._en_passant, self._rights, self._halfmove)

    def _castling_moves(self, color: Color) -> Iterator[Move]:
        """易位：权利还在、中间空着、且王的起点/经过点/终点都不被攻击。"""
        for letter in ("KQ" if color is Color.WHITE else "kq"):
            if letter not in self._rights:
                continue
            king_from, king_to, rook_from, rook_to, empty, safe = CASTLE_PLANS[letter]
            king = self._squares.get(king_from)
            if king is None or any(self._squares.get(s) is not None for s in empty):
                continue
            if any(self.is_attacked(s, color.opponent) for s in safe):
                continue
            yield self.plain_move(king, king_from, king_to, kind=MoveKind.CASTLE,
                                  rook_move=(rook_from, rook_to))

    def pseudo_moves(self, color: Color) -> Iterator[Move]:
        """伪合法着法：按棋子走法能走的一切，**不管走完自己的王会不会挨将**。"""
        for origin, piece in list(self._squares.items()):
            if piece.color is color:
                yield from piece.moves(self, origin)
        yield from self._castling_moves(color)

    def legal_moves(self, color: Color) -> tuple[Move, ...]:
        """合法着法 = 伪合法着法里走完之后自己的王没有挨将的那些。做法是 make/unmake：在同一块
        棋盘上落子、问一句、再精确回滚，比每次深拷贝棋盘便宜，代价是回滚必须和落子严格互逆。"""
        legal = []
        for move in list(self.pseudo_moves(color)):
            self.apply(move)
            if not self.is_attacked(self.king_square(color), color.opponent):
                legal.append(move)
            self.unapply(move)
        return tuple(legal)

    def apply(self, move: Move) -> None:
        if move.captured_square is not None:
            del self._squares[move.captured_square]
        del self._squares[move.origin]
        self._squares[move.target] = (PROMOTION_CLASSES[move.promotion](move.piece.color)
                                      if move.promotion else move.piece)
        if move.rook_move is not None:
            rook_from, rook_to = move.rook_move
            self._squares[rook_to] = self._squares.pop(rook_from)
        self._en_passant = move.piece.en_passant_square(move)
        self._rights = self._rights - set(RIGHT_SQUARES.get(move.origin, "")) \
            - set(RIGHT_SQUARES.get(move.target, ""))
        self._halfmove = 0 if (move.captured is not None or move.piece.resets_clock) else self._halfmove + 1

    def unapply(self, move: Move) -> None:
        """`apply` 的精确逆操作，包括被吃的子、车的位置和三项棋盘状态。"""
        if move.rook_move is not None:
            rook_from, rook_to = move.rook_move
            self._squares[rook_from] = self._squares.pop(rook_to)
        del self._squares[move.target]
        self._squares[move.origin] = move.piece
        if move.captured is not None and move.captured_square is not None:
            self._squares[move.captured_square] = move.captured
        self._en_passant, self._rights, self._halfmove = (
            move.prev_en_passant, move.prev_rights, move.prev_halfmove)

    def position_key(self, to_move: Color) -> tuple[object, ...]:
        """局面指纹：子力摆放 + 该谁走 + 易位权 + 吃过路兵目标格。三次重复就是靠它数出来的。"""
        return (tuple((s.row, s.col, p.symbol) for s, p in self.occupied()),
                to_move, tuple(sorted(self._rights)), self._en_passant)

    def rows(self) -> tuple[str, ...]:
        """从第 8 横线到第 1 横线的字符画，空格用 `.`；给人看，不参与任何判断。"""
        return tuple("".join(p.symbol if (p := self.piece_at(Square(r, c))) else "."
                             for c in range(8)) for r in range(7, -1, -1))

class GameStatus(Enum):
    """终局的四种收场；将死与逼和的区别只有一句"没有合法着法时王在不在将中"。"""
    IN_PROGRESS = "in_progress"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW_FIFTY_MOVE = "draw_fifty_move"
    DRAW_REPETITION = "draw_repetition"

class Game:
    """一局棋：谁该走、走过哪些手、局面重复了几次，以及悔棋。它不复制任何棋盘知识：
    合法着法问 `Board`，终局只是对"合法着法为空"和两个计数的解释。"""

    def __init__(self, board: Board | None = None, to_move: Color = Color.WHITE) -> None:
        self._board = board if board is not None else Board.initial()
        self._to_move = to_move
        self._history: list[Move] = []
        self._seen: dict[tuple[object, ...], int] = {self._board.position_key(to_move): 1}

    @property
    def board(self) -> Board:
        return self._board

    @property
    def to_move(self) -> Color:
        return self._to_move

    @property
    def history(self) -> tuple[Move, ...]:
        return tuple(self._history)

    @property
    def in_check(self) -> bool:
        return self._board.in_check(self._to_move)

    @property
    def repetition_count(self) -> int:
        """当前局面在本局里出现过几次。"""
        return self._seen.get(self._board.position_key(self._to_move), 0)

    @property
    def distinct_positions(self) -> int:
        """局面计数表里有多少条目——悔棋必须让它缩回去，否则一局长棋会无限吃内存。"""
        return len(self._seen)

    def legal_moves(self) -> tuple[Move, ...]:
        return self._board.legal_moves(self._to_move)

    @property
    def status(self) -> GameStatus:
        """终局判定的全部逻辑。将死/逼和优先于和棋规则，和 FIDE 规则一致。"""
        if not self.legal_moves():
            return GameStatus.CHECKMATE if self.in_check else GameStatus.STALEMATE
        if self._board.halfmove_clock >= 100:
            return GameStatus.DRAW_FIFTY_MOVE
        if self.repetition_count >= 3:
            return GameStatus.DRAW_REPETITION
        return GameStatus.IN_PROGRESS

    @property
    def winner(self) -> Color | None:
        return self._to_move.opponent if self.status is GameStatus.CHECKMATE else None

    def move(self, origin: Square | str, target: Square | str, promotion: str | None = None) -> Move:
        """走一手。升变必须显式声明成什么子，否则抛 `PromotionRequiredError`。"""
        if self.status is not GameStatus.IN_PROGRESS:
            raise GameOverError(f"棋局已经结束（{self.status.value}）")
        start, end = Square.of(origin), Square.of(target)
        matches = [m for m in self.legal_moves() if m.origin == start and m.target == end]
        if not matches:
            raise IllegalMoveError(f"{start.name}{end.name} 不是当前局面的合法着法")
        if promotion is None and matches[0].promotion is not None:
            raise PromotionRequiredError(f"{start.name}{end.name} 是升变，请指定 Q/R/B/N")
        chosen = next((m for m in matches if m.promotion == promotion), None)
        if chosen is None:
            raise IllegalMoveError(f"{start.name}{end.name} 不能升变成 {promotion}")
        self._board.apply(chosen)
        self._history.append(chosen)
        self._to_move = self._to_move.opponent
        key = self._board.position_key(self._to_move)
        self._seen[key] = self._seen.get(key, 0) + 1
        return chosen

    def undo(self) -> Move:
        """悔一手：局面计数先减（减到 0 就删键），再让棋盘精确回滚。"""
        if not self._history:
            raise NothingToUndoError("还没有走过任何一手")
        key = self._board.position_key(self._to_move)
        if remaining := self._seen[key] - 1:
            self._seen[key] = remaining
        else:
            del self._seen[key]
        move = self._history.pop()
        self._board.unapply(move)
        self._to_move = self._to_move.opponent
        return move

if __name__ == "__main__":
    game = Game()
    for origin, target in (("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")):
        game.move(origin, target)
    print(*game.board.rows(), sep="\n")
    print(game.status.value, game.winner, " ".join(m.notation() for m in game.history))
