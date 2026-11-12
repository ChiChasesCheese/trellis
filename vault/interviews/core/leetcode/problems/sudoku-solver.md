---
slug: sudoku-solver
---
## Q
**LC 37 解数独**｜Hard

原地填充 `9x9` 数独 `board`（空格为 `'.'`），使每行、每列、每个 `3x3` 宫内 `1-9` 各出现一次。保证有唯一解。

## A
**一句话。** 回溯：对每个空格试行、列、宫都没用过的数字，递归下一格，走不通就撤销。

```python
def solve_sudoku(board):
    row, col, box = [0] * 9, [0] * 9, [0] * 9   # 位掩码
    empty = []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empty.append((r, c))
            else:
                b = 1 << int(board[r][c])
                row[r] |= b
                col[c] |= b
                box[r // 3 * 3 + c // 3] |= b

    def dfs(i):
        if i == len(empty):
            return True
        r, c = empty[i]
        k = r // 3 * 3 + c // 3
        for d in range(1, 10):
            b = 1 << d
            if (row[r] | col[c] | box[k]) & b:
                continue
            board[r][c] = str(d)
            row[r] ^= b; col[c] ^= b; box[k] ^= b
            if dfs(i + 1):
                return True
            row[r] ^= b; col[c] ^= b; box[k] ^= b   # 撤销
        board[r][c] = "."
        return False

    dfs(0)
```

**复杂度。** 时间 `O(9^k)`（`k` 为空格数，剪枝后远小于此），空间 `O(k)`。

**易错点。**
- 宫编号写成 `r // 3 + c // 3`：`(0,3)` 和 `(3,0)` 共用编号，合法数字被误判冲突，求不出解。
- 递归成功后不 `return True` 向上传：已填好的格子又被撤销。
- 回溯时只撤销棋盘、不撤销三个掩码：残留标记让合法数字被误判。

**追问。**
- 怎么再加速？：每次先选候选数字最少的空格（MRV），或用掩码的 `bit_count` 直接选最少者。
- 只想判断是否有效（LC 36）？：不用回溯，一遍扫描用三组集合查重。

**同模式。** LC 36 有效的数独、LC 51 N 皇后、LC 52 N 皇后 II、LC 79 单词搜索
