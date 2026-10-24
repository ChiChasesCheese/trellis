---
id: tlc-patterns-backtracking-4-nqueens
node: patterns.backtracking
type: qa
step: 4
---
## Q
**回溯（Backtracking）｜N 皇后（LC 51）：用三个集合做 O(1) 冲突检查**

怎样按行放皇后、在 `O(1)` 内判断某一格会不会被攻击？剪枝体现在哪里？

## A
逐行放置（每行恰好一个，行冲突天然避免）。一个格子 `(r, c)` 被攻击当且仅当：列 `c` 已有皇后、主对角线 `r - c` 已有、副对角线 `r + c` 已有。三个集合各自 `O(1)` 查询。

```python
def solve_n_queens(n: int) -> list[list[str]]:
    res: list[list[str]] = []
    queens: list[int] = []                 # queens[r] = 第 r 行皇后所在的列
    cols: set[int] = set()
    d1: set[int] = set()                   # r - c 相同：同一条主对角线
    d2: set[int] = set()                   # r + c 相同：同一条副对角线
    def dfs(r: int) -> None:
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue                   # 剪枝：被攻击的格子根本不进入递归
            cols.add(c); d1.add(r - c); d2.add(r + c); queens.append(c)
            dfs(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c); queens.pop()
    dfs(0)
    return res
print(solve_n_queens(4))   # [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
```

`n = 1..9` 的解的个数是 `1, 0, 0, 2, 10, 4, 40, 92, 352`（LC 52 只要个数）。`n <= 9` 时搜索树被剪枝到很小，Python 很快。

- 不剪枝的暴力是 `n^n`（每行任选一列）；"每行一个"已经降到 `n!`；冲突检查再把大量分支提前砍掉。
- 位掩码版本用三个整数表示列、两条对角线，`lowbit` 枚举可放的列，常数更小，是进阶写法。
- 对称性：第一行只枚举左半，结果乘 2（奇数列再加中间列），可以再快一倍。
- **坑**：对角线的编号 `r - c` 可以为负，用集合不用担心下标；改用数组要加偏移 `r - c + n - 1`。
