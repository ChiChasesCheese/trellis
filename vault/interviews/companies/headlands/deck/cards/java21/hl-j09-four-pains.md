---
id: hl-j09-four-pains
node: java21.j09-sequenced-collections
type: qa
step: 3
---
## Q
Java 8 里处理"有顺序的集合"的两端有哪四个痛点？

## A
1. **名字不统一**：同一概念在 `List` 叫 `get(0)`，`Deque` 叫 `peekFirst()` / `getFirst()`，`TreeMap` 叫 `firstEntry()`，写泛型代码没法用同一方法。
2. **有些结构没有 O(1) 写法**：`LinkedHashSet` / `LinkedHashMap` 内部明明维护双向链表，最后一个就在链表尾，API 却不给，只能遍历全表。
3. **`list.get(list.size() - 1)` 易写错**，空列表时抛含糊的 `IndexOutOfBoundsException: Index -1`。
4. **没有统一类型**：写"接受任何有顺序集合并返回最后一个"的方法，`Collection` 太宽（`HashSet` 也是），`List` 太窄（排除 `Deque` 和 `LinkedHashSet`）。
