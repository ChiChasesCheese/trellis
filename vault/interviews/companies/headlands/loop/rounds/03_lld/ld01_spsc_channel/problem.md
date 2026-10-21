# ld01 · 共享内存 SPSC 消息通道（Shared-Memory Single-Writer Single-Reader Channel）

## 背景

行情进程把一条条消息交给策略进程，要求：只有一个写者、一个读者；有界（满了要告诉写者，不能无限涨）；不丢、不重、不乱序；
生产者说"没有更多了"之后，消费者要能区分"暂时没有"和"永远没有了"（这就是 **drained**）。
没有锁、没有系统调用在热路径上——两个进程直接读写同一块物理内存。

## 读题前你需要知道

最少要先懂：

* **进程 vs 线程、进程间通信（IPC）**：线程共享同一地址空间；进程各有独立地址空间，要通信得借助内核提供的机制。共享内存（把同一个文件 / 内存区域映射进两个进程，`mmap`）是最快的一种，因为热路径上没有系统调用和拷贝；
* **环形缓冲区**：固定容量 `capacity`（2 的幂）的数组，`head`（读计数）和 `tail`（写计数）都只增不减，下标 = 计数 `& (capacity-1)`；`tail - head == 0` 为空，`== capacity` 为满，这样空和满是两个不同的差值，不用空一格；
* **release / acquire**：写者先写数据，再用 release 写发布 `tail`；读者用 acquire 读 `tail`，之后读到的数据一定是写者在 release 之前写好的。弱内存序的 CPU（ARM / Apple M）上没有这对屏障，读者可能看到新 `tail` 却读到旧数据；
* **缓存行与伪共享**：CPU 以 64 / 128 字节的缓存行为单位搬运数据。两个线程分别写同一缓存行里的不同变量时，这一行在两核之间来回失效，互相拖慢（伪共享）；解法是把它们隔开至少一条缓存行；
* **FFM `MemorySegment`**：Java 的堆外内存视图，可由 `FileChannel.map` 得到，用 `VarHandle` 按偏移量做带内存序的读写。

## 概述

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `LongRing` (`LongQueue`) | 单线程语义的环形缓冲区：`long` 元素，2 的幂容量，head/tail 计数，满 / 空规则 | 为什么计数自由增长；`& mask` 代替 `%`；没有哨兵值 |
| 2 | `SpscLongRing` | 线程安全 SPSC：`VarHandle` `setRelease`/`getAcquire`、cached index、填充防伪共享 | 内存序；为什么不需要 CAS；怎么**测量**伪共享 |
| 3 | `MessageRing` | 变长消息：长度前缀、8 字节对齐、回绕（PAD 记录）、`finish`/`isDrained`；建在 `MemorySegment` 上 | 回绕不能把记录切成两半；PAD 必须单独发布否则死锁 |
| 4 | `SharedChannel` | 同一个环放进**内存映射文件**；两个独立 JVM 进程各 `mmap` 一份 | 跨进程测试：怎么找到 `java`、怎么传 classpath、怎么保证不挂死 |

所有类在默认包。`LongQueue` 接口（含 `default isFull()`）starter 里已给出。

## 共同约定

* **满不是错误**：`offer` 返回 `false`；**空**：`LongQueue.poll()` 抛 `NoSuchElementException`（`long` 的每个取值都可能是合法消息，没有哨兵）；`MessageRing.poll()` 返回 `null`。
* 容量必须是 2 的幂：`LongQueue` 系 `[1, 2^30]`，`MessageRing` 系 `[16, 2^30]`；否则构造器 / `init` 抛 `IllegalArgumentException`。
* **线程 / 进程角色**：一个对象只做一种角色。生产者对象调 `offer`/`finish`，消费者对象调 `poll`/`isDrained`；`size()`、`bytesPending()` 任何角色可调，是近似值。

## Part 1 · `LongRing`（单线程环形缓冲区）

