---
id: leetcode-c-endlesscheng-caoj45-enumerate-supersets-of-mask-template
node: bitwise-tricks.enumerate-supersets-of-mask
type: cloze
anki: 1787272455081
tags: [concept-cloze, leetcode, recall, template]
---
枚举 t 的所有超集的循环写法是：初始化 s = t，循环条件为 s < {{c1::(1 << n)}}，每轮更新 s = {{c2::(s + 1) | t}}。

循环自然终止于超出全集范围时。

**Evidence**

§4.4 枚举超集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.08%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E8%B6%85%E9%9B%86)
