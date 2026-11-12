---
slug: n-queens-ii
---
## Q
**LC 52 N 皇后 II**｜Hard

在 `n × n` 棋盘上放 `n` 个互不攻击（同行、同列、同斜线）的皇后，返回方案数。

## A
**一句话。** 一行放一个皇后，逐列尝试，用集合记列和两条斜线的占用，放满回溯计数。

```python
def total_n_queens(n):
    cols, d1, d2 = set(), set(), set()  # 列、row-col、row+col

    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if (col in cols or row-col in d1
                    or row+col in d2):
                continue
            cols.add(col); d1.add(row-col); d2.add(row+col)
            count += place(row + 1)
            cols.remove(col); d1.remove(row-col)    # 回溯
            d2.remove(row+col)
        return count

    return place(0)
```

**复杂度。** 时间 `O(n!)`（剪枝后远小于），空间 `O(n)`。

**易错点。**
- 只记列和一个方向的斜线：`n=4` 返回 `7`，应为 `2`。
- 放下后不撤销：`n=4` 返回 `0`，上一分支的占用留着。
- 用定长数组标斜线时 `row-col` 为负：Python 负下标静默绕回，两条斜线混为一条；用集合或加 `n-1` 偏移。

**追问。**
- 怎么更快？：位运算，三个整数掩码表示列和两条斜线，`x & -x` 取最低可放位。
- 要输出所有棋盘（LC 51）？：同一回溯，多记一个 `queens[row] = col`，到底层按列号拼字符串。

**同模式。** LC 51 N 皇后、LC 37 解数独、LC 46 全排列、LC 79 单词搜索
