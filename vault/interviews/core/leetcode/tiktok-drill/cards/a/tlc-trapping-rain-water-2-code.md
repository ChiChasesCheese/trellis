---
id: tlc-trapping-rain-water-2-code
node: a.trapping-rain-water
type: qa
step: 2
---
## Q
**LC 42 接雨水**｜写出 Python 实现

`height` 是 `n` 根宽度为 1 的柱子的高度，`1 <= n <= 2 * 10^4`，`0 <= height[i] <= 10^5`，返回下雨后能接的雨水总量。要求 `O(n)` 时间、`O(1)` 额外空间。

## A
**思路。** 左右两个指针向中间走，各自维护已见过的最大高度。每次处理当前高度较矮的一侧：它的水位已经由自己这侧的最大值决定，直接累加 `最大值 - 当前高度`，再把这个指针往里移一格。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:           # 左边更矮：左格的水位由 left_max 决定
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                                      # 右边更矮或相等：右格的水位由 right_max 决定
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

运行：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`，`[4,2,0,3,2,5]` → `9`；`[5]` → `0`，`[3,3,3]` → `0`，`[5,0,5]` → `5`，`[1,2,3,4]` → `0`；`n = 20000`，高度在 `0` 与 `100000` 之间交替 → `999900000`。

**复杂度。** 时间 `O(n)`：每步移动一个指针，共 `n - 1` 步；空间 `O(1)`。

**写法要点。** `left_max = right_max = water = 0` 链式赋值只用于不可变的整数；先 `max` 更新再累加，当前柱子比历史最大还高时增量恰好是 `0`；`height[left] < height[right]` 的 `else` 分支同时处理「右边更矮」和「相等」，相等时处理哪一侧都对；结果可达 `2 * 10^9`，Python 整数不会溢出，换成 C++ / Java 要用 64 位整数。
