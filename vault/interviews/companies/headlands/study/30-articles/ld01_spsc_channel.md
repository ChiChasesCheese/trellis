# ld01 · 共享内存 SPSC 消息通道 —— 讲义

> 题面：`loop/rounds/03_lld/ld01_spsc_channel/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/`（`LongRing` `SpscLongRing` `MessageRing` `SharedChannel`）
> 实验代码：`study/30-articles/examples/ld01/FalseSharingBench.java`（单独量伪共享）、`SpscBench.java`（SPSC 五种写法）。本文的"实测"来自这两个程序和测试套件在本机（Apple M 系列，12 核，JDK 21.0.12）的运行。
> 写法说明见 `study/TEXTBOOK.md`。这一篇要从"进程是什么、共享内存是什么"讲起。

---

## 1. 这道题在问什么

你有两个**独立运行的程序**（两个进程）：一个不停地产生消息（比如行情），一个不停地消费消息（比如策略）。两个程序各有自己的内存，**互相看不到对方的变量**。你要设计一个**通道**，让消息从前者流到后者：

* **有界**：通道只能装有限多条，满了要明确告诉生产者"满了"，不能无限增长；
* **FIFO**：先进先出，不丢、不重、不乱序；
* **要快**：热路径上不加锁、不做系统调用、不拷贝多次；
* **三种状态要明确**：满（full）、空（empty）、**读完了**（drained：生产者宣布不再有消息，且消费者已经读完所有消息）。

题面原文只有一句：

> bounded shared-memory message channel between two processes, with safe record ownership, FIFO delivery and explicit full, empty and drained…

"单写者单读者"（SPSC，single-producer single-consumer）是关键约束：**只有一个生产者、一个消费者**。这个约束让我们可以不用锁、也不用 CAS。

### 手算一遍（容量 4 的环形缓冲区）

用一个长度 4 的数组当"环"。`head` 是消费者下一个要读的计数，`tail` 是生产者下一个要写的计数；下标 = 计数 `& 3`（取低 2 位，等价于 `% 4`）：

```
 offer(10): buf[0]=10  tail=1      数组 [10, _, _, _]  head=0 tail=1   size=1
 offer(20): buf[1]=20  tail=2      数组 [10,20, _, _]  head=0 tail=2   size=2
 offer(30): buf[2]=30  tail=3
 offer(40): buf[3]=40  tail=4      数组 [10,20,30,40]  head=0 tail=4   size=4  ← 满: tail-head == 4
 offer(50): 满了 → 返回 false
 poll():    读 buf[0]=10  head=1   数组 [10,20,30,40]  head=1 tail=4   size=3
 offer(50): buf[4&3=0]=50 tail=5   数组 [50,20,30,40]  head=1 tail=5   size=4  ← 回绕: 写到了数组开头
 poll() 依次得 20, 30, 40, 50 
```

### 四个 Part 怎么递进

(后三步是我们的 **(reconstructed)** 推断，不是证据)

1. **Part 1**：单线程的环形缓冲区，`long` 元素。满 / 空怎么区分？为什么容量要是 2 的幂？
2. **Part 2**：两个**线程**共享它。不加锁怎么保证正确？（内存序，`setRelease`/`getAcquire`。）怎么让它更快？（cached index、填充防伪共享。）怎么**证明**更快？（测量。）
3. **Part 3**：消息变长了：长度前缀、对齐、回绕时一条记录放不下怎么办？
4. **Part 4**：把环放进**内存映射文件**，让两个独立的 JVM 进程各映射一份。怎么测试它？

---

## 2. 前置知识

### 2.1 进程、线程与进程间通信

`study/00-foundations/os_processes_threads_ipc.md` 有完整讲解；这里只列本题需要的结论：

* **线程**共享同一个进程的内存：线程 A 写一个字段，线程 B 能直接读到（要注意"可见性"，见 2.5）。
* **进程**之间默认**隔离**：每个进程有自己的**虚拟地址空间**，进程 A 的地址 `0x1000` 和进程 B 的地址 `0x1000` 通常指向完全不同的物理内存。进程 A 想给 B 传数据，必须通过操作系统提供的**进程间通信**（IPC）：管道（pipe）、套接字（socket）、消息队列、**共享内存**。
* 管道和套接字每传一次都要经过**系统调用**（`write`/`read`），数据在内核缓冲区里被**拷贝**一到两次，还可能让线程睡眠、唤醒。**共享内存**让操作系统把同一批物理页映射进两个进程的地址空间，之后双方直接读写，没有系统调用、没有拷贝，延迟低一个数量级——这是低延迟系统首选共享内存的原因。

### 2.2 共享内存与内存映射文件（mmap）

**是什么**：`mmap`（memory map）是操作系统提供的一个调用：把一个文件（或一块匿名内存）的内容**映射**到进程的虚拟地址空间里，像访问数组一样访问文件。

**为什么能用来做进程间共享**：如果两个进程用 `MAP_SHARED` 方式映射**同一个文件**，操作系统让两个进程的虚拟页指向同一批**物理页**（页缓存，page cache）：

```
  进程 A 的虚拟地址空间             物理内存（页缓存）              进程 B 的虚拟地址空间
  ┌───────────────┐                                              ┌───────────────┐
  │  0x7f00...页0 ─┼──────────►  ┌──────────────┐ ◄─────────────┼─ 0x7e00...页0  │
  │  0x7f00...页1 ─┼──────────►  │ 同一批物理页  │ ◄─────────────┼─ 0x7e00...页1  │
  └───────────────┘              └──────┬───────┘               └───────────────┘
                                        │ 内核按需写回
                                        ▼
                                     磁盘文件
```

A 写一个字节，B 立刻能读到（CPU 缓存一致性保证，见 2.6），中间没有任何系统调用。文件在这里只是"双方约定的会合点"；也可以用 `/dev/shm`、`shm_open`。用文件的好处：跨平台、测试容易清理、**进程崩溃后数据还在**。

**注意**：第一次访问某一页时会触发**缺页**（page fault），由内核分配或读入物理页——这是一次性的成本，热路径上稳定后不再发生。

**Java 里怎么写**（JDK 21，FFM 预览）：

```java
try (FileChannel ch = FileChannel.open(file, CREATE, READ, WRITE);
     Arena arena = Arena.ofShared()) {
    MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, size, arena);   // 文件被扩展到 size，新增部分全零
    seg.set(ValueLayout.JAVA_INT_UNALIGNED, 12, 1);
}   // arena.close() = 取消映射（munmap）；文件还在磁盘上
```

老办法 `FileChannel.map(...)` 返回 `MappedByteBuffer`：大小限于 2 GiB（`int` 索引）、没有确定性的取消映射。详见 `study/10-java21/J17_ffm_api.md`。

### 2.3 环形缓冲区（ring buffer）从零讲

#### 为什么需要它

想要一个"先进先出、容量固定"的队列，最直观的是数组 + 移动元素：

```
poll(): 取 buf[0]，然后把 buf[1..n-1] 全部往前挪一格      ← O(n)，每次都挪，太慢
```

**环形**的想法：不挪元素，挪**指针**。读指针（head）只往前走，到数组尾部就绕回开头。

#### 怎么区分"满"和"空"