```java
public interface LongQueue {
    int capacity();  int size();  boolean offer(long value);  long poll();  boolean isEmpty();
    default boolean isFull() { return size() == capacity(); }
}
public final class LongRing implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;
    public LongRing(int capacity)         // 2 的幂，否则 IllegalArgumentException
}
```

* `head`、`tail` 是只增不减的 `long` 计数；元素个数 `tail - head`；槽位下标 `计数 & mask`。**空** ⇔ `head == tail`，**满** ⇔ `tail - head == capacity`。不浪费槽位，不另存 size。
* `offer` 满了返回 `false`，**不覆盖**最旧的元素；`poll` 空了抛 `NoSuchElementException`。
* 所有 `long` 值（含 `Long.MIN_VALUE`、`-1`、`0`）都是合法消息。
* 100 万次、1000 万次 `offer`/`poll` 之后计数仍然正确（不会因为下标回绕出错）。

## Part 2 · `SpscLongRing`（线程安全 + 性能）

```java
public final class SpscLongRing implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;
    public SpscLongRing(int capacity)
    // 同 LongQueue；isEmpty/poll 仅消费者线程，offer/isFull 仅生产者线程，size() 任何线程
}
```

* **正确性**：恰好一个生产者线程 + 一个消费者线程，按序、恰好一次。**不许用锁、不许用 CAS**（`tail` 只有生产者写、`head` 只有消费者写，每个变量只有一个写者）。用 `VarHandle` 的 `setRelease` 发布下标、`getAcquire` 读对方的下标：
  先写数据再 release 发布 `tail`；消费者 acquire 读 `tail` 之后才读数据；读完数据再 release 发布 `head`。
* **cached index**：生产者缓存对方的 `head`，只有"按旧值看是满的"才去读真正的 `head`；消费者缓存 `tail`，同理。
* **填充**：生产者写的字段与消费者写的字段相隔至少一条缓存行（Apple M 系列 128 字节）。Java 里常用继承链 + 填充 `long` 的办法：把生产者字段、消费者字段分别放在不同的父类里，父类之间插入若干个填充用的 `long` 字段。
* **测量**（不是断言，是你应该会做的事）：单独量伪共享（两个线程各自自增相邻 / 相隔一条缓存行的计数器），再比较 SPSC 的几种写法（volatile、acquire/release、加填充、加 cached index）的吞吐。
* 不得有"消费者读到上一轮留下的旧值"（把 `setRelease` 改成普通写，在 ARM 上会立刻出错）。

## Part 3 · `MessageRing`（变长消息 + 回绕）

```java
public final class MessageRing {
    public static final int HEADER_BYTES = 512;  MIN_CAPACITY = 16;  MAX_CAPACITY = 1 << 30;
    public static long segmentBytes(int capacity)                 // HEADER_BYTES + capacity
    public static MessageRing init(MemorySegment seg, int capacity)    // 建一个全新的环
    public static MessageRing attach(MemorySegment seg)                // 连接已有的环（比如另一个进程建的）
    public int capacity();  public int maxPayload();               // = capacity - 4
    public boolean offer(byte[] msg);   public void finish();      // 生产者
    public byte[] poll();               public boolean isDrained();   // 消费者
    public long bytesPending();                                    // 含 PAD，近似值
}
```

### 布局

```
偏移    0  magic     long   0x5350534352494E47 ("SPSCRING")，最后用 release 写
偏移    8  capacity  int
偏移   12  version   int    = 1
偏移  128  head      long   消费者已消费的字节计数（只有消费者写）
偏移  256  tail      long   生产者已发布的字节计数（只有生产者写）
偏移  264  closed    long   生产者 finish() 后置 1
偏移  512  数据区    capacity 字节
```

记录 = `[len:int32][payload][补零到 8 字节对齐]`，总长 `(4 + len + 7) & ~7`。放不下连续的一整条时，先写一条 **PAD 记录**（`len = -1`）占满到数据区末尾，再从开头写真记录。

