---
id: hl-omap-qa-rb-vs-skip
node: foundations.ordered-maps-trees
type: qa
step: 36
---
## Q
面试题：红黑树和跳表，你选哪个？

## A
推荐答法：
- 单线程要最坏保证用红黑树，即 `TreeMap`；
- 多线程并发读写同一个有序结构用跳表，因为插入只改局部指针，容易做成无锁；JDK 里有现成的 `ConcurrentSkipListMap`；
- 代价：跳表是概率结构，最坏 O(n) 概率极小，单线程也更慢（put 390 ns 对 230 ns）。
