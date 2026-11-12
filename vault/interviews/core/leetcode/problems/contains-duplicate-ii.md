---
slug: contains-duplicate-ii
---
## Q
**LC 219 存在重复元素 II**｜Easy

判断是否存在两个不同下标 `i`、`j`，使 `nums[i] == nums[j]` 且 `|i - j| <= k`。

## A
**一句话。** 字典记每个值最近一次出现的下标，遇到相同值就看距离是否 `<= k`，每次都更新为当前下标。

```python
def contains_nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i                # 无论是否命中都要更新
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只在首次出现时记录：`[1,0,1,1]`、`k = 1` 会漏掉下标 `2` 和 `3`，应为 `True`。
- 边界写成 `< k`：`[1,2,3,1]`、`k = 3` 距离恰为 `3`，应为 `True`。

**追问。**
- 能只保留窗口吗？：维护大小 `k` 的集合，滑出窗口就删除，空间 `O(k)`。
- 改成值相差不超过 `t`（LC 220）？：窗口内用桶或有序集合找近邻。

**同模式。** LC 217 存在重复元素、LC 220 存在重复元素 III、LC 3 无重复字符的最长子串
