---
id: hl-cx-amortized-spike
node: foundations.complexity
type: qa
step: 27
---
## Q
摊还 O(1) 为什么不等于每次都快？低延迟系统里怎么避免动态数组扩容的毛刺（spike）？

## A
摊还只保证**平均**。扩容那一次仍要抄 n 个元素（n = 一千万时几十毫秒），还要分配大块新内存、产生待回收的垃圾，这是低延迟系统不可接受的毛刺。

解法是**预分配**：
```java
List<Long> prices = new ArrayList<>(1_000_000);
long[] priceRing = new long[1 << 20];
```
知道大概规模就一次性开够，之后不再扩容；更低延迟的做法是根本不用 `ArrayList<Long>`（每个 `Long` 都是一次分配），而是启动时开好原始类型数组，用容量固定的 `long[]` 环形缓冲。
