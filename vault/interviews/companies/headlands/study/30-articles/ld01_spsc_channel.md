# ld01 · 共享内存 SPSC 消息通道 —— 讲义

> 读者：会写基本 Java。本篇从「进程是什么、共享内存是什么」讲起。

---

## 1. 这道题在问什么

两个**独立运行的程序**（进程），一个不停产生消息（如行情），一个不停消费（如策略），**互相看不到对方的变量**。要设计一个**通道**让消息从前者流到后者：

* **有界**：满了要明确告诉生产者"满了"，不能无限增长；
* **FIFO**：不丢、不重、不乱序；
* **要快**：热路径不加锁、不系统调用、不多次拷贝；
* **三种状态明确**：满（full）、空（empty）、**读完了**（drained：生产者宣布不再有消息且消费者已读完）。

题面原文：

> bounded shared-memory message channel between two processes, with safe record ownership, FIFO delivery and explicit full, empty and drained…

关键约束 SPSC（single-producer single-consumer）：**一个生产者、一个消费者**，不用锁也不用 CAS。

### 手算一遍（容量 4 的环形缓冲区）

长度 4 的数组当"环"。`head` 是消费者下一个要读的计数，`tail` 是生产者下一个要写的计数；下标 = 计数 `& 3`（取低 2 位，等价 `% 4`）：

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

### 四个 Part

1. **Part 1**：单线程环形缓冲区，`long` 元素。满 / 空怎么区分？容量为何 2 的幂？
2. **Part 2**：两个**线程**共享。不加锁怎么正确（`setRelease`/`getAcquire`）？怎么更快（cached index、填充）？怎么**证明**更快（测量）？
3. **Part 3**：变长消息：长度前缀、对齐、回绕时放不下怎么办？
4. **Part 4**：环放进**内存映射文件**，让两个独立 JVM 进程各映射一份。怎么测试？

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 进程、线程与进程间通信

* **线程**共享同一进程内存（要注意"可见性"，2.5）。
* **进程**默认**隔离**：各有**虚拟地址空间**，A 的 `0x1000` 与 B 的 `0x1000` 通常是不同物理内存。传数据要经**进程间通信**（IPC）：管道、套接字、消息队列、**共享内存**。
* 管道和套接字每次传输都要**系统调用**（`write`/`read`），数据在内核缓冲区**拷贝**一到两次，还可能让线程睡眠、唤醒。**共享内存**把同一批物理页映射进两个进程的地址空间，之后直接读写，无系统调用、无拷贝，延迟低一个数量级——低延迟系统首选它的原因。

### 2.2 共享内存与内存映射文件（mmap）

`mmap` 把文件（或匿名内存）**映射**到进程虚拟地址空间，像访问数组一样访问文件。两个进程用 `MAP_SHARED` 映射**同一个文件**，两进程的虚拟页指向同一批**物理页**（页缓存，page cache）：

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

A 写一个字节，B 立刻读到（缓存一致性保证，2.6），无系统调用。文件只是"会合点"（也可用 `/dev/shm`、`shm_open`）；好处：跨平台、易清理、**进程崩溃后数据还在**。第一次访问某页触发**缺页**（page fault），由内核分配或读入物理页——一次性成本。

JDK 21（FFM 预览）：

```java
try (FileChannel ch = FileChannel.open(file, CREATE, READ, WRITE);
     Arena arena = Arena.ofShared()) {
    MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, size, arena);   // 文件被扩展到 size，新增部分全零
    seg.set(ValueLayout.JAVA_INT_UNALIGNED, 12, 1);
}   // arena.close() = 取消映射（munmap）；文件还在磁盘上
```

老办法 `FileChannel.map(...)` 返回 `MappedByteBuffer`：限 2 GiB（`int` 索引）、无确定性取消映射。FFM 的 `MemorySegment` + `Arena`：长度 `long`，生命周期由 `Arena` 确定性关闭。

### 2.3 环形缓冲区（ring buffer）从零讲

#### 为什么需要它

"先进先出、容量固定"的队列，最直观是数组 + 移动元素：

```
poll(): 取 buf[0]，然后把 buf[1..n-1] 全部往前挪一格      ← O(n)，每次都挪，太慢
```

**环形**：不挪元素，挪**指针**。读指针（head）只往前走，到尾部绕回开头。

#### 怎么区分"满"和"空"

经典陷阱：`head`、`tail` 都存"数组下标"时，`head == tail` 既可能空也可能满。补救：永远空一个槽位；或另存 `size`（被两线程同时改，要原子操作）。**更好：让 `head`、`tail` 是只增不减的计数**（"自由增长"，free-running），下标是计数对容量取模：

```
空  ⇔  tail - head == 0
满  ⇔  tail - head == capacity
元素个数 = tail - head
下标 = 计数 mod capacity
```

空和满天然不同，不浪费槽位，不需 `size`。`long` 计数每纳秒加 1 要 29 万年才溢出。