最经典的陷阱：如果 `head`、`tail` 都存"数组下标"（0..capacity-1），那么 `head == tail` 既可能表示空，也可能表示满（写了一圈追上了读）。常见补救：

* 永远空一个槽位不用（容量 n 的数组只能放 n-1 个）；
* 另存一个 `size` 变量（但 `size` 被两个线程同时改，并发时就要原子操作）。

**更好的办法：让 `head`、`tail` 是只增不减的计数**（"自由增长"，free-running）。真正的数组下标是计数对容量取模：

```
空  ⇔  tail - head == 0
满  ⇔  tail - head == capacity
元素个数 = tail - head
下标 = 计数 mod capacity
```

两种状态天然不同，不浪费槽位，也不需要 `size`。`long` 计数每纳秒加 1 要 29 万年才溢出，不用担心。

#### 为什么容量要是 2 的幂：`& mask`

`计数 % capacity` 要做一次整数除法（几十个时钟周期）。当 `capacity = 2^k` 时，取模等价于**只保留二进制的低 k 位**，用一次按位与：

```
capacity = 8 = 0b1000        mask = capacity - 1 = 0b0111
计数 13 = 0b1101
13 & 0b0111 = 0b0101 = 5     与 13 % 8 = 5 相同
```

Java 里：`buf[(int) (count & mask)]`。检查 2 的幂：`Integer.bitCount(capacity) == 1`（二进制里只有一个 1）。

对**负数**取模和按位与结果不同，但我们的计数永远非负，没有这个问题。

### 2.4 为什么 SPSC 不需要锁，也不需要 CAS

并发的难点是"两个线程同时改同一个变量"。看我们的环里每个变量**谁写**：

| 变量 | 谁写 | 谁读 |
|---|---|---|
| `tail` | **只有**生产者 | 生产者自己、消费者 |
| `head` | **只有**消费者 | 消费者自己、生产者 |
| `buf[i]` | 生产者（在槽位空闲时） | 消费者（在槽位有数据时） |

每个变量**只有一个写者**——没有"两个人同时改"的情况，所以不需要互斥（锁）或原子的"读-改-写"（CAS）。唯一要解决的是：写者写完之后，读者**什么时候**、**以什么顺序**看得到。这是 2.5 的问题。

多生产者就不一样了：两个生产者都要改 `tail`，必须 CAS 竞争。所以 SPSC 是最容易做到极致的并发队列。这是 LMAX Disruptor 等系统大量使用"单写者原则"（single-writer principle）的原因。

### 2.5 内存序：为什么"先写数据再改 tail"还不够

`study/10-java21/J16_concurrency_primitives.md` §1 详细讲了原因，这里只写本题的推论。

现代 CPU 和编译器为了快，会**重排**没有依赖关系的读写；每个核心有**写缓冲**（store buffer），写操作先进缓冲、之后才对别的核心可见；而且别的核心看到这些写的**顺序**不一定和程序顺序相同。生产者的两行：

```java
buf[i] = v;            // ① 写数据
tail = t + 1;          // ② 发布
```

在"弱内存序"的 CPU（ARM，包括 Apple M 系列）上，其他核心可能**先看到 ② 再看到 ①**：消费者看到 `tail` 变了，去读 `buf[i]`，读到的却是旧数据。**我们在本机实测过**：把 `SpscLongRing` 里的 `TAIL.setRelease(this, t + 1)` 换成普通写 `tail = t + 1`，`SpscLongRingTest` 立刻大面积变红（"first mismatch at seq 369 / 7477 / 13918 / 154157" 之类，消费者读到了上一圈残留的值）。x86 的内存序更强，同样的代码常常"碰巧"是对的——**在 x86 上测试通过不代表对**。

解决：用 **release / acquire** 配对（J16 §2.4）：

* `setRelease(x, v)`：**在它之前的**所有读写，不会被重排到它之后。一道向上的单向门。
* `getAcquire(x)`：**在它之后的**所有读写，不会被重排到它之前。一道向下的单向门。
* 如果消费者的 `getAcquire(tail)` **读到了**生产者的 `setRelease(tail, t+1)` 写下的值，那么生产者在这次 release 之前写的一切（包括 `buf[i]`），消费者在这次 acquire 之后都看得到。

```
生产者:  buf[i] = v;                     // ① 数据
         TAIL.setRelease(t + 1);         // ② release：①不能被重排到②之后
消费者:  t = TAIL.getAcquire();          // ③ acquire：④不能被重排到③之前
         v = buf[i];                     // ④
```

反方向同样需要：消费者读完 `buf[i]` 之后才能 `HEAD.setRelease(h + 1)`，生产者 `HEAD.getAcquire` 看到新 `head` 后才敢覆盖这个槽位——否则生产者可能在消费者读完之前就写进去（"消费者读到的是新值"，丢了一条消息）。

**为什么不直接用 `volatile`**：`volatile` 提供更强的"顺序一致"，多付出一次禁止"写后读"重排的代价（x86 上要 `lock` 前缀指令或 `mfence`）；release/acquire 在 x86 上就是普通 `mov`（x86 本来就不重排 Load-Load / Store-Store），只对编译器起约束作用，没有额外的 CPU 栅栏。见 J16 §2.4。

**跨进程怎么办？** Java 内存模型（JMM）的规范讨论的是同一个程序内的线程。两个**进程**共享同一块物理内存时，硬件的缓存一致性和内存序规则同样适用，`VarHandle.setRelease`/`getAcquire` 编译出来的是同样的屏障指令，无论目标是堆上的数组还是映射的文件。所以"先写数据再 release 发布 tail，对方 acquire 读 tail 再读数据"的协议跨进程同样成立。但这是**基于硬件与 JIT 实现**的推理，不是 JMM 的形式化保证——面试时可以这样说，不要说得太绝对。

### 2.6 缓存一致性、伪共享与 cached index

#### 缓存一致性（一段话）

每个 CPU 核心有自己的缓存，数据按**缓存行**（cache line，x86 常见 64 字节，Apple M 系列 128 字节）为单位搬运。多核要保持一致，协议（MESI 一类）规定：某个核心要**写**一条缓存行时，必须先让别的核心里的副本**失效**；别的核心再读它，就要重新从写者那里取。这个"跨核搬运"一次大约几十纳秒——比一次普通运算慢两个数量级。详见 `study/00-foundations/cpu_cache_locality.md`。

#### 伪共享（false sharing）

如果线程 A 只写变量 `a`，线程 B 只写变量 `b`，`a` 和 `b` 恰好在**同一条缓存行**里：A 每写一次就让 B 的副本失效，B 每写一次又让 A 的失效。两个逻辑上毫不相干的变量，在硬件层面却在**抢同一块东西**。这叫伪共享。

在我们的环里：`tail`（生产者写）和 `head`（消费者写）如果相邻，每次 `offer` 都会把消费者核心里的 `head` 所在行弄失效，每次 `poll` 反过来。

**解决**：**填充**（padding）——让两个变量相隔至少一条缓存行。

#### cached index（缓存对方的下标）

即使 `tail` 和 `head` 已经分开，生产者每次 `offer` 仍要读 `head` 判断满不满——而 `head` 所在的缓存行是消费者在写的，每次读都要跨核搬运。

