---
id: tlc-koko-eating-bananas-4-followup
node: b.koko-eating-bananas
type: qa
step: 4
---
## Q
**LC 875 爱吃香蕉的珂珂**｜追问

面试官接着问：（1）如果每小时可以同时吃多堆，只限制总量 `k`？（2）速度允许是小数？（3）能不能用标准库把二分写短？

## A
1. **每小时可吃多堆**：不再有“一小时只能一堆”的取整损耗，总共要吃 `sum(piles)` 根，最少需要 `ceil(sum(piles) / h)` 的速度，`O(n)`，不需要二分。这也解释了原题的下界可以收窄成 `max(1, ceil(sum / h))`：任何可行速度都不会比它小。
2. **小数速度**：判定改成 `Σ ceil(p / k) <= h`，其中 `k` 是浮点；二分改成 `for _ in range(100)` 固定次数，或 `hi - lo > 1e-9` 作终止条件，`lo = mid` / `hi = mid` 不再 `±1`。注意浮点下 `ceil(p / k)` 在恰好整除处有舍入误差，需要容差。
3. **标准库**：`bisect_left` 的 `key` 参数（3.10+）可以在一个“虚拟序列”上二分，`range` 不占内存：

```python
from bisect import bisect_left


def min_eating_speed_bisect(piles: list[int], h: int) -> int:
    ok = lambda k: sum((p + k - 1) // k for p in piles) <= h
    return 1 + bisect_left(range(1, max(piles) + 1), True, key=ok)
```

   `([3,6,7,11], 8)` → `4`。原理：对 `range(1, M + 1)` 的每个元素用 `key` 映射成 `False / True`，序列是 `FFF…TTT`，`bisect_left` 找第一个 `True` 的位置，再加 `1` 还原成速度。

**Python 提醒**：`bisect` 的 `key` 只作用于序列元素，不作用于被查找的值（这里是 `True`）；序列必须按 `key` 的结果有序。在 3.9 及更早的版本里没有 `key`，只能写显式循环。
