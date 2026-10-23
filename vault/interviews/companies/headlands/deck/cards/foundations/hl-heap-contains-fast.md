---
id: hl-heap-contains-fast
node: foundations.heap-priority-queue
type: qa
step: 39
---
## Q
堆里有一百万个元素，想判断某个值 x 是否在堆中，能比 O(n) 更好吗？

## A
仅靠堆不行：堆只保证父子有序，没有兄弟间信息，无法剪枝。

两种办法：多维护一个 `HashSet`（或 `HashMap<id, count>`）与堆同步，查询 O(1)；或者换成 `TreeSet` / `TreeMap`。
