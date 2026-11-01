---
slug: n-queens-ii
---
## Q
**LC 52 N 皇后 II**｜Hard

n 皇后问题研究的是如何把 `n` 个皇后放在 `n × n` 的棋盘上，使皇后彼此不能相互攻击（同一行、同一列、同一斜线上都不能有两个皇后）。给你整数 `n`，返回 n 皇后问题不同的解决方案的**数量**。`1 <= n <= 9`。例：`n = 4` → `2`；`n = 1` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 回溯（backtracking）：逐行放皇后，用集合记录已占用的列和两个方向的对角线。

**一句话。** 一行放一个皇后，对每一行尝试每一列，只要列、"/"斜线、"\\"斜线都没被占就放下并递归下一行，放满 `n` 行就记一个解。

**识别。** 「放置若干对象且互相约束」「要数方案数 / 列出方案」「`n <= 9`」= 回溯搜索；约束都能用"某个标识是否已被占用"判断，所以每步 `O(1)` 检查。

**推导。** 暴力：在 `n^2` 个格子里选 `n` 个，`C(n^2, n)` 种，`n = 9` 时约 `2.6 * 10^11`。每行恰好一个皇后，所以按行递归，状态只剩"每行选哪一列"，最多 `n^n`，再用约束剪枝，实际搜索量小得多。冲突检查：同列看列号；"\\"斜线上的格子 `row - col` 相同；"/"斜线上的格子 `row + col` 相同。

```python
def total_n_queens(n: int) -> int:
    cols: set[int] = set()   # 已占用的列
    diag1: set[int] = set()  # 已占用的 "\" 斜线：row - col 相同
    diag2: set[int] = set()  # 已占用的 "/" 斜线：row + col 相同

    def place(row: int) -> int:
        """第 0..row-1 行已放好，返回从第 row 行起放完的方案数。"""
        if row == n:  # 每行都放好了：一个合法方案
            return 1
        count = 0
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue  # 被已放的皇后攻击到
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            count += place(row + 1)
            cols.remove(col)  # 回溯：撤销这一步
            diag1.remove(row - col)
            diag2.remove(row + col)
        return count

    return place(0)
```

运行：`n = 1..9` 依次得到 `1, 0, 0, 2, 10, 4, 40, 92, 352`，其中 `n = 4` → `2`、`n = 1` → `1` 与示例一致。

**复杂度。** 时间约 `O(n!)` 量级（带剪枝，实际远小于），空间 `O(n)`（递归深度 `n` 加三个集合）。

**拓展优化。**
- 位运算（bitmask）：用三个整数代替三个集合，`free & -free` 逐个取出可放的列，常数小很多：

```python
def total_n_queens_bits(n: int) -> int:
    full = (1 << n) - 1  # n 位全 1

    def place(cols: int, d1: int, d2: int) -> int:
        """cols：被占用的列；d1、d2：当前行被两个方向斜线封住的列（随行下移而左移 / 右移）。"""
        if cols == full:
            return 1
        count = 0
        free = full & ~(cols | d1 | d2)  # 当前行还能放的列
        while free:
            bit = free & -free  # 取最低位的可放列
            free ^= bit
            count += place(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
        return count

    return place(0, 0, 0)
```

**易错点。**
- 只记列和一个方向的斜线：`n = 4` 返回 `7`，正确是 `2`，另一个方向上的互相攻击没拦住。
- 放下后忘了撤销（没有回溯）：`n = 4` 返回 `0`，因为前一个分支的占用一直留着。
- 改用定长列表做斜线标记时，`row - col` 可能为负，Python 的负下标不报错、静默绕回末尾，两条不同的斜线被混为一条；用集合，或加 `n - 1` 偏移。

**同模式。** LC 51 N 皇后、LC 37 解数独、LC 46 全排列、LC 79 单词搜索。
