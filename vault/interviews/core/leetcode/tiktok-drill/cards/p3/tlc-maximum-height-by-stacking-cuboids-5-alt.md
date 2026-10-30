---
id: tlc-maximum-height-by-stacking-cuboids-5-alt
node: p3.maximum-height-by-stacking-cuboids
type: qa
step: 5
---
## Q
**LC 1691 堆叠长方体的最大高度**｜另一种解法

除了自底向上的 `dp[i]` 数组，还有哪些写法？经典 Box Stacking 把三个朝向都展开成独立项，为什么在这里是错的？什么时候选哪种？

## A
**写法一：记忆化递归（自顶向下）。** 同样先规范化、排序，用 `functools.cache` 定义 `best_on(i)` 为以第 `i` 个为底的最大高度，递归到 `j < i`：
```python
from functools import cache

def max_height_memo(cuboids: list[list[int]]) -> int:
    boxes = sorted(sorted(c) for c in cuboids)

    @cache
    def best_on(i: int) -> int:                      # 以 boxes[i] 为底的最大高度
        return boxes[i][2] + max(
            (best_on(j) for j in range(i) if all(a <= b for a, b in zip(boxes[j], boxes[i]))),
            default=0,
        )

    return max(map(best_on, range(len(boxes))))
```
状态数和转移都和数组版一样，`O(n^2)`；递归深度最多 `n = 100`，不会超限。它的好处是读起来就是递推式；代价是函数调用开销，`n` 再大就要换回数组。

**写法二：展开三个朝向（会错）。** 经典 Box Stacking 允许每种箱子无限个，因此把每个箱子展开成 3 个「底面 + 高」的项再做 LIS。这里每个箱子只有一个，展开后同一个箱子的两个朝向可能互相叠上去：`[[1,2,3]]` 得 `6`，正确答案 `3`。想用它必须额外记录「哪些朝向属于同一个箱子」，反而复杂；规范化成唯一朝向才是关键。

**怎么选。** `n <= 100` 时数组版最短最稳，先写它；想让面试官看到递推式就写记忆化版；`n` 到 `10^5` 才需要 CDQ 加树状数组。
