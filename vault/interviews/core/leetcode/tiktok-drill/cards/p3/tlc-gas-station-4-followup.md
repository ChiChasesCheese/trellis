---
id: tlc-gas-station-4-followup
node: p3.gas-station
type: qa
step: 4
---
## Q
**LC 134 加油站**｜追问

面试官接着问：（1）能不能用前缀和的最小值直接算出起点？（2）如果解不唯一，要返回所有可行起点？（3）油箱有容量上限呢？

## A
1. **前缀和最小值。** 净油量的前缀和 `acc`，总和为负返回 `-1`，否则出发点是 `acc` 最小值（第一次出现）的下一站：
```python
from itertools import accumulate

def can_complete_circuit_acc(gas: list[int], cost: list[int]) -> int:
    diffs = [g - c for g, c in zip(gas, cost)]
    if sum(diffs) < 0:
        return -1
    acc = list(accumulate(diffs))
    return (acc.index(min(acc)) + 1) % len(gas)   # 最小值在末尾时，下一站绕回 0
```
`([1,2,3,4,5], [3,4,5,1,2])` → `3`，`([2,3,4], [3,4,3])` → `-1`。同样 `O(n)`，更好解释，但多一个 `O(n)` 数组。
2. **所有可行起点。** 总和 `>= 0` 时，所有使 `S(k)` 达到全局最小值的位置 `k` 的下一站都可行：`[i + 1 for i, v in enumerate(acc) if v == min(acc)]`，对下标取模。例如 `gas = [2,2,2]`、`cost = [2,2,2]`，三个站都可以出发。
3. **油箱有上限。** 到达加油站时多出来的油装不下，“总油量够就有解”不再成立，前缀和也不再线性叠加。需要从每个起点模拟，或者用线段树 / 单调栈做更复杂的分析；面试里说明贪心的前提（油箱无限）即可。

**Python 提醒**：`list.index(min(acc))` 返回**第一次**出现的位置，这正是贪心里最后一次重置的那个起点；换成 `max(range(n), key=...)` 之类的写法时要留意并列时选谁。
