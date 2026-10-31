---
id: tlc-subarray-sum-equals-k-2-code
node: p2.subarray-sum-equals-k
type: qa
step: 2
---
## Q
**LC 560 和为 K 的子数组**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `2×10^4`，元素在 `[-1000, 1000]`）和整数 `k`（`|k| <= 10^7`），返回和恰好为 `k` 的连续非空子数组的个数。

## A
**思路。** 边扫边维护前缀和 `pre`。哈希表 `seen` 记录每个前缀和出现的次数；以当前位置结尾、和为 `k` 的子数组个数，就是此前出现过前缀和 `pre - k` 的次数。先累加答案，再把当前前缀和记入表中。

```python
from collections import Counter

def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```

运行：`([1,1,1], 2)` → `2`，`([1,2,3], 3)` → `2`，`([1,-1,1], 1)` → `3`，`([0,0,0], 0)` → `6`，`([-1,-1,1], 0)` → `1`，`([1], 0)` → `0`。

**复杂度。** 时间 `O(n)`：每个元素一次查询、一次更新；空间 `O(n)`：最多 `n + 1` 个不同的前缀和。

**写法要点。** `Counter` 对不存在的键返回 `0` 且**不会插入该键**，所以 `seen[pre - k]` 查询无副作用；用 `defaultdict(int)` 做同样的事，每次查询都会把键写进字典，内存翻倍而结果不变。`Counter({0: 1})` 一步完成「空前缀」的初始化。`pre = ans = 0` 链式赋值只适合不可变的数字。
