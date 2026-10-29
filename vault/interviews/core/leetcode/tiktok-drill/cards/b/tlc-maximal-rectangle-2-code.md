---
id: tlc-maximal-rectangle-2-code
node: b.maximal-rectangle
type: qa
step: 2
---
## Q
**LC 85 最大矩形**｜写出 Python 实现

`rows x cols` 的字符矩阵 `matrix`（`1 <= rows, cols <= 200`，元素为 `'0'` 或 `'1'`），返回只包含 `'1'` 的最大矩形的面积。要求时间 `O(rows * cols)`。

## A
**思路。** 逐行维护 `heights`：当前行为 `'1'` 的列高度加一，为 `'0'` 的列清零。每更新一行就在 `heights` 上求「直方图最大矩形」：下标栈保持对应柱高递增，遇到更矮（或相等）的柱子就弹栈结算面积，弹出柱子的宽度由新的栈顶（左边界）和当前下标（右边界）决定。末尾补一根高 `0` 的柱子把栈清空。

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    def largest_in_histogram(heights: list[int]) -> int:
        padded = [*heights, 0]                  # 末尾补一根高 0 的柱子，把栈里剩下的全部弹出
        stack: list[int] = []                   # 下标栈：对应柱高严格递增（相等时先弹旧的）
        best = 0
        for i, h in enumerate(padded):
            while stack and padded[stack[-1]] >= h:
                height = padded[stack.pop()]
                left = stack[-1] if stack else -1       # 左边第一根更矮的柱子
                best = max(best, height * (i - left - 1))
            stack.append(i)
        return best

    heights = [0] * len(matrix[0])              # heights[j]：以当前行为底，第 j 列向上连续 1 的个数
    best = 0
    for row in matrix:
        heights = [h + 1 if cell == "1" else 0 for h, cell in zip(heights, row)]    # 1 则加高，0 则清零
        best = max(best, largest_in_histogram(heights))
    return best
```

**运行。** 题面示例 → `6`；`[["0"]]` → `0`；`[["1"]]` → `1`；`[["1","1"],["1","1"]]` → `4`；`[["1","0"],["0","1"]]` → `1`；`200 x 200` 全 `"1"` → `40000`。

**复杂度。** 时间 `O(rows * cols)`：每行 `O(cols)` 更新高度，栈里每根柱子至多进出一次；空间 `O(cols)`。

**写法要点。** `[h + 1 if cell == "1" else 0 for h, cell in zip(heights, row)]` 用 `zip` 同步遍历旧高度和新一行，一次生成新列表，不用下标；`padded = [*heights, 0]` 用解包补哨兵，不改动原列表；`stack[-1] if stack else -1` 处理栈空（左边界在最左侧之外）；弹栈条件用 `>=`：相等高度先弹旧的，最左边的那根拿到完整宽度，结果仍然正确。
