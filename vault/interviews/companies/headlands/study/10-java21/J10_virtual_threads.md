# J10 · 虚拟线程：让「一个请求一个线程」重新变得便宜

> 版本：Java 21 **正式**（JEP 444）。Java 19 预览（JEP 425），Java 20 第二次预览（JEP 436）。
> 写法说明见 `study/TEXTBOOK.md`。本课所有可运行代码在 `study/10-java21/examples/J10/`，输出都是在本机（JDK 21.0.12，12 核 macOS）上实跑的。
> 前置知识：会写 `new Thread(() -> ...).start()` 就够了。什么是线程、为什么线程贵，第 1 节从零讲。
> 官方出处：JEP 444 — https://openjdk.org/jeps/444 ；JDK 21 指南 — https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html
> 后续版本：JEP 491（JDK 24）去掉了 `synchronized` 的 pinning，见第 5 节。

---

## 1. 先看痛点：线程是什么，为什么一个请求一个线程「写起来最自然、跑起来最贵」

### 1.1 从零讲：进程、线程、栈

* **进程**（process）：一个正在运行的程序。操作系统（OS）给它一块独立的内存。你启动一次 `java Main` 就是一个进程。
* **线程**（thread）：进程里的一条「执行流水线」。同一个进程里的多个线程**共享堆内存**（对象都在堆里），但**各自有一个调用栈**（stack）。
* **调用栈**：记录「我现在在执行哪个方法、它是被谁调用的、局部变量是什么」。方法 `a()` 调 `b()` 调 `c()`，栈上就有三层「栈帧」（frame）。
  方法返回就弹掉一层。这就是为什么异常的 stack trace 能告诉你「调用链」。

```
  线程 T1 的栈               线程 T2 的栈          堆（共享）
  ┌──────────────┐          ┌──────────────┐     ┌─────────────────┐
  │ c()  局部变量 │          │ x()          │     │ Order 对象 ...   │
  │ b()          │          │ main()       │     │ HashMap ...      │
  │ a()          │          └──────────────┘     └─────────────────┘
  │ run()        │
  └──────────────┘
```

CPU 只有有限的**核**（core）。12 核的机器，同一瞬间最多真的在跑 12 条指令流。OS 里有一个**调度器**（scheduler）：
线程比核多时，它轮流让每个线程占一小段时间（时间片），这叫**时间片轮转**。从线程 A 换到线程 B 叫**上下文切换**（context switch），
要保存 A 的寄存器、换成 B 的，量级是微秒，并且会把 CPU 缓存里的热数据冲掉一部分。

### 1.2 「阻塞」是什么

线程执行 `socket.read()`（等网络对端回包）、`Thread.sleep()`、`queue.take()`（等队列里有东西）时，它**什么 CPU 都不用，只是在等**。
这叫**阻塞**（block）。OS 会把它标成「等待中」，不给它时间片，直到事件发生再唤醒。

交易系统里到处都是阻塞：向行情网关请求报价、查风控额度、写数据库、等下游回 ack。一个典型请求 99% 的时间在等。

### 1.3 Java 8 的做法与它的墙

最自然的写法是「一个请求一个线程」（thread-per-request）：代码从上往下写，遇到阻塞就阻塞，调试时栈清清楚楚。

```java
String quote = gateway.fetchQuote(symbol);   // 阻塞 100ms
Limit limit  = risk.fetchLimit(account);     // 阻塞 20ms
```

但**Java 的线程（平台线程，platform thread）= 一个 OS 线程**，而 OS 线程很贵：

| 代价 | 量级（典型 64 位 Linux/macOS，数字是量级，不是保证） |
|---|---|
| 栈 | 默认约 1 MB 的虚拟地址空间预留（`-Xss`），用到才真占物理内存，但每个线程都要在内核里登记 |
| 创建/销毁 | 几十微秒到上百微秒，是系统调用 |
| 上下文切换 | 微秒级，线程数越多越频繁 |
| 数量上限 | 几千到几万个，再多调度器和内存都撑不住 |

