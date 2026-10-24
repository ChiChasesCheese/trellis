---
id: tlc-n-queens-5-alt
node: a.n-queens
type: qa
step: 5
---
## Q
**LC 51 N 皇后**｜另一种解法

用位运算代替三个集合来写 N 皇后，怎么表示冲突、怎么逐行推进？什么时候选它？

## A
**思路。** 用 `n` 位整数表示一行：第 `c` 位为 `1` 代表第 `c` 列。`col_mask` 记录被占用的列，`diag`、`anti` 记录当前行被两个方向的斜线攻击的列：放下一个皇后（位 `bit`）后，进入下一行时主对角线的影响向左移一位，副对角线的影响向右移一位。`free = full & ~(col_mask | diag | anti)` 就是这一行能放的列；循环取最低位 `bit = free & -free` 逐个尝试。

```python
def solve_n_queens(n: int) -> list[list[str]]:
    full = (1 << n) - 1
    result: list[list[str]] = []
    cols: list[int] = []

    def place(col_mask: int, diag: int, anti: int) -> None:
        if col_mask == full:
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            return
        free = full & ~(col_mask | diag | anti)    # 当前行还能放的列（1 = 可放）
        while free:
            bit = free & -free                     # 取最低位的 1
            free ^= bit
            cols.append(bit.bit_length() - 1)
            # 下一行：对角线攻击范围整体左移 / 右移一格
            place(col_mask | bit, ((diag | bit) << 1) & full, (anti | bit) >> 1)
            cols.pop()

    place(0, 0, 0)
    return result
```

运行：`n = 4` → `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`；`n = 1` → `[["Q"]]`；`n = 1` 到 `9` 的解数 `[1, 0, 0, 2, 10, 4, 40, 92, 352]`，与集合版的结果完全一致（顺序也相同）。

**复杂度。** 与集合版同阶，时间上界 `O(n!)`，空间 `O(n)`；常数更小，因为每一行可放的列用一次位运算算出，不必逐列做三次集合查找。

**怎么选。** 默认写集合版：三个集合各对应一个冲突来源，白板上最容易讲清楚、最不容易写错。当面试官追问"能更快吗"或者题目改成只数个数、`n` 更大（LC 52）时，换成位运算版。它的缺点是可读性差，`diag` 和 `anti` 的移位方向容易写反，写反的后果是解数不对，所以一定要用 `n = 4` 的两个解和 `n = 8` 的 `92` 校验。
