---
id: leetcode-q-partition-to-k-equal-sum-subsets-pattern
node: bitwise-tricks.bitmask
type: qa
anki: 1787354597654
tags: [lc::698, leetcode, pattern, recall]
---
## Q
回溯解决「划分为k个相等的子集」(LC 698) 时，如何用状态压缩剪枝减少无效搜索？

## A
1) 用 mask 表示 nums 中已使用的元素，用 cur 表示当前正在填的桶已装的和（对 target 取模，方便去重同余状态）；2) dfs(mask, cur) 用 @cache 记忆化；3) 关键剪枝：当 cur == 0（即当前正在为一个全新的空桶选第一个数）时，如果选 nums[i] 放入这个空桶导致后续搜索全部失败，直接 break，不再尝试用其他数字去开启这个空桶——因为对一个空桶而言，选哪个失败的数字打头都是等价失败，没必要重复尝试。

**Evidence**

```
@cache
def dfs(mask, cur):
    if mask == (1 << n) - 1:
        return True
    for i in range(n):
        if mask & (1 << i):
            continue
        if cur + nums[i] > target:
            continue
        new_sum = (cur + nums[i]) % target
        if dfs(mask | (1 << i), new_sum):
            return True
        if cur == 0:
            break
    return False
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F698%20-%20Partition%20to%20K%20Equal%20Sum%20Subsets)
