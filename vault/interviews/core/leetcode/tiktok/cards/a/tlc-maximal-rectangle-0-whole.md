---
id: tlc-maximal-rectangle-0-whole
node: a.maximal-rectangle
type: qa
---
## Q
**LC 85 最大矩形**｜Hard · CodeTop 国内累计 17 次 · 最近 2026-03-25（CodeTop）

给一个只含 `'0'` 和 `'1'` 的二维矩阵 `matrix`（`rows x cols`），找出只包含 `'1'` 的最大矩形，返回它的面积。`1 <= rows, cols <= 200`，`matrix[i][j]` 是字符 `'0'` 或 `'1'`。例：`[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]` → `6`；`[["0"]]` → `0`；`[["1"]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 逐行把矩阵「压成直方图」：`heights[j]` 是以当前行为底、第 `j` 列向上连续 `1` 的个数；每一行都变成一次 LC 84（柱状图中最大的矩形），用单调栈（monotonic stack）求解，所有行取最大。`O(rows * cols)`。

**识别。** 「0/1 矩阵里全 1 的最大矩形」：任何这样的矩形都有一条底边，底边所在行的上方每一列是一根「连续 1 的柱子」，矩形就是这行直方图里的一个矩形。`rows, cols <= 200` 允许 `O(rows^2 * cols)`（约 `8 * 10^6`），但 `O(rows * cols)` 才是目标。

**推导。** 暴力：枚举两个角，用前缀和检查是否全 1，`O(rows^2 * cols^2)`，约 `1.6 * 10^9`，超时 → 固定底边，向上扩展时维护最小宽度，`O(rows^2 * cols)` → 浪费：每一行的柱子高度是上一行递推出来的，而「直方图里最大矩形」有 `O(cols)` 的单调栈解法 → 逐行更新 `heights`（`1` 加一、`0` 清零），每行跑一次栈，总 `O(rows * cols)`。单调栈里弹出一根柱子时，它左边第一根更矮的柱子和右边第一根更矮的柱子（当前的 `i`）就是它能延伸的边界。

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

运行：题面示例 → `6`，`[["0"]]` → `0`，`[["1"]]` → `1`，`[["1","1"],["1","1"]]` → `4`，`[["1","0"],["0","1"]]` → `1`，`200 x 200` 全是 `"1"` → `40000`。

**复杂度。** 时间 `O(rows * cols)`：每行更新高度 `O(cols)`，栈里每根柱子最多进出一次；空间 `O(cols)`（`heights` 与栈）。

**易错点。**
- 高度遇到 `0` 没有清零：`[["1"],["0"],["1"]]` 得到 `2`（把被 `0` 隔断的两个 `1` 当成连续），正确是 `1`。
- 忘了末尾的哨兵（sentinel）`0` 柱：栈里剩下的柱子没人弹出，`[["1","1"]]` 得到 `1`，正确是 `2`；题面示例得到 `4`，正确是 `6`。
- 用字符串的真值判断 `if cell`：`"0"` 是非空字符串，永远为真，`[["0"]]` 得到 `1`，正确是 `0`；必须写 `cell == "1"`。

**追问。**
- 返回矩形的位置：弹栈算出面积时顺手记下 `(上, 左, 下, 右)`；上 = 当前行 - 高度 + 1，左 = 栈顶 + 1，右 = `i - 1`。
- 只求最大正方形：LC 221，`dp[i][j] = min(上, 左, 左上) + 1`，用完整的二维表。
- 另一种解法：不用栈，用三张表 `height / left / right` 做 DP，见另一种解法。

**同模式。** LC 84 柱状图中最大的矩形、LC 221 最大正方形、LC 1504 统计全 1 子矩形、LC 42 接雨水、LC 739 每日温度（单调栈）。