**观察**：`head` 只增不减。生产者保存一份旧的 `head`（`cachedHead`）。用旧值算出的"剩余空位"**只会偏小，不会偏大**——所以"旧值看起来有空位"一定是真的有空位；只有"旧值看起来满了"才需要去读真正的 `head` 刷新缓存。消费者对 `tail` 同理（`tail` 只增不减，旧值只会让它低估数据量）。

效果：只要队列不是几乎满 / 几乎空，一批消息只触碰一次对方的缓存行，不是每条消息一次。

### 2.7 变长消息：长度前缀、对齐与回绕

#### 长度前缀（length prefix）

变长消息放进字节环：每条消息写成 `[长度: 4 字节][payload]`。读的人先读 4 字节长度，再读那么多字节。

#### 对齐

把每条记录补零到 **8 字节**的倍数（`(4 + len + 7) & ~7`）。好处：记录总是从 8 的倍数偏移开始，所以 4 字节的长度字段永远不会跨越数据区末尾（末尾也是 8 的倍数）；`int`/`long` 读写保持对齐。

#### 回绕（wrap-around）

数据区是个环，但**一条记录必须是连续的**（读的人想要一段连续字节，我们不想把消息切成两半拼起来）。当前位置到数组末尾放不下整条记录时：

```
capacity = 64，tail 在 48，要写一条 24 字节的记录，到末尾只剩 16 字节：

  0                                      48        64
  │ ........ 已被消费的 ........ │  │ 空 16 字节 │ 
                                          ▲
              ① 在这里写一条 PAD 记录 [len=-1]，占满剩下的 16 字节
              ② 然后从偏移 0 开始写真正的 24 字节记录

  消费者读到 len == -1 就知道"这一段是填充，直接跳到开头"
```

**PAD 要单独发布**——这是这道题最容易踩的坑，见 §4.3。

### 2.8 drained：怎么让消费者知道"真的结束了"

消费者 `poll()` 返回 `null`，有两种可能：(1) 现在没有，一会儿还有；(2) 永远不会有了。两者必须能区分，否则消费者要么永远等，要么提前退出丢消息。

办法：头部放一个 `closed` 标志，生产者 `finish()` 时置 1。消费者的 `isDrained()` = `closed == 1` **并且** `head == tail`。

**顺序很重要**：生产者先发布最后一次 `tail`，再置 `closed`。消费者必须**先读 `closed` 再读 `tail`**：看到 `closed == 1` 就保证（通过 release/acquire）看得到最终的 `tail`。反过来先读 `tail`：可能读到旧 `tail`（空），然后生产者发布了最后几条并置了 `closed`，消费者再读 `closed == 1` ——误判 drained，丢掉最后几条。

### 2.9 怎么测试"两个进程"

挑战：

1. **找到 `java`**：`ProcessHandle.current().info().command()` 给出当前 JVM 的可执行文件路径（`Optional<String>`，取不到就用 `java.home/bin/java`）。
2. **类路径**：子进程要能找到被测类。`System.getProperty("java.class.path")` 是当前 JVM 的类路径。**但**用 JUnit console 的 `--class-path` 参数跑测试时，`java.class.path` 只有 JUnit 的 jar（被测类由另一个类加载器从 `--class-path` 目录加载）。所以还要加上被测类实际所在的位置：`SharedChannel.class.getProtectionDomain().getCodeSource().getLocation()`。两者取并集、去重。
3. **预览特性**：FFM 在 JDK 21 是预览，子进程要 `--enable-preview`。
4. **不挂死**：任何一端出错，另一端的自旋循环会永远转下去。所以每个自旋循环都带**截止时间**（`System.nanoTime()` 比较，每 1024 圈检查一次），父进程 `waitFor(超时)`，超时就 `destroyForcibly()`。**测试不能依赖 `Thread.sleep` 来对时序**。
5. **能抓到"丢 / 重 / 乱序"**：每条消息的长度和内容完全由序号决定（`Msgs.make(seq)`：splitmix64 哈希出长度 8..56 和内容，前 8 字节是序号）。收的人只靠"我期待第 `seq` 条"就能校验，不需要额外信息。丢一条 → 序号对不上；重复 → 对不上；乱序 → 对不上；截断 / 损坏 → 内容对不上。最后还要验证"恰好 count 条且 isDrained"，抓多发。

---

## 3. 从最笨的解法开始

**最笨 1**：`ArrayList` 当队列，`remove(0)` 取头。每次取头把后面所有元素前移，O(n)；而且只能在一个进程里用，不能跨进程。

**最笨 2**：线程之间用 `java.util.concurrent.ArrayBlockingQueue`（内部是锁 + 条件变量）。线程间没问题，但：(a) 加锁，竞争时线程睡眠 / 唤醒要系统调用，延迟抖动；(b) **根本跨不了进程**——它的数据在一个 JVM 的堆里。

**最笨 3**：进程之间用套接字 / 管道发消息。能跨进程，但每条消息 = 一次 `write` + 一次 `read`，两次系统调用 + 拷贝，延迟在微秒量级；而且消息边界要自己处理。

**最笨 4**：环形缓冲区，下标 `head`/`tail` 取模存，空一个槽位或另存 `size`。可以工作，但 `%` 慢、浪费槽位 / `size` 被两个线程改。

**最笨 5**：环形缓冲区，`head`/`tail` 都是 `volatile`，每次 `offer`/`poll` 都读对方的 `volatile`。正确，但慢：每次读对方变量都是一次跨核搬运，`volatile` 写在 x86 上还要全栅栏。本机实测约 **31–49 M 条/秒**（见 §4.2）——对大多数程序已经够快，但与优化版相比有差距，并且更重要的是：它仍然不能跨进程。

---

## 4. 一步一步改进

### 4.1 Part 1：从移动元素到自由增长的计数

1. **发现问题**：数组队列 `poll` 要挪 n 个元素，O(n)。
2. **想法**：不挪元素，挪指针；指针到末尾绕回开头（环形）。
3. **新问题**：`head == tail` 既可能空也可能满。
4. **想法**：`head`、`tail` 不存下标，存只增不减的计数；下标由计数取模得到。空 ⇔ `tail - head == 0`，满 ⇔ `== capacity`。
5. **新问题**：`%` 慢。
6. **想法**：容量取 2 的幂，用 `& (capacity - 1)`（§2.3）。
7. **新复杂度**：`offer`/`poll` O(1)，无除法，不浪费槽位。

```java
public boolean offer(long value) {
    if (tail - head == buf.length) return false;
    buf[(int) (tail & mask)] = value;
    tail++;
    return true;
}
```

`poll` 在空队列上抛 `NoSuchElementException`：`long` 的每个取值都可能是合法消息，没有哪个值能当哨兵，所以不能用"返回某个特殊值表示空"。想自旋等待的消费者写 `while (q.isEmpty()) Thread.onSpinWait(); q.poll();`，SPSC 下是安全的（只有消费者能让队列变空，所以 `isEmpty()` 为 `false` 后直到消费者自己 `poll` 它都不会再变空）。

### 4.2 Part 2：从单线程到两线程

