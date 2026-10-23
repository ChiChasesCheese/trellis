---
id: hl-c05-map-vs-unordered
node: cpp-lessons.c05-stl-containers
type: qa
step: 18
---
## Q
面试问：`map` 和 `unordered_map` 怎么选？
Interview question: When should you choose `map` over `unordered_map`?

## A
- 要**有序遍历**、范围查询、`lower_bound`、取最小/最大 → `map`（O(log n)）。
- 只要**点查** → `unordered_map`（平均 O(1)）。
- 元素很少时，**排好序的 `vector` + 二分**往往最快（连续内存）。
- `unordered_map` 遍历顺序不确定，别依赖。