#### 为什么容量要是 2 的幂：`& mask`

`计数 % capacity` 要一次整数除法（几十个周期）。`capacity = 2^k` 时取模等价于**只保留低 k 位**，一次按位与：

```
capacity = 8 = 0b1000        mask = capacity - 1 = 0b0111
计数 13 = 0b1101
13 & 0b0111 = 0b0101 = 5     与 13 % 8 = 5 相同
```

Java：`buf[(int) (count & mask)]`；检查 2 的幂：`Integer.bitCount(capacity) == 1`。负数的取模和按位与结果不同，但计数永远非负。

### 2.4 为什么 SPSC 不需要锁，也不需要 CAS

看每个变量**谁写**：

| 变量 | 谁写 | 谁读 |
|---|---|---|
| `tail` | **只有**生产者 | 生产者自己、消费者 |
| `head` | **只有**消费者 | 消费者自己、生产者 |
| `buf[i]` | 生产者（槽位空闲时） | 消费者（槽位有数据时） |

每个变量**只有一个写者**，无需锁或 CAS。唯一要解决的是写完后读者**何时**、**以什么顺序**看得到（2.5）。多生产者则都改 `tail`，必须 CAS 竞争。所以 SPSC 最易做到极致，LMAX Disruptor 等大量用"单写者原则"。

### 2.5 内存序：为什么"先写数据再改 tail"还不够

CPU 和编译器会**重排**无依赖的读写；每个核心有**写缓冲**（store buffer），写先进缓冲、之后才对别核可见，且别核看到的**顺序**不一定等于程序顺序。生产者的两行：

```java
buf[i] = v;            // ① 写数据
tail = t + 1;          // ② 发布
```

在"弱内存序"CPU（ARM，含 Apple M）上，其他核心可能**先看到 ② 再看到 ①**：消费者看到 `tail` 变了去读 `buf[i]`，读到旧数据。实测把 `TAIL.setRelease(this, t + 1)` 换成普通写，Apple M 上马上大量出错（第 369、7477、13918 条对不上，读到上一圈残留值）。x86 内存序更强，同样代码常"碰巧"对——**x86 上测试通过不代表对**。

解决：用 **release / acquire** 配对：

* `setRelease(x, v)`：**之前的**读写不会被重排到它之后（向上的单向门）。
* `getAcquire(x)`：**之后的**读写不会被重排到它之前（向下的单向门）。
* 若消费者 `getAcquire(tail)` **读到了**生产者 `setRelease(tail, t+1)` 写下的值，则生产者在该 release 之前写的一切（含 `buf[i]`），消费者在该 acquire 之后都看得到。

```
生产者:  buf[i] = v;                     // ① 数据
         TAIL.setRelease(t + 1);         // ② release：①不能被重排到②之后
消费者:  t = TAIL.getAcquire();          // ③ acquire：④不能被重排到③之前
         v = buf[i];                     // ④
```

反方向同样需要：消费者读完 `buf[i]` 后才 `HEAD.setRelease(h + 1)`，生产者 `getAcquire` 看到新 `head` 后才敢覆盖该槽位——否则生产者可能在消费者读完前写入（读到新值，丢一条）。

**为什么不直接 `volatile`**：它是更强的"顺序一致"，多付"写后读"重排禁止的代价（x86 上要 `lock` 前缀或 `mfence`）；release/acquire 在 x86 上就是普通 `mov`，只约束编译器，无额外 CPU 栅栏。

**跨进程呢？** JMM 讨论的是同一程序内的线程。两个**进程**共享同一物理内存时，硬件缓存一致性和内存序同样适用，`setRelease`/`getAcquire` 编译出同样的屏障指令，所以"先写数据、release 发布 tail、对方 acquire 读 tail 再读数据"的协议跨进程同样成立。但这是**基于硬件与 JIT 实现**的推理，不是 JMM 的形式化保证，面试别说太绝对。

### 2.6 缓存一致性、伪共享与 cached index

#### 缓存一致性

每个核心有自己的缓存，数据按**缓存行**（cache line，x86 常见 64 字节，Apple M 128 字节）搬运。协议（MESI 一类）规定：某核心要**写**一条缓存行时，先让别的核心里的副本**失效**；别核再读就要从写者重新取。这次"跨核搬运"约几十纳秒，比普通运算慢两个数量级。

#### 伪共享（false sharing）

线程 A 只写 `a`，B 只写 `b`，二者恰在**同一条缓存行**：A 每写一次让 B 的副本失效，反之亦然。逻辑无关的变量在硬件层面**抢同一块东西**。我们的环里 `tail`（生产者写）和 `head`（消费者写）若相邻，每次 `offer` 都使消费者核心里 `head` 所在行失效，每次 `poll` 反之。**解决**：**填充**（padding），让两变量相隔至少一条缓存行。

