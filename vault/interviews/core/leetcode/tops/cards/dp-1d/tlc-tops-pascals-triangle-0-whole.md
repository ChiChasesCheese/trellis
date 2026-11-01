---
id: tlc-tops-pascals-triangle-0-whole
node: dp-1d.pascals-triangle
type: qa
---
## Q
**LC 118 杨辉三角（Pascal's Triangle）**｜Easy · 全公司热度第 111 名 · Hot 100

给定一个非负整数 `numRows`，生成「杨辉三角」的前 `numRows` 行。在「杨辉三角」中，每个数是它左上方和右上方的数的和。`1 <= numRows <= 30`。例：`numRows = 5` → `[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]`；`numRows = 1` → `[[1]]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 一维 DP：每一行由上一行递推得到。

**一句话。** 第 `i` 行的中间每个数等于上一行相邻两数之和，两端永远是 `1`，从 `[1]` 开始逐行生成。

**识别。** 「每个数由上一行的两个数推出」是递推（DP）：当前行只依赖上一行，状态就是一整行。`numRows <= 30`，直接生成。

**推导。** 用组合数 `C(i, j)` 也能逐项算，但会反复算阶乘；递推关系 `C(i, j) = C(i-1, j-1) + C(i-1, j)` 就是题目描述的「左上加右上」。上一行相邻两数之和用 `pairwise` 一次得到，再在两端补 `1`。

```python
from itertools import pairwise


def generate(num_rows: int) -> list[list[int]]:
    rows = [[1]]
    for _ in range(num_rows - 1):
        prev = rows[-1]
        # 每个数 = 左上 + 右上：中间项是上一行相邻两项之和，两端永远是 1
        rows.append([1] + [a + b for a, b in pairwise(prev)] + [1])
    return rows
```

运行：`5` → `[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]`，`1` → `[[1]]`，`2` → `[[1], [1, 1]]`。

**复杂度。** 时间 `O(numRows²)`（输出本身的大小），空间 `O(numRows²)`。

**拓展优化。**
- 只要第 `k` 行（LC 119）：不必存整个三角，用组合数相邻项的比值 `C(k, j+1) = C(k, j) * (k - j) / (j + 1)` 在 `O(k)` 时间、`O(1)` 额外空间内递推一行。

```python
def get_row(row_index: int) -> list[int]:
    row = [1]
    for j in range(row_index):
        row.append(row[-1] * (row_index - j) // (j + 1))    # C(k, j+1) = C(k, j) * (k - j) / (j + 1)，乘完一定整除
    return row
```

例：`get_row(3)` → `[1, 3, 3, 1]`，`get_row(0)` → `[1]`。

**易错点。**
- 两端漏掉 `1`：只返回 `[a + b for ...]`，第 2 行变成空列表 `[]`，正确 `[1, 1]`。
- 用 `[[1]] * numRows` 初始化：所有行是同一个列表对象，改一行三行一起变（`rows = [[1]] * 3`，`rows[0].append(9)` 后得到 `[[1, 9], [1, 9], [1, 9]]`）。
- 循环次数写成 `num_rows`：多生成一行；`numRows = 1` 时初始就有 `[1]`，要再生成 `num_rows - 1` 行。

**同模式。** LC 119 杨辉三角 II、LC 70 爬楼梯、LC 62 不同路径、LC 120 三角形最小路径和。
