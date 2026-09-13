---
id: leetcode-q-majority-element-pattern
node: arrays-hash-prefix.boyer-moore-majority-vote-algorithm
type: qa
anki: 1787776730578
tags: [lc::169, leetcode, pattern, recall]
---
## Q
求数组中出现次数超过 n/2 的多数元素，如何在 O(n) 时间、O(1) 空间内解决？

## A
使用 Boyer-Moore 投票法：维护候选值 cand 和计数器 cnt（初始为 0）。遍历数组，若当前元素等于 cand 则 cnt+1，否则 cnt-1；当 cnt < 0 时，将候选值换成当前元素并把 cnt 重置为 0。遍历结束后 cand 即为多数元素。

```
def majorityElement(self, nums):
    cand = cnt = 0
    for num in nums:
        cnt += 1 if num == cand else -1
        if cnt < 0:
            cand, cnt = num, 0
    return cand
```

**Evidence**

笔记标注该解法为“面试标准答案”，代码：cand = cnt = 0; for num in nums: cnt += 1 if num == cand else -1; if cnt < 0: cand, cnt = num, 0; return cand

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F169%20-%20Majority%20Element)