#### cached index（缓存对方的下标）

即使分开，生产者每次 `offer` 仍要读 `head` 判断满不满，而该行是消费者在写，每次读都跨核搬运。**观察**：`head` 只增不减。生产者保存旧 `head`（`cachedHead`）：旧值算出的"剩余空位"**只会偏小不会偏大**——"旧值看起来有空位"一定真有；只有"看起来满了"才读真 `head` 刷新。消费者对 `tail` 同理。效果：队列不是几乎满 / 几乎空时，一批消息只触碰一次对方的缓存行。

### 2.7 变长消息：长度前缀、对齐与回绕

**长度前缀**：每条消息写成 `[长度: 4 字节][payload]`，先读长度再读那么多字节。

**对齐**：每条记录补零到 **8 字节**倍数（`(4 + len + 7) & ~7`），记录总从 8 的倍数偏移开始，4 字节长度字段永不跨越数据区末尾，`int`/`long` 读写保持对齐。

**回绕（wrap-around）**：数据区是环，但**一条记录必须连续**。当前位置到末尾放不下整条记录时：

```
capacity = 64，tail 在 48，要写一条 24 字节的记录，到末尾只剩 16 字节：

  0                                      48        64
  │ ........ 已被消费的 ........ │  │ 空 16 字节 │ 
                                          ▲
              ① 在这里写一条 PAD 记录 [len=-1]，占满剩下的 16 字节
              ② 然后从偏移 0 开始写真正的 24 字节记录

  消费者读到 len == -1 就知道"这一段是填充，直接跳到开头"
```

**PAD 要单独发布**——这道题最易踩的坑，见 §4.3。

### 2.8 drained：怎么让消费者知道"真的结束了"

`poll()` 返回 `null` 有两种可能：现在没有、一会儿还有，或永远不会有了。必须区分，否则消费者要么永远等要么提前退出丢消息。头部放 `closed` 标志，生产者 `finish()` 置 1；`isDrained()` = `closed == 1` **并且** `head == tail`。

**顺序很重要**：生产者先发布最后一次 `tail` 再置 `closed`；消费者必须**先读 `closed` 再读 `tail`**：看到 `closed == 1` 就保证（经 release/acquire）看得到最终 `tail`。先读 `tail` 可能读到旧值（空），随后生产者发布最后几条并置 `closed`，消费者再读 `closed == 1`——误判 drained，丢最后几条。

### 2.9 怎么测试"两个进程"

1. **找到 `java`**：`ProcessHandle.current().info().command()`（`Optional<String>`，取不到用 `java.home/bin/java`）。
2. **类路径**：`java.class.path` 是当前 JVM 的类路径，**但**测试运行器用自己的类加载器从别处加载被测类时（如 JUnit console 的 `--class-path`），里面只有运行器的 jar。所以再并上被测类实际位置 `SharedChannel.class.getProtectionDomain().getCodeSource().getLocation()`，去重。
3. **预览特性**：JDK 21 的 FFM 是预览，子进程要 `--enable-preview`。
4. **不挂死**：一端出错，另一端自旋会永远转。每个自旋循环带**截止时间**（`System.nanoTime()`，每 1024 圈检查一次），父进程 `waitFor(超时)`，超时 `destroyForcibly()`。**测试不能依赖 `Thread.sleep` 对时序**。
5. **抓得到"丢 / 重 / 乱序"**：每条消息的长度和内容完全由序号决定（splitmix64 小哈希算出长度 8..56 和内容，前 8 字节是序号）。收的人只靠"我期待第 `seq` 条"校验：丢、重复、乱序、截断 / 损坏都对不上；最后验证"恰好 count 条且 isDrained"抓多发。

---

## 3. 从最笨的解法开始

* **最笨 1**：`ArrayList` + `remove(0)`，每次前移 O(n)，且只能在一个进程里用。
* **最笨 2**：线程间 `ArrayBlockingQueue`（锁 + 条件变量）：(a) 竞争时线程睡眠 / 唤醒要系统调用，延迟抖动；(b) **跨不了进程**。
* **最笨 3**：进程间套接字 / 管道：每条消息一次 `write` + 一次 `read`，两次系统调用 + 拷贝，微秒量级，消息边界要自己处理。
* **最笨 4**：环形缓冲区，下标取模存，空一槽位或另存 `size`：`%` 慢、浪费槽位 / `size` 被两线程改。
* **最笨 5**：环形缓冲区，`head`/`tail` 都 `volatile`，每次读对方的 `volatile`：正确但慢，每次读是跨核搬运，`volatile` 写在 x86 上还要全栅栏，约 **31–49 M 条/秒**（§4.2）；仍不能跨进程。

---

## 4. 一步一步改进

### 4.1 Part 1：从移动元素到自由增长的计数

