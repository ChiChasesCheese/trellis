---
slug: contiguous-array
---
## Q
**LC 525 连续数组**｜Medium

二进制数组 `nums`，求 `0` 和 `1` 数量相同的最长连续子数组的长度。

## A
**一句话。** 把 `0` 当 `-1`，转成「前缀和相等的最远两点」，哈希表记每个前缀和第一次出现的下标。

```python
def find_max_length(nums):
    first = {0: -1}    # 空前缀在下标 -1
    best = bal = 0
    for i, x in enumerate(nums):
        bal += 1 if x else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i     # 只记第一次，区间才最长
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 每次都覆盖下标：区间变短，`[0,1,0,1]` 得 `2`，应为 `4`。
- 漏了预置 `{0: -1}`：从下标 `0` 开始的子数组算不到，`[0,1]` 得 `0`。

**追问。**
- 和为 `k` 的最长子数组？：改查 `bal - k`，其余不变。
- 要返回子数组本身？：更新 `best` 时记下起点 `first[bal] + 1`。

**同模式。** LC 560 和为 K 的子数组、LC 325 和等于 k 的最长子数组、LC 1124 表现良好的最长时间段、LC 974 和可被 K 整除的子数组