**步骤 1：什么都不加会怎样？** 让 `LongRing` 直接被两个线程用，`head`/`tail` 是普通字段。两种失败：(a) **可见性**：消费者的循环 `while (isEmpty())` 里，JIT 可以把对普通字段 `tail` 的读提到循环外（"反正没人在这个线程里改它"），永远读不到新值——死循环；(b) **顺序**：§2.5 的 ①②重排。

**步骤 2：`volatile`**。`head`、`tail` 声明成 `volatile`：可见性和顺序都对了（`SpscBench` 的 A 版）。

**步骤 3：release / acquire**。用 `VarHandle` 的 `setRelease`/`getAcquire` 代替 `volatile`（B 版）。在 x86 上这是真正的省（省掉全栅栏）；据 J16 的说明，HotSpot 在 AArch64 上把两者都编成 `ldar`/`stlr`，差别应该很小（我们没有反汇编验证）。

**步骤 4：cached index**（§2.6）。D 版：A/B 的每次 `offer`/`poll` 都读对方的变量，D 只在"旧值看起来满 / 空"时才读。

**步骤 5：填充**。C 版 = B + 填充；E 版 = D + 填充（就是参考解 `SpscLongRing` 的写法）。

**五种写法的实测**（`SpscBench`：每种传 5000 万个 `long`，容量 1024；单位百万条/秒；下表是 6 次独立运行，每次五种各取 5 轮里最好的一轮，再对 6 次运行取中位数）：

| 写法 | 中位数 | 6 次运行的范围 |
|---|---|---|
| A volatile | 38 | 31 – 49 |
| B acq/rel | 34 | 29 – 49 |
| C acq/rel + 填充 | 27.5 | 27 – 30 |
| D acq/rel + cache | 34 | 29 – 40 |
| E acq/rel + cache + 填充 | **44** | 31 – 48 |

怎么读：

* **E 的中位数最高**（44 对 34 – 38），但范围（31 – 48）和 A、B 大面积重叠——收益存在，**不显著**。
* C（只填充、不缓存）的结果很稳、也最低（27 – 30）。我们**没有深究**为什么；一个猜测是：不缓存时每条消息仍然要读一次对方的行，而填充把"顺手带过来"的同行数据也拿走了。这只是猜测，不要在面试里当结论说。
* **范围很宽**是这台机器的特点：Apple M 系列有性能核（P）和能效核（E），macOS 不允许把线程固定到核心，调度器会在运行中把生产者和消费者放到不同核心簇。碰巧在同一簇上时跨核搬运很快，落在不同簇上就慢。**做微基准时，说清"测的是什么、噪声多大、取的是中位数还是最大值"，比报一个最大值诚实得多。**

> 所以填充的效果要**单独**量：`FalseSharingBench`。两个线程各自对"自己的计数器"做 2 亿次 `setOpaque` 自增，互不相干：
>
> | 布局 | 6 轮（ms，排序后） | 中位数 |
> |---|---|---|
> | 相邻（同一缓存行） | 821, 822, 1457, 1755, 1775, 1811 | 1606 |
> | 相隔 128 字节以上 | 790, 800, 802, 838, 933, 1090 | 820 |
> | （第二次运行）相邻 | 831, 834, 1698, 1817, 1844, 1867 | 1757 |
> | （第二次运行）分开 | 798, 802, 893, 942, 965, 1084 | 917 |
>
> **相邻的慢约 2 倍**（两次运行都是）；而且相邻那一行呈**双峰**：前两轮 ~820（两个线程碰巧在同一个核心簇上，缓存行在簇内共享）、后四轮 ~1800（落在不同簇上，必须跨簇搬运）。分开的一直很快。这才是伪共享的干净证据。

**所以填充为什么还要在 SPSC 里做**：它在这台机器上的收益被噪声盖住，但 (a) 伪共享的代价是真实且大的（上表）；(b) 对象的字段布局取决于你写了什么字段、JVM 怎么排，不做填充就**无法控制**它们是否同行；(c) 在 x86 的服务器上（64 字节缓存行，核心间延迟更稳定）这类优化的收益通常更明显。面试时的说法：「我会填充，因为代价小、风险大；我用 `FalseSharingBench` 这样的单变量实验验证过它的真实性，而且我知道我测到的 SPSC 吞吐差异在这台机器上淹没在噪声里。」

**Java 里怎么做填充**：Java 没有 `alignas`。常用办法是**继承链 + 填充 `long`**。JVM 总是把父类的字段排在子类字段之前，且不会跨类重排字段，所以：

```java
abstract class RingBase      { final long[] buf; final int mask; }          // 只读，两个线程都读
abstract class PadA extends RingBase { long a01, ..., a15; }                // 15 个 long = 120 字节
abstract class ProducerFields extends PadA { long tail; long cachedHead; }  // 只有生产者写
abstract class PadB extends ProducerFields { long b01, ..., b15; }
abstract class ConsumerFields extends PadB { long head; long cachedTail; }  // 只有消费者写
abstract class PadC extends ConsumerFields { long c01, ..., c15; }
public final class SpscLongRing extends PadC implements LongQueue { ... }
```

`buf`/`mask` 放在最前面的基类：它们只读，如果和 `head` 同一行，消费者写 `head` 会让生产者的 `buf` 副本失效，每次 `offer` 都要重新取 `buf` 引用。JDK 内部用 `@jdk.internal.vm.annotation.Contended`；用户代码需要 `-XX:-RestrictContended`，所以用继承技巧。

### 4.3 Part 3：变长消息

#### 步骤 1：把 `long[]` 换成字节环 + 长度前缀

`head`/`tail` 现在是**字节**计数；记录 `[len:int32][payload][补零到 8 字节对齐]`；记录总长 `recordSize(len) = (4 + len + 7) & ~7`；最大消息 `maxPayload = capacity - 4`（一条记录得能整个放进空环里）。

#### 步骤 2：回绕——一条记录放不下连续空间

见 §2.7。第一版的想法（**也是错的那个**）：

```
offer(msg):
    if (pad + rec > 空闲字节) return false;      // 先算好总共需要多少，放不下就拒绝
    写 PAD（如果需要）；写记录；发布 tail
```

**这个版本会死锁**（我们是在设计时推演出来的，没有真的实现它）。看这个状态：环是空的（消费者把所有消息都读完了，`head == tail`），但 `tail` 恰好停在偏移 8（`toEnd = 56`），生产者想发一条 `maxPayload` 的大消息（记录 64 字节）：

* 需要 PAD 56 字节 + 记录 64 字节 = 120 > 64（容量）→ 永远 `false`；
* 消费者没东西可读，`head` 不会前进，空间永远不会多出来。

生产者和消费者互相等：**死锁（活性丧失）**。

> 这个性质有一个容易写错的镜像：我们给它写测试时，第一版 `anEmptyRingAcceptsAMaxSizeMessageFromEveryPosition` 假设"空环上连续两次 `offer` 就放得进"，在参考解上红了。原因：参考解确实单独发布了 PAD，但 PAD 占着的字节要等**消费者越过它**（`poll` 返回 `null`）才释放，只调 `offer` 不调 `poll` 当然放不进。测试改成 `offer → poll → offer` 才是正确的活性性质：它要求**两边同时**做对——(1) 生产者单独发布 PAD；(2) 消费者越过 PAD。