1. **问题**：数组队列 `poll` 要挪 n 个元素，O(n)。
2. **想法**：挪指针不挪元素；到末尾绕回开头（环形）。
3. **新问题**：`head == tail` 既可能空也可能满。
4. **想法**：`head`、`tail` 存只增不减的计数，下标由计数取模。空 ⇔ `tail - head == 0`，满 ⇔ `== capacity`。
5. **新问题**：`%` 慢 → 容量取 2 的幂，用 `& (capacity - 1)`（§2.3）。
6. **复杂度**：`offer`/`poll` O(1)，无除法，不浪费槽位。

```java
public boolean offer(long value) {
    if (tail - head == buf.length) return false;
    buf[(int) (tail & mask)] = value;
    tail++;
    return true;
}
```

`poll` 在空队列上抛 `NoSuchElementException`：`long` 每个取值都可能是合法消息，没有哨兵值表示空。自旋等待写 `while (q.isEmpty()) Thread.onSpinWait(); q.poll();`，SPSC 下安全（只有消费者能让队列变空）。

### 4.2 Part 2：从单线程到两线程

**步骤 1：什么都不加？** 两线程直接用 `LongRing`（普通字段）。(a) **可见性**：消费者 `while (isEmpty())` 里 JIT 可把对普通字段 `tail` 的读提到循环外，永远读不到新值——死循环；(b) **顺序**：§2.5 的 ①② 重排。
**步骤 2：`volatile`**：可见性和顺序都对（A 版）。
**步骤 3：release / acquire**：`VarHandle` 的 `setRelease`/`getAcquire` 代替 `volatile`（B 版）。x86 上省掉全栅栏；HotSpot 在 AArch64 上两者都编成 `ldar`/`stlr`，差别应很小（未反汇编验证）。
**步骤 4：cached index**（§2.6）：A/B 每次都读对方变量，D 只在"旧值看起来满 / 空"时才读。
**步骤 5：填充**：C 版 = B + 填充；E 版 = D + 填充（即 `SpscLongRing`）。

**五种写法的数据**（每种传 5000 万个 `long`，容量 1024；百万条/秒；6 次独立运行，每次五种各取 5 轮最好，再对 6 次取中位数）：

| 写法 | 中位数 | 6 次运行的范围 |
|---|---|---|
| A volatile | 38 | 31 – 49 |
| B acq/rel | 34 | 29 – 49 |
| C acq/rel + 填充 | 27.5 | 27 – 30 |
| D acq/rel + cache | 34 | 29 – 40 |
| E acq/rel + cache + 填充 | **44** | 31 – 48 |

* **E 中位数最高**（44 对 34 – 38），但范围（31 – 48）与 A、B 大面积重叠——收益存在，**不显著**。
* C（只填充不缓存）稳也最低（27 – 30），原因没深究（猜测：不缓存时每条仍要读对方的行，填充把"顺手带过来"的同行数据也拿走了；别当结论）。
* **范围宽**是这台机器的特点：Apple M 有性能核（P）和能效核（E），macOS 不允许固定线程到核心，调度器会把生产者和消费者放到不同核心簇；同簇跨核搬运快，不同簇慢。**微基准要说清"测的是什么、噪声多大、取中位数还是最大值"**，比报最大值诚实。

> 填充要**单独**量：两线程各对"自己的计数器"做 2 亿次 `setOpaque` 自增，互不相干：
>
> | 布局 | 6 轮（ms，排序后） | 中位数 |
> |---|---|---|
> | 相邻（同一缓存行） | 821, 822, 1457, 1755, 1775, 1811 | 1606 |
> | 相隔 128 字节以上 | 790, 800, 802, 838, 933, 1090 | 820 |
> | （第二次运行）相邻 | 831, 834, 1698, 1817, 1844, 1867 | 1757 |
> | （第二次运行）分开 | 798, 802, 893, 942, 965, 1084 | 917 |
>
> **相邻慢约 2 倍**，且呈**双峰**：前两轮 ~820（两线程碰巧同一核心簇）、后四轮 ~1800（不同簇，必须跨簇搬运）；分开的一直很快。这才是伪共享的干净证明。

**SPSC 里为何还要填充**：吞吐收益被噪声盖住，但 (a) 伪共享代价真实且大；(b) 字段布局取决于 JVM 排布，不填充就**无法控制**是否同行；(c) x86 服务器（核心间延迟更稳定）上收益通常更明显。说法：「我填充，因为代价小、风险大；单变量实验验证过它的真实性，也知道 SPSC 吞吐差异在这台机器上淹没在噪声里。」

**Java 里填充**：没有 `alignas`，用**继承链 + 填充 `long`**。JVM 总把父类字段排在子类字段之前且不跨类重排：

