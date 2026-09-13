---
id: leetcode-c-endlesscheng-yfxfdf-q1-two-pointer-near-palindromic-deletion-recognition
node: strings.q1-two-pointer-near-palindromic-deletion
type: cloze
anki: 1787272438605
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求“删除恰好一个元素后能否变成回文”时，应使用 {{c1::双指针从两端向中心匹配}}，一旦发现不对称立即分两种情况验证。

避免枚举所有删除位置，将复杂度从 O(n^2) 降到 O(n)

**Evidence**

Q1 贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.01%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E7%A1%AE%E5%AE%9A%E5%88%A0%E4%B8%80%E4%B8%AA%E5%85%83%E7%B4%A0%E5%90%8E%E8%83%BD%E5%90%A6%E5%9B%9E%E6%96%87)
