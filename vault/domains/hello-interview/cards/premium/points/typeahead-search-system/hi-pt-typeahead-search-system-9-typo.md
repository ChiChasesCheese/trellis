---
id: hi-pt-typeahead-search-system-9-typo
node: qb.sd.typeahead-search-system.points
type: qa
step: 9
---
## Q
**搜索联想 · 拼写纠错**｜追问 · 出自：搜索联想 › 深入 5

用户拼错了前缀，精确前缀匹配没有结果。怎么处理，放在哪一步？

## A
**做法。** 先做精确前缀匹配；结果太少时再用编辑距离 1 的候选补充（如 BK 树或拼写归一化）。

**为什么放第二步。** 避免拖慢主路径；多数请求是正确拼写，只有少数走纠错。
