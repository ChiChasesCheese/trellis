# 运行时与并发八股：Java（HashMap / 线程池 / GC）、Go（GMP）、Python（GIL）

面试官会按你简历上的语言来问运行时：Java 问集合、锁、线程池和垃圾回收（GC）；Go 问调度器（GMP）、channel 和 GC；Python 问全局解释器锁（GIL）和异步。目的是看你是否理解并发安全背后的机制，而不是背 API。每题按 **机制 → 为什么 → 数字或取舍 → 追问** 作答。三种语言各取最常考的几题，可以只准备自己的主语言，另外两种了解到能比较即可。与数据库和缓存的并发见 [[tiktok-mysql]]、[[tiktok-redis]]。

## 速记：这一页的 14 个问题

| # | 语言 | 问题 | 一句话答案 |
|---|---|---|---|
| 1 | Java | HashMap 结构与扩容 | 数组 + 链表/红黑树，负载因子 0.75，翻倍扩容 |
| 2 | Java | ConcurrentHashMap 怎么线程安全 | 空桶 CAS，非空桶锁头节点；读无锁 |
| 3 | Java | 线程池的参数与执行顺序 | 核心线程 → 队列 → 最大线程 → 拒绝 |
| 4 | Java | 线程池大小怎么定 | CPU 密集 N+1；IO 密集按等待比例放大；压测定 |
| 5 | Java | synchronized 与 ReentrantLock | 都可重入；后者可中断、可超时、可公平、多条件 |
| 6 | Java | volatile 与 CAS | 可见性 + 禁止重排，不保证原子；CAS 有 ABA |
| 7 | Java | GC 怎么选、怎么排查 Full GC | G1 默认；ZGC 低延迟；jstat、堆转储 |
| 8 | Java | ThreadLocal 内存泄漏 | key 是弱引用，value 是强引用；用完 remove |
| 9 | Java | 用 LinkedHashMap 实现 LRU | accessOrder=true + removeEldestEntry |
| 10 | Go | GMP 调度模型 | G 协程、M 线程、P 处理器；本地队列 + 偷任务 |
| 11 | Go | channel 与并发安全 | 环形缓冲 + 等待队列；map 不安全 |
| 12 | Go | Go 的 GC | 并发三色标记 + 写屏障；GOGC |
| 13 | Python | GIL 是什么，怎么绕过 | 一次只有一个线程跑字节码；多进程、C 扩展、asyncio |
| 14 | Python | asyncio、线程、进程怎么选 | IO 密集用 asyncio/线程，CPU 密集用多进程 |

## Q1. Java 的 HashMap 底层结构？怎么扩容？

- **结构**：数组（桶，bucket）+ 链表；JDK 8 起链表长度到 8 且数组长度 ≥ 64 时转红黑树，树节点退到 6 以下转回链表（留出 6 到 8 的缓冲避免来回转换）。数组长度是 2 的幂，索引 `(n-1) & hash`，用位运算代替取模；`hash = h ^ (h >>> 16)` 让高位参与运算，减少碰撞。
- **扩容**：元素数超过 `容量 × 0.75`（负载因子）时容量翻倍，重新分布。因为容量是 2 的幂，每个元素要么留在原下标，要么移到「原下标 + 旧容量」，由 hash 的新增那一位决定，不用重新算哈希。
- **为什么 0.75**：空间和碰撞的折中；太小浪费内存，太大链表变长。
- **预估大小**：知道要放 N 个元素，初始化容量 `N / 0.75 + 1`，避免多次扩容。
- **线程不安全的表现**：JDK 7 头插法并发扩容形成环，`get` 死循环；JDK 8 改尾插，不再死循环，但仍有数据覆盖丢失、`size` 不准。
- **追问 · 为什么树化用红黑树？** 最坏查找从 O(n) 降到 O(log n)，防止哈希碰撞攻击；红黑树比 AVL 的插入删除旋转少。
- **追问 · `hashCode` 和 `equals` 的约定？** 相等的对象必须有相同的 hashCode；作 key 的对象要不可变，否则改了字段就找不到了。

