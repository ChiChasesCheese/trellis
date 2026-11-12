---
slug: largest-rectangle-in-histogram
---
## Q
**LC 84 柱状图中最大的矩形**｜Hard

给宽度都为 `1` 的柱子高度 `heights`，求柱状图中能勾勒出的最大矩形面积。

## A
**一句话。** 单调递增栈：遇到更矮的柱子就弹出栈顶并结算面积，末尾补一根高 `0` 的哨兵清栈。

```python
def largest_rectangle_area(heights):
    stack = []                   # 下标，高度严格递增
    best = 0
    for i, h in enumerate([*heights, 0]):   # 0 是哨兵
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]   # 右边界是 i
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 没有哨兵：栈里剩下的柱子没人结算，`[2,4]` 返回 `0`，应为 `4`。
- 宽度写成 `i - left`：漏掉 `- 1`，`[2,4]` 得 `8`，应为 `4`。
- 栈空时 `left` 写成 `0`：应为 `-1`，表示延伸到最左边。

**追问。**
- 01 矩阵里的最大全 1 矩形（LC 85）？：逐行把每列连续 1 的个数当柱高，每行调一次，`O(mn)`。
- 不用栈怎么做？：左右各预处理「最近更矮」数组，再算 `高 × 宽` 取最大。

**同模式。** LC 42 接雨水、LC 85 最大矩形、LC 739 每日温度、LC 907 子数组的最小值之和
