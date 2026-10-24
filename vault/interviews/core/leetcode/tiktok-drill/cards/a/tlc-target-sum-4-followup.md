---
id: tlc-target-sum-4-followup
node: a.target-sum
type: qa
step: 4
---
## Q
**LC 494 目标和**｜追问

面试官接着问：（1）如果 `nums` 里允许出现负数，上面的变换还成立吗？（2）`n <= 20` 但数值很大（和到 `10^9`），怎么做？（3）要把所有满足条件的表达式都列出来呢？

## A
1. **允许负数**：「加的那堆」和「减的那堆」都是子集和这个前提不成立（`P` 可能为负，数组下标也没法用）。改用字典记录每一步可达的和及对应方案数，值域不受限，复杂度是「不同和的个数 × n」。

```python
from collections import Counter


def ways(nums: list[int], target: int) -> int:
    cnt: Counter[int] = Counter({0: 1})       # 当前可达的和 -> 方案数
    for x in nums:
        nxt: Counter[int] = Counter()
        for s, c in cnt.items():
            nxt[s + x] += c
            nxt[s - x] += c
        cnt = nxt
    return cnt[target]
```

`[1,1,1,1,1]`，`3` → `5`；`[-1,2,3]`，`4` → `1`。
2. **和很大**：数组 DP 的空间爆炸，但 `n <= 20`。折半枚举（meet in the middle）：前后两半各自求出所有「和 → 方案数」，每半最多 `2^10` 项，再枚举左半的和 `s`，在右半里查 `target - s`，`O(2^(n/2))`。
3. **列出所有表达式**：回溯，每个位置选 `+` 或 `-`，到末尾检查和；最多 `2^20` 个，所以用生成器逐个产出，不一次性建大列表。

**Python 提醒**：`Counter` 对不存在的键返回 `0` 且不会插入它，所以 `cnt[target]` 是安全的；换成 `defaultdict(int)` 则读取时会悄悄插入键，在循环中遍历它时会触发「字典在迭代中改变大小」的 `RuntimeError`。
