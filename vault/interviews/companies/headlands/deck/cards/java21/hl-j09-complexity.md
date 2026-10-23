---
id: hl-j09-complexity
node: java21.j09-sequenced-collections
type: qa
step: 19
---
## Q
`ArrayList`、`ArrayDeque`、`LinkedHashSet/Map`、`TreeSet/Map` 的 `getFirst`、`addFirst` / `removeFirst`、`addLast` / `removeLast`、`reversed()` 创建的复杂度分别是多少？

## A
| 操作 | `ArrayList` | `ArrayDeque` / `LinkedList` | `LinkedHash*` | `Tree*` |
|---|---|---|---|---|
| `getFirst` / `getLast` | O(1) | O(1) | O(1) | O(log n)（沿红黑树走到底） |
| `addLast` / `removeLast` | 摊还 O(1) | O(1) | O(1) | 不支持添加；`pollLastEntry` O(log n) |
| `addFirst` / `removeFirst` | **O(n)**（要挪动所有元素） | O(1) | O(1) | 不支持添加；`pollFirstEntry` O(log n) |
| `reversed()` 创建 | O(1) | O(1) | O(1) | O(1) |