```java
abstract class RingBase      { final long[] buf; final int mask; }          // 只读，两个线程都读
abstract class PadA extends RingBase { long a01, ..., a15; }                // 15 个 long = 120 字节
abstract class ProducerFields extends PadA { long tail; long cachedHead; }  // 只有生产者写
abstract class PadB extends ProducerFields { long b01, ..., b15; }
abstract class ConsumerFields extends PadB { long head; long cachedTail; }  // 只有消费者写
abstract class PadC extends ConsumerFields { long c01, ..., c15; }
public final class SpscLongRing extends PadC implements LongQueue { ... }
```

`buf`/`mask` 放最前面的基类：它们只读，若与 `head` 同行，消费者写 `head` 会使生产者的 `buf` 副本失效。JDK 内部用 `@jdk.internal.vm.annotation.Contended`，用户代码需 `-XX:-RestrictContended`，所以用继承技巧。

### 4.3 Part 3：变长消息

#### 步骤 1：`long[]` 换成字节环 + 长度前缀

`head`/`tail` 是**字节**计数；记录 `[len:int32][payload][补零到 8 字节对齐]`，总长 `recordSize(len) = (4 + len + 7) & ~7`；最大消息 `maxPayload = capacity - 4`。

#### 步骤 2：回绕——记录放不下连续空间

见 §2.7。第一版想法（**也是错的那个**）：

```
offer(msg):
    if (pad + rec > 空闲字节) return false;      // 先算好总共需要多少，放不下就拒绝
    写 PAD（如果需要）；写记录；发布 tail
```

**这个版本会死锁**。环是空的（`head == tail`），但 `tail` 恰停在偏移 8（`toEnd = 56`），生产者想发 `maxPayload` 的大消息（记录 64 字节）：需要 PAD 56 + 记录 64 = 120 > 64（容量）→ 永远 `false`；消费者没东西可读，`head` 不前进，空间永不增。双方互等：**死锁（活性丧失）**。

> 易写错的镜像：假设"空环上连续两次 `offer` 就放得进"是错的——PAD 占的字节要等**消费者越过它**（`poll` 返回 `null`）才释放，只调 `offer` 不调 `poll` 当然放不进。正确的活性性质是 `offer → poll → offer`，要求**两边同时**做对：生产者单独发布 PAD，消费者越过 PAD。

**修复**：PAD **单独发布**。需要 PAD 时只要有 `toEnd` 字节空位就写 PAD、`tail += toEnd`、release 发布，哪怕随后真记录挤不进（`offer` 返回 `false`）。消费者 `poll` 读到 PAD 跳到开头，`head` 前进，环重新"空且 `tail` 在偏移 0"，任何 ≤ `maxPayload` 的消息都放得进。代价：`offer` 返回 `false` 时 `tail` 可能已变（对消息序列无影响，但 `bytesPending` 含 PAD 字节）。

#### 步骤 3：drained

§2.8。`finish()`：`closed = 1`（release）；`isDrained()`：先 acquire 读 `closed`，再 acquire 读 `tail`，比较 `head`。边界：末尾可能残留一条 PAD（`offer` 发布了 PAD 但真记录没放进，随后 `finish`）——此时 `head != tail`，`isDrained()` 为 `false`；消费者再 `poll` 一次越过 PAD（返回 `null`）后为 `true`。所以消费者标准写法：

```java
while (!ring.isDrained()) {
    byte[] m = ring.poll();
    if (m == null) { Thread.onSpinWait(); continue; }
    handle(m);
}
```

### 4.4 Part 4：放进内存映射文件

`MessageRing` 建在 `MemorySegment` 上；给另一个**进程**用则内存必须是两进程都能映射的。用内存映射文件（§2.2）：`FileChannel.map(READ_WRITE, 0, size, arena)` 直接返回 `MemorySegment`，`MessageRing` 一行不改。要补：
* **自描述头部**：`open` 的一方不知容量，头部写 `capacity`、`version`、`magic`。`magic` **最后写**（release），读的一方先 acquire 读 `magic`，对了才信任别的字段——与 `tail` 同一"先写数据后发布"协议。对着全零 / 随机内容 / 太小的文件 `open` 得明确的 `IllegalStateException`，而非读到垃圾。
* **头部各字段分开缓存行**：`head` 在偏移 128，`tail` 在 256，数据从 512 开始。
* **创建顺序**：`create` 必须在对方 `open` 之前完成。

**数据**：父进程发 500 万条消息（平均约 32 字节，共约 160 MB）、子进程收，启动到收完约 **190 ms**，**约 2600 万条/秒**（含子 JVM 启动；两端每条各分配一个 `byte[]`）。单进程内两线程 1000 万条 `long` 约 180 ms，约 5500 万条/秒。

---

## 5. 逐段讲解法

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

`bitCount(capacity) != 1` → 不是 2 的幂（含 0 和负数；`Integer.MIN_VALUE` 的 bitCount 是 1，但先被 `capacity < 1` 拦下）。`size()` 的 `(int)` 强转安全：`tail - head ≤ capacity ≤ 2^30`。

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