**修复**：PAD **单独发布**。需要 PAD 时，只要有 `toEnd` 字节的空位，就写 PAD、`tail += toEnd`、release 发布，哪怕随后真记录挤不进去（`offer` 返回 `false`）。下一步消费者 `poll` 读到 PAD 就跳到开头，`head` 前进，环重新是"空且 `tail` 在偏移 0"——此时任何 ≤ `maxPayload` 的消息都放得进。代价：`offer` 返回 `false` 时 `tail` 可能已经变了（对消息序列没有影响，但 `bytesPending` 会包含 PAD 字节）。

#### 步骤 3：drained

§2.8。`finish()`：`closed = 1`（release）。`isDrained()`：先 acquire 读 `closed`，再 acquire 读 `tail`，比较 `head`。边界：末尾可能残留一条 PAD（`offer` 发布了 PAD 但真记录没放进，随后 `finish`）——此时 `head != tail`，`isDrained()` 为 `false`；消费者再 `poll` 一次越过 PAD（返回 `null`），之后 `isDrained()` 为 `true`。测试 `trailingPadIsConsumedBeforeDrained` 锁住这一点，所以消费者标准写法是：

```java
while (!ring.isDrained()) {
    byte[] m = ring.poll();
    if (m == null) { Thread.onSpinWait(); continue; }
    handle(m);
}
```

### 4.4 Part 4：放进内存映射文件

**发现问题**：`MessageRing` 建在一个 `MemorySegment` 上，在同一个 JVM 里它可以是 `Arena.allocate` 出来的内存。要给另一个**进程**用，这块内存必须是两个进程都能映射的东西。
**想法**：用内存映射文件（§2.2）。`FileChannel.map(READ_WRITE, 0, size, arena)` 直接返回 `MemorySegment`——`MessageRing` 一行不用改。
**要补的东西**：
* **自描述的头部**：`open` 的一方不知道容量，头部要写 `capacity`、`version`、`magic`。`magic` **最后写**（release），读的一方先 acquire 读 `magic`，对了才信任别的字段——和 `tail` 的"先写数据后发布"是同一个协议。这样，对着一个全零 / 随机内容 / 太小的文件 `open` 会得到明确的 `IllegalStateException`，而不是读到垃圾（测试 `openRejectsFilesThatAreNotChannels`）。
* **头部各字段分开缓存行**：`head` 在偏移 128，`tail` 在 256，数据从 512 开始（§4.2 步骤 5 的同一个原因）。
* **创建的顺序**：`create` 必须在对方 `open` 之前完成。这是约定，测试保证了顺序：先 `create` 再启动子进程。

**实测**：`SharedChannelTest` 三个跨进程用例各启动一个子 JVM，合计约 0.35 s（实测 170 / 150 / 34 ms）。更大的负载：父进程发 500 万条消息（平均约 32 字节，共约 160 MB）、子进程收，从启动子进程到收完约 **190 ms**，即 **约 2600 万条/秒**（含子 JVM 启动；每条消息两端各分配一个 `byte[]`）。单进程内两线程 1000 万条 `long`（`SpscLongRing`）约 180 ms，约 5500 万条/秒。

---

## 5. 逐段讲参考解

### 5.1 `LongRing`（Part 1）

```java
public LongRing(int capacity) {
    if (capacity < 1 || capacity > MAX_CAPACITY || Integer.bitCount(capacity) != 1)
        throw new IllegalArgumentException("capacity must be a power of two in [1, 2^30]: " + capacity);
    this.buf = new long[capacity];
    this.mask = capacity - 1;
}
@Override public int size() { return (int) (tail - head); }
@Override public boolean isEmpty() { return head == tail; }
```

`Integer.bitCount(capacity) != 1`：二进制里不是恰好一个 1 → 不是 2 的幂（含 0 和负数；负数 `Integer.MIN_VALUE` 的 bitCount 是 1，但它先被 `capacity < 1` 拦下）。`size()` 的 `(int)` 强转安全：`tail - head ≤ capacity ≤ 2^30`。

### 5.2 `SpscLongRing`（Part 2）

```java
public boolean offer(long value) {
    long t = tail;                                  // 自己独占写，普通读即可
    if (t - cachedHead == buf.length) {             // 按旧快照看是满的 → 才去读真正的 head
        cachedHead = (long) HEAD.getAcquire(this);
        if (t - cachedHead == buf.length) return false;
    }
    buf[(int) (t & mask)] = value;                  // ① 数据
    TAIL.setRelease(this, t + 1);                   // ② 发布
    return true;
}
```

逐行：
1. `long t = tail`：`tail` 只有生产者线程写，所以生产者读自己的字段用普通读，不需要任何内存序。
2. `t - cachedHead == buf.length`：用旧的 `head` 算"满不满"。旧 `head` ≤ 真 `head`，所以 `t - cachedHead ≥ t - 真head`——旧值只会高估占用量。旧值说不满，真的不满；旧值说满，不一定满，所以：
3. 刷新 `cachedHead = HEAD.getAcquire(this)`，acquire 保证：看到新 `head`，就保证消费者在 release `head` 之前的读（`buf[old]`）已经完成，生产者可以放心覆盖那个槽位。
4. 重新判断，仍满 → `false`。
5. 写数据，再 `setRelease` 发布 `tail`。

```java
public long poll() {
    long h = head;
    if (h == cachedTail) {
        cachedTail = (long) TAIL.getAcquire(this);
        if (h == cachedTail) throw new NoSuchElementException("ring is empty");
    }
    long v = buf[(int) (h & mask)];                 // ④
    HEAD.setRelease(this, h + 1);                   // ⑤ 读完才归还
    return v;
}
```

对称。⑤ 的 release 保证 ④ 的读发生在生产者看到新 `head` 之前。

`size()` 用 `Math.clamp(t - h, 0, buf.length)`（J15，Java 21）夹到 `[0, capacity]`：先读 `head` 再读 `tail`，期间两者都可能前进，差值理论上可能略超出范围，夹一下就保证对任何线程都是合法值。

字段布局见 §4.2 的继承链。`VarHandle` 通过 `MethodHandles.lookup().findVarHandle(ConsumerFields.class, "head", long.class)` 取得——对**非 `volatile` 的普通字段**做 release/acquire 访问，这是 `VarHandle` 相对于 `volatile` 字段的好处（J16 §2.4）。

### 5.3 `MessageRing`（Part 3）

```java
public boolean offer(byte[] msg) {
    int len = msg.length;
    if (len > maxPayload()) throw new IllegalArgumentException(...);
    if (finished) throw new IllegalStateException("producer already finished");
    int rec = recordSize(len);
    long t = tail;
    int idx = (int) (t & mask);
    int toEnd = capacity - idx;
    if (rec > toEnd) {                                // 放不下连续的一整条：先单独发布一条 PAD
        if (!hasRoom(t, toEnd)) return false;
        seg.set(JAVA_INT_UNALIGNED, HEADER_BYTES + idx, PAD);
        t += toEnd;
        tail = t;
        LONG.setRelease(seg, OFF_TAIL, t);
        idx = 0;
    }
    if (!hasRoom(t, rec)) return false;
    long at = HEADER_BYTES + idx;
    MemorySegment.copy(msg, 0, seg, JAVA_BYTE, at + 4, len);        // payload
    seg.set(JAVA_INT_UNALIGNED, at, len);                           // 长度前缀
    tail = t + rec;
    LONG.setRelease(seg, OFF_TAIL, t + rec);                        // 发布
    return true;
}
```

