---
nodes: [machine.false-sharing, machine.coherence, machine.cache-lines]
tags: [drill]
---
# 练习：两个互不相干的线程，为什么互相拖慢

两个线程各对自己的计数器自增 5000 万次，两个计数器是相邻的两个 `long`。一次实测：相邻放着约 613 ms，用 `alignas(64)` 隔开到不同缓存行后约 69 ms。同一台机器上，另有 8 个线程对同一个共享计数器做原子加一，吞吐并没有随线程数上升。

**要你给出的**
- 先预测慢多少倍，再逐步写出硬件上发生了什么（缓存行在两个核之间的状态变化），说明为什么代码里看不出任何共享。
- 粗算 8 线程共享计数器的吞吐上限（缓存行在核之间转移一次约 50 ns），给出两种改法，并说清各自适合什么场景、有什么代价。
- 写出 Java 里手工加了填充字段却仍然没好的 3 种原因，以及怎样确认问题真的消失。
- 把"单写者原则"套到 SPSC 队列的 `head` 和 `tail` 上，讲给同事听。

**评分要点**
- 缓存一致性以整条缓存行（通常 64 字节，Apple M 系列是 128 字节）为单位，不是以变量为单位；写之前必须先独占这一行，别的核的副本被标成作废，下次读要从写的核把最新内容搬过来 ([[hft-machine-coherence-mesi-mechanism]], [[hft-machine-cache-lines-what-a-line-is]])
- 伪共享：A 写 `x`、B 写 `y` 同在一行，这一行在两个核之间来回弹跳，每次约几十 ns；"不同变量"不等于"不同缓存行" ([[hft-machine-false-sharing-mechanism]])
- 倍数：613 ÷ 69 ≈ 9 倍；一般在 3 倍到十几倍；原子读改写最敏感，普通 `volatile` 写次之，只读几乎无影响；先用 `perf c2c` 确认再动手 ([[hft-machine-false-sharing-magnitude]], [[hft-cpp-spsc-seqlock-cache-line-padding]])
- 共享计数器：缓存行转移约 50 ns，上限约 1 ÷ 50 ns = 2000 万次每秒，线程再多也不变，还会更慢；改成每个线程一份再汇总（`LongAdder`），槽位之间仍要用填充隔开 ([[hft-machine-coherence-shared-counter-bottleneck]])
- 填充适合变量个数固定、各线程写各自位置（如 Disruptor 的序号），代价是浪费内存；分片适合写很多、读总数很少的统计量，代价是读总数要遍历且只是近似快照；能不共享就不共享 ([[hft-machine-false-sharing-padding-vs-sharding]])
- 填充无效的三个坑：JVM 会重排字段（用继承或 `@Contended`，用 `jol` 打印布局验证）；缓存行不是 64 字节；只填了一侧，前后相邻对象的字段仍可能同行；最后用 `perf c2c` 或前后计时对比确认 ([[hft-machine-false-sharing-padding-pitfalls]])
- 单写者：每个可变变量只有一个线程写，缓存行留在写者核里；SPSC 里生产者独占写 `tail`、消费者独占写 `head`，不用 CAS，也没有写竞争 ([[hft-machine-coherence-single-writer]])
- 核间交接的下限就是一次缓存行搬运，约几十 ns，线程间每多一次交接就加一次；3 次交接约 0.3 µs，占 10 µs 预算的 3% ([[hft-machine-coherence-cross-core-cost]], [[hft-architecture-threading-handoff-cost]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
