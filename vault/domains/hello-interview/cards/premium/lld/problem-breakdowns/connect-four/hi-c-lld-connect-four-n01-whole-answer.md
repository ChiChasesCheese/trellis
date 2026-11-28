---
id: hi-c-lld-connect-four-n01-whole-answer
node: lld.problem-breakdowns.connect-four.notes
type: qa
step: 1
---
## Q
**四子棋 · 完整解答（一张卡）**｜摘要 · 必会

设计双人四子棋（Connect Four）的面向对象方案：7 列 6 行，轮流投子，先连成四子者胜。给出需求、实体与接口、整体设计、关键实现、深入问题和各级别的期望。

## A
**一句话。** 三个类各管一层：`Game` 管回合与结局，`Board` 管网格物理与连线，`Player` 只是数据；状态用枚举，四个方向用向量数据而不是四个类。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–6 分 | 澄清：动作、结局、错误、范围 |
| 6–10 分 | 实体与关系：Game、Board、Player |
| 10–25 分 | 类设计：由需求推状态与方法 |
| 25–45 分 | 实现：`make_move`、`place`、`check_win` |
| 45–50 分 | 走一局验证 |
| 50–60 分 | 追问：悔棋、棋盘大小、机器人 |

**需求。**
- 功能：
  - 7 列 6 行，子落到该列最低空位
  - 横、竖、斜连四子获胜，棋盘满且无人获胜为平局
  - 非法操作（满列、没轮到、结束后再下）被明确拒绝且不破坏状态
- 范围外：界面、并发多局、历史与悔棋、可配置棋盘

**实体与接口。**
- `Game`：持有 `Board`、两名玩家、当前玩家、状态、赢家；`make_move(player, col) -> bool` 是唯一改状态的入口
- `Board`：`place(col, color) -> row`（失败返回 -1）、`is_full()`、`check_win(row, col, color)`
- `Player`：名字与棋色，不含逻辑

**整体设计。**
1. `Game` 先校验：游戏已结束、没轮到该玩家，都直接拒绝
2. 交给 `Board` 落子，网格相关的校验（越界、满列）全在 `Board` 内
3. 只检查刚落下的这一子是否连成四；否则看是否平局；否则换人

**核心实现。** 约 80 行：

```python
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class Color(Enum):
    RED = auto()
    YELLOW = auto()


class State(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    DRAW = auto()


@dataclass(frozen=True)
class Player:                      # 纯数据：名字和棋色，没有游戏逻辑
    name: str
    color: Color


DIRS = ((0, 1), (1, 0), (1, 1), (-1, 1))   # 横、竖、两条斜线：方向是数据，不是类


class Board:
    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        self.rows, self.cols = rows, cols
        self.grid: list[list[Optional[Color]]] = [[None] * cols for _ in range(rows)]

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def place(self, col: int, color: Color) -> int:
        """返回落点行，非法（越界或满列）返回 -1；所有网格校验都在这里"""
        if not 0 <= col < self.cols or self.grid[0][col] is not None:
            return -1
        for r in range(self.rows - 1, -1, -1):          # 行 0 在顶部，从底往上找空位
            if self.grid[r][col] is None:
                self.grid[r][col] = color
                return r
        return -1

    def is_full(self) -> bool:
        return all(self.grid[0][c] is not None for c in range(self.cols))

    def _run(self, r: int, c: int, dr: int, dc: int, color: Color) -> int:
        n = 0
        r, c = r + dr, c + dc
        while self.in_bounds(r, c) and self.grid[r][c] == color:
            n, r, c = n + 1, r + dr, c + dc
        return n

    def check_win(self, r: int, c: int, color: Color) -> bool:
        """只检查刚落下的一子：每个方向向两边数连续同色，加上自身"""
        if not self.in_bounds(r, c) or self.grid[r][c] != color:
            return False
        return any(1 + self._run(r, c, dr, dc, color) + self._run(r, c, -dr, -dc, color) >= 4
                   for dr, dc in DIRS)


class Game:
    def __init__(self, p1: Player, p2: Player) -> None:
        self.board, self.players = Board(), (p1, p2)
        self.current, self.state = p1, State.IN_PROGRESS
        self.winner: Optional[Player] = None

    def make_move(self, player: Player, col: int) -> bool:
        if self.state is not State.IN_PROGRESS or player != self.current:   # 先拒绝，后改状态
            return False
        row = self.board.place(col, player.color)
        if row == -1:
            return False
        if self.board.check_win(row, col, player.color):
            self.state, self.winner = State.WON, player
        elif self.board.is_full():
            self.state = State.DRAW
        else:
            self.current = self.players[1] if player == self.players[0] else self.players[0]
        return True
```

**运行。** 第 0 列底部已有两枚红子：
- 红方下第 0 列落在第 3 行，竖向 3 连，未赢，换黄方
- 红方再下第 0 列落在第 2 行，竖向 4 连，状态变为 `WON`
- 黄方再下任何列都返回 `False`

**深入。**
1. 【必讲】状态：三个布尔值有 8 种组合、只有 3 种合法，用 `State` 枚举让非法状态无法表示；`winner` 仍是可空字段，理想做法是让 `WON` 携带赢家
2. 【必讲】判胜：四个方向算法相同，差别只是 `(dr, dc)`，用方向向量加一个计数函数；四个 `WinChecker` 类是为不会变的需求预留扩展
3. 【必讲】校验放哪：回合与结局归 `Game`，越界与满列归 `Board`；先全部拒绝再改状态
4. 【追问再讲】悔棋：所有走棋经 `make_move`，记录 `Move` 入栈，撤销时清格、还原当前玩家、重置状态
5. 【追问再讲】棋盘大小：行列改成 `Board` 构造参数，其余逻辑已依赖这两个值
6. 【追问再讲】机器人：规则不变，加 `BotEngine.choose_move(game) -> col`，游戏循环里轮到机器人就调它再走 `make_move`；`Player` 保持纯数据
7. 【加分】联网对战加锁；用位棋盘做 O(1) 判胜

**级别期望。**
- 中级：职责分离不靠引导，先校验后变更，方向向量
- 高级：主动解释 `Player` 为什么只是数据、状态为什么是枚举、判胜为什么在 `Board`，并比较多种扩展方案
