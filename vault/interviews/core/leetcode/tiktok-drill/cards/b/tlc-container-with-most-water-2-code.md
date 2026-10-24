---
id: tlc-container-with-most-water-2-code
node: b.container-with-most-water
type: qa
step: 2
---
## Q
**LC 11 盛最多水的容器**｜写出 Python 实现

整数数组 `height`（长度 `2..10^5`，元素 `0..10^4`）。选两条线 `i < j`，容器水量为 `min(height[i], height[j]) * (j - i)`。返回最大水量，要求 `O(n)`。

## A
**思路。** `left`、`right` 从两端出发。每步算当前面积并更新答案，然后移动较矮的一侧；相等时移动任意一侧。直到两指针相遇。

```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])     # 水位由短板决定
        best = max(best, h * (right - left))
        if height[left] < height[right]:         # 移动长板只会让宽度变小、水位不会更高，所以动短板
            left += 1
        else:
            right -= 1
    return best
```

**运行。** `[1,8,6,2,5,4,8,3,7]` → `49`；`[1,1]` → `1`；`[0,0]` → `0`；`[4,3,2,1,4]` → `16`；`[1,2,1]` → `2`。

**复杂度。** 时间 `O(n)`：每次循环两指针的距离减 `1`；空间 `O(1)`。

**写法要点。** `left, right = 0, len(height) - 1` 同时初始化；`min(...)` 先算水位 `h`，让面积公式 `h * (right - left)` 一目了然；`best = max(best, …)` 是内置函数，不需要先 `if`；`if … < … else` 的 `else` 同时覆盖"右边更矮"和"相等"两种情况，保证每轮一定有指针移动，循环必然终止。
