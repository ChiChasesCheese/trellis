---
id: hl-j09-first-last-old
node: java21.j09-sequenced-collections
type: qa
step: 1
---
## Q
Java 21 之前，`List`、`Deque`、`LinkedHashSet`、`LinkedHashMap`、`TreeMap` 各自怎么取"第一个"和"最后一个"？

## A
| | 第一个 | 最后一个 |
|---|---|---|
| `List` | `list.get(0)` | `list.get(list.size() - 1)` |
| `Deque` | `peekFirst()` / `getFirst()` | `peekLast()` / `getLast()` |
| `LinkedHashSet` / `LinkedHashMap` | `set.iterator().next()` / `map.entrySet().iterator().next()` | **没有办法，只能遍历到底，O(n)** |
| `TreeMap` | `firstEntry()` | `lastEntry()` |

这些集合都"有顺序"（有 encounter order，遇见顺序），但取法完全不统一。
