---
id: hl-omap-entry-snapshot
node: foundations.ordered-maps-trees
type: qa
step: 25
---
## Q
`TreeMap.firstEntry().setValue(0)` 能把最优价位的数量改成 0 吗？

## A
不能，抛 `UnsupportedOperationException`。`ceilingEntry`、`firstEntry`、`floorEntry` 等返回的 `Map.Entry` 是**调用时刻的快照**，不支持通过 `setValue` 修改底层 Map。

改值用 `map.put(key, newValue)`，或用 `pollFirstEntry()` 删除整个价位。