**利特尔定律**（Little's law，排队论里最有用的一条）：`同时在途的请求数 = 吞吐量 × 单个请求的耗时`。

> 例：网关每秒要处理 10 000 个请求，每个请求 100 ms（几乎全在等网络）。同时在途 = 10 000 × 0.1 = **1 000 个**。
> 如果每个在途请求占一个线程，就要 1 000 个线程——勉强。吞吐翻 10 倍到 10 万/秒，就是 1 万个线程——开始撑不住。

于是 Java 8 时代的人只能二选一，两条路都痛：

**路 1：线程池限流。** 开 50 个线程的固定池，任务排队。吞吐被池的大小锁死。本课 `examples/J10/J10Old.java`：

```java
ExecutorService pool = Executors.newFixedThreadPool(50);
for (int i = 0; i < 1_000; i++) futures.add(pool.submit(() -> fetchQuote(sym))); // 每个 sleep 100ms
```

理论上 1000 个任务 ÷ 50 线程 = 20 批 × 100ms = 2 秒。本机实测输出：

```
fixed pool(50): 1000 个 100ms 任务耗时约 4185 ms
```

（比 2 秒大约慢一倍，是因为本机 macOS 上 `Thread.sleep(100)` 实际要睡 ~200ms 才醒——计时器合并；后面所有 sleep 实验都带这个系数，
**看比例，不看绝对值**。）线程大多数时间在睡觉，CPU 空着，吞吐却上不去。

**路 2：异步回调 / 响应式**（`CompletableFuture`、Netty、Reactor）。线程不阻塞了，但代码变成
`fetchQuote(sym).thenCompose(q -> fetchLimit(acct).thenApply(l -> ...))`。代价：

* 调用链被切碎——异常的 stack trace 只剩回调框架的栈，看不出是谁发起的；
* 调试器单步跟不进去；
* `try/catch`、`try-with-resources`、循环这些普通控制流都得改写成链式调用；
* 一个同步库（JDBC 驱动）混进来，整个异步链就卡住。

**虚拟线程的承诺**：保留路 1 的好写法（同步、阻塞、栈清楚），去掉它的贵。线程变得极便宜，**一个任务一个线程**，不用池，不用限流（限流改用别的手段）。

---

## 2. 语法逐条讲

### 2.1 创建

```java
// 1. 创建并立刻启动
Thread t = Thread.ofVirtual().name("v-1").start(() -> work());
// 2. 最短写法（没有名字）
Thread t2 = Thread.startVirtualThread(() -> work());
// 3. builder：先 unstarted，再手动 start；name("v-", 0) 会自动编号 v-0, v-1, ...
Thread t3 = Thread.ofVirtual().name("v-", 0).unstarted(() -> work());
t3.start();
// 对照：平台线程
Thread p = Thread.ofPlatform().name("p-1").start(() -> work());
```

`Thread.ofVirtual()` 返回 `Thread.Builder.OfVirtual`；`Thread.ofPlatform()` 返回 `Thread.Builder.OfPlatform`（可以设优先级、栈大小、是否守护）。
两种 builder 都有 `.factory()`，得到一个 `ThreadFactory`，能塞进任何接受 `ThreadFactory` 的 API。

### 2.2 最常用：每任务一个虚拟线程的 ExecutorService

```java
try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Quote> f = ex.submit(() -> fetch(sym));
    Quote q = f.get();
}   // close()：不再接新任务，并且等所有已提交任务结束
```

* 它**不是线程池**：每次 `submit` 都新建一个虚拟线程，任务结束线程就消失，不复用。因为虚拟线程便宜到不需要复用。
* 从 Java 19 起 `ExecutorService` 实现了 `AutoCloseable`，所以能放进 `try-with-resources`：离开块时自动 `shutdown()` 再 `awaitTermination()`。
  老的 `ExecutorService` 忘了 `shutdown()` 会让 JVM 退不出去；新写法不会忘。

### 2.3 判断与特性

```java
Thread.currentThread().isVirtual();     // 是不是虚拟线程
```

