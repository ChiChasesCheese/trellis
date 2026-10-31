---
id: tlc-gas-station-2-code
node: p2.gas-station
type: qa
step: 2
---
## Q
**LC 134 加油站**｜写出 Python 实现

环形路线有 `n` 个加油站（`1 <= n <= 10^5`），`gas[i]` 是第 `i` 站的汽油量，`cost[i]` 是从第 `i` 站开往下一站的耗油量（都在 `0` 到 `10^4`）。油箱无限大，出发时为空。返回能绕一圈的出发站编号，不能则返回 `-1`（有解时唯一）。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 累加总净油量 `total` 和从候选起点出发的当前油量 `tank`。`tank` 一旦为负，就把候选起点推到下一站并清空 `tank`。扫描结束后，若 `total >= 0`，最后一个候选起点就是答案。

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c                        # 在 i 站净得多少油
        total += diff
        tank += diff
        if tank < 0:                        # 从 start 出发走不到 i+1：start..i 都不能当起点
            start, tank = i + 1, 0
    return start if total >= 0 else -1      # 总油量够，从最后一次重置的位置出发一定可行
```

运行：`([1,2,3,4,5], [3,4,5,1,2])` → `3`，`([2,3,4], [3,4,3])` → `-1`，`([5], [4])` → `0`，`([2], [2])` → `0`，`([3,1,1], [1,2,2])` → `0`。

**复杂度。** 时间 `O(n)`：一趟扫描；空间 `O(1)`：四个整数变量。

**写法要点。**
- `enumerate(zip(gas, cost))` 配合 `for i, (g, c) in ...` 一步解包下标和两个值，避免 `gas[i] - cost[i]` 的重复索引。
- `start, tank = i + 1, 0` 一次完成两个赋值，表达“重新开始”这一个动作。
- 不需要模拟绕回：总油量够就保证从 `start` 出发能走完，不用再走第二遍环形。
- 等价的函数式写法：`acc = list(accumulate(g - c for g, c in zip(gas, cost)))`，总和 `acc[-1] < 0` 返回 `-1`，否则 `(acc.index(min(acc)) + 1) % n`。