### 规则

* `init`：清零头部、写 `capacity`/`version`，**最后**才 release 写 `magic`；`capacity` 非法或 segment 太小 → `IllegalArgumentException`。`attach`：`magic`/`version`/尺寸不对 → `IllegalStateException`。
* `offer`：`msg.length > maxPayload()` → `IllegalArgumentException`（**永远**放不下，不同于"暂时满"）；暂时放不下 → `false`；`finish()` 之后 → `IllegalStateException`。
* **PAD 要单独发布**：需要 PAD 时，只要有 PAD 那么多的空间就先写 PAD 并发布 `tail`，即使随后真记录没挤进去（`offer` 返回 `false`）。否则空环上 `tail` 恰好靠近末尾、`pad + 记录 > capacity` 时永远放不进去（死锁）。
  代价是：`offer` 返回 `false` 时可能已经悄悄发布了一条 PAD；消费者越过它（`poll` 返回 `null`）之后，下一次 `offer` 才放得下。
* `poll`：没有消息返回 `null`（遇到 PAD 就越过它，不算消息）。`null` **不等于**结束。
* `isDrained`：生产者已 `finish` **且** `head` 追上了 `tail`（包括末尾残留的 PAD）。**先读 `closed` 再读 `tail`**。
* 内存序同 Part 2：写完记录字节后 release 发布 `tail`；消费者 acquire 读 `tail` 后才读字节；读完 release 发布 `head`。数据区的字节读写是普通读写。
  `VarHandle` 可用 `MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)`（坐标：段、字节偏移）。**堆上的 `byte[]` 段不支持这种原子访问**——测试用 `Arena.ofShared().allocate(bytes, 128)`。

## Part 4 · `SharedChannel`（内存映射文件，两个进程）

```java
public final class SharedChannel implements AutoCloseable {
    public static SharedChannel create(Path file, int capacity) throws IOException
    public static SharedChannel open(Path file) throws IOException
    public int capacity();  public int maxPayload();
    public boolean send(byte[] msg);   public void finish();           // 生产者
    public byte[] receive();           public boolean isDrained();     // 消费者
    public void close();                                               // 取消映射，幂等，不删文件
}
```

* `create`：新建 / 覆盖文件，大小 `MessageRing.segmentBytes(capacity)`；`FileChannel.map(READ_WRITE, 0, size, arena)` 得到 `MemorySegment`（`Arena.ofShared()`）；`MessageRing.init`。`capacity` 非法 → `IllegalArgumentException`，且**不要动文件**。
* `open`：映射已有文件并 `attach`；文件不存在 → `NoSuchFileException`；文件太小 / 全零 / 随机内容 → `IllegalStateException`。
* `close` 之后 `send`/`receive` 抛 `IllegalStateException`；文件留在磁盘上。关闭后重新 `open`，积压的消息还在（数据在文件里）。
* **跨进程测试怎么做**（父进程 + 子进程）：
  * 找 `java`：`ProcessHandle.current().info().command()`，取不到退回 `System.getProperty("java.home")/bin/java`；
  * 类路径：`System.getProperty("java.class.path")` **加上**被测类和子进程入口类所在的目录（`getProtectionDomain().getCodeSource().getLocation()`）。用 JUnit console 的 `--class-path` 跑时，`java.class.path` 只有 junit 的 jar，被测类在另一个类加载器里，光传 `java.class.path` 子进程找不到 `SharedChannel`；
  * 必须传 `--enable-preview`（FFM 在 JDK 21 是预览）；
  * 子进程成功时打印 `OK <count>` 并以 0 退出，失败打印 `FAIL <原因>` 以 1 退出；父进程用 `waitFor(超时)`，超时 `destroyForcibly()`；两端的自旋循环都带截止时间——**任何一端挂死都不能让整个测试挂死**；
  * 三个用例：父生产→子消费；子生产→父消费；父先写完并 `close`，子之后才启动再读（证明数据在文件里）。每条消息的长度和内容由序号决定（`Msgs.make(seq)`），收的人不需要额外信息就能校验"是不是第 seq 条"——丢、重、乱序、截断都会被抓到。

