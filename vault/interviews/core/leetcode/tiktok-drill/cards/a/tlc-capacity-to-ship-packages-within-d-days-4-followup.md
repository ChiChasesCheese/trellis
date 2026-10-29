---
id: tlc-capacity-to-ship-packages-within-d-days-4-followup
node: a.capacity-to-ship-packages-within-d-days
type: qa
step: 4
---
## Q
**LC 1011 在 D 天内送达包裹的能力**｜追问

面试官接着问：（1）要输出每天具体装哪些包裹？（2）二分的范围还能收窄吗？（3）如果问题改成“把数组分成 `m` 段，使最大段和最小”？

## A
1. **输出方案**：拿到最终载重后再跑一遍贪心，换天时把当前这一天的包裹存起来。

```python
def plan(weights: list[int], capacity: int) -> list[list[int]]:
    days: list[list[int]] = [[]]
    load = 0
    for w in weights:
        if load + w > capacity:
            days.append([])
            load = 0
        days[-1].append(w)
        load += w
    return days
```

   `plan([1,2,3,4,5,6,7,8,9,10], 15)` → `[[1, 2, 3, 4, 5], [6, 7], [8], [9], [10]]`，正好 `5` 天。
2. **收窄范围**：平均每天至少要运 `ceil(sum / days)`，所以下界可以取 `max(max(weights), -(-sum(weights) // days))`。二分轮数略少，渐进复杂度不变。
3. **分成 `m` 段使最大段和最小**（LC 410）：与本问题完全同构，`days` 换成 `m`，`weights` 换成数组，代码一行不用改。若问最小化“最大值”的反问题——最大化“最小值”（如 LC 1231 分享巧克力），判定改成“每段至少 `x`”，二分的方向反过来，要找最后一个可行值，`mid` 向上取整以避免死循环。

**Python 提醒**：`-(-a // b)` 是整数向上取整的惯用写法（`//` 向下取整，对负数取反两次）；`math.ceil(a / b)` 经过浮点，数很大时可能出现误差。`days[-1].append(w)` 写在换天判断之后，保证新的一天已经存在。