## Q2. ConcurrentHashMap 是怎么保证线程安全的？

- **JDK 7**：分段锁，`Segment` 继承 `ReentrantLock`，默认 16 段，并发度 16。
- **JDK 8 及以后**：去掉分段，锁粒度是单个桶：
  - 桶为空：**CAS** 把新节点放进去，无锁；
  - 桶非空：对桶的**头节点** `synchronized`，在链表或树里操作；
  - `get` 不加锁，节点的 `val` 和 `next` 是 `volatile`，保证可见性；
  - 扩容支持多线程协助：其他线程遇到正在迁移的桶（`ForwardingNode`）会帮忙搬一部分；
  - 计数：`baseCount` + `CounterCell[]`，类似 `LongAdder`，分散竞争。
- **为什么不允许 null**：`get` 返回 null 时分不清「没有这个 key」还是「值就是 null」，而并发下没法再用 `containsKey` 补查，因为两步之间可能被改。
- **复合操作不是原子的**：`if (!map.containsKey(k)) map.put(k, v)` 有竞态。用 `putIfAbsent`、`computeIfAbsent`、`merge`，它们在桶锁内完成。注意 `computeIfAbsent` 的函数里不要再修改同一个 map，可能死锁或抛异常。
- **追问 · 迭代器是强一致的吗？** 不是，弱一致：反映创建迭代器时的状态，也可能反映之后的部分修改，不会抛 `ConcurrentModificationException`。
- **追问 · 为什么用 `synchronized` 不用 `ReentrantLock`？** JDK 6 之后 `synchronized` 优化好（锁升级），不需要为每个桶创建一个锁对象，省内存。

## Q3. 线程池的参数和执行流程？

- **七个参数**：`corePoolSize`、`maximumPoolSize`、`keepAliveTime`（非核心线程空闲多久回收）、`unit`、`workQueue`、`threadFactory`、`handler`（拒绝策略）。
- **提交任务的顺序（必背）**：
  1. 运行线程数 < 核心数 → 新建线程执行；
  2. 否则放进队列；
  3. 队列满了，线程数 < 最大数 → 新建**非核心**线程；
  4. 仍然满 → 触发拒绝策略。
- **拒绝策略**：`AbortPolicy`（默认，抛异常）、`CallerRunsPolicy`（调用者线程自己执行，天然反压）、`DiscardPolicy`（静默丢）、`DiscardOldestPolicy`（丢队列头）。
- **`Executors` 的坑**：`newFixedThreadPool` 和 `newSingleThreadExecutor` 用无界 `LinkedBlockingQueue`，任务堆积会 OOM；`newCachedThreadPool` 最大线程数是 `Integer.MAX_VALUE`，并发高时创建海量线程。生产上直接用 `ThreadPoolExecutor` 并使用**有界队列**。
- **异常**：`execute` 里的异常会让线程死掉并打印；`submit` 的异常被包进 `Future`，不调用 `get` 就静默吞掉。
- **关闭**：`shutdown()` 不再接收新任务，等已有的做完；`shutdownNow()` 尝试中断正在执行的任务并返回队列里没执行的。
- **追问 · 队列大小怎么定？** 按可接受的排队延迟：队列长度 ≈ 吞吐 × 可容忍的等待时间。
- **追问 · Java 21 的虚拟线程？** 为每个任务创建一个虚拟线程（`Executors.newVirtualThreadPerTaskExecutor()`），阻塞时挂起并释放载体线程，IO 密集场景不再需要精心调池大小；限制并发要用信号量，不是靠池大小。

## Q4. 线程池大小怎么设？

