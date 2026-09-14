# pc20 · Connect Four — canPlayWin → 加重力 drop → OOD 设计整个游戏

> TrueInterview 87 题清单第 16 题（`canPlayWin`，2026-06）与第 18 题（"Design Connect Four" LLD，
> 2026-05）同族，本 kit 合并成一题的三个 Part。Part 1 是一手预览原题；Part 2、Part 3 的具体 API
> **(reconstructed)**，但"加重力落子"与"设计整个游戏"两个方向是 TrueInterview 预览明确给出的。

## 背景

TrueInterview（`kevin-2023-code/Tech-Interview-Questions`，见 `../../../catalog/raw/github_repos.md`
§2 第 16、18 行、§3）列出两道 Snowflake 题：一道 Algorithm "`canPlayWin(board, x, y, player)`"（board
格子是 `"a"`/`"b"`/`""`，判断落子后是否四连），一道 LLD "Design Connect Four"。二者显然是同一游戏的
不同深度追问，本 kit 按"先判定 → 加重力 → 完整设计"的自然顺序合并为 pc20 的三个 Part。

## 输入 / 约定

棋盘 `board` 是行列表，`board[0]` 是**最上面一行**，`board[-1]` 是**最下面一行**；每个格子是
`"a"`、`"b"` 或 `""`（空）。坐标 `(x, y)` = `(行, 列)`，从 0 开始。

## API 契约（英文签名）

```python
def can_play_win(board: list[list[str]], x: int, y: int, player: str) -> bool
def drop_and_check(board: list[list[str]], col: int, player: str) -> tuple[int, bool]

class ConnectFour:
    def __init__(self, rows: int = 6, cols: int = 7) -> None
    def current_player(self) -> str
    def winner(self) -> str | None
    def is_draw(self) -> bool
    def is_over(self) -> bool
    def drop(self, col: int) -> int
```

## 规则

### Part 1 — `can_play_win`：落子已经发生，判断是否四连（一手原题）

假设 `board[x][y]` **已经**等于 `player`（子已经落下）；从 `(x, y)` 沿四个方向轴（横、竖、两条斜线）
向两边扩展数同色连续格，任意一个方向轴数到 `≥4` 就是赢。`player` 不是 `"a"`/`"b"`、坐标越界、或
`board[x][y] != player` 都是 `ValueError`。

### Part 2 — 加重力：按列落子 **(reconstructed)**

`drop_and_check(board, col, player)`：子会掉到该列**最下面的空格**（重力），原地修改 `board`，
返回 `(落到的行号, 是否四连)`；`col` 越界或该列已满 → `ValueError`。内部直接复用 Part 1 的判定逻辑。

### Part 3 — 完整游戏设计（"Design Connect Four" LLD） **(reconstructed)**

`ConnectFour` 维护一整局游戏：`'a'` 先手，轮流落子；`drop(col)` 每次调用后回合都会切换（哪怕这一步
刚好获胜——获胜后 `current_player()` 表示"理论上下一个该走的人"，游戏已经结束，谁都不能再走）；
出现四连立刻记为赢家，游戏结束；棋盘落满且无人四连是平局；游戏结束后或列号非法/该列已满时
`drop()` 抛 `ValueError`，且失败的调用不改变任何状态。`rows`/`cols` 小于 4 时构造函数直接拒绝
（四子棋的定义就需要至少 4×4）。

## Worked examples（全部由 `solution.py` 实际运行得出）

- 4×4 空棋盘，`col0` 连续落子 4 次（轮流 `a`,`b`,`a`,`b`,`a`,`b`,`a`）：第 4 次落 `col0` 时 `a` 已经
  在第 0、2、4 行都是 `a`（第 1、3、5 步是 `b` 落进别的列），最终第 7 步 `a` 落到第 0 行，`col0` 四行
  全是 `a` → `winner() == "a"`，`current_player()` 切到 `"b"`（下一个理论上该走的人，但游戏已结束）。
