---
id: tlc-partition-equal-subset-sum-4-followup
node: b.partition-equal-subset-sum
type: qa
step: 4
---
## Q
**LC 416 分割等和子集**｜追问

面试官接着问：（1）要把数组分成两堆使重量差最小（LC 1049）？（2）要输出其中一个子集？（3）数字很大、总和到 `10^9`，DP 还能用吗？

## A
1. **最小差**：同样的位集，找最接近 `total / 2` 的置位。
```python
def min_partition_diff(nums: list[int]) -> int:
    total = sum(nums)
    bits = 1
    for x in nums:
        bits |= bits << x
    return min(abs(total - 2 * i) for i in range(total + 1) if bits >> i & 1)
```
`[1,5,11,5]` → `0`，`[1,2,3,5]` → `1`。
2. **输出一个子集**：保存每个数处理后的 `bits` 列表 `history`；从目标 `t = total // 2` 倒推：对 `i` 从后往前，若 `history[i]` 的第 `t` 位为真而 `history[i - 1]` 的第 `t` 位为假，说明第 `i` 个数必须选，`t -= nums[i]`。空间 `O(n · S)` 位。
3. **总和巨大**：DP 的状态数随 `S` 增长，不能用。此时 `n` 通常很小，用**折半枚举**（meet in the middle）：把数组分成两半各枚举子集和，排序后双指针匹配，`O(2^(n/2) · n)`。`n <= 40` 左右可行。

**Python 提醒**：位集 `bits` 的大小随最大子集和增长，`10^4` 位只有约 `1.3 KB`；但若总和到 `10^9`，大整数有 `10^9` 位（约 `125 MB`），这个技巧就不适用了。
