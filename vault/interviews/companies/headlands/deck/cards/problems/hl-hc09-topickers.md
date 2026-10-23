---
id: hl-hc09-topickers
node: problems.hc09-top-trades-by-notional
type: qa
step: 7
---
## Q
Part 2 按 ticker 聚合取 top-k 怎么做？`HashMap.merge`、`topOf`、Stream 版和 `teeing` 各是什么？

## A
**一趟扫描 + `HashMap.merge`**：
```java
var totals = new HashMap<String, Long>();
for (int i = 0; i < n; i++) totals.merge(tickers[i], notionalAt(i), Math::addExact);
```
`merge(key, value, f)`：key 不存在就放 value，存在就用 `f(旧值, value)` 替换；老写法 `get` 再 `put` 两次哈希查找还要手写 null 判断；对 `ConcurrentHashMap` 还是**原子**的。期望 O(n)。`Math::addExact` 保证「每个事件都不溢出但加起来溢出」也被发现。对每个 ticker 重扫整个数组是 O(n·m)，m=10⁵、n=10⁶ 就是 10¹¹。

**对 m 个不同 ticker 取 top-k**：(a) 全排序 O(m log m)；(b) 大小为 k 的最小堆 O(m log k)。m=10⁵、k=50：堆版约 41–58 ms，Stream 版约 82–103 ms。`topOf(Map<String,Long>, k)` 抽成独立方法，Part 4 合并后复用（不做 `long` 快速拒绝，`Map.Entry` 已是现成对象）。总额降序，相同按 ticker 升序；没出现过的 ticker 不存在，出现过但总额为 0 的存在（排最后）。

**Stream 版**：
```java
Collectors.groupingBy(i -> tickers[i], Collectors.reducing(0L, i -> notionalAt(i), Math::addExact))
// 然后 sorted().limit(k).toList()
```
比手写慢：`IntStream.boxed()` 装箱，`groupingBy` 有中间容器，整体排序 O(m log m)。

**`teeing`**（Java 12）：把同一个流同时喂给两个收集器，再用第三个参数合并结果，一趟遍历同时算总额和最大事件：
```java
Collectors.teeing(
    Collectors.reducing(0L, Trade::notional, Math::addExact),
    Collectors.minBy(BEST_FIRST),
    Summary::new)
```
得到 `Summary(grandTotal, Optional<Trade> largest)`。老写法要遍历两次或手写累加器类。两个收集器有顺序依赖就别用。