* 虚拟线程**永远是守护线程**（daemon）：`main` 结束时，还没跑完的虚拟线程不会拦着 JVM 退出。别指望「启动完不 join 它也会跑完」。
* 优先级固定为 `NORM_PRIORITY`，设置无效。
* 可以有 `ThreadLocal`（见第 5 节：能用，但别当缓存池）。
* `Thread.sleep`、`Object.wait`、`BlockingQueue.take`、`Lock.lock`、`socket.read` 等照常可用——这就是整个卖点：**阻塞 API 不用改**。

### 2.4 限流改用信号量（Semaphore）

线程池的副作用之一是「线程数 = 并发上限」，所以它顺带限了流（比如下游网关最多接受 20 个并发请求）。去掉池以后，限流要**显式**写：

```java
Semaphore inFlight = new Semaphore(20);
inFlight.acquire();            // 虚拟线程在此阻塞是廉价的
try { return gateway.fetch(sym); } finally { inFlight.release(); }
```

---

## 3. 编译器和 JVM 到底做了什么

编译器几乎什么都没做——虚拟线程是**纯运行时（JVM + JDK 库）特性**，没有新语法。重点在运行时。

### 3.1 三个角色

* **虚拟线程**（virtual thread）：一个普通的 Java 对象（`java.lang.VirtualThread`），里面装着「一段可暂停的执行」。
* **载体线程**（carrier thread）：真正的 OS 线程，数量很少，默认等于 CPU 核数。它们属于一个专用的 `ForkJoinPool`（调度器）。
  从 `J10Ex1` 的输出里能直接看见这个关系：

```
  running in VirtualThread[#20,v-1]/runnable@ForkJoinPool-1-worker-1  isVirtual=true  daemon=true
```

  读法：虚拟线程 `#20`（名字 `v-1`），当前状态 runnable，正跑在载体 `ForkJoinPool-1-worker-1` 上。
* **续体**（continuation）：JVM 内部机制，能把「一个线程当前的整条调用栈」**冻结**成一个堆上对象，以后再**解冻**接着跑。
  这是虚拟线程的魔法所在。

### 3.2 挂载（mount）与卸载（unmount）

```
  虚拟线程 V1..V10000         调度器（ForkJoinPool，N 个载体线程 = N 个 OS 线程）
  ┌────┐ ┌────┐ ┌────┐        ┌────────────┐ ┌────────────┐
  │ V1 │ │ V2 │ │ V3 │ ...    │ carrier-1  │ │ carrier-2  │ ...  <- 只有这些是真 OS 线程
  └────┘ └────┘ └────┘        │ 正在跑 V7   │ │ 正在跑 V2   │
                              └────────────┘ └────────────┘
   V1 在等网络：栈被冻结存在堆上，不占任何载体
```

1. 虚拟线程 `V` 被调度时，调度器把它**挂载**到某个空闲载体上：把 `V` 堆上保存的栈帧拷回载体的栈（实际按需、一部分一部分地拷），然后接着跑。
2. `V` 执行到阻塞操作（比如 `Thread.sleep(100)`）。JDK 库里的阻塞实现被改写过：它不再让 OS 线程睡，而是调用 `LockSupport.park`，
   park 在虚拟线程上变成「**yield**」：把 `V` 的栈帧拷出来存进堆（一个 `StackChunk` 对象），然后 `V` 被**卸载**——载体立刻空出来去跑别的虚拟线程。
3. 事件到来（定时器到点、socket 可读）时，JDK 内部的辅助机制调用 `unpark(V)`，相当于把 `V` 重新提交给调度器，等某个载体空了再挂载它，接着从阻塞点后面一行继续跑。

对写代码的人来说，这一切**不可见**：`Thread.sleep(100)` 看起来就是「卡住 100ms 然后继续」，调用栈、局部变量、异常全都保持。

### 3.3 为什么便宜

