---
id: leetcode-c-endlesscheng-yfxfdf-q4-subset-enumeration-bitmask-hashmap-template
node: contest-misc.q4-subset-enumeration-bitmask-hashmap
type: cloze
anki: 1787272440008
tags: [concept-cloze, leetcode, recall, template]
---
encode_skills 函数把多个小整数拼接成一个哈希 key 的方式是：{{c1::用位移和按位或，将每个值左移固定位数后拼接}}。

bits_per_skill 需要覆盖单个取值的最大位宽，例如技能值 <2^10 时用 10 位

**Evidence**

Q4 提示 2、提示 3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.05%20-%20%E5%B0%8F%E9%9B%86%E5%90%88%E5%AD%90%E9%9B%86%E6%9E%9A%E4%B8%BE%20%2B%20%E4%BD%8D%E6%8E%A9%E7%A0%81%E5%93%88%E5%B8%8C%E8%AE%A1%E6%95%B0%E5%88%A4%E6%96%AD%E5%AD%90%E9%9B%86%E5%85%B3%E7%B3%BB)
