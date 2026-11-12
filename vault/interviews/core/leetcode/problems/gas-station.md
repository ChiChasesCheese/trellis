---
slug: gas-station
---
## Q
**LC 134 加油站**｜Medium

环形路线上有 `n` 个加油站，`gas[i]` 是加油量，`cost[i]` 是开往下一站的耗油。油箱无限、初始为空，返回能绕一圈的出发站编号，没有则返回 `-1`（解唯一）。

## A
**一句话。** 贪心一趟扫描：累计油量变负就把起点改成下一站，最后用总净油量判断有无解。

```python
def can_complete_circuit(gas, cost):
    total = tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:             # start..i 都不能当起点
            start, tank = i + 1, 0
    return start if total >= 0 else -1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉 `total >= 0`：`gas=[2,3,4]`，`cost=[3,4,3]` 总油不够，却返回 `2`，应为 `-1`。
- 重置写成 `start = i`：失败发生在 `i` 站，起点应是 `i + 1`。
- 把 `total` 和 `tank` 合并：重置后 `total` 只剩最后一段，判断失效。

**追问。**
- 为什么总油够就一定有解？：取净油前缀和最小的位置，从它的下一站出发，油量永远不为负。

**同模式。** LC 55 跳跃游戏、LC 45 跳跃游戏 II、LC 53 最大子数组和、LC 135 分发糖果