* `len > maxPayload()` 抛异常（**永远**放不下），与"暂时满"的 `false` 区分开：调用方对两者的处理完全不同（前者是 bug，后者是背压）。
* `rec > toEnd` 就是 §4.3 的 PAD 逻辑。注意 PAD 路径里发布了 `tail`，之后如果真记录放不下 `return false`，**PAD 已经发布**。
* 长度前缀用 `JAVA_INT_UNALIGNED`：记录起点 8 字节对齐所以实际是对齐的，但 `_UNALIGNED` 不依赖 segment 基址的对齐，对堆 segment 也不抛。
* `MemorySegment.copy(byte[], …, MemorySegment, …)`：把字节数组批量拷进 segment，一条（可能向量化的）拷贝。
* 内存序：所有数据字节和长度都是普通写；只有 `tail` 用 `setRelease`——它保护之前所有的普通写。

```java
private boolean hasRoom(long t, int need) {
    if (capacity - (t - cachedHead) >= need) return true;
    cachedHead = (long) LONG.getAcquire(seg, OFF_HEAD);
    return capacity - (t - cachedHead) >= need;
}
```

cached index，同 §5.2。

```java
public byte[] poll() {
    long h = head;
    while (true) {
        if (h == cachedTail) {
            cachedTail = (long) LONG.getAcquire(seg, OFF_TAIL);
            if (h == cachedTail) return null;
        }
        int idx = (int) (h & mask);
        long at = HEADER_BYTES + idx;
        int len = seg.get(JAVA_INT_UNALIGNED, at);
        if (len == PAD) {                              // 跳到数据区开头
            h += capacity - idx;
            head = h;
            LONG.setRelease(seg, OFF_HEAD, h);
            continue;
        }
        byte[] out = new byte[len];
        MemorySegment.copy(seg, JAVA_BYTE, at + 4, out, 0, len);
        h += recordSize(len);
        head = h;
        LONG.setRelease(seg, OFF_HEAD, h);             // 读完才归还
        return out;
    }
}
```

遇到 PAD：把 `head` 前进到数据区末尾（`capacity - idx` 字节）、**立即发布**（生产者在等这一段空间）、`continue` 去读下一条（它在偏移 0）。读到真记录：先拷出来，再发布 `head`。

```java
public boolean isDrained() {
    if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
    return head == (long) LONG.getAcquire(seg, OFF_TAIL);
}
```

先 `closed` 后 `tail`（§2.8）。

`LONG` 是 `MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)`，坐标 `(MemorySegment, long 字节偏移)`。**注意**：JDK 21 里 `ValueLayout.JAVA_LONG.varHandle()` 只有 `(MemorySegment)` 一个坐标，没有偏移；JDK 22 才改成 `(MemorySegment, long)`（J17 §5.1）。堆上的 `byte[]` 段做 8 字节对齐的原子访问会抛 `IllegalArgumentException: Misaligned access`（我们试过）——所以环必须建在原生 / 映射内存上。

### 5.4 `SharedChannel`（Part 4）

```java
public static SharedChannel create(Path file, int capacity) throws IOException {
    long size = MessageRing.segmentBytes(capacity);       // 先校验 capacity，再动文件
    Arena arena = Arena.ofShared();
    try (FileChannel ch = FileChannel.open(file, CREATE, READ, WRITE, TRUNCATE_EXISTING)) {
        MemorySegment seg = ch.map(MapMode.READ_WRITE, 0, size, arena);
        return new SharedChannel(arena, MessageRing.init(seg, capacity));
    } catch (IOException | RuntimeException e) {
        arena.close();
        throw e;
    }
}
```

* `MessageRing.segmentBytes(capacity)` 在 `FileChannel.open` **之前**调用，而且它自己会校验容量（非法 → `IllegalArgumentException`）。这个顺序是有意的：如果先 `open(…, TRUNCATE_EXISTING)` 再让 `init` 去校验，对一个**已有的文件**调用 `create(file, 100)` 会先把它截断成空文件、再抛异常——调用方丢了数据。测试 `createRejectsBadCapacityWithoutTouchingFiles…` 专门锁住"非法容量不留下文件、不截断已有文件"。
* `try-with-resources` 关掉的是 `FileChannel`，**映射仍然有效**直到 `arena.close()`。
* 失败路径关闭 `arena`，不泄漏映射。

```java
public static SharedChannel open(Path file) throws IOException {
    Arena arena = Arena.ofShared();
    try (FileChannel ch = FileChannel.open(file, READ, WRITE)) {
        long size = ch.size();
        if (size < MessageRing.HEADER_BYTES) throw new IllegalStateException("file too small to be a channel: " + size);
        MemorySegment seg = ch.map(MapMode.READ_WRITE, 0, size, arena);
        return new SharedChannel(arena, MessageRing.attach(seg));
    } ...
}
```

`attach` 校验 `magic`/`version`/容量/尺寸，不合法抛 `IllegalStateException`。

### 5.5 测试怎么写（`SpscChild`、`Msgs`、`SharedChannelTest`）

* `Msgs.make(seq)`：splitmix64（一个很小的、质量不错的 64 位哈希）把 `seq` 变成伪随机数 `m`；长度 `8 + (m >>> 1) % 49`（8..56）；前 8 字节是 `seq`（大端）；其余字节由 `m` 派生。`Msgs.check(got, seq)` 返回 `null`（对）或错误描述（丢 / 重 / 乱序 / 损坏）。
* `SpscChild.main(args)`：`switch (mode)` 表达式（J05）选 `consume` / `produce`，成功打印 `OK <count>`，失败打印 `FAIL …` 退出码 1。`consume` / `produce` 是 `public static`，父进程测试直接复用，保证两端对"正确"的定义一致。
* `SharedChannelTest.spawn`：`ProcessHandle.current().info().command()` 找 `java`；`classPath()` 取 `java.class.path` ∪ `SpscChild` / `SharedChannel` / `MessageRing` 的 `getCodeSource().getLocation()`；`--enable-preview -XX:+UseSerialGC`（SerialGC 让子 JVM 启动更快、线程更少）。
* `assertChildOk`：`waitFor(CHILD_TIMEOUT + 2s)`，超时 `fail`；`finally` 里 `destroyForcibly()` 保证不留下孤儿进程。

---

## 6. Java 21 特性小课

