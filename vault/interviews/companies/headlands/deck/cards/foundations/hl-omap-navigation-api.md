---
id: hl-omap-navigation-api
node: foundations.ordered-maps-trees
type: qa
step: 21
---
## Q
`asks = {101=50, 103=20, 105=70, 110=10}` 上，`floorKey(104)`、`lowerKey(103)`、`ceilingKey(104)`、`higherKey(105)`、`floorKey(100)` 各返回什么？floor / ceiling / lower / higher 的语义口诀是什么？

## A
- `floorKey(104)` = **103**（≤ 104 的最大 key）；
- `lowerKey(103)` = **101**（< 103 的最大 key）；
- `ceilingKey(104)` = **105**（≥ 104 的最小 key）；
- `higherKey(105)` = **110**（> 105 的最小 key）；
- `floorKey(100)` = `null`（没有 ≤ 100 的 key）。

口诀：**floor / ceiling 含相等，lower / higher 不含相等**。每个 `xxxKey` 都有 `xxxEntry` 版本，同时返回 key 和 value，省一次 `get`。
