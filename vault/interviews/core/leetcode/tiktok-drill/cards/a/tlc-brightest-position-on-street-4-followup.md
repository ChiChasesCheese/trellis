---
id: tlc-brightest-position-on-street-4-followup
node: a.brightest-position-on-street
type: qa
step: 4
---
## Q
**LC 2021 街上最亮的位置**｜追问

面试官接着问：（1）要返回所有最亮的位置？（2）坐标范围很小（比如 `0..10^6`），能不能不排序？（3）灯会动态增删，还要随时查最亮的位置？

## A
1. **所有最亮的位置。** 扫描时记录最大亮度出现的区间：亮度等于最大值的一段 `[x_i, x_{i+1})` 都是答案。需要先扫一遍求最大值，再扫第二遍收集区间。
2. **小范围。** 开数组 `diff[0..R+1]`，直接用 `itertools.accumulate` 求前缀和，再取 `max` 的下标，`O(n + R)`：

```python
from itertools import accumulate


def brightest_small(lights: list[list[int]], size: int) -> int:
    diff = [0] * (size + 2)
    for pos, rng in lights:
        diff[max(pos - rng, 0)] += 1
        diff[min(pos + rng, size) + 1] -= 1
    levels = list(accumulate(diff))
    return levels.index(max(levels))             # index 返回第一个最大值，即坐标最小
```

3. **动态增删。** 坐标离散化后用线段树维护"区间加、全局最大及其最左位置"；每次增删一盏灯是一次区间更新 `O(log n)`。

**Python 提醒**：`list.index(max(levels))` 返回最大值**第一次**出现的下标，正好满足"并列取坐标最小"；而 `max(range(len(levels)), key=levels.__getitem__)` 在并列时也返回第一个，两种写法都可靠。