## 样例

```java
var q = new LongRing(4);
q.offer(10); q.offer(20); q.offer(30); q.offer(40);
q.offer(50);          // false —— 满了
q.poll();             // 10
q.offer(50);          // true —— 回绕到数组开头
q.size();             // 4

var seg = Arena.ofShared().allocate(MessageRing.segmentBytes(64), 128);
var ring = MessageRing.init(seg, 64);
ring.offer(new byte[20]);     // 记录 24 字节
ring.offer(new byte[20]);     // 记录 24 字节，tail = 48
ring.poll(); ring.poll();     // head = 48，环空
ring.offer(new byte[20]);     // 到末尾只剩 16 < 24：先发布 16 字节的 PAD，再从开头写 24 字节 → bytesPending() == 40
```

## 边界清单（隐藏测试会打）

| 类别 | 例子 |
|---|---|
| 容量 | `0`、负数、非 2 的幂、`2^30 + 1`、`Integer.MIN_VALUE`；`MessageRing` 另有 `< 16`；容量 1 的 `LongRing` |
| 满 / 空 | 满了 `offer` 不覆盖；空了 `poll` 抛 / 返回 `null`；满 → 腾一个 → 回绕写入 |
| 值 | `Long.MIN_VALUE`、`-1`、`0`、`Long.MAX_VALUE` 都是合法消息 |
| 计数 | 百万次之后仍正确；`size()` 不为负、不超过容量 |
| 消息 | 空消息（`len = 0`，占 8 字节）、`len = 4`（4+4=8）、`len = 5`（4+5→16）、`len = maxPayload()`（恰好占满）、`maxPayload()+1`（IAE）、含 `0xFF` / `0` 的二进制 |
| 回绕 | 到末尾剩 8 字节；剩的不够放当前记录；PAD 已发布但真记录没挤进去；空环 + 最大消息 + `tail` 在任意位置 |
| drained | 空但没 `finish` ≠ drained；有消息没读完 ≠ drained；末尾残留 PAD 要越过才 drained；`finish` 之后 `offer` 抛异常 |
| 内存序 | 消费者不能读到上一轮的旧值；`tail` 不能先于数据可见 |
| 进程 | 文件不存在 / 太小 / 全零 / 随机内容；`close` 后访问；`close` 后重开仍有积压；子进程崩溃 / 超时不挂死 |
| 性能 | 单线程 1000 万次 `offer+poll` < 2 s；两线程 1000 万条 `long` < 2 s；200 万条变长消息 < 2–3 s |

## 相关变体

* C++ 版：`std::atomic<uint64_t>` + `memory_order_release/acquire`，`mmap`/`shm_open`；追问 `alignas(64)`、`std::hardware_destructive_interference_size`。
* 多生产者：`tail` 变成 CAS 竞争，或每个生产者一个环（SPSC 的 N 个副本）——这时才需要 `compareAndSet`；
* 消息带"所有权转移"：不拷贝，生产者写到环里预留的区域再"提交"（Aeron 的 `claim/commit`，Disruptor 的 `next()/publish()`）；
* 通道要能跨崩溃恢复：消费者崩溃重启后从哪里继续？（把 `head` 放在文件里，这里的实现已经做了，但"处理了一半的消息"需要幂等设计。）

## 考什么

不是"写一个环形缓冲区"，而是：**每个共享变量只有一个写者时，release/acquire 就够了**（不需要 CAS）；
**为什么 head/tail 要自由增长**；**变长消息回绕时的活性问题**（PAD 必须单独发布）；**跨进程的内存序依然成立**，以及**怎么测试它**（子进程、截止时间、确定性消息）。
