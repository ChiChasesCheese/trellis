---
slug: non-decreasing-subsequences
---
## Q
**LC 491 非递减子序列**｜Medium

整数数组 `nums`，返回所有长度至少为 2 的、不同的非递减子序列（值序列不同才算不同，顺序任意）。

## A
**一句话。** 回溯：依次选下一个元素（不小于上一个）；为了去重，同一层里相同的值只选一次，用一个局部集合记录。

```python
def find_subsequences(nums):
    res, path = [], []
    def dfs(start):
        if len(path) >= 2:
            res.append(path[:])
        used = set()             # 同一层相同的值只选一次
        for j in range(start, len(nums)):
            if nums[j] in used:
                continue
            if path and nums[j] < path[-1]:
                continue         # 要保持非递减
            used.add(nums[j])
            path.append(nums[j])
            dfs(j + 1)
            path.pop()
    dfs(0)
    return res
```

**复杂度。** 时间 `O(n · 2^n)`，空间 `O(n)`（不计结果）。

**易错点。**
- 先排序再用 `nums[j] == nums[j - 1]` 去重：这里的子序列要保持原顺序，不能排序。
- 去重集合放成全局：`used` 必须按层局部创建，否则不同分支之间互相误杀。
- 长度为 1 的子序列也收集：要求至少 2 个元素。

**追问。**
- 为什么同层去重不会漏？：同一层选择的位置不同但值相同，后面能延伸出的序列相同（靠前的那个覆盖了靠后的）。
- 与 LC 90 子集 II 的区别？：那里能排序后相邻去重，这里顺序固定，只能用哈希集合。

**同模式。** LC 90 子集 II、LC 78 子集、LC 47 全排列 II、LC 40 组合总和 II
