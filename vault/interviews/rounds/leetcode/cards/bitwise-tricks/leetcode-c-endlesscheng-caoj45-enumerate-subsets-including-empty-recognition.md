---
id: leetcode-c-endlesscheng-caoj45-enumerate-subsets-including-empty-recognition
node: bitwise-tricks.enumerate-subsets-including-empty
type: cloze
anki: 1787272454580
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求枚举集合 s 的所有子集且明确包含空集时，应在非空子集枚举模板基础上，把空集判断放在处理逻辑{{c1::之后}}再决定是否退出循环。

这是对 enumerate-nonempty-subsets-of-mask 模板的一个小改动。

**Evidence**

§4.3 枚举子集（包含空集）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.07%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E6%89%80%E6%9C%89%E5%AD%90%E9%9B%86%EF%BC%88%E5%90%AB%E7%A9%BA%E9%9B%86%EF%BC%89)
