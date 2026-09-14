---
id: leetcode-c-endlesscheng-0vinmk-grouping-loop-recognition
node: arrays-hash-prefix.grouping-loop
type: cloze
anki: 1787268629137
tags: [concept-cloze, leetcode, recall, recognition]
---
当数组按规则被分割成若干组,且每组处理逻辑相同时,应使用{{c1::分组循环}},避免对最后一组做特判。

当数组按规则被分割成若干组、且每组的判断/处理逻辑相同时,用外层循环负责记录组的起点并在组结束后更新答案,内层循环负责把当前组走到底,从而不需要对最后一组做特判。

**Evidence**

六、分组循环

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.11%20-%20%E5%88%86%E7%BB%84%E5%BE%AA%E7%8E%AF)
