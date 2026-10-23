---
nodes: [os-network.jitter, os-network.interrupts, os-network.cpu-isolation, os-network.page-faults]
tags: [drill]
---
# 练习：p99.9 每隔 4 秒跳一次，按可能性列出原因

行情处理线程绑在隔离核上，每秒处理 100 万条消息，p50 是 3 µs，但 p99.9 每隔约 4 秒就跳到 2 ms 以上再回落。你在这个核上跑了一个空转计时器（hiccup meter，紧凑循环里反复读时钟，记录相邻两次读数之间的大间隔，不做任何业务）：每 4 ms 出现一个约 3 µs 的间隔，每 4 秒出现一个约 4 ms 的间隔。

**要你给出的**
- 算一算：一次多长的停顿，才会让 4 秒窗口里的 p99.9 被抬高。
- 按可能性从高到低列出至少 5 个嫌疑，每个写三样：为什么周期或量级对得上，一条验证的命令或证据，一条修复。
- 说明空转计时器的结果能排除什么、不能排除什么。
- 写出"修好了"的验收标准。

**评分要点**
- 为什么看尾部：均值和 p50 会把偶发尖刺平均掉，而竞争发生在行情最忙的关键时刻。4 秒里共 400 万条，p99.9 对应 4000 条；一次 4 ms 的停顿期间到达 1M × 0.004 = 4000 条，刚好占 0.1%，所以 4 ms 级的停顿就能把 p99.9 抬起来，50 µs 的停顿做不到 ([[hft-os-network-jitter-what-and-why-tail]], [[hft-measurement-distributions-mean-hides]])
- 空转计时器不碰内存、不做业务，所以任何明显的间隔都是线程被外部夺走了 CPU。每 4 ms 一个约 3 µs，对应 250 Hz 的调度器 tick，说明 `nohz_full` 没生效；每 4 秒一个 4 ms 另有来源；同时它排除了自己代码里的 GC、锁、缺页和缓存问题 ([[hft-os-network-jitter-hiccup-meter]])
- 嫌疑清单和量级：调度器 tick 几微秒；SMI 几十微秒到几毫秒；透明大页整理可达毫秒；内核后台线程几微秒到几百微秒；频率变化几十微秒 ([[hft-os-network-jitter-source-list]])
- SMI 由固件触发，操作系统无法屏蔽也看不见，所有核一起停；用 `hwlatdetect` 或 `turbostat` 发现，在 BIOS 里关掉不需要的特性 ([[hft-os-network-jitter-smi]])
- 中断：每秒读两次 `/proc/interrupts` 看交易核那一列是否增长，查 `irqbalance` 是否在运行；它会把网卡队列的中断挪到交易核上。修复是关掉 `irqbalance`、手动绑中断亲和性 ([[hft-os-network-interrupts-irqbalance-scenario]], [[hft-os-network-interrupts-irq-affinity]])
- 只绑核不够：别的线程仍可能被调度到这个核上，一次抢占几百微秒到几毫秒；`isolcpus`、`nohz_full`、`rcu_nocbs` 合起来才让核"安静"，并用 `ps -eLo psr,comm` 核对实际的线程分布 ([[hft-os-network-cpu-isolation-affinity-vs-isolation]], [[hft-os-network-cpu-isolation-boot-params]])
- 间隔固定的毛刺簇常对应某个后台任务（每秒刷盘、每 10 秒导出指标）：冷线程与热线程在同一物理核的两个超线程上，或共用 L3 和内存带宽。把延迟按时间画出来，对上周期就是它 ([[hft-architecture-hot-cold-path-cold-path-still-hurts]])
- 验收：交易核的中断计数在运行期间基本不再增长，空转计时器在隔离核上几乎没有大间隔；之后再查缺页等"自己代码"的来源，用 `perf stat` 看缺页计数在稳定交易期间不增长 ([[hft-os-network-page-faults-surprise-sources]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
