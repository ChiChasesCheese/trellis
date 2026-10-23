---
id: hl-hc09-parallel-impls
node: problems.hc09-top-trades-by-notional
type: qa
step: 12
---
## Q
四种并行聚合实现（`parallel()` 流、ForkJoin、`StructuredTaskScope`、共享 `ConcurrentHashMap`）怎么写，各有什么 bug 要避免？

## A
**`parallel()` 流**：
```java
IntStream.range(0, n).parallel().collect(
    HashMap<String, Long>::new,                                              // supplier：每个线程新容器
    (m, i) -> m.merge(tickers[i], notionalAt(...), Math::addExact),          // accumulator
    (left, right) -> right.forEach((k, v) -> left.merge(k, v, Math::addExact)));  // combiner：并进第一个
```
契约：supplier 每次产生新的互不共享的容器；combiner 把第二个并进**第一个**。bug：combiner 写反（`BiConsumer` 无返回值，框架认为结果在第一个参数里，写反就丢了 left）；supplier 写成 `() -> sharedMap` 回到数据竞争。底层是 `ForkJoinPool.commonPool()`（JVM 共享）。

**ForkJoin**：`RecursiveTask`，`to - from <= threshold` 直接算；否则 `mid = (from + to) >>> 1`，`left.fork()`，`right.compute()`（自己算右半，不要 fork 两个再 join 两个），`left.join()`，`mergeInto(l, r)`。threshold 太小任务开销超过计算，太大并行度不够，经验任务总数约核数的 4–8 倍。`>>> 1` 防两个接近 int 上限的下标相加溢出（经典二分 bug）。

**`StructuredTaskScope.ShutdownOnFailure`** + 虚拟线程：每块一个子任务，`scope.join()` 等全部结束或一个失败，`scope.throwIfFailed(e -> e instanceof RuntimeException re ? re : new IllegalStateException(e))` 让运行时异常**原样**抛出；不调 `throwIfFailed` 失败会被悄悄忽略。`boundary(n, chunks, c) = (int)((long) n * c / chunks)`，`n*c` 要先转 `long`；块 `[boundary(c), boundary(c+1))` 首尾相接不重叠不遗漏。预览 API（需 `--enable-preview`）。

**共享 `ConcurrentHashMap`**（对照组）：`shared.merge(ticker, notional, Math::addExact)` 对单个 key 原子，函数抛异常时不记录映射；但热点 ticker（AAPL 占 30% 成交）上所有线程抢同一桶的锁，扩展性差。

**取消**：中断是协作式的，只设标志。`accumulate` 每 4096 个事件检查一次 `isInterrupted()`，被中断抛 `CancellationException`，否则其余块算完才返回，取消形同虚设。`ExecutorService + Future` 一个失败不取消其他，要手动 `cancel(true)` 并保证 `shutdown`。

C++：`jthread` + `stop_source`、`std::async`、手写分片；工作线程里异常逃出 = `std::terminate`，要 `catch (...)` 保存 `std::current_exception()`，join 后 `rethrow_exception`。
