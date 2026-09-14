---
id: leetcode-c-endlesscheng-yfxfdf-q4-complement-counting-template
node: contest-misc.q4-complement-counting
type: cloze
anki: 1787272439705
tags: [concept-cloze, leetcode, recall, template]
---
count_valid_pairs 函数中，答案的计算方式是 {{c1::总组合数 C(n,2) 减去 count_violating 的返回值}}。

count_violating 的具体实现依赖问题本身（如子集哈希计数）

**Evidence**

Q4 提示 1

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.04%20-%20%E9%80%86%E5%90%91%E8%AE%A1%E6%95%B0%EF%BC%9A%E7%BB%9F%E8%AE%A1%E4%B8%8D%E6%BB%A1%E8%B6%B3%E6%9D%A1%E4%BB%B6%E7%9A%84%E6%95%B0%E9%87%8F%E5%86%8D%E7%94%A8%E6%80%BB%E6%95%B0%E7%9B%B8%E5%87%8F)