1. `long t = tail`：`tail` 只有生产者写，读自己的字段用普通读。
2. `t - cachedHead == buf.length`：用旧 `head` 算"满不满"。旧 `head` ≤ 真 `head`，旧值只高估占用：说不满则真不满；说满不一定满，所以：
3. 刷新 `cachedHead = HEAD.getAcquire(this)`：看到新 `head` 就保证消费者在 release `head` 之前的读（`buf[old]`）已完成，可覆盖该槽位。
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

对称：⑤ 的 release 保证 ④ 的读发生在生产者看到新 `head` 之前。`size()` 用 `Math.clamp(t - h, 0, buf.length)` 夹到 `[0, capacity]`：先读 `head` 再读 `tail`，期间两者都可能前进，差值理论上可能略超范围。字段布局见 §4.2 继承链；`VarHandle` 经 `MethodHandles.lookup().findVarHandle(ConsumerFields.class, "head", long.class)` 取得——对**非 `volatile` 的普通字段**做 release/acquire 访问，这是它相对 `volatile` 字段的好处。

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

* `len > maxPayload()` 抛异常（**永远**放不下），与"暂时满"的 `false` 区分：前者是 bug，后者是背压。
* `rec > toEnd` 即 §4.3 的 PAD 逻辑：PAD 路径发布了 `tail`，之后真记录放不下 `return false`，**PAD 已发布**。
* 长度前缀用 `JAVA_INT_UNALIGNED`：实际对齐，但 `_UNALIGNED` 不依赖 segment 基址对齐，堆 segment 也不抛。`MemorySegment.copy(byte[], …)` 一条（可能向量化的）批量拷贝。
* 内存序：数据字节和长度都是普通写；只有 `tail` 用 `setRelease`，它保护之前所有普通写。

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

遇到 PAD：`head` 前进到数据区末尾、**立即发布**（生产者在等这段空间）、`continue` 读下一条（偏移 0）。读到真记录：先拷出来再发布 `head`。

```java
public boolean isDrained() {
    if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
    return head == (long) LONG.getAcquire(seg, OFF_TAIL);
}
```

先 `closed` 后 `tail`（§2.8）。`LONG` 是 `MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)`，坐标 `(MemorySegment, long 字节偏移)`（JDK 21 里 `ValueLayout.JAVA_LONG.varHandle()` 只有 `(MemorySegment)` 一个坐标，JDK 22 才加偏移）。堆上 `byte[]` 段做 8 字节对齐的原子访问会抛 `IllegalArgumentException: Misaligned access`——环必须建在原生 / 映射内存上。

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

* `MessageRing.segmentBytes(capacity)` 在 `FileChannel.open` **之前**调用且自己校验容量（非法 → `IllegalArgumentException`）。顺序有意：若先 `open(…, TRUNCATE_EXISTING)` 再校验，对**已有文件**调 `create(file, 100)` 会先截断再抛异常——调用方丢了数据。
* `try-with-resources` 关的是 `FileChannel`，**映射仍有效**直到 `arena.close()`；失败路径关闭 `arena`，不泄漏映射。

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

### 5.5 跨进程测试怎么写

* **确定性消息**：splitmix64 把序号 `seq` 变伪随机数 `m`；长度 `8 + (m >>> 1) % 49`（8..56）；前 8 字节是 `seq`（大端），其余由 `m` 派生。收的一端用同样函数校验，返回 `null`（对）或错误描述。
* **子进程入口**：`switch (mode)` 表达式选 `consume` / `produce`，成功打印 `OK <count>`，失败打印 `FAIL …` 并退出码 1。生产 / 消费写成 `public static` 方法，进程内测试复用，保证两端对"正确"的定义一致。
* **启动**：`ProcessHandle` 找 `java`；类路径并上被测类位置；加 `--enable-preview -XX:+UseSerialGC`（子 JVM 启动更快、线程更少）。
* **不留孤儿**：`waitFor(超时)`，超时判失败；`finally` 里 `destroyForcibly()`。

---

## 6. Java 21 特性小课

