# pc29 · Valid Tic-Tac-Toe (Extended)：两两相交不等于存在公共交点

> [!tldr]
> - 这题考的是：LC 794 推广到 N×N/K 连的"可达性"判定——把游戏规则翻译成局面的代数约束（落子数
>   关系、赢了就停、双方不能都赢、同一人多条连线的真正条件）
> - 三步套路：先查落子数关系（`#X - #O ∈ {0,1}`）→ 查双方不能都赢、赢家的落子数必须精确匹配 →
>   查"同一人的全部连线是否有一个共同交点"（不是两两检查）
> - 最值得带走的一个模式：**"所有 N 个对象两两满足某关系"不等价于"存在一个点同时满足全部对
>   象"——N≥3 时，三条线可以两两相交却没有共同交点，必须直接对全体求交集，两两检查是一个看似
>   合理、实则不完整的充分条件**

## 1. 题目在说什么（人话版）

`N×N` 棋盘，`K` 连子获胜（行/列/两条对角线方向），X 先手、交替落子、一旦有人获胜游戏立刻停
止；给一个局面，判断它是否**可达**（是否存在一个合法的落子顺序能产生这个局面）。`N=3, K=3` 就
是 LC 794 原题。

三行小例子：
```
["XXX","   ","OOO"] -> False     (X、O 都赢了，游戏应该在先赢的那一刻就停止)
["XXX","XOO","XOO"] -> True      (行0与列0共享格子(0,0)，最后一步落这里同时补齐两条线)
["XO  ","OXOO"," XXX","OX  "]（4x4,K=3）-> False（X 的三条连线两两相交，但没有共同交点）
```

## 2. 读题：把文字变成模型

- **实体**：棋盘格子、X/O 各自的全部 K 连线（每条线是一个格子集合）。
- **输入长什么样**：`board: list[str]`，字符 `'X'/'O'/' '`；Part 2/3 额外给 `n`、`k`。
- **输出要什么**：`bool`（Part 1/2）或原因码字符串（Part 3：`OK`/`COUNT`/`BOTH_WIN`/
  `X_WIN_BAD_COUNT`/`O_WIN_BAD_COUNT`/`DOUBLE_WIN_IMPOSSIBLE`）。
- **状态**：每个人当前拥有的全部 K 连线（`list[frozenset[(r,c)]]`），不需要维护对局历史。
- **一句话建模**：可达性判断本质是**把"落子交替 + 赢了就停"这条游戏规则翻译成局面本身的代数约
  束**，不需要真的搜索落子顺序。

> [!note] 为什么"多条连线"要求交集而不是两两相交
> 一个人能同时拥有多条 K 连线，当且仅当**最后一步棋恰好落在这些连线的共同格子上**——之前每条
> 线都因为缺这一个格子而没完成，最后一步一次性补齐全部。当只有两条线时，"两两相交"和"存在公共
> 交点"是同一件事；但三条或更多线时，**每两条线各自有一个交点，不代表三条线有同一个交点**——
> 想象一个人同时占了一行、一列、一条对角线：行×列在一点相交，行×对角线在另一点相交，列×对角
> 线又在第三点相交，两两都相交，却没有一个格子同时在三条线上。这种局面不可达：不管把哪个交点
> 当作"最后一步"，另一条不经过它的线早就已经独立完成，游戏会在那一刻结束。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **扫描四个方向**：写 `_winning_lines(board, n, k, mark)`，收集某个 mark 的全部 K 连线（行、
   列、主对角线方向、副对角线方向），每条线表示成格子的 `frozenset`。
2. **落子数关系**：`#X - #O` 必须是 `0` 或 `1`，否则直接不可达。
3. **双方不能都赢**：先查这个，再分别处理各自的获胜情形。
4. **赢家的落子数精确关系**：X 赢要求 `#X - #O == 1`，O 赢要求 `#X == #O`。
5. **多条连线的公共交点**：对赢家的全部连线求交集（不是两两检查），非空才可达。
6. **收尾**：Part 3 把上面每一步失败的地方换成对应原因码；用暴力枚举 3×3 全部 19683 种局面做
   零差异交叉验证。

