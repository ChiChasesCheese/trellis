---
id: tlc-tops-trapping-rain-water-0-whole
node: two-pointers.trapping-rain-water
type: qa
---
## Q
**LC 42 接雨水**｜Hard · 全公司热度第 9 名 · NeetCode 150、Hot 100、Top Interview 150

给定 `n` 个非负整数表示每个宽度为 `1` 的柱子的高度图，计算按此排列的柱子下雨之后能接多少雨水。`n == height.length`，`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`。例：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`；`[4,2,0,3,2,5]` → `9`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 对撞双指针 + 左右最大值：每个位置的水量 = `min(左侧最高, 右侧最高) - 自身高度`。

**一句话。** 比较两端柱高，较矮的一侧的水位已经确定（由它自己这一侧的最高柱决定），结算后向内移动。

**识别。** 「每个位置的结果由左右两侧的最大值共同决定」是前后缀最大值的信号；`n = 2 * 10^4`，`O(n^2)` 勉强能过，面试要的是 `O(n)`，并且追问 `O(1)` 空间。

**推导。** 对位置 `i`，能存的水是 `min(max(height[:i+1]), max(height[i:])) - height[i]`。暴力对每个 `i` 求两个最大值，`O(n^2)`。浪费在重复求最大值，预处理出前缀最大值与后缀最大值数组即可 `O(n)`。再进一步，只要左右两个指针比较「哪边矮」：矮的一侧（设左边）右边一定有不矮于它的柱子，所以它的水位由左侧最高柱决定，不需要知道右侧最大值的具体数字。

**简单解法。** 预处理两个数组：`left_max[i]` 是 `height[:i+1]` 的最大值，`right_max[i]` 是 `height[i:]` 的最大值，答案 `sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))`，时间 `O(n)`，空间 `O(n)`，逻辑最直接；双指针只是把这两个数组压成两个变量。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0  # 各自一侧到目前为止见过的最高柱
    water = 0
    while left < right:
        # 处理较矮的一侧。设 height[left] < height[right]：右侧至少有一根不矮于 height[right] 的柱，
        # 所以 left 处的水位 = left_max（左侧最高）一定不被右侧卡住，可以立刻结算
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

运行：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`；`[4,2,0,3,2,5]` → `9`；`[3]` → `0`；`[2,0,2]` → `2`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 单调栈（monotonic stack）按「层」计算：栈内保持高度递减，遇到更高的柱子时弹出凹槽底，用左右边界与底的高度差乘宽度累加。同样 `O(n)`，空间 `O(n)`，适合被追问「逐层 / 逐个凹槽」的场景。

**易错点。**
- 先结算再更新最大值：`water += left_max - height[left]` 写在 `left_max = max(...)` 之前，会在遇到新的最高柱时算出负数；`[4,2,0,3,2,5]` 会得到 `5`，正确是 `9`。
- 两端的柱子本身存不了水，初始 `left_max = right_max = 0` 且减去自身高度时恰好为 `0`，不会出错。

**同模式。** LC 11 盛最多水的容器、LC 84 柱状图中最大的矩形、LC 238 除了自身以外数组的乘积、LC 407 接雨水 II。