| | 平台线程 | 虚拟线程 |
|---|---|---|
| 栈 | OS 分配固定预留（约 1 MB），内核管理 | 在堆上，起步只有几百字节到几 KB，随调用深度增长，**由 GC 管理** |
| 创建 | 系统调用 | `new` 一个对象 + 提交给调度器，微秒以内 |
| 阻塞时 | OS 线程睡眠，资源一直占着 | 栈拷到堆，载体放走 |
| 数量 | 千～万级 | 百万级（受堆内存限制） |

实测（`J10Ex2`，同样 1000 个 100ms 任务）：

```
固定池 50 线程, 1000 任务: 4121 ms
虚拟线程每任务一个, 1000 任务: 216 ms
虚拟线程每任务一个, 10000 任务: 273 ms
```

10 倍的任务数，耗时几乎没变——因为任务全在「睡觉」，睡觉不占载体。

### 3.4 哪些操作会让虚拟线程卸载，哪些不会（JDK 21）

| 操作 | 卸载？ |
|---|---|
| `Thread.sleep`、`LockSupport.park`、`java.util.concurrent` 里的锁/队列/`Semaphore`/`CountDownLatch` | 是 |
| `java.net.Socket`、`SocketChannel`、`HttpClient` 等网络 I/O（JDK 内部已改成非阻塞 + 轮询器） | 是 |
| 文件 I/O（`FileInputStream.read` 等） | **否**：载体被占住；调度器会临时多开一个载体来补偿（上限 `maxPoolSize`，默认 256） |
| 在 `synchronized` 块里阻塞、`Object.wait()` | **否，pinning（钉住）**，见 5.1 |
| 执行 native 方法 / FFM 下行调用期间阻塞 | **否，pinning** |

### 3.5 调度是**协作式**的，不是抢占式

OS 线程可以被 OS 随时打断（时间片到了）。虚拟线程**只有在主动阻塞（park）时才让出载体**。
一个虚拟线程如果在做纯计算、循环 100 亿次，它就一直霸占那个载体，直到算完。后面第 5.2 节会实测。

---

## 4. 三个例子（由浅入深）+ 两个对照实验

### 例 1：最简单——创建与观察（`J10Ex1.java`）

见 2.1。关键输出：

```
方式 1 ofVirtual().start
  running in VirtualThread[#20,v-1]/runnable@ForkJoinPool-1-worker-1  isVirtual=true  daemon=true
对照：平台线程
  running in Thread[#25,p-1,5,main]  isVirtual=false  daemon=false
virtual isDaemon=true priority=5
```

平台线程的 toString 是 `Thread[#25,p-1,5,main]`（编号、名字、优先级、线程组）；虚拟线程是 `VirtualThread[#20,v-1]/runnable@载体`。

### 例 2：进阶——吞吐对比（`J10Ex2.java`）

见 3.3 的表和输出。要点：

```java
try (var vex = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < n; i++) fs.add(vex.submit(() -> fetchQuote(s)));
    for (var f : fs) f.get();
}
```

代码和固定池版本只差一行 `Executors.xxx`，但并发度从 50 提高到 10 000。

### 例 3：贴近真实——并发取行情，同时限制下游并发（`J10Ex3.java`）

500 个代码，每个调用一次「行情网关」（模拟 50ms）。网关只允许 20 个并发。用虚拟线程 + `Semaphore(20)`：

```java
static Quote fetch(String sym) throws InterruptedException {
    IN_FLIGHT.acquire();                       // 满了就在这里排队（廉价地阻塞）
    try {
        Thread.sleep(50);                      // 模拟网络
        return new Quote(sym, 10_000 + h, 10_001 + h);
    } finally { IN_FLIGHT.release(); }
}
```

实测输出：

```
取回 500 个行情, 第一个 = Quote[symbol=SYM0, bidTicks=14713, askTicks=14714]
最大同时在途 = 20 (上限 20), 总耗时约 3813 ms
```

最大并发恰好 20，守住了下游上限。耗时 3813 ms 比理论 1250 ms 大得多，原因有二：本机 sleep 偏长（见 1.3），以及这次运行时机器上还有别的编译任务在跑
（`uptime` 负载 4.9）。**这里想说明的是「限流变成了显式的、可读的一行」，不是性能数字。**

