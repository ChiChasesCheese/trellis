# hc13 · 思路与追问

## 概要

「定长内存池」是少数明确偏系统编程的题，考 API 设计和内存管理。
对 Java 岗，面试官想看四件事：(1) 能不能把借 / 还的所有失败模式列全（池满、重复归还、归还别人的块、编号被复用）；(2) 能不能解释为什么要池（GC 压力 → 尾延迟），并诚实地说出它不会让吞吐更快；(3) 知道 Java 里"堆外"是什么、代价是什么；(4) 并发下 ABA 与内存序。

## 逐 Part 思路

1. IndexPool：`int[] next` 当侵入式空闲链表，`head` 指向第一个空闲块；`next[b] = -2 (ALLOCATED)` 表示在用，重复归还检测不需要另开数组。allocate / free 都是 O(1)。free 判定顺序：越界 → INVALID；`next[b] != ALLOCATED` → DOUBLE_FREE（含"从没借过"）。
2. GenPool：handle = `generation << 32 | index`。版本号奇数在用、偶数空闲，借还各 +1。free：下标越界或版本为偶数 → INVALID；版本为奇数但与槽位当前不同 → DOUBLE_FREE。`0L`、`NONE (-1)` 自动无效；32 位回绕后奇偶性不变。
3. OffHeapOrderPool：`Arena.ofShared()` 一次分配 `capacity × 32` 字节、64 字节对齐；槽位 `[gen:int][next:int][id:long][px:long][qty:int][side:int]`，字段用 `StructLayout` + `SequenceLayout(MAX_CAPACITY)` 生成的 `static final VarHandle`。allocate 清零载荷；`put(h, id, px, qty, side)` / `px(h)` / `qty(h)` 是零分配热路径，`put(h, Order)` 用 record 模式转调，`get(h)` 会 new。close() 幂等。
4. ConcurrentPool：`head` 是 long（高 32 位 tag、低 32 位栈顶编号），`VarHandle.compareAndSet` 更新；每次成功 push / pop tag + 1。free 先用 `CAS(gens[i], g, g+1)` 选出唯一赢家再压栈。`next[]` 用 opaque，`head` 读用 acquire，`gens` 写用 release，计数用 LongAdder。

## 隐藏测试会打的坑

* 打包 handle 忘了 `& 0xFFFFFFFFL`；free 不检查状态（同一块进链表两次）；复用槽位不清零。
* 只测"50/50 随机借还"漏掉 O(n) 扫描——随机负载下池里只有几百块在用，扫描很快。所以要专门测「池填满后 150 万次换块」。
* 没有 tag 的 Treiber 栈（ABA）；free 的"检查 + 修改"不是一次 CAS（并发 double-free 双赢）。
* `Arena.ofConfined()` + JUnit 超时断言换线程 → WrongThreadException；`close()` 重复调用抛异常；`put(h, null)` 应抛 NPE；陈旧 handle 的 get 读到新主人的数据。

## 复杂度

| 操作 | 时间 | 空间 |
|---|---|---|
| IndexPool.allocate/free | O(1) | 4 × capacity 字节 |
| GenPool.allocate/free | O(1) | 8 × capacity 字节 |
| OffHeapOrderPool 各操作 | O(1) | 32 × capacity 字节堆外，一次分配 |
| ConcurrentPool.allocate/free | O(1) 期望；争用下 CAS 重试无界（lock-free，不是 wait-free） | 8 × capacity 字节 |

量级参考（12 核）：IndexPool 近满换块 150 万次 11 ms、随机 300 万次 40 ms；GenPool 10 / 27 ms；OffHeapOrderPool 100 万记录 62 ms；ConcurrentPool 4 线程 × 5 万轮 × 16 次借还 450 ms。
O(n) 扫描版：近满换块约 3.9 µs/步 → 150 万步约 6 s；50/50 随机负载只要 125 ms（所以随机负载测不出它）。
池化的价值（3000 万条消息，窗口 100 万，-Xmx256m）：堆上 new 与堆外池总耗时几乎相同（500–800 ms，噪声 ±30%），但 G1 / Parallel 下 new 版最慢一次 4.5 / 22 ms、几十个操作超过 1 ms，池版 0.02 ms、0 个；分代 ZGC 下两者最慢都 < 0.2 ms。
争用对比（百万次/秒）：8 线程 locked ≈ 80、treiber ≈ 3.9、cached ≈ 1020；1 线程 150 / 108 / 230。无锁在高争用下可以比锁慢 20 倍；每线程缓存快一个数量级以上。数字波动大，趋势稳定。

