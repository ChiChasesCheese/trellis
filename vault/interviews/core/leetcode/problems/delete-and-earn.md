---
slug: delete-and-earn
---
## Q
**LC 740 删除并获得点数**｜Medium

每次选一个 `nums[i]` 获得其点数，并删除所有等于 `nums[i]±1` 的元素，求最大总点数。

## A
**一句话。** 选了数值 `v` 就一次拿走所有 `v`，按数值升序做打家劫舍：相邻数值二选一，不相邻随便选。

```python
def delete_and_earn(nums):
    total = Counter(nums)
    take = skip = 0           # 选 / 不选当前数值的最优
    prev = None
    for v in sorted(total):
        gain = v * total[v]   # 一次拿走所有 v
        if prev is not None and prev + 1 == v:
            take, skip = skip + gain, max(take, skip)
        else:                 # 不相邻：互不影响
            m = max(take, skip)
            take, skip = m + gain, m
        prev = v
    return max(take, skip)
```

**复杂度。** 时间 `O(n + k log k)`，空间 `O(k)`。

**易错点。**
- 不相邻时仍用 `skip + gain`：`[1,3,5]` 得 `6`，应为 `9`。
- 收益只算 `v`：`[2,2,3,3,3,4]` 得 `6`，应为 `9`，要乘个数。
- 只比较相邻下标不比较数值差：相差 2 的数值没有冲突。

**追问。**
- 值域非常大怎么办？：本解法按排序后的不同数值走，不依赖值域。
- 规则改成 `x±2` 也要删除？：冲突范围变长，状态要多记一位。

**同模式。** LC 198 打家劫舍、LC 213 打家劫舍 II、LC 2320 统计放置房子的方式数、LC 983 最低票价
