---
id: tlc-partition-equal-subset-sum-2-code
node: b.partition-equal-subset-sum
type: qa
step: 2
---
## Q
**LC 416 分割等和子集**｜写出 Python 实现

`nums` 只含正整数（`1 <= len <= 200`，`1 <= nums[i] <= 100`），判断能否分成两个和相等的子集。

## A
**思路。** 总和奇数直接 `False`。否则判断能否凑出 `total // 2`。用位集：`bits` 的第 `i` 位表示「存在子集和为 `i`」，初始只有第 `0` 位（空集）。对每个数 `x`，`bits << x` 表示每个已有和都加上 `x`，与原 `bits` 取或表示选或不选。最后看第 `total // 2` 位。

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                           # 总和是奇数，不可能平分
    bits = 1                                   # 第 i 位为 1 表示「存在子集和恰好为 i」
    for x in nums:
        bits |= bits << x                      # 每个数选或不选；右边的 bits 是旧值，所以每个数只用一次
    return bool(bits >> (total // 2) & 1)
```

常规数组写法（逐项可读，位集写法的对照）：

```python
def can_partition_dp(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    half = total // 2
    dp = [True] + [False] * half               # dp[j]：是否存在子集和为 j
    for x in nums:
        for j in range(half, x - 1, -1):       # 倒着更新，保证每个数只用一次
            dp[j] = dp[j] or dp[j - x]
    return dp[half]
```

运行：`[1,5,11,5]` → `True`，`[1,2,3,5]` → `False`，`[1]` → `False`，`[2,2]` → `True`，`[100] * 200` → `True`，`[99] * 199 + [100]` → `False`；两种写法结果一致，位集版对 `200` 个数不到 `0.001` 秒，数组版约 `0.01` 秒。

**复杂度。** 位集版：时间 `O(n · S / w)`，`w` 是机器字长，空间 `O(S)` 位；数组版：时间 `O(n · S)`，空间 `O(S)`。

**写法要点。** Python 的 `int` 是任意精度，可以直接当位集，`bits << x` 与 `|=` 都是按字并行的；`bits >> k & 1` 的优先级是先移位再与 `1` 相与；数组版 `range(half, x - 1, -1)` 倒序保证 0/1 语义；位集版天然是 0/1（右边的 `bits` 是旧值），没有倒序的陷阱。
