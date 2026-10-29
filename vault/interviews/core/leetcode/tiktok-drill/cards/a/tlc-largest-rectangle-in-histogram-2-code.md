---
id: tlc-largest-rectangle-in-histogram-2-code
node: a.largest-rectangle-in-histogram
type: qa
step: 2
---
## Q
**LC 84 柱状图中最大的矩形**｜写出 Python 实现

`heights` 有至多 `10^5` 根宽为 `1` 的柱子（高度 `0` 到 `10^4`），返回柱状图中最大矩形的面积，要求 `O(n)`。

## A
**思路。** 栈里存下标，高度严格递增。读到高度 `h` 时，把所有不低于 `h` 的栈顶依次弹出：被弹出的柱子，右边界是当前下标 `i`，左边界是弹出后的新栈顶，当场算面积。末尾补一根高 `0` 的柱子，让栈里所有柱子都被结算。

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []                      # 下标，对应高度严格递增
    best = 0
    for i, h in enumerate([*heights, 0]):      # 末尾补一根高 0 的柱子，把栈清空
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]      # 这根柱子在 i 处找到了右边界
            left = stack[-1] if stack else -1  # 左边第一根更矮的柱子
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

运行：`[2,1,5,6,2,3]` → `10`，`[2,4]` → `4`，`[0]` → `0`，`[5]` → `5`，`[2,2,2]` → `6`，`[6,5,4,3,2,1]` → `12`，`10^5` 根同高 `10^4` → `1000000000`。

**复杂度。** 时间 `O(n)`：每个下标入栈、出栈各一次；空间 `O(n)`：单调递增时栈会装满。

**写法要点。** `[*heights, 0]` 用解包造出补了哨兵的新列表，不改入参；`enumerate` 同时给下标和高度，而 `heights[stack[-1]]` 仍用原数组（哨兵下标 `n` 永远不会进栈再被读取）；`stack[-1] if stack else -1` 把栈空情形统一成 `left = -1`，宽度公式 `i - left - 1` 不必分情况；比较用 `>=` 让等高柱子也被弹出，最右边那根会算出完整宽度。
