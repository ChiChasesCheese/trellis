---
id: tlc-trapping-rain-water-4-followup
node: a.trapping-rain-water
type: qa
step: 4
---
## Q
**LC 42 接雨水**｜追问

面试官接着问：（1）改用单调栈怎么做？（2）要输出每一格的水量，而不只是总量？（3）柱子变成二维的高度网格（LC 407）怎么办？

## A
1. **单调栈**：栈里存下标，对应高度从栈底到栈顶递减。遇到比栈顶高的柱子 `h`，把栈顶弹出当作"坑底"；如果栈还有元素，新栈顶是坑的左壁，当前柱子是右壁，宽度是两壁之间的格数，高度是两壁较矮者减坑底，把"一层"水加上去。

```python
def trap_stack(height: list[int]) -> int:
    stack: list[int] = []
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            if not stack:
                break                                   # 没有左壁，存不住水
            width = i - stack[-1] - 1
            water += (min(height[stack[-1]], h) - bottom) * width
        stack.append(i)
    return water
```

`trap_stack([0,1,0,2,1,0,1,3,2,1,2,1])` → `6`，和双指针一致。这是按"层"累加，每个下标进出栈各一次，`O(n)` 时间，空间 `O(n)`。
2. **每格水量**：用前缀 / 后缀数组：`min(prefix[i], suffix[i]) - height[i]`，空间 `O(n)`，思路最直观，见另一种解法。
3. **二维（LC 407）**：水位由最低的"外墙"决定。把四周的格子放进小根堆，每次弹出最低的边界格，检查它的未访问邻居：邻居比它矮就积水 `当前高度 - 邻居高度`，并以 `max(邻居高度, 当前高度)` 作为新的边界高度入堆。`O(mn log(mn))`。

**Python 提醒**：`height[stack[-1]]` 这类取栈顶的写法要先保证 `stack` 非空，弹栈后再访问 `stack[-1]` 前必须重新判断，否则空列表会抛 `IndexError`。