## Java 21 特性

| 特性 | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| record | `Order` + `Order.ZERO` | 一行替代 30 行样板；equals 逐字段，测试直接 assertEquals |
| record 模式 | `OffHeapOrderPool.put(long, Order)`：`case Order(long id, long px, int qty, int side) ->` | 一次解构四个字段，组件个数 / 类型由编译器检查 |
| switch 表达式 | `IndexPool.freeOrThrow`：`RuntimeException failure = switch (free(block)) {…}` | 无 fall through；对 enum 穷尽性检查 |
| var | `var pool = new IndexPool(3)` | 右边已写类型时不重复 |
| 虚拟线程 | 2000 个虚拟线程各 200 轮借还 | 不用调线程池；任务短小不自旋 |
| VarHandle / LongAdder | `ConcurrentPool`：`findVarHandle` 对 long head CAS；`arrayElementVarHandle(int[].class)` 对 gens / next 做 CAS / opaque / release；LongAdder 计数 | 不需要每槽位一个原子对象；按需选访问强度 |
| FFM | `OffHeapOrderPool`：Arena.ofShared、StructLayout、SequenceLayout、布局生成的 VarHandle | 容量 long、确定性释放、字段按名字访问；GC 看不见 |

## 面试官可能的追问

1. Java 有 GC，为什么要自己做池？答：new 本身便宜（TLAB 指针碰撞）；池化为的是尾延迟（GC 暂停、GC 线程抢 CPU），不是吞吐。先用 `-Xlog:gc` / JFR 确认；分代 ZGC 已把暂停压到亚毫秒，先试换 GC。代价：use-after-free 变逻辑 bug、数据泄漏、老年代写屏障。
2. 怎么检测重复归还？答：`next[b]` 放哨兵 ALLOCATED，free 先检查，不另开数组。进阶：编号会被复用时下标无身份，要版本号。
3. A 还了块 7，B 借到 7，A 又还一次，怎么防？答：handle = (版本号, 下标)，槽位每次归还版本号变；奇偶表示状态；free 比较版本。32 位回绕奇偶不变；2^31 次借还后旧 handle 才可能撞上，可退役槽位。
4. 无锁怎么做？ABA 是什么？答：Treiber 栈 + 对 head 的 CAS；线程 1 读到 head=A、next[A]=B 后被挂起，线程 2 弹 A、弹 B、压 A，线程 1 的 CAS 成功却把 B 装回栈里。解法：head 带 tag（每次成功操作 +1），CAS 比较整个 64 位；tag 回绕需 2^32 次操作，可忽略；更严格用 hazard pointer。
5. 并发下两个线程同时 free 同一个 handle？答：`CAS(gens[i], g, g+1)` 仲裁，输的返回 DOUBLE_FREE；奇偶版本号让"校验 + 切换状态"成为一次 CAS。
6. 无锁一定比锁快吗？每线程缓存呢？答：不一定。8 线程抢同一个 head 时 Treiber 栈比 ReentrantLock 慢近 20 倍。每线程缓存（批量补货）快一个数量级以上；代价：搁浅、缓存内重复归还不可见、线程退出要冲刷、虚拟线程下 ThreadLocal 数量爆炸（改按载体线程 / CPU 分片）、LIFO 语义变化。
7. 池满了怎么办？答：返回 NONE 让调用方决定（背压 / 丢弃 / 告警）；或阻塞（Semaphore）；扩容会引入分配、打破固定容量。低延迟系统通常选第一种并告警。
8. 为什么堆外？有什么代价？答：GC 看不见、布局连续对齐、close() 确定性释放、容量 long；代价：手动 close、固定容量、边界检查（JIT 能消掉大部分）、JDK 21 里 FFM 仍是预览（22 转正，API 有改名）。