- `drop_and_check` 在 2×2 空棋盘的 `col0` 连续落两次不出现四连（棋盘太小放不下四连）。
- `ConnectFour(4, 4)` 用暴力搜索找到的落子序列
  `[0, 2, 1, 3, 3, 0, 2, 3, 1, 2, 1, 2, 0, 1, 3, 0]` 能把 4×4 棋盘落满而不出现任何四连——真平局。

## `main()` 命令流

```
PART 1                                    PART 2                          PART 3
a,a,a,_;_,_,_,_;_,_,_,_;_,_,_,_ | 0 2 a    _,_,_,_;_,_,_,_;_,_,_,_;_,_,_,_ | 2 a    4 4
→ false                                    → 3 false                       0
                                                                            1
                                                                            0
                                                                            1
                                                                            0
                                                                            1
                                                                            0
                                                                            → ...
                                                                              0 b a false
```
棋盘序列化：行用 `;` 分隔，格子用 `,` 分隔，`_` 表示空格子。Part 1/2 每行：`board | ...`；
Part 3 第一行 `ROWS COLS`，之后每行一个要落子的列号，每次落子输出一行
`落到的行号 下一个该走的人 赢家或NONE 是否平局(true/false)`。

## 边界清单

- Part 1：只有 3 连不算赢；坐标越界、`player` 非法、`board[x][y]` 与 `player` 不符都要 `ValueError`
- Part 2：列已满、列越界 → `ValueError`；落在已有子的列上要落到正确的高度（不是最底行）
- Part 3：非法列号（负数、`>= cols`）、列已满、游戏已结束后继续落子，都要 `ValueError` 且不改变状态
- Part 3：棋盘小于 4×4（无法四连）在构造函数直接拒绝
- Part 3：真平局（棋盘落满且没有任何四连）与"某一步获胜后棋盘恰好也满了"要分清楚（赢家优先于平局）

## 追问

1. **为什么 `can_play_win` 假设子已经落下，而不是自己模拟落子？** 把"落子"和"判定"拆开是两件独立的
   事——Part 2 才引入"落子"（重力），Part 1 只回答"如果这个位置已经有这个子，算不算赢"，职责更单一，
   也是这道题在预览里给出的原始签名形状。
2. **为什么每次 `drop()` 都切换回合，即使这一步刚好获胜？** 让 `current_player()` 的含义永远是
   "下一个理论上该走的人"，不需要在"游戏是否已结束"这件事上做特判——查游戏是否结束应该去问
   `winner()` / `is_draw()` / `is_over()`，而不是从 `current_player()` 反推。
3. **能不能把 `can_play_win` 优化成增量维护，不用每次都扫四个方向？** 可以维护每个格子在四个方向轴上
   的"连续计数"表，落子时 O(1) 更新，但对电面规模（棋盘几十到几百）没必要，扫描本身已经是 O(1)
   （每个方向轴最多扫 3+3 格）。

## 来源与置信度

- **MED（聚合站，题面付费，仅预览可见）**：`kevin-2023-code/Tech-Interview-Questions`
  `companies/snowflake.md`，第 16 行 "Four-in-a-row Game canPlayWin"（2026-06 报告）、第 18 行
  "Design Connect Four"（2026-05 报告）。见 `../../../catalog/raw/github_repos.md` §2 第 16、18
  行、§3。`can_play_win` 的签名与格子取值 `"a"`/`"b"`/`""` 为一手预览原文。
- Part 2、Part 3 的具体 API 与状态机为重建，方向（加重力、完整 LLD）由预览的两条 TrueInterview
  条目共同确认。

## 考什么

S01 网格上四个方向轴的扫描 · S07 小型 OOD：把状态（棋盘、回合、赢家、平局）封装进一个类、边界情况
（非法输入不改变状态）· 把"判定"和"落子"和"整局游戏状态机"拆成三层递进的追问。
