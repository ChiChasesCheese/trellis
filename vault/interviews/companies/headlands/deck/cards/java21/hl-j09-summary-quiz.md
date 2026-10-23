---
id: hl-j09-summary-quiz
node: java21.j09-sequenced-collections
type: qa
step: 34
---
## Q
面试追问：Java 21 的 Sequenced Collections 解决了什么问题？它改了语法或 JVM 吗？列出三个最值得记的事实。

## A
解决：给"有顺序"的集合（`List`、`Deque`、`LinkedHashSet/Map`、`TreeSet/Map`）一套**统一**的两端操作和倒序视图，取代各集合五花八门的写法。**没有新语法，编译器和 JVM 也没改**，纯库改动。

三个事实：
1. `getFirst()` / `getLast()` 空集合抛 `NoSuchElementException`，而 `SequencedMap.firstEntry()` 空时返回 `null`；
2. `reversed()` 是 O(1) 的**视图**，读写穿透原集合；
3. `ArrayList.removeFirst()` / `addFirst()` 是 O(n)，做队列用 `ArrayDeque`。
