---
id: tlc-tops-sudoku-solver-0-whole
node: backtracking.sudoku-solver
type: qa
---
## Q
**LC 37 解数独（Sudoku Solver）**｜Hard · 全公司热度第 289 名

编写程序，通过填充空格来解决数独问题。数独的解法需遵循：数字 `1-9` 在每一行只能出现一次；每一列只能出现一次；每一个以粗实线分隔的 `3x3` 宫内只能出现一次。数独部分空格内已填入数字，空白格用 `'.'` 表示。原地修改 `board`。`board.length == 9`，`board[i].length == 9`，`board[i][j]` 是一位数字或者 `'.'`，题目数据保证输入数独仅有一个解。例：`board` 第一行 `"53..7...."`，其余行 `"6..195..."`、`".98....6."`、`"8...6...3"`、`"4..8.3..1"`、`"7...2...6"`、`".6....28."`、`"...419..5"`、`"....8..79"` → 填完后第一行 `"534678912"`，最后一行 `"345286179"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 回溯（backtracking）：逐个空格尝试 `1..9`，用行/列/宫位掩码（bitmask）O(1) 判断冲突。

**一句话。** 先收集所有空格并记下行、列、宫已用数字；依次对每个空格尝试没被占用的数字，递归下一个空格，走不通就撤销换下一个数字。

**识别。** 「在约束下填满所有格子，保证有解」是回溯（和 N 皇后同一类）。数独只有 9×9，状态空间虽大但约束很强，剪枝后很快；每填一个数只需要检查它所在的行、列、宫。

**推导。** 暴力：每个空格试 9 个数，最后再检查合法性，`9^k` 次。改进：每次试数前就检查冲突，不合法的分支立即放弃；冲突检查用位掩码，`used = rows[r] | cols[c] | boxes[b]`，第 `d` 位为 1 表示已用，判断是 `O(1)`。递归深度等于空格数（至多 81）。

```python
def solve_sudoku(board: list[list[str]]) -> None:
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9     # 位掩码：第 d 位为 1 表示该行/列/宫已经有数字 d
    empties: list[tuple[int, int]] = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empties.append((r, c))
            else:
                bit = 1 << int(board[r][c])
                rows[r] |= bit
                cols[c] |= bit
                boxes[r // 3 * 3 + c // 3] |= bit

    def dfs(idx: int) -> bool:                    # 填第 idx 个空格；全部填完返回 True
        if idx == len(empties):
            return True
        r, c = empties[idx]
        b = r // 3 * 3 + c // 3
        used = rows[r] | cols[c] | boxes[b]
        for d in range(1, 10):
            bit = 1 << d
            if used & bit:                        # 行、列、宫里已有 d：跳过
                continue
            board[r][c] = str(d)
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if dfs(idx + 1):
                return True
            rows[r] ^= bit                        # 回溯：撤销这一步
            cols[c] ^= bit
            boxes[b] ^= bit
        board[r][c] = "."
        return False

    dfs(0)
```

运行：示例盘面填完后每行依次为 `534678912`、`672195348`、`198342567`、`859761423`、`426853791`、`713924856`、`961537284`、`287419635`、`345286179`。

**复杂度。** 最坏 `O(9^k)`（`k` 是空格数），剪枝使实际远小于此；空间 `O(k)`，递归深度 `k <= 81`，不会触发递归限制。

**拓展优化。**
- 最少候选优先（MRV, minimum remaining values）：每次不按固定顺序，而是挑「候选数字最少」的空格先填，分支最少、死路暴露得最早。对极难的盘面能把秒级降到毫秒级。

```python
def solve_sudoku_mrv(board: list[list[str]]) -> None:
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    empties: set[tuple[int, int]] = set()
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empties.add((r, c))
            else:
                bit = 1 << int(board[r][c])
                rows[r] |= bit
                cols[c] |= bit
                boxes[r // 3 * 3 + c // 3] |= bit

    def candidates(r: int, c: int) -> int:        # 能填的数字掩码（第 1..9 位）
        return ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & 0b1111111110

    def dfs() -> bool:
        if not empties:
            return True
        r, c = min(empties, key=lambda p: candidates(*p).bit_count())   # 候选最少的格子先填：分支最少，死路暴露得最早
        b = r // 3 * 3 + c // 3
        empties.remove((r, c))
        mask = candidates(r, c)
        for d in range(1, 10):
            bit = 1 << d
            if not mask & bit:
                continue
            board[r][c] = str(d)
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            if dfs():
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
        board[r][c] = "."
        empties.add((r, c))
        return False

    dfs()
```

**易错点。**
- 宫编号写成 `r // 3 + c // 3`：不同的宫会共用编号（`(0, 3)` 和 `(3, 0)` 都得 `1`），合法数字被误判冲突，求解失败，示例盘面保持 `53..7....` 未被填完；正确是 `r // 3 * 3 + c // 3`。
- 递归成功后没有 `return True` 向上传递，继续试下一个数字：已经填好的格子又被撤销，盘面回到未解状态。
- 回溯时只撤销棋盘、没有撤销三个掩码：后续分支看到残留的占用标记，把合法数字误判为冲突，求不出解。

**同模式。** LC 36 有效的数独、LC 51 N 皇后、LC 52 N 皇后 II、LC 79 单词搜索。
