---
id: leetcode-q-shortest-and-lexicographically-smallest-beautiful-string-pattern
node: two-pointers-window.sliding-window
type: qa
anki: 1787776731028
tags: [lc::2904, leetcode, pattern, recall]
---
## Q
给定二进制字符串 s 和整数 k，要求找出恰好包含 k 个 '1' 的最短且字典序最小的子串（beautiful substring），如何避免暴力枚举所有子串？

## A
先收集所有 '1' 字符的下标 indices。答案子串必然是从某个 '1' 到另一个 '1'（含首尾），因为收缩掉两端多余的 '0' 只会更短或字典序更小。于是只需枚举长度为 k 的连续下标窗口 [i, i+k-1]，候选子串为 s[indices[i] : indices[i+k-1]+1]，共 m-k+1 个候选（m 为 '1' 的总数），再用 min(candidates, key=(len, str)) 取最短且字典序最小的。这样把 O(n^2) 暴力枚举优化为 O(m) 级别的候选生成。

**Evidence**

indices = [idx for idx in range(n) if s[idx] == '1']; 遍历 i in range(m-k+1)，候选 s[indices[i]: indices[i+k-1]+1]，用 min(candidates(), key=lambda x: (len(x), x)) 取结果，对比另一版本 shortestBeautifulSubstring0 中对所有长度 size 和起点 i 做双重循环加 count('1')==k 判断的暴力做法。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2904%20-%20Shortest%20and%20Lexicographically%20Smallest%20Beautiful%20String)
