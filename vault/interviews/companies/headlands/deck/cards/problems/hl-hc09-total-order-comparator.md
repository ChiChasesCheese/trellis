---
id: hl-hc09-total-order-comparator
node: problems.hc09-top-trades-by-notional
type: qa
step: 3
---
## Q
top-k 的 `Comparator` 为什么必须是全序（total order）？`BEST_FIRST` 的三级规则是什么，`reversed()` 放哪里？

## A
只写「notional 大的在前」时，notional 相同的事件谁在前**未定义**（取决于堆内部实现和输入顺序）：`topEvents(k=4)` 的第 4 名可能是下标 1 或 4，写不出稳定期望；并行后平局随线程调度而变——不可复现的 bug 最难查。所以写成**全序**：任意两个不同事件比较结果必不是 0。

```java
Comparator<Trade> BEST_FIRST =
    Comparator.comparingLong(Trade::notional).reversed()   // 1. notional 降序
              .thenComparing(Trade::ticker)                // 2. ticker 升序（String.compareTo）
              .thenComparingInt(Trade::index);             // 3. 下标升序
```
下标全局唯一，所以第 3 条一定能分出胜负，比较器永不返回 0，结果唯一。去掉第三级，「notional 与 ticker 都相同」的事件（样例下标 1 与 4）顺序就由堆内部实现决定，结果随 JDK 版本、输入顺序而不稳定。

`reversed()` 反转它**前面**的整条链：`comparingLong(A).thenComparing(B).reversed()` 会把 B 也反转，所以 `reversed()` 要紧跟第一个条件。不用 `reversed()` 的写法：`(a, b) -> { int c = Long.compare(b.notional(), a.notional()); return c != 0 ? c : a.ticker().compareTo(b.ticker()); }`，用 `Long.compare` 而不是 `b - a`（极端值溢出）。

堆比较器取 `BEST_FIRST.reversed()`：`PriorityQueue` 把「最小」放堆顶，反过来后「最小」= 「最差」，堆顶是守门员。

C++ 字符串比较的是字节（unsigned char）字典序，Java 是 UTF-16 码元。
