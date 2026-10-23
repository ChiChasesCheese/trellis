---
id: hl-omap-headmap-tailmap
node: foundations.ordered-maps-trees
type: qa
step: 23
---
## Q
在 `{101=50, 103=20, 105=70, 110=10}` 上，`headMap(105)`、`headMap(105, true)`、`tailMap(105)`、`subMap(103, 110)` 各是什么？边界规则是什么？

## A
- `headMap(105)` = `{101=50, 103=20}`（key < 105，**不含**边界）；
- `headMap(105, true)` = `{101=50, 103=20, 105=70}`（≤ 105）；
- `tailMap(105)` = `{105=70, 110=10}`（key ≥ 105，**含**边界）；
- `subMap(103, 110)` = `{103=20, 105=70}`（`[from, to)`）。

口诀：`headMap` 默认不含边界，`tailMap` 默认含边界，「一头一尾不对称」是最常见的 off-by-one。`descendingMap()` 返回反向视图。
