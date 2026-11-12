---
slug: valid-sudoku
---
## Q
**LC 36 有效的数独**｜Medium

判断 `9 x 9` 数独是否有效：只验证已填数字，`1-9` 在每行、每列、每个 `3 x 3` 宫内至多出现一次，空格用 `'.'`。

## A
**一句话。** 扫一遍，用 9 个行集合、9 个列集合、9 个宫集合记录已出现的数字，重复就返回 `false`，宫编号是 `r // 3 * 3 + c // 3`。

```python
def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == ".":
                continue
            b = r // 3 * 3 + c // 3     # 宫编号 0..8
            if ch in rows[r] or ch in cols[c] \
                    or ch in boxes[b]:
                return False
            rows[r].add(ch)
            cols[c].add(ch)
            boxes[b].add(ch)
    return True
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`（固定 81 格）。

**易错点。**
- 宫编号写成 `r // 3 + c // 3`：`(0, 3)` 和 `(3, 0)` 都是 `1`，不同宫撞号。
- 只检查行和列：`(0,0)` 与 `(2,2)` 都是 `5` 同宫冲突，行列却不冲突。
- 把 `'.'` 也加入集合：第二个 `'.'` 被判成重复。

**追问。**
- 求解数独（LC 37）？：回溯加这三类集合判可行，优先填候选最少的格子。
- 推广到 `n x n`？：宫边长 `k = √n`，宫编号 `r // k * k + c // k`。

**同模式。** LC 37 解数独、LC 51 N 皇后、LC 217 存在重复元素、LC 73 矩阵置零