## 4. 代码怎么组织

```
_winning_lines(board, n, k, mark) -> list[frozenset]     # 四个方向扫描，收集全部 K 连线
_all_lines_share_a_common_cell(lines) -> bool             # 全体求交集，不是两两检查
_reachable_reason(board, n, k) -> str                      # 落子数 -> 双赢 -> 精确关系 -> 交集
valid_tic_tac_toe / valid_tic_tac_toe_nk / valid_tic_tac_toe_reason   # 薄包装，共用 _reachable_reason
```
三个对外函数都只是 `_reachable_reason` 的薄包装（前两个只看是否等于 `"OK"`），这样"可达性判定"
这条主线逻辑只写一次，Part 1/2/3 之间不会因为各自维护一份判断逻辑而产生不一致。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def _all_lines_share_a_common_cell(lines):
    # True 当且仅当存在一个格子同时属于全部连线——不是"每两条线两两相交"
    common = set(lines[0])
    for line in lines[1:]:
        common &= line
        if not common:
            return False
    return bool(common)

def _reachable_reason(board, n, k):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    if not (o_count == x_count or o_count == x_count - 1):
        return "COUNT"

    x_lines = _winning_lines(board, n, k, "X")
    o_lines = _winning_lines(board, n, k, "O")
    if x_lines and o_lines:
        return "BOTH_WIN"                       # 先赢的那一刻游戏就结束了，不可能两人都赢
    if x_lines:
        if x_count - o_count != 1:
            return "X_WIN_BAD_COUNT"
        if len(x_lines) >= 2 and not _all_lines_share_a_common_cell(x_lines):
            return "DOUBLE_WIN_IMPOSSIBLE"       # 关键：求交集，不是两两检查
    if o_lines:
        if x_count != o_count:
            return "O_WIN_BAD_COUNT"
        if len(o_lines) >= 2 and not _all_lines_share_a_common_cell(o_lines):
            return "DOUBLE_WIN_IMPOSSIBLE"
    return "OK"
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「只考虑标准的行/列/对角线方向连续 K 个，不考虑折线，这是 LC 794 类题目的通用约
  定，我先确认一下。」
- 写双赢检查时：「一个人如果有两条以上连线，我不做'每两条线两两相交'的检查，而是对全部连线求
  交集——两两相交是必要不充分条件，三条线可以两两相交却没有共同格子，我会用一个具体例子验证这
  一点。」
- 交付时：「样例过了；我用暴力枚举 3×3 全部 19683 种局面和这份实现比对，结果完全一致，4×4 用
  随机采样做了同样的交叉验证。」

## 7. 常见跑偏（方法层面，3 条）

- 只检查"任意两条连线是否共享一个格子"就判定"双赢"可达——这是很多 LC 794 题解也会犯的错误，
  在 3×3 棋盘上很难构造出反例，一旦推广到更大的 N 就会出问题（例 6 就是在 4×4 上找到的反例）。
- 忘记"双方都赢是不可能的"这条检查，或者忘记赢家自己的落子数关系必须精确匹配（不是"合理"就
  行，X 赢必须恰好 `#X - #O == 1`）。
- 对角线/副对角线的扫描起点范围写错（比如没有正确限制 `r`、`c` 的范围到 `n-k+1`/`k-1`），导致
  漏掉或多算某些 K 连线。

## 8. 同族题 / 延伸

- 是 LC 794 原题的直接推广；本 kit 在实现阶段用暴力枚举把"两两相交不等于公共交点"这个 bug 亲
  手抓出来过一次，这个方法论——**对"看似正确的充分条件"保持怀疑、用暴力枚举验证边界情形**——
  与 `pc21_accumulator_interpreter` 里"先想当然写对再被自己的测试推翻"是同一种工程习惯。
- 与 `pc06_happy_number`（判环）不同族在具体算法，但同族在"棋盘/局面类问题需要把规则翻译成代
  数约束"这条技能线。
- 练习命令：`python3 loop/mock.py start pc29`
