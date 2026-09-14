---
id: leetcode-c-endlesscheng-yfxfdf-q2-small-constant-brute-force-template
node: backtracking-search.q2-small-constant-brute-force
type: cloze
anki: 1787272439106
tags: [concept-cloze, leetcode, recall, template]
---
best_candidate 模板中，核心循环只做两件事：调用 {{c1::evaluate 函数计算当前候选的值}}，然后与已知最优比较更新。

evaluate 是外部传入的问题相关逻辑，模板本身与具体问题解耦

**Evidence**

Q2 模拟

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.02%20-%20%E5%B8%B8%E6%95%B0%E8%A7%84%E6%A8%A1%E4%B8%8B%E6%9E%9A%E4%B8%BE%E5%8F%96%E6%9C%80%E4%BC%98%E7%9A%84%E6%9A%B4%E5%8A%9B%E7%AD%96%E7%95%A5)
