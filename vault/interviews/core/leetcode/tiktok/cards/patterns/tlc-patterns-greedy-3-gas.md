---
id: tlc-patterns-greedy-3-gas
node: patterns.greedy
type: qa
step: 3
---
## Q
**贪心（Greedy）｜正确性：加油站（LC 134）为什么"失败就从下一站重新开始"**

环形路线里一次扫描怎么找起点？为什么失败点之前的任何站都不可能是起点，总油量为什么只需最后判断一次？

## A
```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        total += g - c                     # 全程净油量
        tank += g - c                      # 从 start 出发到 i 的油量
        if tank < 0:
            start = i + 1                  # [start, i] 中任何一个点出发都走不到 i + 1：从 i + 1 重新开始
            tank = 0
    return start if total >= 0 else -1
print(can_complete_circuit([1,2,3,4,5], [3,4,5,1,2]), can_complete_circuit([2,3,4], [3,4,3]), can_complete_circuit([5], [4]))   # 3 -1 0
```

**为什么失败点之前的站都不是起点**：设从 `start` 出发在 `i` 处第一次油量为负。对 `start < k <= i` 的任意起点 `k`：从 `start` 出发到达 `k` 时油量 `>= 0`（否则之前就失败了），所以从 `k` 出发（油量为 0）到 `i` 时的油量**不会比**从 `start` 出发更多，同样为负。

**为什么只需最后判断 `total >= 0`**：若全程净油量不小于 0，则存在起点；上面的扫描得到的 `start` 之后的一段（直到末尾）保证 `tank >= 0`，而前面各段的亏空由总油量 `>= 0` 补偿。

**漏掉总油量判断的反例**：`gas = [1, 2]`，`cost = [3, 2]`，总净油量为 `-2`，实际无解，应返回 `-1`。
- 去掉 `total` 判断，只返回 `start`：`i = 0` 时亏空，`start = 1`；`i = 1` 时 `tank = 0`，不为负，返回 `1`。
- 正确答案是 `-1`。

- 时间 `O(n)`，空间 `O(1)`；暴力是 `O(n^2)`，`n = 10^5` 不可行。
- 题目保证有解时答案唯一，所以返回 `start` 即可。
