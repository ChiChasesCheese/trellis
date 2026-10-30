---
id: tlc-container-with-most-water-4-followup
node: b.container-with-most-water
type: qa
step: 4
---
## Q
**LC 11 盛最多水的容器**｜追问

面试官接着问：（1）要返回是哪两条线？（2）接雨水（LC 42）和它有什么区别，怎么写？（3）线的高度有重复，指针移动会不会有问题？

## A
1. **返回是哪两条线。** 更新最大值时同时记下指针位置：

```python
def max_area_with_pair(height: list[int]) -> tuple[int, int, int]:
    left, right = 0, len(height) - 1
    best, pair = 0, (0, 0)
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        if area > best:                          # 严格大于：并列时保留先找到的
            best, pair = area, (left, right)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best, pair[0], pair[1]
```

2. **接雨水（LC 42）。** 那里要累计所有柱子上方的水，每个位置的水量是 `min(左侧最高, 右侧最高) - height[i]`；用双指针时维护 `left_max`、`right_max`，每步处理较矮一侧，结构相似但目标不同：这里选两条线，那里每根柱子都要计算。
3. **高度重复。** 相等时移动任意一侧都正确，因为两条线高度相同，谁也不能与对方的外侧形成更好的容器；上面的 `else` 移动右侧。

**Python 提醒**：`max(best, h * (right - left))` 用内置 `max` 比 `if` 更短；但需要同时记录下标时必须写 `if`，因为 `max` 只返回值，不告诉你取到了哪一对。