### 对照实验 A：pinning（`J10Ex4Pinning.java`）

把调度器限制到 2 个载体，8 个虚拟线程各自「持有一把自己的锁，睡 200ms」。锁互相独立，所以没有任何锁竞争，差别只来自「是否 pin」：

```
$ java --enable-preview -Djdk.virtualThreadScheduler.parallelism=2 -Djdk.virtualThreadScheduler.maxPoolSize=2 J10Ex4Pinning
carrier 并行度 = 2
ReentrantLock 内 sleep: 312 ms
synchronized 内 sleep : 1324 ms
```

* `ReentrantLock` 版：线程睡着时被卸载，2 个载体轮流服务 8 个虚拟线程，总耗时≈一次 sleep（本机 ~300ms）。
* `synchronized` 版：睡着的线程**抱着载体不放**，2 个载体一次只能睡 2 个，8 个要 4 批，≈ 4 × 330 ≈ 1300 ms。

打开诊断可以看到是谁被钉住（`-Djdk.tracePinnedThreads=short`）：

```
VirtualThread[#39]/runnable@ForkJoinPool-1-worker-1 reason:MONITOR
    J10Ex4Pinning.lambda$timeIt$0(J10Ex4Pinning.java:24) <== monitors:1
```

`reason:MONITOR` = 因为持有 monitor（`synchronized`）；`<== monitors:1` 标出是哪一行的栈帧持有它。

### 对照实验 B：CPU 密集不该用（`J10Ex5CpuBound.java`）

24 个纯计算任务（每个 2 亿步 xorshift），12 核机器：

```
cores = 12
固定池(核数): 1214 ms
虚拟线程    : 1554 ms
```

虚拟线程**没有更快**（略慢是因为负载噪声 + 调度开销；两者的并行度上限都是 12 个核）。原因在 6 节讲。

---

## 5. 坑与限制

### 5.1 Pinning：JDK 21 里 `synchronized` 会钉住载体

**定义**：虚拟线程在**无法卸载**的状态下阻塞，就叫被钉住（pinned）——它和载体绑死，载体也陪着睡。
JDK 21 里两个主要原因：

1. 阻塞发生在 `synchronized` 块/方法**里面**（或 `Object.wait()`）。原因是 JVM 的 monitor 实现把「谁持有锁」记在**OS 线程**的栈帧上，
   把栈拷走会让锁的归属乱掉，所以 JDK 21 选择不卸载。
2. 栈上有 native 帧（如 JNI、FFM 下行调用回调到 Java 再阻塞）。

**注意不是「用了 `synchronized` 就有问题」**：`synchronized` 里只做内存里的短操作（`counter++`）完全没事，因为没有阻塞，也就没有「该卸载而不能卸载」。
问题是 **在 `synchronized` 里做 I/O 或 sleep**。

**症状**：吞吐莫名其妙被限制在核数；载体全被钉住时，其他虚拟线程饿死。极端情况：所有载体都被钉住的线程占着，而它们等的事件要靠另一个（没载体可跑的）虚拟线程来触发，就死锁。

**对策（JDK 21）**：

* 把「持锁时阻塞」的 `synchronized` 改成 `ReentrantLock`（`lock()/unlock()` 放 `try/finally`）。`ReentrantLock` 基于 `LockSupport.park`，可卸载。
* 自己的代码改，第三方库里的 `synchronized` 无能为力（老 JDBC 驱动曾经是重灾区；升级驱动）。
* 诊断：`-Djdk.tracePinnedThreads=full|short`（打印被钉住时的栈，见 4 节）；或 JFR 事件 `jdk.VirtualThreadPinned`（持续时间超过阈值，默认 20ms，才记录）。

