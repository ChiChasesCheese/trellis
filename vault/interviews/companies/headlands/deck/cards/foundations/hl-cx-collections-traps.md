---
id: hl-cx-collections-traps
node: foundations.complexity
type: qa
step: 12
---
## Q
Java 集合里哪些操作看着便宜、实际是 O(n)？

## A
- `ArrayList.add(0, x)` / `remove(0)`：**O(n)**，要把后面的元素整体挪动。
- `ArrayList.contains(x)` / `indexOf(x)`：**O(n)**，逐个调用 `equals`。
- `PriorityQueue.remove(Object)` / `contains`：**O(n)**，要先线性找到元素。
- `LinkedList.get(i)`：**O(n)**，要顺着指针走。

这些操作放进循环里，就成了隐藏的 O(n²)。需要频繁头部插入时用 `ArrayDeque`，需要快速判断存在时用 `HashSet`。