| id | 用在哪 | 老写法 | 新写法 / 为什么 |
|---|---|---|---|
| `VarHandle` | `SpscLongRing` 的 `HEAD`/`TAIL`；`MessageRing` 的 `memorySegmentViewVarHandle` | 全 `volatile`（过强）、`AtomicLong`（布局难控）、`sun.misc.Unsafe`（私有 API） | 对**普通字段**选访问强度；release/acquire 恰是 SPSC 所需；布局自己控制，填充才有意义 |
| FFM | `MessageRing` 建在 `MemorySegment` 上；`SharedChannel` 用 `FileChannel.map(mode, off, size, Arena)` | `MappedByteBuffer`：`int` 索引（≤ 2 GiB）、无确定性取消映射、原子访问要 `Unsafe` | `long` 大小、`Arena.close()` 确定性取消映射、`VarHandle` 原子访问映射内存。JDK 21 预览，22 转正 |
| `Math.clamp`（Java 21） | `SpscLongRing.size()`、`MessageRing.bytesPending()`：`Math.clamp(t - h, 0, capacity)` | `Math.max(0, Math.min(x, capacity))`（嵌套两层，易写反） | 一个方法，语义"夹到 `[min, max]`"；`clamp(long, int, int)` 返回 `int` 省强转 |
| 接口 `default` 方法 | `LongQueue.isFull()`：`default boolean isFull() { return size() == capacity(); }` | 抽象基类（占用唯一继承名额——`SpscLongRing` 的继承链已被填充用掉） | 接口给默认实现，实现类可覆盖（`SpscLongRing.isFull` 只读 `tail` 与 `head`，不依赖近似的 `size()`）。**实际理由**：填充继承链占了 `extends`，公共行为只能放接口 |
| switch 表达式 | 子进程入口 `String err = switch (mode) { case "consume" -> …; case "produce" -> …; default -> … };` | `if / else if` 链 + 临时变量 | 每分支产生值，`default` 必须有（字符串 switch 不能穷尽） |
| `var` | `var ring = MessageRing.init(...)` | 重复写类型 | 右边已写类型 |

---

## 7. 追问预演

### 追问 1：为什么 head / tail 要自由增长，而不是取模后存下标？

存下标时空 / 满不可区分，补救（浪费一格 / 另存 size）各有缺点。自由增长：空 ⇔ `tail - head == 0`，满 ⇔ `== capacity`，不浪费槽位，不需被两线程同时改的 `size`，`long` 溢出要几十万年。

### 追问 2：为什么容量要是 2 的幂？

取模变按位与（`count & (capacity-1)`），除法（几十周期）变一周期；检查 `Integer.bitCount(c) == 1`；代价是容量只能取 2 的幂，空间最多浪费一半。

### 追问 3：为什么 SPSC 不需要 CAS？

每个共享变量只有一个写者（`tail` 只生产者写，`head` 只消费者写），没有"读-改-写"竞争；只需可见性和顺序，release/acquire 足够。多生产者才需 CAS。

### 追问 4：release/acquire 具体保护了什么？去掉会怎样？

生产者 `setRelease(tail)` 保证数据写入先于 tail 可见；消费者 `getAcquire(tail)` 保证读数据晚于读 tail；`head` 方向保护"读完才归还槽位"。去掉（改普通写）：弱内存序 CPU 上消费者读到旧值——Apple M 上很快大量错误；x86 上常碰巧对。

### 追问 5：什么是伪共享？怎么证明它存在？

两线程写同一缓存行里的不同变量，行在两核间来回失效。证明：单变量实验只改两计数器的距离；相邻比分开慢约 2 倍，且呈双峰（取决于两线程是否在同一核心簇）。SPSC 吞吐上收益被噪声掩盖——要给诚实结论。

### 追问 6：cached index 为什么安全？

`head`/`tail` 只增不减，旧快照只低估对方进度：旧 `head` ≤ 真 `head` → 算出占用量偏大 → "旧值说有空位"必定真有空位；"旧值说满"才读真值。正确性来自**单调性**。

### 追问 7：变长消息回绕时怎么处理？什么情况下死锁？

§4.3：PAD 单独发布；若把"PAD + 记录"整体判断，空环 + tail 靠近末尾 + 大消息会永远放不下（消费者没东西可读不前进，两边互相等）；`offer` 返回 `false` 时可能已发布 PAD。

### 追问 8：`null` / `false` 和 drained 怎么区分？

`closed` 标志；`isDrained() = closed && head == tail`；先读 `closed` 再读 `tail`，否则丢最后几条；末尾残留 PAD 要 `poll` 越过后才 drained。

### 追问 9：跨进程时内存序还成立吗？

成立的是硬件 + VarHandle 发出的屏障，不是 JMM 的形式化保证。两进程映射同一批物理页，缓存一致性由硬件保证，release/acquire 约束各自 CPU 和编译器的重排。说法要谨慎。

### 追问 10：怎么测试跨进程代码，怎么避免挂死？

§2.9：子进程 + 确定性消息 + 每端自旋带截止时间 + `waitFor(超时)` + `destroyForcibly`；类路径含被测类实际位置；不依赖 `sleep` 对时序。

### 追问 11：改成多生产者怎么办？

`tail` 要 CAS 竞争（先 CAS 预留，再写，再按序提交——Disruptor 的 `next()` + `publish()`、Aeron 的 `tryClaim` + `commit`）；或每个生产者一个 SPSC 环、消费者轮询多个环（无争用，但无全局顺序）。

### 追问 12：消费者崩溃重启怎么办？

`head`/`tail` 在文件里，重启后 `attach` 能接着读；`head` 读完才发布，崩溃于处理中会重读这条——至少一次（at-least-once），处理需幂等；要恰好一次，需消息带序号并让消费者持久化处理进度。