- **CPU 密集型**：`N_cpu + 1`（多出的一个在某线程偶尔缺页时顶上）。
- **IO 密集型**：`N_cpu × (1 + W / C)`，W 是等待时间，C 是计算时间。例：8 核，每个请求 90ms 等数据库、10ms 计算，W/C = 9，线程数 ≈ 8 × 10 = 80。
- **局限**：公式只是起点。真正的做法是压测：逐步加线程，找吞吐不再上升或延迟开始恶化的拐点；同时受下游连接池大小限制（线程多于连接数只会排队）。
- **隔离**：不同类型的任务用不同的池（舱壁隔离，见 [[tiktok-service-protection]]），避免一个慢依赖耗尽所有线程。
- **监控**：活跃线程数、队列长度、拒绝次数、任务耗时。

## Q5. synchronized 和 ReentrantLock 有什么区别？

| | synchronized | ReentrantLock |
|---|---|---|
| 层面 | JVM 关键字，自动释放 | JDK 类（基于 AQS），必须在 `finally` 中 `unlock` |
| 可重入 | 是 | 是 |
| 公平性 | 非公平 | 默认非公平，可选公平 |
| 可中断 / 超时 | 否 | `lockInterruptibly`、`tryLock(timeout)` |
| 条件变量 | 一个（`wait/notify`） | 多个 `Condition` |
| 性能 | JDK 6 之后与 ReentrantLock 接近 | 竞争激烈时略有优势 |

- **synchronized 的升级**：无竞争时用 mark word 里的偏向（JDK 15 起默认关闭）→ 轻量级锁（CAS 自旋）→ 竞争加重膨胀为重量级锁（操作系统互斥量，线程阻塞）。
- **AQS**（AbstractQueuedSynchronizer）：一个 `volatile int state` 加一个 FIFO 的等待队列；获取失败的线程入队并 park，释放时唤醒后继。`ReentrantLock`、`Semaphore`、`CountDownLatch` 都是基于它。
- **JDK 21 提示**：虚拟线程在 `synchronized` 块里阻塞会把载体线程钉住（pinning），JDK 24 才修复；需要和虚拟线程配合的代码优先用 `ReentrantLock`。
- **追问 · 死锁的四个条件和避免？** 互斥、持有并等待、不可抢占、循环等待；破坏循环等待的办法是所有线程按固定顺序加锁；用 `tryLock` 带超时；用 `jstack` 排查，它会直接打印死锁线程。

## Q6. volatile 做了什么？CAS 有什么问题？

- **volatile**：保证**可见性**（写后立即刷到主内存，读时重新取）和**禁止指令重排序**（通过内存屏障），不保证复合操作的原子性：`count++` 是读—改—写三步，volatile 下仍有丢失更新。
- **典型用途**：状态标志位；双重检查锁定（double-checked locking）单例里的 `instance` 必须 volatile，否则对象还没初始化完成其他线程就可能看到非空引用（`new` 分为分配内存、初始化、赋引用，可能被重排）。
- **happens-before**：Java 内存模型（JMM）的规则：解锁 happens-before 后续对同一把锁的加锁；volatile 写 happens-before 后续对它的读；线程 `start` 前的操作 happens-before 线程内的操作。
- **CAS**（compare-and-swap）：CPU 原子指令，「如果当前值等于期望值才更新」。`AtomicInteger` 靠它实现无锁更新。
- **CAS 的问题**：ABA（值 A→B→A，看起来没变，用 `AtomicStampedReference` 加版本号）；高竞争下自旋耗 CPU（用 `LongAdder`，分段累加，读时求和）；一次只能操作一个变量。
- **追问 · `AtomicLong` 与 `LongAdder`？** 写多读少的计数器用 `LongAdder`；需要精确的瞬时值或 CAS 语义用 `AtomicLong`。

## Q7. JVM 垃圾回收：怎么选收集器？线上 Full GC 频繁怎么排查？

