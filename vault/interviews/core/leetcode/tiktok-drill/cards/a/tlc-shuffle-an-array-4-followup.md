---
id: tlc-shuffle-an-array-4-followup
node: a.shuffle-an-array
type: qa
step: 4
---
## Q
**LC 384 打乱数组**｜追问

面试官接着问：（1）只给你 `random.random()`（返回 `[0, 1)` 的浮点数），怎么生成 `j`？（2）只需要随机排列的前 `k` 个元素呢？（3）数据是一个长度未知的流，要等概率抽 `k` 个？

## A
1. **只有 `random.random()`**：`j = i + int(random.random() * (n - i))`，`int` 向零截断，结果落在 `[i, n)`。`n` 很大时浮点精度会让少数下标的概率略有偏差，标准库的 `randrange` 用随机位拒绝采样避免了这个问题。
2. **只要前 `k` 个**：Fisher–Yates 只跑前 `k` 步就停，`arr[:k]` 已经是均匀的 `k` 元排列，`O(k)` 次交换。标准库对应 `random.sample(population, k)`，返回新列表。
3. **长度未知的流（蓄水池抽样，reservoir sampling）**：前 `k` 个直接放进池子；第 `t` 个元素（`t > k`，从 1 计数）以 `k/t` 的概率进入池子，替换池中随机一个。每个元素最终留在池里的概率都是 `k/N`。`k = 1` 就是 LC 382 链表随机节点。

```python
import random
from collections.abc import Iterable


def reservoir_sample(stream: Iterable[int], k: int) -> list[int]:
    pool: list[int] = []
    for t, x in enumerate(stream, 1):
        if t <= k:
            pool.append(x)
        elif (j := random.randrange(t)) < k:     # 概率 k/t 换进池子，换掉第 j 个
            pool[j] = x
    return pool
```

**Python 提醒**：`random.shuffle(arr)` 就地打乱并返回 `None`；要新列表用 `random.sample(arr, len(arr))`。
