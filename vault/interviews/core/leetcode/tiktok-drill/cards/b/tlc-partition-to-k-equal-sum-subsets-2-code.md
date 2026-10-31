---
id: tlc-partition-to-k-equal-sum-subsets-2-code
node: b.partition-to-k-equal-sum-subsets
type: qa
step: 2
---
## Q
**LC 698 划分为k个相等的子集**｜写出 Python 实现

整数数组 `nums`（长度 `1..16`，元素 `1..9999`）和整数 `k`（`1..len(nums)`）。判断能否把 `nums` 划分成 `k` 个和相等的非空子集。

## A
**思路。** 先把每桶的目标和算出来，总和不能整除 `k` 或最大数超过目标就直接 `false`。数组升序后，用一个长度 `2^n` 的数组 `dp` 记「用掉 `mask` 里的数后，当前桶已装多少」，`-1` 表示不可达，`dp[0] = 0`。从每个可达状态出发，依次尝试放入一个还没用的数；放得下就更新后继状态，装满一桶则余数清零。最后看全集状态是否可达（值为 `0`）。

```python
def can_partition_k_subsets(nums: list[int], k: int) -> bool:
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums = sorted(nums)                   # 升序：放不下当前数，更大的也放不下
    if nums[-1] > target:
        return False
    n = len(nums)
    # dp[mask]：用掉 mask 里的数、凑满若干桶后，当前桶已装的和；-1 表示 mask 不可达
    dp = [-1] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] < 0:
            continue
        for i, x in enumerate(nums):
            if dp[mask] + x > target:
                break                     # 当前桶装不下 x，也装不下之后更大的数
            if mask >> i & 1:
                continue
            nxt = mask | 1 << i
            if dp[nxt] < 0:
                dp[nxt] = (dp[mask] + x) % target   # 装满一桶就清零，开新桶
    return dp[-1] == 0
```

运行：`nums=[4,3,2,3,5,2,1], k=4` → `True`，`nums=[1,2,3,4], k=3` → `False`，`nums=[2,2,2,2,3,3], k=2` → `True`，`nums=[5], k=1` → `True`，`16 个 1, k=16` → `True`，`nums=[10,10,10,7,7,7,7,7,7,6,6,6]（总和 90 不能被 4 整除）, k=4` → `False`。

**复杂度。** 时间 `O(n·2^n)`：`2^n` 个状态，每个状态枚举 `n` 个数（升序遍历，装不下就 `break`，实际更少）；`n = 16` 时约 `10^6` 次。空间 `O(2^n)`。

**写法要点。** `total % k` 作为真值直接用于 `if`；`sorted(nums)` 之后的 `break` 剪枝：升序里当前数放不下，后面更大的也放不下；`mask >> i & 1` 取第 `i` 位（运算符优先级：`>>` 高于 `&`），`mask | 1 << i` 置位（`<<` 高于 `|`）；`(dp[mask] + x) % target` 一步完成「装满一桶清零」；`dp[-1]` 取全集状态，比 `dp[(1 << n) - 1]` 简洁；`enumerate(nums)` 同时给下标和值。
