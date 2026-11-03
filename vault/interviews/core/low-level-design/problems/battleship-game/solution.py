"""海战棋（Battleship）：两名玩家、N x N 棋盘、布阵规则、开火、沉船与胜负判定。

核心思路：每个玩家一个 `_Side`，里面三样东西各管一件事：还没摆的舰队（`to_place`）、
"格子 -> 船"的反查表（`at`，开火时 O(1) 找到被打的船）、已被打过的格子（`shots`）。
船自己记录被命中的格子，"沉没"就是命中数等于长度，不另外存一份状态去同步。
流程由一个三态的 `Phase`（摆放中、对战中、结束）驱动：每个公开方法先看阶段，
再校验参数，最后才改状态——校验失败时棋盘不会被改动半截。
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum

Cell = tuple[int, int]


class ShotResult(Enum):
    MISS = "miss"
    HIT = "hit"
    SUNK = "sunk"


class Phase(Enum):
    PLACING = "placing"
    PLAYING = "playing"
    OVER = "over"


class BattleshipError(Exception):
    """所有失败路径的公共基类。"""


class InvalidPlacementError(BattleshipError):
    """摆放违规：越界、重叠、紧贴（第 3 关）、或这个长度已经没有额度。"""


class InvalidShotError(BattleshipError):
    """开火的坐标越界。"""


class AlreadyFiredError(BattleshipError):
    """这个格子已经打过；不消耗回合。"""


class NotYourTurnError(BattleshipError):
    """还没轮到这个玩家。"""


class GameStateError(BattleshipError):
    """阶段不对：摆放没完成就开火、对战开始后还摆船、游戏结束后还开火。"""


@dataclass(frozen=True, slots=True)
class Rules:
    touching_allowed: bool = True    # 第 3 关：False 时船与船（含斜角）不能相邻
    extra_turn_on_hit: bool = False  # 第 3 关：命中后同一玩家继续
    salvo: bool = False              # 第 4 关：每回合连发"存活舰数"枚炮弹


@dataclass(slots=True)
class _Ship:
    cells: frozenset[Cell]
    hits: set[Cell] = field(default_factory=set)

    @property
    def sunk(self) -> bool:
        return len(self.hits) == len(self.cells)


@dataclass(slots=True)
class _Side:
    to_place: list[int]                                     # 还没摆的舰队长度
    ships: list[_Ship] = field(default_factory=list)
    at: dict[Cell, _Ship] = field(default_factory=dict)     # 格子 -> 占着它的船
    shots: dict[Cell, bool] = field(default_factory=dict)   # 被打过的格子 -> 是否命中

    @property
    def alive(self) -> int:
        return sum(not s.sunk for s in self.ships)


class Game:
    def __init__(self, size: int = 10, fleet: Sequence[int] = (5, 4, 3, 3, 2), rules: Rules = Rules()) -> None:
        if size < 1 or not fleet or any(not 1 <= n <= size for n in fleet):
            raise ValueError("bad size or fleet")
        self.size, self.rules = size, rules
        self._sides = [_Side(list(fleet)), _Side(list(fleet))]
        self.phase = Phase.PLACING
        self.current_player: int | None = None
        self.winner: int | None = None

    # ---------------------------------------------------------------- 第 1 关：摆放与开火

    def place_ship(self, player: int, row: int, col: int, length: int, horizontal: bool) -> None:
        side = self._side(player)
        if self.phase is not Phase.PLACING:
            raise GameStateError("placement is over")
        if length not in side.to_place:
            raise InvalidPlacementError(f"no ship of length {length} left to place")
        cells = [(row, col + i) if horizontal else (row + i, col) for i in range(length)]
        if not all(self._inside(c) for c in cells):
            raise InvalidPlacementError("ship leaves the board")
        for r, c in cells:
            if (r, c) in side.at:
                raise InvalidPlacementError("ships overlap")
            if not self.rules.touching_allowed and any(
                    (r + dr, c + dc) in side.at for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                raise InvalidPlacementError("ships may not touch")
        ship = _Ship(frozenset(cells))
        side.ships.append(ship)
        side.at.update({c: ship for c in cells})
        side.to_place.remove(length)
        if not self._sides[0].to_place and not self._sides[1].to_place:
            self.phase, self.current_player = Phase.PLAYING, 0

    def fire(self, player: int, row: int, col: int) -> ShotResult:
        self._check_can_shoot(player)
        if self.rules.salvo:
            raise GameStateError("use fire_salvo in salvo mode")
        target = self._sides[1 - player]
        self._check_shot(target, (row, col))
        result = self._apply(target, (row, col))
        self._after_turn(player, extra=self.rules.extra_turn_on_hit and result is not ShotResult.MISS)
        return result

    def _side(self, player: int) -> _Side:
        if player not in (0, 1):
            raise ValueError(f"player must be 0 or 1, got {player!r}")
        return self._sides[player]

    def _inside(self, cell: Cell) -> bool:
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    def _check_shot(self, target: _Side, cell: Cell, pending: set[Cell] = frozenset()) -> None:
        if not self._inside(cell):
            raise InvalidShotError(f"{cell} is off the board")
        if cell in target.shots or cell in pending:
            raise AlreadyFiredError(f"{cell} was already fired at")

    def _apply(self, target: _Side, cell: Cell) -> ShotResult:
        ship = target.at.get(cell)
        target.shots[cell] = ship is not None
        if ship is None:
            return ShotResult.MISS
        ship.hits.add(cell)
        return ShotResult.SUNK if ship.sunk else ShotResult.HIT

    # ---------------------------------------------------------------- 第 2 关：回合与胜负

    def _check_can_shoot(self, player: int) -> None:
        self._side(player)
        if self.phase is Phase.PLACING:
            raise GameStateError("fleets are not placed yet")
        if self.phase is Phase.OVER:
            raise GameStateError("the game is over")
        if player != self.current_player:
            raise NotYourTurnError(f"it is player {self.current_player}'s turn")

    def _after_turn(self, player: int, extra: bool) -> None:
        if self._sides[1 - player].alive == 0:   # 对手舰队全沉：先判胜负，再谈换人
            self.phase, self.winner, self.current_player = Phase.OVER, player, None
        elif not extra:
            self.current_player = 1 - player

    def remaining_ships(self, player: int) -> int:
        return self._side(player).alive

    # ---------------------------------------------------------------- 第 3 关：视图

    def board_view(self, viewer: int, owner: int) -> list[str]:
        """`owner` 的棋盘，从 `viewer` 的视角看：'.' 未知，'o' 落空，'X' 命中，自己的船 '#'。"""
        self._side(viewer)
        side = self._side(owner)
        rows = []
        for r in range(self.size):
            line = []
            for c in range(self.size):
                if (r, c) in side.shots:
                    line.append("X" if side.shots[(r, c)] else "o")
                else:
                    line.append("#" if viewer == owner and (r, c) in side.at else ".")
            rows.append("".join(line))
        return rows

    # ---------------------------------------------------------------- 第 4 关：齐射

    def fire_salvo(self, player: int, cells: Sequence[Cell]) -> list[ShotResult]:
        self._check_can_shoot(player)
        if not self.rules.salvo:
            raise GameStateError("salvo mode is off")
        if len(cells) != self._sides[player].alive:
            raise InvalidShotError(f"a salvo has exactly {self._sides[player].alive} shots")
        target, seen = self._sides[1 - player], set()
        for cell in cells:                  # 先整体校验，通过了才开始改状态：要么全打、要么一发不打
            self._check_shot(target, cell, seen)
            seen.add(cell)
        results = [self._apply(target, cell) for cell in cells]
        self._after_turn(player, extra=False)
        return results
