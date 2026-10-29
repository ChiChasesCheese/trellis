---
id: tlc-pile-box-lcci-5-alt
node: b.pile-box-lcci
type: qa
step: 5
---
## Q
**面试题 08.13 堆箱子**｜另一种解法

不写自底向上的表，用「记忆化递归」怎么表达同一个 DP？`n = 3000` 时会不会爆递归栈？两种写法怎么选？

## A
**思路。** 定义 `tower(i)` = 以 `boxes[i]` 为底的最高箱堆，直接按定义递归：`h_i` 加上所有能放在上面的 `tower(j)` 的最大值；`@cache` 保证每个 `i` 只算一次。

```python
from functools import cache


def pile_box_memo(box: list[list[int]]) -> int:
    boxes = sorted(box)

    @cache
    def tower(i: int) -> int:                    # 以 boxes[i] 为最底层的最高箱堆
        w, d, h = boxes[i]
        return h + max((tower(j) for j in range(i)
                        if boxes[j][0] < w and boxes[j][1] < d and boxes[j][2] < h), default=0)

    return max(tower(i) for i in range(len(boxes)))
```

运行：`[[1,1,1],[2,2,2],[3,3,3]]` → `6`，`[[1,1,1],[2,3,4],[2,6,7],[3,4,5]]` → `10`，3000 个 `[i,i,i]` → `4501500`。

**递归深度。** 外层按 `i` 升序调用：轮到 `tower(i)` 时，所有更小下标的值都已缓存，它调用的 `tower(j)` 立刻返回，深度是常数。内层按 `j` 升序也有同样效果：`tower(i)` 先算 `tower(j)`，而能放在 `j` 上面的 `j' < j` 也能放在 `i` 上面（严格支配可传递），早已在本轮算过。只有两处都倒序（直接从最大的 `i` 开始、内层 `range(i - 1, -1, -1)`）时，链状输入才会递归到深度 `n = 3000`，超过默认上限 `1000`，触发 `RecursionError`。

**取舍。** 记忆化写法贴近定义、不用想填表顺序，适合先写对；自底向上的表没有递归开销和栈深度风险，常数更小，是交付版。复杂度相同：`O(n^2)` 时间、`O(n)` 空间（`@cache` 的字典多一些常数）。`max(..., default=0)` 处理「上面不放箱子」的情况，避免对空序列调用 `max` 抛 `ValueError`。
