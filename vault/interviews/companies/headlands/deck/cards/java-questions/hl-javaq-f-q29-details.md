---
id: hl-javaq-f-q29-details
node: java-questions.f-concurrency
type: qa
step: 17
---
## Q
Java 8 对 `HashMap` 做了哪些改动？可变键有什么坑？为股票代码设计专用 map 该怎么做？遍历顺序有保证吗？
Is `HashMap` thread-safe? What's the iteration order of `HashMap`?

## A
- **Java 8 改动**：链表转红黑树（防碰撞攻击，最坏 O(log n) 而非 O(n)）；**尾插法**（Java 7 头插 + 并发扩容可能形成环 → 死循环）。
- **线程安全**：不是，并发 `merge` 会丢更新。
- **可变键**：放进去后改了参与 `hashCode` 的字段 → 找不到。键需要稳定的 `hashCode / equals`。
- **遍历顺序**：不保证；`LinkedHashMap` 保插入序。
- **股票代码专用 map**：键是固定长度字符串 → 打包成 `long`；开放寻址 + 线性探测 + `long[] keys / int[] vals`；容量 2 的幂；负载因子 ≤ 0.5；避免装箱和 `Node` 对象。
