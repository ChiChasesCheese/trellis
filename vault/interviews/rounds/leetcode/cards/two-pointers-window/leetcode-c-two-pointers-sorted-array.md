---
id: leetcode-c-two-pointers-sorted-array
node: two-pointers-window.two-pointers-sorted-array
type: cloze
anki: 1787102263809
tags: [concept-cloze, leetcode, recall]
---
在排序数组上做 Two Pointers 时，循环条件应为 {{c1::l < r}}（严格小于），且每次跳过重复元素的检查应该在 {{c2::移动指针之后}}立即进行，以避免产生重复的结果组合。

l 和 r 永远不能指向同一个元素；若用 l <= r 会导致重复计算同一元素与自身配对。跳过重复元素必须在移动后立即做（如 while l < r and nums[l]==nums[l+1]: l+=1），否则会漏跳或重复统计相同的三元组/二元组。

**Evidence**

Invariants: l和r永远不会指向同一个元素（l < r严格）；每次移动l或r，搜索空间严格缩小。Python Tricks: 跳过重复元素：while l < r and nums[l]==nums[l+1]: l+=1（在移动后立即做）。Pitfalls: 忘记处理重复元素导致重复答案。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E6%9C%89%E5%BA%8F%E6%95%B0%E7%BB%84%E5%8F%8C%E6%8C%87%E9%92%88)
