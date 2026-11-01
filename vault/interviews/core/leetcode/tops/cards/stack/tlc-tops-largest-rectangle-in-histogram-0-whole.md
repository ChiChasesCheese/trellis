---
id: tlc-tops-largest-rectangle-in-histogram-0-whole
node: stack.largest-rectangle-in-histogram
type: qa
---
## Q
**LC 84 柱状图中最大的矩形**｜Hard · 全公司热度第 75 名 · NeetCode 150、Hot 100

给定 `n` 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 `1`。求在该柱状图中，能够勾勒出来的矩形的最大面积。`1 <= heights.length <= 10^5`，`0 <= heights[i] <= 10^4`。

例：`heights = [2,1,5,6,2,3]` → `10`（高 `5` 宽 `2`）；`heights = [2,4]` → `4`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 单调栈求「每根柱子左右两侧第一个更矮的柱子」；以每根柱子的高度为矩形高度，枚举最大宽度。

**一句话。** 最大矩形的高度一定等于其中某根柱子的高度；对每根柱子，向左右各扩展到第一个更矮的柱子之前，面积 = 高 × 宽；用单调栈一次扫描得到所有的左右边界。

**识别。** 「柱状图 / 最大矩形」「左右第一个更小」是单调栈信号。`n` 到 `10^5`，枚举所有区间 `O(n²)` 超时。

**推导。** 枚举所有 `(l, r)` 区间取最小高度，`O(n²)` 以上。换个角度：最优矩形的高度必是区间内最矮那根的高度，所以只枚举「以第 `i` 根为最矮」的最大区间：左边界是 `i` 左边第一个比它矮的位置，右边界是右边第一个比它矮的位置，宽度 = 右 − 左 − 1。这两个边界正是单调栈擅长的「下一个更小元素」，每根柱子只入栈出栈一次，`O(n)`。

**简单解法。** 同样的思路，先分别用单调栈求出每根柱子的左边界数组和右边界数组，再扫一遍求面积：
```python
def largest_rectangle_area_two_pass(heights: list[int]) -> int:
    n = len(heights)
    left, right = [-1] * n, [n] * n     # 左/右第一个严格更矮的下标，不存在时取 -1 / n
    stack: list[int] = []
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] >= h:
            right[stack.pop()] = i      # i 是被弹出柱子的右边第一个不高于它的位置
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    return max(h * (right[i] - left[i] - 1) for i, h in enumerate(heights))
```

**最优解：** 一遍扫描 + 哨兵，弹出时就地结算。

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []               # 下标，对应高度严格递增：栈内每根柱子的左边界就是它下面那根
    best = 0
    for i, h in enumerate(heights + [0]):           # 末尾哨兵 0：把栈里剩下的柱子全部逼出来结算
        while stack and heights[stack[-1]] >= h:    # i 是栈顶柱子的右边界（第一个不高于它的位置）
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1       # 弹出后栈顶是左边第一个更矮的柱子，栈空则左边都不矮
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

**运行。** `[2,1,5,6,2,3]` → `10`；`[2,4]` → `4`；`[5]` → `5`；`[0]` → `0`；`[2,2,2]` → `6`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 最大全 1 矩形（LC 85）：逐行把每列的连续 1 的个数当作柱子高度，对每行跑一次这个算法。
- 分治法：以区间最矮的柱子分割，`O(n log n)` 平均，最坏 `O(n²)`；线段树取区间最小值可压到 `O(n log n)`。

**易错点。**
- 不加哨兵：`[2,4]` 扫完后栈里还剩两根柱子没有结算，`best` 保持 `0`，正确是 `4`。
- 宽度写成 `i - left`：多算一格，`[2,4]` 得到 `8`（正确是 `4`），应是 `i - left - 1`。
- 栈空时左边界取 `0` 而不是 `-1`：栈空表示左边都不矮，宽度要从第 0 根算起；`[5,3]` 里高度 `3` 的柱子宽度应为 `2`，取 `0` 会少算一格，返回 `3` 而不是 `6`。

**同模式。** LC 85 最大矩形、LC 42 接雨水、LC 739 每日温度、LC 496 下一个更大元素 I。
