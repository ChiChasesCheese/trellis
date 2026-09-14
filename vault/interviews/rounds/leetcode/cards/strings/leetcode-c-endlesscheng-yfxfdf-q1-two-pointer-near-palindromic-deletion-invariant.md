---
id: leetcode-c-endlesscheng-yfxfdf-q1-two-pointer-near-palindromic-deletion-invariant
node: strings.q1-two-pointer-near-palindromic-deletion
type: cloze
anki: 1787272438707
tags: [concept-cloze, invariant, leetcode, recall]
---
双指针第一次遇到不匹配的位置 i、j 时，可行的删除方案只能是 {{c1::删 a[i] 或删 a[j]}}，因为在此之前的部分已经对称。

利用了“越靠近中心的删除点越可能使内部子串回文”这一贪心直觉

**Evidence**

Q1 贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.01%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E7%A1%AE%E5%AE%9A%E5%88%A0%E4%B8%80%E4%B8%AA%E5%85%83%E7%B4%A0%E5%90%8E%E8%83%BD%E5%90%A6%E5%9B%9E%E6%96%87)
