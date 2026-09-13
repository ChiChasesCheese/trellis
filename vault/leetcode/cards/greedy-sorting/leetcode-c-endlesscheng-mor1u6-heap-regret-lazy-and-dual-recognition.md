---
id: leetcode-c-endlesscheng-mor1u6-heap-regret-lazy-and-dual-recognition
node: greedy-sorting.heap-regret-lazy-and-dual
type: cloze
anki: 1789002114120
tags: [concept-cloze, leetcode, recall, recognition]
---
贪心过程中允许用更好选择替换旧选择时，用 {{c1::反悔堆}}。

反悔贪心用堆替换先前较差选择；懒删除把任意删除延迟到堆顶；对顶堆把数据分为低半与高半以维护中位数或动态排名。

**Evidence**

§5.5 反悔堆

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.10%20-%20%E5%8F%8D%E6%82%94%E5%A0%86%E3%80%81%E6%87%92%E5%88%A0%E9%99%A4%E5%A0%86%E4%B8%8E%E5%AF%B9%E9%A1%B6%E5%A0%86)
