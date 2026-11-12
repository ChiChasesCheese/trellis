---
slug: container-with-most-water
---
## Q
**LC 11 盛最多水的容器**｜Medium

数组 `height` 的每个元素是一条垂线的高度，选两条线与 `x` 轴构成容器（不能倾斜），求最大盛水量。

## A
**一句话。** 对撞双指针从最宽处开始，每次移动较短的那条线，只有换掉短板水位才可能升高。

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])   # 短板决定水位
        best = max(best, h * (right - left))
        if height[left] < height[right]:
            left += 1          # 丢掉短板
        else:
            right -= 1
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 移动较长的一侧：水位不会升、宽度又变小，`[1,8,6,2,5,4,8,3,7]` 得 `8`，应为 `49`。
- 水位取 `max`：容器不能倾斜，短板决定容量。

**追问。**
- 为什么丢掉短板不会漏掉最优解？：短板与任何更靠内的板配对，水位不超过短板、宽度更小，不会更优。
- 两边高度相等时移动哪边？：任意一边都对，丢掉任意一条都不会漏掉最优解。

**同模式。** LC 42 接雨水、LC 15 三数之和、LC 167 两数之和 II、LC 1679 K 和数对的最大数目