| id | 用在哪 | 老写法 | 新写法 / 为什么 |
|---|---|---|---|
| J16 `VarHandle` | `SpscLongRing` 的 `HEAD`/`TAIL`（`findVarHandle` + `setRelease`/`getAcquire`）；`MessageRing` 的 `memorySegmentViewVarHandle` | 全部 `volatile`（强度过剩）或 `AtomicLong`（每个计数一个对象，且 `AtomicLong` 在对象头之外还占空间，不好控制布局）或 `sun.misc.Unsafe`（私有 API） | 对**普通字段**选访问强度；release/acquire 恰好是 SPSC 需要的；字段布局完全由自己控制，填充才有意义。详见 `J16_concurrency_primitives.md` §2.4 |
| J17 FFM | `MessageRing` 建在 `MemorySegment` 上；`SharedChannel` 用 `FileChannel.map(mode, off, size, Arena)` | `MappedByteBuffer`：`int` 索引（≤ 2 GiB）、无确定性取消映射、`ByteBuffer` 的原子访问要 `Unsafe` | `long` 大小、`Arena.close()` 确定性取消映射、`VarHandle` 原子访问映射内存。JDK 21 预览，22 转正。详见 `J17_ffm_api.md` |
| J15 `Math.clamp`（Java 21） | `SpscLongRing.size()`、`MessageRing.bytesPending()`：`Math.clamp(t - h, 0, capacity)` | `Math.max(0, Math.min(x, capacity))`（嵌套两层，顺序易写反） | 一个方法；语义是"夹到 `[min, max]`"；`long` 值夹到 `int` 范围时返回 `int` 的重载（`clamp(long, int, int)`）省掉强转。详见 `J15_math_string_utils.md` |
| J18 接口 `default` 方法 | `LongQueue.isFull()`：`default boolean isFull() { return size() == capacity(); }` | 抽象基类（占用唯一的继承名额——而 `SpscLongRing` 的继承链已经被填充用掉了！） | 接口给默认实现，实现类可以覆盖（`SpscLongRing.isFull` 覆盖成只读 `tail` 与 `head`，不依赖近似的 `size()`）。这是个**实际的**理由：填充用的继承链占掉了 `extends`，所以公共行为只能放接口。详见 `J18_comparators_interfaces.md` |
| J05 switch 表达式 | `SpscChild.main`：`String err = switch (mode) { case "consume" -> …; case "produce" -> …; default -> … };` | `if / else if` 链 + 临时变量 | 每个分支产生值，`default` 必须有（字符串 switch 不能穷尽）。详见 `J05_switch_expressions.md` |
| J08 `var` | 测试里的 `var ring = MessageRing.init(...)`、`var producer = new Thread(...)` | 重复写类型 | 右边已经写了类型。详见 `J08_var.md` |

**特别说明**：`LongQueue.isFull()` 的 default 是个很好的"为什么不用抽象基类"的例子——这类设计题常被问到。

---

## 7. 追问预演

### 追问 1：为什么 head / tail 要自由增长，而不是取模后存下标？

**思考过程**：先说取模存下标的问题（空 / 满不可区分），再说两种补救（浪费一格 / 另存 size）各自的缺点，然后给自由增长的好处。
**答案要点**：空 ⇔ `tail - head == 0`，满 ⇔ `== capacity`，天然不同；不浪费槽位；不需要被两个线程同时修改的 `size`；`long` 溢出需要几十万年。
**一段话**：「如果 head、tail 都存下标，head==tail 既可能是空也可能是满。我让它们是只增不减的 long 计数，下标用计数 & mask，这样空和满是两个不同的差值，不浪费槽位，也不需要一个会被两个线程同时改的 size 变量。」

### 追问 2：为什么容量要是 2 的幂？

**答案要点**：取模变按位与（`count & (capacity-1)`），除法（几十周期）变一周期；检查用 `Integer.bitCount(c) == 1`；代价是容量只能取 2 的幂，空间最多浪费一半。

### 追问 3：为什么 SPSC 不需要 CAS？

**答案要点**：每个共享变量只有一个写者（`tail` 只有生产者写、`head` 只有消费者写），没有"读-改-写"的竞争；只需要可见性和顺序，release/acquire 足够。多生产者才需要 CAS。

### 追问 4：release/acquire 具体保护了什么？去掉会怎样？

**思考过程**：画 ①②③④ 四步图；说清楚每一对配对保护什么；说出本机实测。
**答案要点**：生产者的 `setRelease(tail)` 保证数据写入先于 tail 可见；消费者的 `getAcquire(tail)` 保证读数据晚于读 tail；`head` 方向保护"读完才归还槽位"。去掉（改普通写）：弱内存序 CPU 上消费者读到旧值——本机（Apple M）实测：`SpscLongRingTest` 的多个用例大面积变红，first mismatch 出现在第几百到十几万条之间；x86 上常常碰巧是对的。
**一段话**：「release 保证我在它之前写的数据，别人 acquire 看到这次发布之后一定看得到。去掉它，在 ARM 上我实测消费者会读到上一圈留下的旧值。」

### 追问 5：什么是伪共享？怎么证明它存在？

**答案要点**：两个线程写同一缓存行里的不同变量，行在两个核心间来回失效；证明：单变量实验（`FalseSharingBench`），只改变两个计数器的距离，其他全不变；本机相邻比分开慢约 2 倍，且相邻的结果呈双峰（取决于两个线程是否在同一核心簇）。注意：在 SPSC 吞吐上的收益被噪声掩盖——要说诚实的结论。

### 追问 6：cached index 为什么是安全的？

**答案要点**：`head`/`tail` 只增不减，旧快照只会低估对方的进度：旧 `head` 小于等于真 `head` → 算出的占用量偏大 → "旧值说有空位"必定真有空位；"旧值说满"才去读真值。正确性来自**单调性**。

### 追问 7：变长消息回绕时你怎么处理？什么情况下会死锁？

**答案要点**：见 §4.3。PAD 记录单独发布；若把"PAD + 记录"作为整体判断，空环 + tail 靠近末尾 + 大消息会永远放不下。`offer` 返回 `false` 时可能已发布 PAD。
**一段话**：「记录必须连续，所以放不下时先写一条 PAD 填满到末尾。关键是 PAD 要单独发布：如果我等到 PAD 加记录整体放得下才写，那么在环是空的、tail 又靠近末尾时，消费者没东西可读不会前进，生产者永远放不下，两边互相等。」

### 追问 8：`null` / `false` 和 drained 怎么区分？

**答案要点**：`closed` 标志；`isDrained() = closed && head == tail`；先读 `closed` 再读 `tail`，否则会丢最后几条；末尾残留 PAD 要 `poll` 越过后才 drained。

### 追问 9：跨进程时内存序还成立吗？

**答案要点**：成立的是硬件 + VarHandle 发出的屏障，不是 JMM 的形式化保证（JMM 谈的是同一程序内的线程）。两进程映射同一批物理页，缓存一致性由硬件保证，release/acquire 约束各自 CPU 和编译器的重排。说法要谨慎。

### 追问 10：怎么测试跨进程代码，怎么避免挂死？

**答案要点**：见 §2.9。子进程 + 确定性消息 + 每端自旋带截止时间 + `waitFor(超时)` + `destroyForcibly`；类路径要包含被测类的实际位置；不依赖 `sleep` 对时序。

### 追问 11：改成多生产者怎么办？

**答案要点**：`tail` 要 CAS 竞争（先 CAS 预留一段，再写，再按序提交——Disruptor 的 `next()` + `publish()`、Aeron 的 `tryClaim` + `commit`）；或者每个生产者一个 SPSC 环、消费者轮询多个环（避免争用，代价是没有全局顺序）。

### 追问 12：消费者崩溃重启怎么办？

