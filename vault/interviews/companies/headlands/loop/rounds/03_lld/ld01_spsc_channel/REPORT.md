# ld01 · REPORT

## 概要

「两进程间有界共享内存消息通道」出自 FastPrep 的 Low-level design 题（2023-08-24），1p3a 同日帖摘要含 "shared memory"。Java 对应：内存映射文件 + 环形缓冲区 + 内存序。
面试官想看：(1) 单写者原则——每个共享变量只有一个写者时 release/acquire 就够，不需要 CAS；(2) 环形缓冲区的细节（自由增长的计数、2 的幂掩码、满 / 空判定）；(3) 变长消息回绕时的活性问题（PAD 必须单独发布）；(4) 知道缓存行 / 伪共享 / cached index，并且会测量；(5) 怎么测试跨进程代码。
讲义：`study/30-articles/ld01_spsc_channel.md`。

## 来源与置信度

置信度 中（FastPrep 1 + 1p3a 1011799 1，按日期 + 主题合并；都只有标题 / 摘要）。FastPrep 原文："bounded shared-memory message channel between two processes, with safe record ownership, FIFO delivery and explicit full, empty and drained…"。
(reconstructed)：四个 Part 的划分、头部布局（magic / capacity / version / head@128 / tail@256 / closed@264 / 数据@512）、记录格式（int32 长度前缀 + 8 字节对齐 + PAD = -1）、PAD 单独发布规则、drained 协议、跨进程测试方法。能确定的是：两进程、有界、共享内存、FIFO、记录所有权安全、full / empty / drained 显式。

## 逐 Part 思路

1. LongRing：head / tail 是只增不减的 long 计数，空 ⇔ tail-head==0，满 ⇔ ==capacity，下标 = 计数 & mask（容量 2 的幂）。poll 空抛 NoSuchElementException（long 没有哨兵值）。
2. SpscLongRing：tail 只有生产者写、head 只有消费者写；`TAIL.setRelease` 发布数据，`getAcquire` 读对方下标；cachedHead / cachedTail 只在"旧值看起来满 / 空"时刷新（下标单调，旧值只会低估对方进度，所以安全）；继承链 `RingBase → PadA → ProducerFields → PadB → ConsumerFields → PadC` 把生产者字段与消费者字段推开 128 字节，只读的 buf / mask 放在最前面的基类。
3. MessageRing：字节环；记录 `[len:int32][payload][补零到 8 字节]`；放不下连续的一整条时先写 PAD（len=-1）占满到末尾——PAD 单独发布，否则空环 + tail 靠近末尾 + 大消息会死锁。finish() 置 closed；isDrained() 先读 closed 再读 tail。init 最后用 release 写 magic，attach 校验 magic / version / 尺寸。VarHandle 用 `MethodHandles.memorySegmentViewVarHandle(JAVA_LONG)`（JDK 21 坐标 = 段 + 字节偏移）。
4. SharedChannel：`FileChannel.map(READ_WRITE, 0, size, Arena.ofShared())` 得到 MemorySegment，套 MessageRing。create 先校验容量再动文件；open 校验文件。跨进程测试：子进程 `SpscChild`，消息由序号确定性生成（Msgs.make），每端自旋带截止时间，父进程 waitFor 超时后 destroyForcibly。

## 隐藏测试会打的坑

* `head == tail` 当作空（取模存下标时也可能是满）；用 `%` 而不是掩码；容量不是 2 的幂不报错。
* 弱内存序机器（Apple M / ARM）上把 setRelease 写成普通写：消费者读到上一圈的旧值（实测大面积红）；x86 上常碰巧对。
* 把 PAD + 记录当整体判断 → 死锁；PAD 发布了但真记录没挤进去时 offer 返回 false；消费者必须越过 PAD（poll 返回 null）后才放得进。
* 先读 tail 再读 closed → 漏掉最后几条；末尾残留 PAD 时 isDrained 要等 poll 越过才为 true。
* 子进程只传 java.class.path → 找不到被测类（JUnit console --class-path 时只有 junit jar）；用 Thread.sleep 对时序；一端出错另一端空转永不退出。
* 堆 byte[] 段上做 long 的原子访问 → Misaligned access；create 非法容量时先截断了已有文件。

## 复杂度 + 实测时间

offer / poll 均 O(1)（变长消息再加 O(消息长度) 的拷贝）；空间 capacity 字节（+512 字节头）。
本机（Apple M 系列，12 核，JDK 21.0.12）：全套 155 个测试约 1.4 s；SpscLongRing 两线程 1000 万条 long 184 ms（≈5500 万条/秒）；MessageRing 两线程 200 万条变长消息 87 ms；跨进程三个用例 171 / 151 / 34 ms；500 万条变长消息（≈160 MB）跨进程约 190 ms（≈2600 万条/秒，含子 JVM 启动）。
伪共享单独量（FalseSharingBench，每线程 2 亿次自增）：相邻 1606 / 1757 ms（中位数，两次运行）对相隔 820 / 917 ms，约 2 倍；相邻那一行呈双峰（~820 与 ~1800，取决于两线程是否在同一核心簇）。
SPSC 五种写法（SpscBench，6 次运行中位数，M 条/秒）：volatile 38、acq/rel 34、acq/rel+填充 27.5、acq/rel+cache 34、acq/rel+cache+填充 44；范围 27–49，大面积重叠——M 系列有 P/E 核且 macOS 不能绑核，噪声很大，不要对这台机器上的吞吐差异下结论。