- **回收基础**：从 GC Roots（线程栈、静态变量、JNI 引用）出发做可达性分析，不可达的对象回收。堆分代：新生代（Eden + 两个 Survivor，复制算法，存活的晋升）和老年代（标记—清除/整理）。
- **收集器**：

| 收集器 | 特点 | 适用 |
|---|---|---|
| Parallel | 吞吐优先，停顿较长 | 批处理 |
| G1（JDK 9+ 默认） | 把堆分成多个 Region，优先回收垃圾多的；目标停顿 `-XX:MaxGCPauseMillis`（默认 200ms） | 通用服务，堆几 GB 到几十 GB |
| ZGC | 并发标记和整理，停顿通常小于 1ms，与堆大小几乎无关；JDK 21 加 `-XX:+UseZGC -XX:+ZGenerational` 启用分代 | 低延迟，大堆 |

- **Full GC 频繁的排查步骤**：
  1. `jstat -gcutil <pid> 1000` 看老年代使用率、Full GC 次数和耗时；
  2. 看 GC 日志（`-Xlog:gc*`）确认触发原因：老年代满、元空间（Metaspace）满、显式 `System.gc()`、晋升失败；
  3. `jmap -histo:live <pid>` 看对象个数分布，或导出堆转储（`jmap -dump` / `-XX:+HeapDumpOnOutOfMemoryError`），用 MAT 看谁占内存、被谁引用；
  4. 常见根因：无界的静态集合/缓存、`ThreadLocal` 没清、一次查询加载超大结果集、大对象直接进老年代、堆太小；
  5. 修复后复测，必要时调整堆大小和收集器参数。
- **追问 · OOM 有哪几种？** 堆 OOM（`Java heap space`）；元空间；无法创建本地线程（线程数或 ulimit 限制）；直接内存（`Direct buffer memory`，Netty 常见）；容器被 OOMKilled（超过 cgroup 限制，进程消失，没有 Java 异常）。
- **追问 · 怎么减少 GC 压力？** 少创建临时对象、对象池谨慎使用、避免大对象、设置合理的新生代比例。

## Q8. ThreadLocal 为什么会内存泄漏？

- **结构**：每个 `Thread` 有一个 `ThreadLocalMap`，key 是 `ThreadLocal` 对象的**弱引用**，value 是**强引用**。
- **泄漏过程**：`ThreadLocal` 对象失去外部引用被 GC 后，key 变成 null，但 value 仍被 `ThreadLocalMap` 强引用，而 map 被线程引用。线程池里的线程长期存活，这些 value 永远回收不掉。
- **还有一个更常见的问题**：线程池复用线程，上一个请求放进 ThreadLocal 的用户信息，被下一个请求读到（数据串了）。
- **做法**：用完在 `finally` 里 `remove()`；把 ThreadLocal 声明为 `static final`；跨线程传递用 `TransmittableThreadLocal` 之类，或显式传参；`ScopedValue`（JDK 21 起预览，JDK 25 定稿）是更安全的替代，尤其适合虚拟线程。

## Q9. 用 LinkedHashMap 实现 LRU 缓存？

- **机制**：`LinkedHashMap` 在哈希表之外维护一条双向链表；构造时 `accessOrder=true`，每次 `get` / `put` 访问都把节点移到链表尾；重写 `removeEldestEntry`，在 `size() > capacity` 时返回 true，自动删除链表头（最久未使用）。

