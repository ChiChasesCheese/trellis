---
id: leetcode-c-array-index-as-hash
node: arrays-hash-prefix.array-index-as-hash
type: cloze
anki: 1787102263760
tags: [concept-cloze, leetcode, recall]
---
在 442 题的负号标记解法中，遍历到当前槽位的值时必须取 {{c1::abs(value)}} 而不能直接用 value，因为该槽位可能早已被之前遇到的某个值标记为负数；判断某个值 v 是否已出现过的依据是 {{c2::nums[v - 1] < 0}}。

负号标记利用值域 [1,n] 与数组长度 n 一一对应的性质，把每个槽位当作一个 bit 位记录“对应值是否出现过”。第一次遇到 v 时把 nums[v-1] 取反；第二次遇到时发现 nums[v-1] 已经是负数，说明重复。整个过程原地完成，O(n) 时间、O(1) 额外空间，但会修改输入数组。

**Evidence**

不变量：nums[v - 1] < 0 表示值 v 已经出现过。必须使用 abs(value)，因为当前遍历到的槽位可能早已被之前的值改成负数。第一次遇到 v 写状态；第二次遇到 v 输出答案。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E6%95%B0%E7%BB%84%E5%8E%9F%E5%9C%B0%E4%B8%8B%E6%A0%87%E5%93%88%E5%B8%8C%EF%BC%9A%E9%87%8D%E5%A4%8D%E4%B8%8E%E7%BC%BA%E5%A4%B1)