**答案要点**：`head`/`tail` 在文件里，重启后 `attach` 能接着读；问题在"处理了一半的消息"：`head` 在读完才发布，所以崩溃于处理中会重新读到这条——至少一次（at-least-once）语义，处理需要幂等；如果要恰好一次，需要消息带序号并让消费者持久化自己处理到哪。

---

## 8. 常见误区

### 误区 1：以为 x86 上测试通过就代表内存序对

x86 不重排 Store-Store，所以把 `setRelease` 写成普通写，在 x86 上常常"碰巧"正确，在 ARM（含 Apple M 系列、很多云服务器）上就错。**正确**：按 release/acquire 的语义写，并在弱内存序机器上测试。来自 §2.5 的实测。

### 误区 2：`head == tail` 就是空

下标取模存储时它也可能是满。**正确**：自由增长的计数 + 差值。

### 误区 3：把 PAD + 记录当作一个整体判断能不能放进去

空环上会死锁（§4.3）。**正确**：PAD 单独发布。来自测试 `padIsPublishedEvenIfTheRecordDoesNotFit` 和 `anEmptyRingAcceptsAMaxSizeMessageFromEveryPosition`。

### 误区 4：先读 tail 再读 closed

漏掉最后几条。**正确**：先 `closed`（acquire），再 `tail`。

### 误区 5：只传 `java.class.path` 给子进程

用 JUnit console 的 `--class-path` 运行时，子进程找不到被测类（`ClassNotFoundException`）。**正确**：加上被测类的 `getCodeSource().getLocation()`。

### 误区 6：用 `Thread.sleep` 等对方

跨进程测试里"睡 100 ms 等子进程准备好"既慢又不可靠。**正确**：协议自己处理（`magic` 最后写；自旋 + 截止时间）。

### 误区 7：在堆上的 `byte[]` segment 上做原子访问

`MemorySegment.ofArray(new byte[n])` 上对 `long` 做 `setRelease` 抛 `IllegalArgumentException: Misaligned access`（堆段只保证 1 字节对齐）。**正确**：用 `Arena.allocate(size, 128)` 或映射文件。

### 误区 8：用继承链填充，却把只读字段放在热字段后面

`buf`/`mask` 和 `head` 同一行：消费者写 `head` 使生产者的 `buf` 副本失效。**正确**：只读字段放在最前面的基类，填充在热字段之间与之后。

---

## 9. 自测题

1. 容量 8 的环，`head = 13`、`tail = 17`，此刻有几个元素？下一次 `offer` 写 `buf` 的哪个下标？下一次 `poll` 读哪个下标？
2. 解释为什么 `SpscLongRing.offer` 里可以用 `cachedHead` 判断"有空位"，而不会错误地覆盖未读的数据。
3. 把 `MessageRing.offer` 里的 `LONG.setRelease(seg, OFF_TAIL, t + rec)` 换成普通写，会出什么 bug？在什么机器上更容易暴露？
4. 容量 64 的 `MessageRing`，环是空的，`head = tail = 8`。要发一条 60 字节的消息（`maxPayload` 恰好，记录 64 字节）。逐步写出 `offer`、`poll`、`offer` 三次调用的返回值和每次之后 `bytesPending()` 的值，并说明为什么第一次 `offer` 返回的是那个值。
5. 编程题：不看参考解，写出 `isDrained()` 的正确实现，并说明为什么读两个变量的顺序不能反。

<details><summary>答案</summary>

1. 元素数 `17 - 13 = 4`；`offer` 写 `buf[17 & 7] = buf[1]`；`poll` 读 `buf[13 & 7] = buf[5]`。
2. `head` 只增不减，所以 `cachedHead ≤ 真 head`，用旧值算出的占用量 `t - cachedHead ≥ 真占用量`。旧值说"没满"，真实情况一定也没满，所以写入的槽位确实是消费者已读完的。旧值说"满"才需要刷新，不会产生错误的"有空位"结论。
3. 数据字节和长度前缀可能晚于 `tail` 对消费者可见：消费者看到 `tail` 前进，读到的长度或 payload 是上一圈的旧值（长度错误可能导致读越界到别的记录）。弱内存序机器（ARM，如 Apple M 系列）更容易暴露；x86 常常碰巧正确。
4. 第一次 `offer`：`idx = 8`，`toEnd = 56 < 64`，需要 PAD；空位 64 ≥ 56，所以写 PAD、`tail` 变成 64 并**发布**；然后真记录要 64 字节，但环里还有 56 字节的 PAD 没被消费（`tail - head = 56`），空位只有 8，放不下 → 返回 `false`，`bytesPending() == 56`。`poll`：读到 PAD，跳到偏移 0、`head = 64`，没有别的消息 → 返回 `null`，`bytesPending() == 0`。第二次 `offer`：`tail = 64`，`idx = 0`，`toEnd = 64 ≥ 64` 不需要 PAD，空位 64 ≥ 64 → `true`，`bytesPending() == 64`。要点：PAD 单独发布，加上消费者越过 PAD，是让大消息最终放得进的两个条件。
5. ```java
   public boolean isDrained() {
       if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
       return head == (long) LONG.getAcquire(seg, OFF_TAIL);
   }
   ```
   生产者先发布最后的 `tail` 再置 `closed`。先读 `closed`：看到 1 就保证（release/acquire）能看到最终 `tail`。若先读 `tail`（旧值，恰好等于 `head`），生产者随后发布了最后几条并置 `closed`，再读 `closed` 看到 1，就会误判 drained，丢最后几条。

</details>

---

## 10. 延伸阅读

* M. Thompson, D. Farley, M. Barker, P. Gee, A. Stewart, *Disruptor: High performance alternative to bounded queues for exchanging data between concurrent threads*, LMAX, 2011 —— 单写者原则、环形缓冲区、缓存行填充的工业来源。
* L. Lamport, *Specifying Concurrent Program Modules*, ACM TOPLAS 5(2), 1983 —— 里面有单生产者单消费者环形缓冲区的正确性证明，说明这类队列可以不用互斥。
* Linux 内核文档 `Documentation/core-api/circular-buffers.rst`（Howells & McKenney）—— 内核里生产者 / 消费者环形缓冲区和内存屏障的权威讲解，对应本讲义 §2.5。
* Agrona `OneToOneRingBuffer` / Aeron 日志缓冲区文档 —— 变长消息 + PAD 记录 + 对齐的实际工程实现，对应 §2.7。
* U. Drepper, *What Every Programmer Should Know About Memory* —— 缓存行、一致性协议、伪共享的深入讲解（第 3、6 章）。
* JEP 442 *Foreign Function & Memory API (Third Preview)* https://openjdk.org/jeps/442 —— `FileChannel.map(…, Arena)`、`MemorySegment`、`VarHandle` 访问；JDK 22 正式版 JEP 454。
* `java.lang.invoke.VarHandle` Javadoc —— plain / opaque / acquire-release / volatile 的权威定义。
* `mmap(2)` 手册页（POSIX）—— `MAP_SHARED` 的语义，对应 §2.2。
* 同 kit：`study/10-java21/J16_concurrency_primitives.md`、`study/10-java21/J17_ffm_api.md`、`study/00-foundations/cpu_cache_locality.md`、`study/00-foundations/os_processes_threads_ipc.md`。
