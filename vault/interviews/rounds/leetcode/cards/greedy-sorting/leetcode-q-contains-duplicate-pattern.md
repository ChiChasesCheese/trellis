---
id: leetcode-q-contains-duplicate-pattern
node: greedy-sorting.sorting
type: qa
anki: 1787102261882
tags: [lc::217, leetcode, pattern, recall]
---
## Q
如何用 O(n) 时间判断数组中是否存在重复元素？

## A
用哈希集合（set）去重后比较长度：len(set(nums)) < len(nums) 则存在重复。或用 Counter 统计频次判断是否有值 >= 2。核心思路：用哈希结构以空间换时间，把「是否出现过」的判断从 O(n) 查找降为 O(1)。变体：数值范围有限时可用位掩码（bitmask）按正负分别标记出现过的数字，进一步节省内存。

**Evidence**

```
def containsDuplicate2(self, nums): return len(set(nums)) < len(nums)
def containsDuplicate3(self, nums): return any(x >= 2 for x in Counter(nums).values())
```

ⵣ 以及位运算版本 containsDuplicate1 使用 posCheck/negCheck 位掩码记录已出现的正负数字。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F217%20-%20Contains%20Duplicate)
