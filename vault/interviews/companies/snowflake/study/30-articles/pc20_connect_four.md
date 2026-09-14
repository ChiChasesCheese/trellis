# pc20 · Connect Four：练的是"判定 → 落子 → 整局状态机"三层递进的小型 OOD

> [!tldr]
> - 这题考的是：四子棋从"判断落子是否四连"到"加重力落子"再到"完整游戏状态机"的三层递进；Part 1 一手预览原题，Part 2/3 具体 API **(reconstructed)**
> - 三步套路：假设子已落下判定四连 → 加重力算落点后复用判定 → 用一个类封装回合/赢家/平局，非法操作不改变状态
> - 最值得带走的一个模式：**小型 OOD 设计把"判定"、"执行动作"、"整局状态机"拆成三层递进，每一层只服务自己的职责，非法操作必须在状态改变前被拒绝**

## 1. 题目在说什么（人话版）

棋盘每格是 `"a"`、`"b"` 或空。Part 1 假设一步棋已经下在 `(x,y)`，判断是否四连；Part 2 加上重力，
子会掉到某一列最下面的空格；Part 3 把整局游戏（轮流下棋、判赢、判平局）封装成一个类。

小例子：
```
can_play_win(board, x, y, "a")            # board[x][y] 已经是 "a"，判断这步是否完成四连
drop_and_check(board, col, "a")           # 子掉到 col 最下面的空格，返回 (行号, 是否四连)
game = ConnectFour(4, 4); game.drop(0)    # 完整游戏：回合切换、赢家、平局
```

## 2. 读题：把文字变成模型

- **实体**：棋盘（二维格子）、方向轴（横竖两斜）、游戏状态（回合、赢家、平局）。
- **输入**：Part 1/2 是棋盘 + 坐标；Part 3 是一串落子的列号。
- **输出**：布尔值 / `(行号, 布尔值)` / 每步落子后的状态快照。
- **状态**：Part 3 需要棋盘、当前回合、赢家、已落子数——这些决定了 `is_draw`/`is_over`。
- **一句话建模**：这是一个 **"从纯函数判定，逐层加上副作用和状态机"** 的 OOD 递进题。

> [!note] 为什么 `can_play_win` 假设子已经落下，而不是自己模拟落子
> 把"落子"和"判定"拆开是两件独立的事——Part 2 才引入重力这个动作，Part 1 只回答"如果这个位置
> 已经有这个子，算不算赢"，职责更单一，也是预览给出的原始签名形状。

## 3. 下笔顺序

1. **问清**：棋盘坐标约定（`board[0]` 是最上面一行还是最下面一行）？平局的定义是"棋盘落满且无
   四连"吗？
2. **Part 1 最小可用**：从落子点沿横、竖、两条斜线四个方向轴，向两边扩展数连续同色格，任意一轴
   `count>=4` 即赢。
3. **Part 2 叠加**：在指定列找最下面的空格落子（原地改棋盘），再对落点复用 Part 1 的判定。
4. **Part 3 叠加**：`ConnectFour` 封装棋盘 + 回合 + 赢家 + 落子计数；`drop()` 复用 Part 2，赢了
   立刻记赢家，回合始终切换（哪怕这步刚好获胜）；游戏结束或非法列时抛错且不改变状态。
5. **收尾**：只有 3 连不算赢；列已满/越界报错；小于 4×4 的棋盘在构造函数直接拒绝；真平局与
   "赢了同时棋盘也满"要分清楚（赢家优先）。

## 4. 代码怎么组织

```
_DIRECTIONS                              # 四个方向轴的两两反方向对
can_play_win(board, x, y, player)        # Part 1：四方向扫描
drop_and_check(board, col, player)       # Part 2：找落点 + 复用 Part 1
class ConnectFour:                       # Part 3：状态机，drop() 复用 Part 2
part1 / part2 / part3(lines)
```
三层依次复用：Part 2 的核心就是"找到落点后调用 Part 1"，Part 3 的核心就是"调用 Part 2 后更新
状态"，没有重复实现判定逻辑。

## 5. 核心代码（骨架）

```python
_DIRECTIONS = (((0,1),(0,-1)), ((1,0),(-1,0)), ((1,1),(-1,-1)), ((1,-1),(-1,1)))

def can_play_win(board, x, y, player):
    for (dx1, dy1), (dx2, dy2) in _DIRECTIONS:
        count = 1
        cx, cy = x + dx1, y + dy1
        while _in_bounds(board, cx, cy) and board[cx][cy] == player:
            count += 1; cx, cy = cx + dx1, cy + dy1
        cx, cy = x + dx2, y + dy2
        while _in_bounds(board, cx, cy) and board[cx][cy] == player:
            count += 1; cx, cy = cx + dx2, cy + dy2
        if count >= 4:
            return True
    return False

def drop_and_check(board, col, player):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == "":
            board[row][col] = player
            return row, can_play_win(board, row, col, player)
    raise ValueError(f"column {col} is full")

class ConnectFour:
    def __init__(self, rows=6, cols=7):
        if rows < 4 or cols < 4:
            raise ValueError("needs at least a 4x4 board")
        self._board = [["" for _ in range(cols)] for _ in range(rows)]
        self._turn, self._winner, self._moves = "a", None, 0

    def drop(self, col):
        if self.is_over():
            raise ValueError("game is already over")
        player = self._turn
        row, won = drop_and_check(self._board, col, player)
        self._moves += 1
        if won: self._winner = player
        self._turn = "b" if player == "a" else "a"   # 始终切换，即使刚获胜
        return row
```

## 6. 面试里怎么说

- 开始前：「我先确认棋盘坐标约定：`board[0]` 是最上面一行，还是最下面一行？」
- 写 Part 1 时：「我沿四个方向轴各自向两边扩展，任意一轴数到 4 就是赢，不需要预先建索引，扫描
  本身已经是 O(1)（每轴最多 3+3 格）。」
- 到 Part 3 时：「每次 `drop()` 我都会切换回合，即使这步刚好获胜——这样 `current_player()` 永远
  表示'下一个理论上该走的人'，判断游戏是否结束应该去问 `winner()`/`is_draw()`，不需要在回合切换
  上做特判。」
- 交付时：「样例过了；非法操作（列满、越界、游戏已结束）我都确认不会改变任何状态。」

## 7. 常见跑偏

- Part 1 里判定逻辑和落子逻辑写在一起，导致 Part 2 加重力时要改 Part 1 的函数签名。
- Part 3 的非法操作（列满、游戏结束后继续下）在检查失败之前就已经改了棋盘或回合，测试用
  "失败调用后状态应不变"就能抓出来。
- 把"平局"判断成"棋盘落满"，忘记赢家优先于平局——某一步刚好在棋盘落满的同时获胜，应该记为赢，
  不是平局。

## 8. 同族题 / 延伸

- 与 `od01`~`od10` 系列同属 OOD 考法，都是"状态封装 + 非法操作不改变状态"的设计，但 pc20 额外
  叠加了一个纯几何判定（四方向扫描）。
- 与 `pc02`（Closest Facility Grid）同样是网格上的方向扫描，但 pc02 考的是并列 tie-break，
  pc20 考的是判定 → 动作 → 状态机的分层。
- 练习命令：`python3 loop/mock.py start pc20`

## 索引行

| [pc20_connect_four](pc20_connect_four.md) | `../../loop/rounds/03_phone_coding/pc20_connect_four/` | 电面 coding | 小型 OOD 设计把"判定"、"执行动作"、"整局状态机"拆成三层递进，每一层只服务自己的职责，非法操作必须在状态改变前被拒绝 |
