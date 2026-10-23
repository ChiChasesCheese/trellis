---
id: hl-cx-qa-hashmap-treemap
node: foundations.complexity
type: qa
step: 44
---
## Q
追问：O(1) 的 `HashMap` 一定比 O(log n) 的 `TreeMap` 快吗？怎么选？

## A
推荐答法：「渐近上是；实际看常数。100 万随机 key，`HashMap.put` 60 ns，`TreeMap.put` 239 ns，约 4 倍；而且 `TreeMap` 能做范围查询和有序遍历，`HashMap` 不能。」

选哪个取决于**是否需要有序**：只做点查用 `HashMap`；需要 `floorKey`、范围、有序遍历用 `TreeMap`。
