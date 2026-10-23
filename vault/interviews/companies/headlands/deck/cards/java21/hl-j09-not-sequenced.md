---
id: hl-j09-not-sequenced
node: java21.j09-sequenced-collections
type: qa
step: 5
---
## Q
哪些常见集合**不是** Sequenced？`SequencedMap<String,Integer> m = new HashMap<>();` 会怎样？

## A
不是 Sequenced 的：
- `HashSet`、`HashMap`（无序）；
- `PriorityQueue`（遍历顺序不是优先级顺序，而是堆数组层序）；
- `Set.of(...)`、`Map.of(...)`（顺序故意不固定）。

`SequencedMap<String,Integer> m = new HashMap<>();` 是**编译错误**。

`PriorityQueue` 要最小的元素用 `peek()` / `poll()`，它没有 `getFirst`。
