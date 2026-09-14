---
id: leetcode-c-dfs-path-collection
node: design-simulation.dfs-path-collection
type: cloze
anki: 1787102263359
tags: [concept-cloze, leetcode, recall]
---
在DFS收集路径时，若用可变的list（path_stack）传递路径状态，必须在递归返回后显式{{c1::pop}}该元素以撤销修改；而用字符串拼接（如 path + '->'）传递时，因字符串不可变、每次拼接都生成新副本，所以{{c2::不需要回溯（backtrack）}}。

list是引用传递，多个递归分支会共享并累积同一个对象，忘记pop会导致所有路径都指向同一份被污染的list；字符串每次+操作产生新对象，天然隔离各分支。

**Evidence**

Python Tricks: 字符串path参数自动在每条分支创建新副本，避免回溯问题；list作参数时需要显式pop或创建副本，否则会串联

[原文 ↗](obsidian://open?vault=lc&file=concepts%2FDFS%20%E8%B7%AF%E5%BE%84%E6%94%B6%E9%9B%86)
