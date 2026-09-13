---
id: leetcode-c-endlesscheng-yfxfdf-q1-two-pointer-near-palindromic-deletion-template
node: strings.q1-two-pointer-near-palindromic-deletion
type: cloze
anki: 1787272438805
tags: [concept-cloze, leetcode, recall, template]
---
验证某个删除方案是否可行时，需要对剩余区间调用一个独立的 {{c1::双指针回文校验函数}}，而不是重新扫描整个数组。

is_palindrome_range(i, j) 是可复用的辅助函数

**Evidence**

Q1 贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.01%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E7%A1%AE%E5%AE%9A%E5%88%A0%E4%B8%80%E4%B8%AA%E5%85%83%E7%B4%A0%E5%90%8E%E8%83%BD%E5%90%A6%E5%9B%9E%E6%96%87)
