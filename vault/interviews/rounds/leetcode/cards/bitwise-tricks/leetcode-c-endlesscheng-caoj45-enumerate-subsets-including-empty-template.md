---
id: leetcode-c-endlesscheng-caoj45-enumerate-subsets-including-empty-template
node: bitwise-tricks.enumerate-subsets-including-empty
type: cloze
anki: 1787272454779
tags: [concept-cloze, leetcode, recall, template]
---
枚举 s 的所有子集（含空集）时循环写成 while True，每次处理完 sub 后检查 {{c1::if sub == 0: break}}，否则继续计算 sub = (sub - 1) & s。

这一步判断是区分「含空集」与「不含空集」两种模板的关键。

**Evidence**

§4.3 枚举子集（包含空集）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.07%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E6%89%80%E6%9C%89%E5%AD%90%E9%9B%86%EF%BC%88%E5%90%AB%E7%A9%BA%E9%9B%86%EF%BC%89)