## 测试清单（脚本数）

共 155 个测试，0 失败：part1 19、part2 82、part3 46、part4 8；edge 54、perf 5、conc 85、io 3。
LongQueueContract（抽象基类，由 LongRingTest 标 part1 与 SpscLongRingSequentialTest 标 part2 各跑一遍：FIFO、满 / 空规则、空 poll 抛异常、容量 1、所有 long 值合法、百万次后计数仍对、非 2 的幂容量、对照 ArrayDeque、perf）；SpscLongRingTest（@RepeatedTest(20) × 3 的有序恰好一次传输、容量 1、不读到旧槽位、size 任何线程在界内、1000 万条 perf）；MessageRingTest（init / attach、垃圾 / 太小 segment、坏容量、记录对齐与满规则、maxPayload、回绕、PAD 单独发布、空环任意位置放得下最大消息、随机对照、finish / drained、末尾 PAD、20 轮双线程传输、两个 perf）；SharedChannelTest（同 JVM 两个映射共享数据、满后恢复、关闭重开后积压仍在、非法文件、非法容量不动文件、close 幂等、三个跨进程用例）。
变异检查：把 setRelease 换成普通写 → SpscLongRingTest 的有序传输与旧槽位用例大面积红（first mismatch 出现在第 369–154157 条之间）。

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J16 VarHandle | SpscLongRing 的 HEAD / TAIL（普通字段 + setRelease / getAcquire）；MessageRing 的 memorySegmentViewVarHandle | 按需选访问强度，不必全 volatile；字段布局自己控制（填充才有意义） |
| J17 FFM | MessageRing 建在 MemorySegment 上；SharedChannel 用 `FileChannel.map(mode, off, size, Arena)` | long 大小、Arena.close() 确定性取消映射；MappedByteBuffer 是 int 索引且无法确定性 unmap |
| J15 Math.clamp | SpscLongRing.size()、MessageRing.bytesPending() | 一个方法代替 `Math.max(0, Math.min(x, cap))` |
| J18 接口 default 方法 | LongQueue.isFull()（SpscLongRing 覆盖它） | 实现类的继承链已被填充用掉，公共行为只能放接口 |
| J05 switch 表达式 | SpscChild.main：`String err = switch (mode) {…}` | 每个分支产生值，无 fall through |
| J08 var | 测试里的 `var ring = MessageRing.init(…)`、`var producer = new Thread(…)` | 右边已写类型时不重复 |

## 面试官可能的追问

1. 为什么 head / tail 自由增长？答：下标存取模值时 head==tail 空 / 满不可分，补救（空一格 / 另存 size）各有代价；自由增长的计数让空和满是两个不同的差值，不浪费槽位；long 溢出要几十万年。
2. 为什么 SPSC 不需要 CAS？答：每个共享变量只有一个写者，没有读-改-写竞争；只需要可见性和顺序，release/acquire 足够。多生产者才需要 CAS（Disruptor 的 next()/publish()，Aeron 的 tryClaim/commit），或每个生产者一个环。
3. release/acquire 具体保护什么？去掉会怎样？答：生产者 setRelease(tail) 保证数据先于 tail 可见，消费者 getAcquire(tail) 保证读数据晚于读 tail；head 方向保证读完才归还槽位。去掉后在 ARM 上消费者读到旧值（本机实测大面积红），x86 常碰巧对。
4. 什么是伪共享，怎么证明？答：两个线程写同一缓存行里的不同变量，行在核心间来回失效；证明要单变量实验（FalseSharingBench）；本机相邻约慢 2 倍。同时要诚实：SPSC 整体吞吐的差异在这台机器上被噪声淹没。
5. cached index 为什么安全？答：head / tail 只增不减，旧快照只会低估对方进度——旧值说有空位 / 有数据必然为真；说满 / 空才刷新。
6. 变长消息回绕怎么处理？什么情况死锁？答：记录须连续，放不下先写 PAD 填到末尾；PAD 必须单独发布，否则空环 + tail 靠近末尾 + 大消息时 pad+记录 > capacity，消费者无物可读，两边互相等。
7. null / false 与 drained 怎么区分？答：closed 标志；isDrained = closed && head==tail；先读 closed 再读 tail，否则丢最后几条；残留 PAD 要 poll 越过后才 drained。
8. 跨进程内存序还成立吗？答：成立的是硬件缓存一致性 + VarHandle 发出的屏障，不是 JMM 的形式化保证（JMM 谈同一程序内的线程）；说法要谨慎。
9. 消费者崩溃重启怎么办？答：head / tail 在文件里，重启后 attach 能接着读；读完才发布 head，所以处理中崩溃会重读那条——至少一次语义，处理需幂等；要恰好一次需消息带序号并持久化处理进度。
10. 怎么测试跨进程代码、避免挂死？答：子进程 + 确定性消息（长度和内容由序号决定，丢 / 重 / 乱序 / 损坏都能抓到）+ 每端自旋带截止时间 + waitFor 超时后 destroyForcibly；类路径要含被测类的实际位置；不靠 sleep 对时序。