```java
class LRU<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    LRU(int capacity) {
        super(16, 0.75f, true);
        this.capacity = capacity;
    }
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

- **复杂度**：`get` 和 `put` 都是 O(1)。
- **线程安全**：不安全。简单做法 `Collections.synchronizedMap`，高并发用 Caffeine（见 [[tiktok-cache-problems]]）。
- **手写版本（常被要求）**：哈希表（key → 节点）+ 自己实现的双向链表（头尾哨兵节点），`get` 时把节点摘下插到头部，`put` 超容量时删尾部节点并从哈希表删除；必须在节点里存 key，否则删尾节点时不知道要从哈希表删哪个 key。

## Q10. Go 的 GMP 调度模型是什么？

- **角色**：**G**（goroutine，协程，初始栈 2KB，可增长）、**M**（machine，操作系统线程）、**P**（processor，逻辑处理器，数量默认等于 CPU 核数，`GOMAXPROCS`）。P 持有本地运行队列（最多 256 个 G）；M 必须绑定一个 P 才能运行 G。另有全局运行队列。
- **调度顺序**：M 先从绑定的 P 的本地队列取 G；每执行 61 次调度检查一次全局队列（防饿死）；本地和全局都空，查网络轮询器（netpoller）；还是空，**从别的 P 的队列偷一半**（work stealing）。
- **系统调用**：G 做阻塞的系统调用时，M 跟着阻塞，P 被后台监控线程（sysmon）摘走交给别的 M，继续跑其他 G；调用返回后 G 重新排队。网络 IO 用 epoll，由 netpoller 管理，G 挂起而不阻塞 M。
- **抢占**：Go 1.14 起基于信号的异步抢占，运行超过约 10ms 的 G 会被打断，防止死循环霸占 P。
- **为什么 goroutine 比线程轻**：栈小且动态增长（线程栈固定几百 KB 到 MB）；切换在用户态，不进内核，只保存几个寄存器，约几百纳秒（线程切换约几微秒）；所以一个进程里可以有几十万个。
- **追问 · goroutine 泄漏？** goroutine 永远阻塞（等没人发送的 channel、没人解锁的锁），没有被回收。用 `context` 传取消信号，`select` 里加 `ctx.Done()`，用 `pprof` 的 goroutine profile 查看数量增长。

## Q11. Go 的 channel 是怎么实现的？map 并发安全吗？

- **channel 结构（`hchan`）**：环形缓冲区（有缓冲时）+ 一个互斥锁 + 发送等待队列和接收等待队列。无缓冲 channel 发送方和接收方必须同时就绪（同步交接）；有缓冲的，缓冲满了发送阻塞，空了接收阻塞。
- **规则**：向 nil channel 发送或接收永远阻塞；向已关闭的 channel 发送 panic；从已关闭的 channel 接收返回零值和 `ok=false`；只有发送方关闭，关闭两次 panic。`select` 多个 case 同时就绪时随机选一个。
- **map 不是并发安全的**：并发读写会触发运行时检测并 `fatal error: concurrent map writes`（无法 recover）。方案：`sync.RWMutex` 保护；读多写少用 `sync.Map`；分片加锁降低竞争。
- **`sync.Mutex`**：正常模式下新来的 goroutine 可以和被唤醒的竞争（吞吐高）；等待超过 1ms 进入饥饿模式，锁直接交给队首（公平）。
- **常用同步工具**：`WaitGroup`（等一组 goroutine）、`Once`、`atomic`、`errgroup`（带错误和取消）。
- **追问 · 用 channel 还是锁？** 传递数据所有权、流水线用 channel；保护共享状态用锁，更简单更快。

## Q12. Go 的 GC 怎么工作的？

- **算法**：并发的三色标记清除（tri-color mark and sweep）。对象分白（未访问）、灰（已访问，引用还没扫完）、黑（全部扫完）。标记阶段与应用并发，靠**写屏障**（write barrier）保证并发修改指针时不漏标；只有开始和结束的两次很短的 STW（stop-the-world，通常亚毫秒）。
- **触发**：堆增长到上次回收后存活大小的 `1 + GOGC/100` 倍（`GOGC` 默认 100，即翻倍）；Go 1.19 起可设 `GOMEMLIMIT` 软内存上限，在容器里防 OOM。
- **取舍**：Go 的 GC 不分代、不整理（不移动对象），所以停顿低但吞吐有损耗，GC 占用约 25% 的 CPU 做并发标记。
- **优化**：减少堆分配，让对象留在栈上（逃逸分析，`go build -gcflags=-m`）；复用对象（`sync.Pool`）；预分配 slice 容量；调大 `GOGC` 用内存换 CPU。
- **追问 · 对比 Java 的 G1？** G1 分代、Region、会移动对象，停顿可预测但调参多；Go 简化为单一并发回收器，调参只有 `GOGC` 和 `GOMEMLIMIT`。

## Q13. Python 的 GIL 是什么？怎么绕过？

- **机制**：CPython 里的 GIL（global interpreter lock）是一把全局互斥锁，同一时刻只有一个线程在执行 Python 字节码。
- **为什么存在**：CPython 内存管理用引用计数，对象的计数器不是线程安全的；用一把全局锁比给每个对象加锁简单、单线程更快，也方便 C 扩展。
- **切换**：线程做阻塞 IO（读文件、网络、`sleep`）时释放 GIL；纯计算时每隔 5ms（`sys.getswitchinterval()`）请求切换。
- **结果**：CPU 密集的多线程代码没有加速，甚至因为抢锁变慢；IO 密集的多线程仍然有效，因为等 IO 时 GIL 被释放。
- **绕过**：
  1. **多进程**（`multiprocessing`、`concurrent.futures.ProcessPoolExecutor`）：每个进程有独立的解释器和 GIL，代价是进程间通信要序列化；
  2. **C 扩展释放 GIL**：NumPy、pandas 的核心计算在 C 里不持有 GIL；
  3. **异步 IO**：单线程处理大量并发连接；
  4. **新版本**：3.12 起每个子解释器可以有独立的 GIL（PEP 684）；3.13 起有可选的自由线程构建（free-threaded，PEP 703），3.14 成为受支持的构建，但不是默认。
- **追问 · 有 GIL 就线程安全吗？** 不是。GIL 保证单条字节码原子，但 `x += 1` 对应多条字节码，线程切换会丢更新；`list.append`、`dict[key] = v` 这类单次操作是原子的；复合逻辑仍需 `threading.Lock`。

## Q14. asyncio、多线程、多进程怎么选？

| 场景 | 选择 | 原因 |
|---|---|---|
| 大量并发网络请求（爬虫、调用下游 API） | asyncio | 单线程事件循环，一个连接几 KB，可上万并发 |
| 阻塞的库（同步 SDK、数据库驱动） | 线程池（`run_in_executor`） | 不能 `await`，放进线程避免阻塞事件循环 |
| CPU 密集（图像处理、压缩、模型推理） | 多进程 | 绕过 GIL，利用多核 |
| 混合 | asyncio 做 IO，进程池做计算 | 各取所长 |

- **asyncio 的机制**：单线程事件循环（event loop）调度协程；协程遇到 `await` 让出控制权，IO 就绪后恢复；底层用 epoll。
- **最大的坑**：在协程里调用阻塞函数（`time.sleep`、同步的 `requests.get`、重计算）会卡住整个事件循环。用 `asyncio.sleep`、异步库（`httpx`、`aiohttp`），或 `asyncio.to_thread`。
- **Python 的内存管理补充**：引用计数为主（计数为 0 立即回收），再加分代的循环垃圾回收器处理环引用（三代，默认阈值 700 / 10 / 10）。
- **追问 · 协程和线程的区别？** 协程是用户态的协作式调度，切换点明确（`await`），没有竞态的问题（同一时刻只有一个协程运行），但一个协程不让出就卡全部；线程由操作系统抢占式调度，需要锁。

## 延伸阅读

- Java 并发：JDK 文档 `java.util.concurrent`；JEP 444（虚拟线程）
- Go 调度器：Go 运行时源码 `runtime/proc.go`
- PEP 703（自由线程 Python）
- 相关：[[tiktok-networking-os]] · [[tiktok-cache-problems]] · [[tiktok-fundamentals]]
