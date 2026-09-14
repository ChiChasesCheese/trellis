---
id: leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-template
node: bitwise-tricks.enumerate-nonempty-subsets-of-mask
type: cloze
anki: 1787272454480
tags: [concept-cloze, leetcode, recall, template]
---
枚举 s 的所有非空子集时，初始化 sub = s，每轮处理完 sub 后执行 sub = {{c1::(sub - 1) & s}} 得到下一个子集。

该写法常用于状压 DP 中「枚举子集转移」的场景。

**Evidence**

§4.2 枚举非空子集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.06%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E9%9D%9E%E7%A9%BA%E5%AD%90%E9%9B%86)
