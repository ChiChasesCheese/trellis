"""海战棋（Battleship）——起始模板。公开的类名、签名、枚举和异常与 `solution.py` 一致。"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

Cell = tuple[int, int]  # (row, col)，从 0 开始


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
    """开火的坐标越界（第 4 关：齐射发数不对也用它）。"""


class AlreadyFiredError(BattleshipError):
    """这个格子已经打过；不消耗回合。"""


class NotYourTurnError(BattleshipError):
    """还没轮到这个玩家。"""


class GameStateError(BattleshipError):
    """阶段不对：摆放没完成就开火、对战开始后还摆船、游戏结束后还开火。"""


@dataclass(frozen=True)
class Rules:
    touching_allowed: bool = True
    extra_turn_on_hit: bool = False
    salvo: bool = False


class Game:
    phase: Phase                  # 第 2 关
    current_player: int | None    # 第 2 关：对战中是 0 或 1，其余阶段是 None；玩家 0 先手
    winner: int | None            # 第 2 关

    def __init__(self, size: int = 10, fleet: Sequence[int] = (5, 4, 3, 3, 2), rules: Rules = Rules()) -> None:
        """size 或 fleet 不合理（size < 1、fleet 为空、某艘长度不在 1..size）抛 ValueError。两名玩家的舰队相同。"""
        raise NotImplementedError

    def place_ship(self, player: int, row: int, col: int, length: int, horizontal: bool) -> None:
        """摆一艘船：(row, col) 是船头，横放向右延伸，竖放向下延伸。

        - player 不是 0 或 1 抛 ValueError；摆放阶段已结束抛 GameStateError。
        - 越界、与自己的船重叠、该长度已经没有额度，抛 InvalidPlacementError。
        - 第 3 关：touching_allowed 为 False 时，与自己已有的船（含斜角相邻）相邻也抛 InvalidPlacementError。
        - 两名玩家都摆完整支舰队后自动进入 PLAYING，玩家 0 先手。
        """
        raise NotImplementedError

    def fire(self, player: int, row: int, col: int) -> ShotResult:
        """玩家向对手的 (row, col) 开火，返回 MISS / HIT / SUNK（这一炮刚好打沉一艘船）。

        - 摆放没完成或游戏已结束抛 GameStateError；越界抛 InvalidShotError；
          同一格子重复打抛 AlreadyFiredError（不消耗回合）。
        - 第 2 关：没轮到该玩家抛 NotYourTurnError；打沉对手最后一艘船则游戏结束；否则换人。
        - 第 3 关：extra_turn_on_hit 为 True 时，命中（HIT 或 SUNK）后仍是该玩家。
        - 第 4 关：salvo 模式下调用 fire 抛 GameStateError。
        """
        raise NotImplementedError

    def remaining_ships(self, player: int) -> int:
        """第 2 关：该玩家还没被打沉的船数。"""
        raise NotImplementedError

    def board_view(self, viewer: int, owner: int) -> list[str]:
        """第 3 关：owner 的棋盘从 viewer 视角看，size 行、每行 size 个字符，返回新列表。

        '.' 未知，'o' 已打过且落空，'X' 已被命中；viewer == owner 时，还没被打到的船格显示 '#'。
        绝不能泄露对手没被打到的船位置。
        """
        raise NotImplementedError

    def fire_salvo(self, player: int, cells: Sequence[Cell]) -> list[ShotResult]:
        """第 4 关：齐射。仅 salvo 模式可用，否则抛 GameStateError。

        cells 的个数必须恰好等于该玩家当前存活的船数，否则抛 InvalidShotError；每个坐标都要合法、
        彼此不同且没打过（越界 InvalidShotError，重复 AlreadyFiredError）。校验在先：任何一发非法，
        整个齐射不生效。返回逐发结果；齐射后一律换人（忽略 extra_turn_on_hit）。
        """
        raise NotImplementedError
