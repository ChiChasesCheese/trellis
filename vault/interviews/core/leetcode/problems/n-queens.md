---
slug: n-queens
---
## Q
**LC 51 N 皇后**｜Hard

在 `n x n` 棋盘上放 `n` 个互不攻击（同行、同列、同斜线）的皇后，返回所有摆法。

## A
**一句话。** 回溯一行放一个皇后，用列、主对角线（`r-c`）、副对角线（`r+c`）三个集合判冲突。

```python
def solve_n_queens(n):
    res, cols = [], []           # cols[r]：第 r 行皇后的列
    used_col, diag, anti = set(), set(), set()
    def place(r):
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1)
                        for c in cols])
            return
        for c in range(n):
            if (c in used_col or r - c in diag
                    or r + c in anti):
                continue
            cols.append(c)
            used_col.add(c)
            diag.add(r - c)
            anti.add(r + c)
            place(r + 1)
            anti.remove(r + c)       # 撤销要全
            diag.remove(r - c)
            used_col.remove(c)
            cols.pop()
    place(0)
    return res
```

**复杂度。** 时间 `O(n!)`（冲突剪枝后远小于），空间 `O(n)`。

**易错点。**
- 少查一条对角线：`n=4` 得 7 个解，应为 2 个。
- 回溯没撤销全：任漏一个集合，后面的分支被错误剪枝，解变少。
- 用 `[["."] * n] * n` 建棋盘：所有行共享同一个列表。

**追问。**
- 只要解的个数（LC 52）？：用位运算表示列和两条对角线，`n=12` 也能很快算完。
- 怎么再提速？：利用左右对称只搜第一行前一半，结果翻倍，`n` 为奇数时中间列单独算。

**同模式。** LC 52 N 皇后 II、LC 37 解数独、LC 46 全排列、LC 79 单词搜索
