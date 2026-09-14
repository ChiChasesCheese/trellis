---
id: leetcode-q-count-integers-appearing-in-a-single-block-pattern
node: topics.uncategorised
type: qa
anki: 1788391211498
tags: [lc::4038, leetcode, pattern, recall]
---
## Q
如何判断数组中某个数值的所有出现位置是否构成单一连续区块？

## A
用哈希表记录每个数值出现的所有下标（num2indices[num].append(i)），然后对每个数值的下标列表做 pairwise 相邻比较：只要存在相邻下标之差 > 1，说明中间被别的数值隔开，不是单一区块；否则计数加一。核心是把“值是否连续出现”转化为“该值下标列表是否连续（相邻差值恒为1）”。

**Evidence**

num2indices = defaultdict(list); for i, num in enumerate(nums): num2indices[num].append(i) ... if any(cur - prev > 1 for prev, cur in pairwise(indices)): continue; cnt += 1

[原文 ↗](obsidian://open?vault=lc&file=questions%2F4038%20-%20Count%20Integers%20Appearing%20in%20a%20Single%20Block)
