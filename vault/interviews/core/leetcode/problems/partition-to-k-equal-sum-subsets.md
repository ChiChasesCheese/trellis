---
slug: partition-to-k-equal-sum-subsets
---
## Q
**LC 698 划分为k个相等的子集**｜Medium

能否把 `nums`（长度 `<= 16`）分成 `k` 个非空子集，且和都相等？

## A
**一句话。** 状压 DP：`dp[mask]` 是用掉 `mask` 里的数后当前桶的已装量，装满就清零开新桶。

```python
def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums.sort()                # 升序：当前数放不下，更大的也放不下
    if nums[-1] > target:
        return False
    n = len(nums)
    dp = [-1] * (1 << n)       # -1：mask 不可达
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] < 0:
            continue
        for i, x in enumerate(nums):
            if dp[mask] + x > target:
                break
            if mask >> i & 1:
                continue
            nxt = mask | 1 << i
            if dp[nxt] < 0:
                dp[nxt] = (dp[mask] + x) % target
    return dp[-1] == 0
```

**复杂度。** 时间 `O(n·2^n)`，空间 `O(2^n)`。

**易错点。**
- 不检查 `sum % k`：`[1,1,1,1,1,1]`, `k=4`，`target` 取整成 `1`，错返回 `true`。
- 用 `0` 表示不可达：`0` 是合法状态（空桶或刚装满），要用 `-1`。
- 大数优先一桶一桶贪心装：`[2,2,2,2,3,3]`, `k=2`，先装 `3+3` 失败，实际 `{3,2,2}` 两组可行。

**追问。**
- 回溯怎么写？：数降序，逐个放进桶；同层相同的桶当前和只试一次，剪枝后常数小。
- 要输出划分？：多存 `parent[mask]`（最后加入的数），从全集往回走，桶清零处断开。

**同模式。** LC 416 分割等和子集、LC 473 火柴拼正方形、LC 1723 完成所有工作的最短时间、LC 2305 公平分发饼干
