---
id: hl-j16-orderbook-threading
node: java21.j16-concurrency-primitives
type: qa
step: 40
---
## Q
面试官问：「多线程共享这个订单簿怎么办？」订单簿当前用 `TreeMap`，怎么回答？
(How would you share the order book across threads?)

## A
当前设计是**单线程撮合**（Disruptor 式）：一个线程独占订单簿，别的线程通过队列投递命令，所以用普通 `TreeMap`（`SequencedMap<Long, PriceLevel> bids = new TreeMap<>(Comparator.reverseOrder())`）。

回答骨架：
1. 先说「**单写线程 + 队列**」，避免共享可变状态；
2. 必须共享就换 `ConcurrentSkipListMap`；
3. 但 `PriceLevel` 里 FIFO 和 `total` 的**复合更新**还需要锁或不可变替换，跳表只保证单个 Map 操作的原子性。