**后续版本**：**JDK 24 的 JEP 491 "Synchronize Virtual Threads without Pinning"** 让虚拟线程在 `synchronized` 里阻塞也能卸载，
`Object.wait()` 同样。仍然 pin 的情形：栈上有 native 帧；类初始化器（`static {}`）里阻塞或等别的线程初始化类。
同时 `jdk.tracePinnedThreads` 被移除，只保留 JFR 事件 `jdk.VirtualThreadPinned`。出处：https://openjdk.org/jeps/491
**面试话术**：「在 21 里持锁阻塞要用 `ReentrantLock`；24 起 `synchronized` 不再 pin，但我们的目标版本是 21，所以按 21 的规则写。」

### 5.2 CPU 密集不是虚拟线程的用武之地

虚拟线程解决的是「**线程太多、大多数在等**」。如果任务都在算，瓶颈是**核数**，不是线程数：

* 12 核最多同时算 12 件事，开 100 万个虚拟线程也不会算得更快；
* 调度是协作式的，一个死循环的虚拟线程会占住一个载体，没有时间片抢占；
* 所以 CPU 密集用固定大小 = 核数的池（或 `ForkJoinPool`、并行流）。

判断口诀：**任务里 `等` 的时间占比越高，虚拟线程收益越大。** Little 定律里并发数 = 吞吐 × 耗时，耗时全是计算时，并发数封顶于核数。

### 5.3 不要池化虚拟线程

池化的目的是复用昂贵的东西。虚拟线程不贵，池化它反而引入排队。**虚拟线程就是用来 `new` 的。**
想限制并发，用 `Semaphore`（2.4），不要限制线程数。

### 5.4 `ThreadLocal` 可以用，但别把它当缓存

每个虚拟线程有自己的 `ThreadLocal` 副本。一百万个虚拟线程 = 一百万份。如果你原来靠「线程池 50 个线程 → 50 份 `SimpleDateFormat`/缓冲区」来省内存，
换成虚拟线程后这个假设崩了。要传请求上下文，J12 的 `ScopedValue`（预览）是新方案。

### 5.5 无界并发会压垮下游

以前线程池是天然的闸门。去掉它，10 万个虚拟线程同时打向数据库会直接把连接池打满。**永远要有显式的并发上限**（`Semaphore`、连接池大小、令牌桶）。

### 5.6 栈很深的虚拟线程、大量活跃线程的 GC 代价

每个虚拟线程的栈是堆对象。几十万个活跃虚拟线程各带几 KB 栈，堆压力和 GC 扫描都会增加。这是用 ZGC/G1 调堆时要考虑的新因素（见 J19）。

### 5.7 线程 dump

`jstack` 看不到虚拟线程。要用 `jcmd <pid> Thread.dump_to_file -format=json <file>`（JDK 21 新增）。

---

## 6. 在本 kit 哪里用到

**`loop/rounds/01_video/hc02_merge_k_streams/reference/ConcurrentMerge.java` 第 118–131 行**：k 路合并，每路数据源一个生产者。

```java
// 虚拟线程：source 的 hasNext 可能阻塞在 I/O 上，虚拟线程阻塞时不占 OS 线程，开 k 个很便宜
producers.add(Thread.ofVirtual().name("merge-producer-" + i).start(() -> {
    try {
        produce(idx, src, q);
    } catch (InterruptedException _) {
        // close() 叫我们走：不需要终止标记，没人在听了
    } catch (Throwable t) { ... q.put(new Failed<>(t)) ... }
}));
```

为什么对：每个生产者的大部分时间阻塞在 `q.put(...)`（有界队列满了等消费者）或数据源的 I/O 上——正是「等」占多数的场景。
`ArrayBlockingQueue.put` 基于 `ReentrantLock` + `Condition`，所以阻塞时虚拟线程会卸载，不 pin。注意 `close()` 里 `producers.forEach(Thread::interrupt)` 与
`t.join(Duration.ofSeconds(1))`：虚拟线程同样支持中断和 `join(Duration)`。第 192 行 `Thread.ofVirtual().factory()` 把虚拟线程工厂交给 `StructuredTaskScope`，见 J11。

**`loop/rounds/01_video/hc03_recursive_sum/reference/RecursiveSum.java` 第 285–287 行**：

