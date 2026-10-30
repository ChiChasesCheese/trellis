---
id: tlc-n-queens-4-followup
node: p3.n-queens
type: qa
step: 4
---
## Q
**LC 51 N 皇后**｜追问

面试官接着问：（1）只要解的个数（LC 52）而且 `n` 更大，怎么提速？（2）怎样只找一个解就停？（3）可以怎样利用棋盘的对称性减少一半搜索？

## A
1. **只数个数，用位运算**：用整数的位表示"哪些列、哪些斜线被占"，一次位运算就能算出当前行所有可放的列，不再逐列检查集合。三个掩码：`cols`（列）、`diag`（主对角线影响到本行的位置）、`anti`（副对角线）；进入下一行时 `diag` 左移一位、`anti` 右移一位。

```python
def total_n_queens(n: int) -> int:
    full = (1 << n) - 1

    def place(cols: int, diag: int, anti: int) -> int:
        if cols == full:
            return 1
        free, count = full & ~(cols | diag | anti), 0   # 当前行还能放的列（1 = 可放）
        while free:
            bit = free & -free                          # 取最低位的 1
            free ^= bit
            count += place(cols | bit, ((diag | bit) << 1) & full, (anti | bit) >> 1)
        return count

    return place(0, 0, 0)
```

`n = 1` 到 `10` 依次是 `1, 0, 0, 2, 10, 4, 40, 92, 352, 724`；`n = 12` 得 `14200`（约 0.1 秒），`n = 13` 得 `73712`（不到 1 秒）。
2. **只找一个解**：让 `place` 返回布尔值，递归调用成功就立刻返回 `True`，把整条 `cols` 当结果；不要继续枚举。通常在 `n` 很大（上百）时，用"最少冲突"的启发式搜索而不是回溯。
3. **对称性**：棋盘左右镜像后仍然是合法摆法。只搜第一行放在前一半列（`c < n // 2`）的解，镜像得到另一半；`n` 为奇数时第一行放在正中间的解要单独处理，不能重复计数。

**Python 提醒**：`free & -free` 提取最低位的 `1` 利用补码，在 Python 的任意精度整数上同样成立；递归里不要用可变的全局计数，返回值累加更不容易出错。