---

## 8. 常见误区

### 误区 1：以为 x86 上跑通就代表内存序对

x86 不重排 Store-Store，普通写常"碰巧"正确，ARM（含 Apple M、很多云服务器）上就错。**正确**：按 release/acquire 语义写，并在弱内存序机器上测试。

### 误区 2：`head == tail` 就是空

下标取模存储时也可能是满。**正确**：自由增长的计数 + 差值。

### 误区 3：把 PAD + 记录当整体判断能不能放进去

空环上会死锁（§4.3）。**正确**：PAD 单独发布。

### 误区 4：先读 tail 再读 closed

漏掉最后几条。**正确**：先 `closed`（acquire），再 `tail`。

### 误区 5：只传 `java.class.path` 给子进程

运行器用自己的类加载器加载被测类时，子进程 `ClassNotFoundException`。**正确**：加上被测类的 `getCodeSource().getLocation()`。

### 误区 6：用 `Thread.sleep` 等对方

既慢又不可靠。**正确**：协议自己处理（`magic` 最后写；自旋 + 截止时间）。

### 误区 7：在堆上的 `byte[]` segment 上做原子访问

`MemorySegment.ofArray(new byte[n])` 上对 `long` 做 `setRelease` 抛 `Misaligned access`（堆段只保证 1 字节对齐）。**正确**：`Arena.allocate(size, 128)` 或映射文件。

### 误区 8：继承链填充，却把只读字段放在热字段后面

`buf`/`mask` 与 `head` 同行：消费者写 `head` 使生产者的 `buf` 副本失效。**正确**：只读字段放最前面的基类，填充在热字段之间与之后。

---

## 9. 自测题

1. 容量 8 的环，`head = 13`、`tail = 17`，此刻几个元素？下一次 `offer` 写 `buf` 的哪个下标？下一次 `poll` 读哪个下标？
2. 解释 `SpscLongRing.offer` 为什么可用 `cachedHead` 判断"有空位"而不会错误覆盖未读数据。
3. 把 `MessageRing.offer` 里的 `LONG.setRelease(seg, OFF_TAIL, t + rec)` 换成普通写，会出什么 bug？什么机器上更易暴露？
4. 容量 64 的 `MessageRing`，环是空的，`head = tail = 8`。发一条 60 字节消息（`maxPayload` 恰好，记录 64 字节）。逐步写出 `offer`、`poll`、`offer` 三次调用的返回值和每次之后 `bytesPending()`，并说明第一次 `offer` 为何返回那个值。
5. 编程题：不看答案写出 `isDrained()` 的正确实现，并说明读两个变量的顺序为什么不能反。

<details><summary>答案</summary>

1. 元素数 `17 - 13 = 4`；`offer` 写 `buf[17 & 7] = buf[1]`；`poll` 读 `buf[13 & 7] = buf[5]`。
2. `head` 只增不减，所以 `cachedHead ≤ 真 head`，旧值算出的占用量 `t - cachedHead ≥ 真占用量`。旧值说"没满"则真实一定没满，写入槽位确实是消费者已读完的；旧值说"满"才刷新，不会产生错误的"有空位"结论。
3. 数据字节和长度前缀可能晚于 `tail` 对消费者可见：消费者看到 `tail` 前进，读到的长度或 payload 是上一圈旧值（长度错可能读越界到别的记录）。弱内存序机器（ARM，如 Apple M）更易暴露；x86 常碰巧正确。
4. 第一次 `offer`：`idx = 8`，`toEnd = 56 < 64`，需 PAD；空位 64 ≥ 56，写 PAD、`tail` 变 64 并**发布**；真记录要 64 字节，但环里还有 56 字节 PAD 没被消费（`tail - head = 56`），空位只有 8，放不下 → 返回 `false`，`bytesPending() == 56`。`poll`：读到 PAD，跳到偏移 0、`head = 64`，没别的消息 → 返回 `null`，`bytesPending() == 0`。第二次 `offer`：`tail = 64`，`idx = 0`，`toEnd = 64 ≥ 64` 不需 PAD，空位 64 ≥ 64 → `true`，`bytesPending() == 64`。要点：PAD 单独发布加消费者越过 PAD，是大消息最终放得进的两个条件。
5. ```java
   public boolean isDrained() {
       if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
       return head == (long) LONG.getAcquire(seg, OFF_TAIL);
   }
   ```
   生产者先发布最后的 `tail` 再置 `closed`。先读 `closed`：看到 1 就保证（release/acquire）能看到最终 `tail`。若先读 `tail`（旧值，恰好等于 `head`），生产者随后发布最后几条并置 `closed`，再读 `closed` 看到 1，就会误判 drained，丢最后几条。

</details>

---

「延伸」LMAX Disruptor 技术论文（单写者原则、环形缓冲区、缓存行填充）。