```java
/** 每块一个虚拟线程（StructuredTaskScope，预览 API）。正确，但 CPU 密集任务并不该用它：
 *  虚拟线程只是多路复用在 carrier（= 核数个平台线程）上，不会多出并行度，也不会时间片抢占。 */
```

这是 5.2 的正面例子：对数组求和是纯计算，kit 里同一题同时提供了 `parallelSumStream`（ForkJoinPool）和 `sumVirtual`，前者才是该用的。

面试时被问「为什么这里用虚拟线程」：答「生产者阻塞在 I/O 和有界队列上，是 I/O 型」；被问「为什么求和不用」：答「CPU 密集，瓶颈是核数」。

---

## 7. 自测题

1. 解释 Little 定律，并用它说明「每秒 5 万请求、每个 200ms、全在等网络」需要多少并发，为什么平台线程池难以满足。
2. 虚拟线程、载体线程、续体分别是什么？一个虚拟线程调 `Thread.sleep(100)` 时，从被挂载到再次被挂载，发生了哪几步？
3. 为什么说「虚拟线程不适合 CPU 密集任务」？给出两条理由。
4. 在 JDK 21 里，下面哪些会 pin？(a) `synchronized(lock) { counter++; }` (b) `synchronized(lock) { Thread.sleep(50); }` (c) `lock.lock(); try { Thread.sleep(50); } finally { lock.unlock(); }`（`lock` 是 `ReentrantLock`）(d) 文件 `FileInputStream.read`
5. 代码里原来用 `newFixedThreadPool(20)` 顺便限制了对下游的并发，换成 `newVirtualThreadPerTaskExecutor()` 后应该怎么保持这个上限？

<details><summary>答案</summary>

1. 同时在途数 = 吞吐 × 耗时 = 50 000 × 0.2 = 10 000。平台线程要 1 万个 OS 线程：每个预留约 1 MB 栈、内核要调度它们、上下文切换频繁，不现实；虚拟线程 1 万个只是 1 万个堆对象。
2. 虚拟线程 = 堆上的 `VirtualThread` 对象，代表一段可暂停的执行；载体线程 = 真正的 OS 线程（调度器 ForkJoinPool 的 worker，默认核数个）；续体 = JVM 把整条调用栈冻结/解冻的机制。
   步骤：挂载到载体运行 → `sleep` 内部调用 park → 栈帧拷到堆（StackChunk），虚拟线程卸载，载体去跑别人 → 定时器到点 unpark，虚拟线程重新提交给调度器 → 某个载体空闲时再挂载，从 `sleep` 返回处继续。
3. 一是并行度上限是核数，再多线程也没有更多 CPU；二是调度协作式，只在阻塞时让出，长计算会霸占载体，没有时间片抢占（J10Ex5：24 个计算任务，固定池 1214 ms，虚拟线程 1554 ms，没有更快）。
4. (a) 不 pin（没阻塞）；(b) pin；(c) 不 pin；(d) 文件 I/O 不卸载，载体被占住（调度器会补偿性多开载体），严格说是「载体被占」而非 monitor 引起的 pin。
5. 用 `Semaphore(20)`：`acquire()` 在调用下游之前，`release()` 放 `finally`（例 3）。或者用大小为 20 的连接池/客户端并发限制。

</details>

---

## 8. 延伸阅读

* JEP 444 Virtual Threads — https://openjdk.org/jeps/444 —— 动机、「不要池化」「不要用于 CPU 密集」的官方说法，读 Description 里关于 `ThreadLocal` 与 pinning 的小节。
* JEP 425 / JEP 436（预览）— https://openjdk.org/jeps/425 、https://openjdk.org/jeps/436 —— 看设计演进。
* JEP 491 Synchronize Virtual Threads without Pinning — https://openjdk.org/jeps/491 —— JDK 24 起 `synchronized` 不再 pin，以及仍然会 pin 的情形。
* Oracle JDK 21 Core Libraries 指南「Virtual Threads」— https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html —— 官方使用指南，含 `jcmd` 线程 dump 的用法。
* `java.lang.Thread` Javadoc — https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Thread.html —— `Thread.Builder` 全部方法。
