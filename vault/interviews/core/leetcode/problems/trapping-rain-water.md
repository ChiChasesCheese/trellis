---
slug: trapping-rain-water
---
## Q
**LC 42 接雨水**｜Hard

给柱子高度数组，求下雨后能接多少单位的水。

## A
**一句话。** 双指针向中间收拢，每次结算较矮的一侧：它的水位只由自己这侧的最大值决定。

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:   # 左矮
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                              # 右矮或等
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 结算前没先更新 `left_max`：当前柱比历史最大还高时得到负数。
- 处理了较高的一侧：`[0,0,1]` 得 `1`，应为 `0`。
- 用整体最大值减高度：`[4,2,0,3,2,5]` 得 `14`，应为 `9`。

**追问。**
- 单调栈怎么做？：遇到更高的柱子就弹出栈顶当坑底，按「层」累加宽度乘高度差。
- 二维版（LC 407）？：从边界起用小根堆，弹出最低的边界格向内扩展，水位取 `max(水位, 邻格高度)`。

**同模式。** LC 11 盛最多水的容器、LC 84 柱状图中最大的矩形、LC 407 接雨水 II、LC 238 除自身以外数组的乘积
