---
id: leetcode-q-find-the-duplicate-number-mistake
node: linked-list.floyd-s-cycle-finding-algorithm
type: qa
anki: 1787102262158
tags: [lc::287, leetcode, mistake, recall]
---
## Q
写 findDuplicate 时用了原地交换（cycle sort）思路，为什么这个解法不满足题目要求？

## A
题目要求不能修改原数组（视为只读），而 cycle-sort 思路（把 nums[i] 换到正确位置 nums[i]-1，直到某位置值冲突即为重复）需要原地交换修改 nums，违反了这一约束。代码里作者自己标注了'不符合题目要求'，正确做法应改用 Floyd 判圈法或位运算/负数标记等不破坏原数组语义的方法（本题的负数标记法虽然也修改数组，但通常按题意可接受时才用）。

**Evidence**

代码中 findDuplicate0 方法上方注释写着 '# 不符合题目要求'，该方法通过 swap 原地修改 nums 数组来定位重复值；且笔记 frontmatter 中 last_result: failed，说明本次尝试未通过。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F287%20-%20Find%20the%20Duplicate%20Number)
