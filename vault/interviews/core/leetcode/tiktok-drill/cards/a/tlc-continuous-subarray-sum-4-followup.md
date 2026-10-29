---
id: tlc-continuous-subarray-sum-4-followup
node: a.continuous-subarray-sum
type: qa
step: 4
---
## Q
**LC 523 连续的子数组和**｜追问

面试官接着问：（1）如果 `k` 可能是 0 呢？（2）要统计这样的子数组个数，没有「长度至少 2」？（3）如果 `nums` 里有负数？

## A
1. **`k = 0`**：0 的倍数只有 0，条件变成「区间和为 0」，即两个前缀和**相等**。把取余改成 `prefix = (prefix + x) % k if k else prefix + x`，其余不变。
2. **统计个数**（LC 974）：每个余数出现过多少次，当前前缀每多一个同余的旧前缀就多一个子数组。
```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 空前缀余数为 0，出现 1 次
    prefix = ans = 0
    for x in nums:
        prefix = (prefix + x) % k
        ans += seen[prefix]
        seen[prefix] += 1
    return ans
```
3. **有负数**：Python 的 `%` 对正的 `k` 结果始终在 `[0, k)`，代码不用改；C++/Java 的余数可能为负，要写 `((x % k) + k) % k`。

**Python 提醒**：`Counter` 读取不存在的键返回 0 且不会插入该键，所以 `seen[prefix]` 可以直接累加。
