# J16 · 并发原语：Java 内存模型、`volatile`、CAS、`VarHandle`、`LongAdder`、`ConcurrentSkipListMap`、`ReentrantLock`

> 版本：`ReentrantLock` 5 · `AtomicLong` 5 · `ConcurrentSkipListMap` 6 · `LongAdder` 8 · **`VarHandle` 9**。全部正式特性。
> 与 JDK 21 相关：虚拟线程下 `synchronized` 会 **pin**、`ReentrantLock` 不会（J10）；JDK 24 去掉了 `synchronized` 的 pinning。
> 可运行代码：`examples/J16/`。性能数字是粗糙计时（Apple Silicon arm64，12 核），只看趋势，不是基准。
> 前置：会写 `Thread`、`synchronized`、`AtomicInteger`。内存模型、CPU 缓存、CAS 第 1 节从零讲。这是全 kit 最重要也最难的一课，慢慢读。

---

## 1. 先看痛点：为什么「多线程读写同一个变量」比想象中难得多

### 1.1 三个问题：原子性、可见性、有序性

线程 A 写一个变量，线程 B 读它——你以为「A 写完 B 就能看到」。**不是。** 有三类彼此独立的问题：

| 问题 | 一句话 | 例子 |
|---|---|---|
| **原子性**（atomicity） | 一个操作能不能被别的线程「看到一半」 | `count++` 其实是「读、加 1、写」三步，两个线程交错就丢更新 |
| **可见性**（visibility） | A 写的值，B 什么时候、能不能看到 | B 一直读到旧值，永远等不到 `stop = true` |
| **有序性**（ordering） | 代码里先写 x 再写 y，别的线程看到的顺序是不是也是这样 | B 看到了 `ready = true`，却看不到 `ready` 之前写的 `data` |

### 1.2 从零讲：CPU 为什么会让你「看不到」

一台机器读写内存的方式（简化）：

| 部件 | 位置 | 说明 |
|---|---|---|
| 寄存器 | 核 0、核 1 各一份 | 最快，每个核私有 |
| store buffer（写缓冲） | 核 0、核 1 各一份 | 写先放这里，稍后才写进缓存 |
| L1 缓存 | 核 0、核 1 各一份 | 以 64 字节（缓存行）为单位 |
| 共享的 L2/L3 缓存 / 内存 | 核 0 和核 1 共享 | |

* 内存比 CPU 慢上百倍，所以每个核有**私有缓存**；**缓存一致性协议**（如 MESI）保证最终大家看到同一份数据，但不是瞬时的。
* **写缓冲**（store buffer）：核执行 `x = 1` 时不等写落到缓存，先丢进写缓冲继续往下执行，别的核要等它**排空**才看得到。
* 所以：核 0 先写 `x` 后读 `y`，核 1 先写 `y` 后读 `x`——两个「读」都可能发生在对方的「写」可见之前，两个都读到 0。每个线程自己看合理，全局看违反直觉。

**编译器也会动你的代码**：JIT 看到 `while (!stop) n++;` 发现循环里没人写 `stop`，就把 `stop` 读到寄存器里**只读一次**（循环不变量外提，loop-invariant hoisting）。单线程下这是完全正确的优化。

### 1.3 实验一：可见性（`examples/J16/J16Ex1Visibility.java`）

```java
static boolean plainStop;
static volatile boolean volatileStop;
static long spinPlain() { long n = 0; while (!plainStop) n++; return n; }
```

主线程 sleep 300ms 让 reader 被 JIT 编译，然后设 stop = true，`join(1000)`：

```
$ java --enable-preview J16Ex1Visibility
plain   : 1 秒后仍在运行 —— 没看到 stop 的写入！
volatile: 已正常结束

$ java --enable-preview -Xint J16Ex1Visibility        # 关掉 JIT，只用解释器
plain   : 已正常结束
volatile: 已正常结束
```

* 普通字段版：reader 永远停不下来。
* 加 `-Xint`（只解释执行）又「正常」了——**同一份代码，行为取决于 JIT 是否编译了它**。这是并发 bug 最阴险处：开发机、单元测试、低负载下全对，上线跑热才出问题。

### 1.4 实验二：重排序（`J16Ex2Reorder.java`）

```
线程 1: x = 1; r1 = y;        线程 2: y = 1; r2 = x;
```

按「逐句顺序执行」的直觉 r1、r2 不可能同时为 0。100 万次（两次运行，数字会变）：

```
普通字段  ，1000000 次中 (r1,r2)=(0,0) 出现 977579 次    (另一次运行: 990150 次)
volatile  ，1000000 次中 (r1,r2)=(0,0) 出现 0 次
```

几乎每次都出现「不可能」的结果（arm64 内存模型比 x86 弱所以更夸张，x86 上同样能复现，概率低些）。改成 `volatile` 后一次都没有。

### 1.5 Java 内存模型（JMM）：规则怎么写才能说清「什么时候能看到」

需要一套**规则**说明什么情况下线程 B 一定看到线程 A 的写入，这就是 **Java 内存模型**（JMM）。核心概念只有一个：

> **先行发生**（happens-before，HB）：X HB Y ⇒ X 的结果对 Y **可见**，且 X 不会被重排到 Y 之后。

JMM 规定的 HB 规则（面试常问，背下来）：

1. **程序顺序**：同一个线程里，前面的操作 HB 后面的操作。
2. **监视器锁**：对同一把锁，`unlock` HB 之后对它的 `lock`。（`synchronized` 退出 → 进入）
3. **volatile**：对同一个 volatile 变量，写 HB 之后的读。
4. **线程启动**：`t.start()` HB `t` 里的所有操作。
5. **线程终止**：`t` 里所有操作 HB 别的线程里 `t.join()` 的返回。
6. **传递性**：X HB Y 且 Y HB Z ⇒ X HB Z。
7. **final 字段**：构造器正常结束后，`final` 字段的值对任何拿到该对象引用的线程可见（安全发布，freeze）。

**数据竞争（data race）**：两个线程访问同一变量、至少一个是写、且它们之间**没有 HB 关系**。有数据竞争的程序 JMM 几乎不保证什么（只保证「不凭空造值」）。目标：**每一对「写—读」之间都能找到一条 HB 链**。

---

## 2. 语法与 API 逐条讲

### 2.1 `volatile`

```java
static volatile boolean stop;
```

* 保证 1：**可见性**：写入对后续的读可见。
* 保证 2：**有序性**：volatile 写之前的操作不会被重排到它之后；volatile 读之后的操作不会被重排到它之前（规则 3 + 传递性——「用 volatile 标志位发布数据」成立的原因）。
* **不保证原子性**：`volatile int count; count++;` 仍是「读-加-写」三步，会丢更新。`volatile` 只修饰单次读或单次写。
* `long`/`double`：JLS 保证 volatile 的 64 位读写原子（非 volatile 的 64 位在 32 位 JVM 上理论上可拆成两半）。

### 2.2 `synchronized`

互斥（同一时刻只有一个线程进入）+ HB（规则 2）。进入 = 获取 monitor，退出（含异常退出）= 释放。粗但安全。JDK 21 注意：虚拟线程里持锁阻塞会 pin（J10）。

### 2.3 原子类与 CAS

**CAS**（compare-and-swap）：CPU 提供的**原子指令**：

```
compareAndSet(addr, expected, new):
    if (*addr == expected) { *addr = new; return true; }
    else return false;                     // 整个过程不可分割
```

x86 上是 `lock cmpxchg`；ARM 上是 `ldxr/stxr`（LL/SC）或 ARMv8.1 的 `cas`。`AtomicLong.incrementAndGet()` 等价于一个 **CAS 循环**：

```java
long prev;
do { prev = value.get(); } while (!value.compareAndSet(prev, prev + 1));   // 失败说明别人改过，重读重试
```

好处：**无锁**（lock-free）——没有线程会因别的线程被挂起而阻塞，任一时刻总有某个线程成功。代价：竞争激烈时大量重试（2.5）。

**ABA 问题**：CAS 只比较「值是否还是我读到的」，不管中间变没变过。线程 1 读到 `A` 被暂停；线程 2 把 `A` 改 `B` 再改回 `A`；线程 1 恢复，CAS 一比还是 `A`，成功——但世界已经变了。无锁栈是教科书例子（例 4）。对策：给值加**版本号**（`AtomicStampedReference`：引用 + `int` 戳，CAS 同时比较两者；`AtomicMarkableReference` 是布尔标记版）。有 GC 的 Java 里纯"对象引用"的 ABA 少得多（旧对象还被引用就不会被回收再分配到同一地址），但**节点复用/对象池**、**计数器回绕**、**把值当状态机状态**时仍会遇到。

### 2.4 `VarHandle`（Java 9）：「对一个变量做各种力度的原子/有序访问」

**为什么要有它**：

* Java 5–8 对**普通字段**做 CAS 只能用 `AtomicIntegerFieldUpdater`（反射，慢，限制多）或 `sun.misc.Unsafe`（私有 API，JDK 在收紧）。
* `volatile` 太"重"：每次读写都是最强的顺序一致（Sequentially Consistent）保证，很多无锁结构只需要更弱更便宜的保证。

`VarHandle` 把「变量」抽象成句柄，提供**不同强度的访问模式**：

| 模式（方法名前缀） | 保证 | 典型用途 |
|---|---|---|
| plain：`get` / `set` | 没有任何额外保证（等价于普通字段访问） | 线程内自己的数据 |
| **opaque**：`getOpaque` / `setOpaque` | 单个变量上读写不被撕裂、不被编译器缓存/消除（最终会看到）；**不保证**跨变量的顺序 | 自旋等待标志、统计 |
| **acquire / release**：`getAcquire` / `setRelease` | 单向栅栏（见下） | 发布/订阅数据、SPSC 队列 |
| **volatile**：`getVolatile` / `setVolatile` | 完整的 `volatile` 语义（顺序一致） | 同 `volatile` 字段 |
| **CAS 家族**：`compareAndSet`、`compareAndExchange`、`weakCompareAndSet*`、`getAndAdd`、`getAndSet`、`getAndBitwiseOr`... | 原子读-改-写 | 无锁更新 |

**release / acquire**（面试高频）：

* `setRelease(x)`：**之前**的所有读写不会被重排到这次写之后——"向上"的单向门。
* `getAcquire()`：**之后**的所有读写不会被重排到这次读之前——"向下"的单向门。
* B 的 `getAcquire` 读到 A 的 `setRelease` 写的值时，A 在 release 之前写的一切，B 在 acquire 之后都能看到——这就是「发布—订阅」。

```java
// 写者                                 // 读者
price = p; qty = q;                    if ((int) READY.getAcquire(this) == 1) {
READY.setRelease(this, 1);                 use(price, qty);   // 一定看到 p 和 q
                                       }
```

为什么不直接用 `volatile`？**因为 volatile 多禁止了「写之后的读」被重排到写之前（StoreLoad）**——正是 1.4 写缓冲造成的那种重排。禁止它 CPU 必须**排空写缓冲**，x86 上要一条 `lock`/`mfence` 类全栅栏，约十几到几十个周期。release/acquire 不禁止 StoreLoad，所以 x86 上 release 写和 acquire 读**就是普通 mov**（x86 本就不重排 Load-Load / Store-Store / Load-Store），只约束编译器，没有 CPU 栅栏开销。（AArch64 上 HotSpot 把 volatile 和 acquire/release 都编成 `ldar`/`stlr`，差别没 x86 明显，别说得太绝对。）

**用法**：

```java
private static final VarHandle READY;                 // 一定要 static final！
static { READY = MethodHandles.lookup().findVarHandle(Box.class, "ready", int.class); }
...
READY.setRelease(this, 1);
int v = (int) READY.getAcquire(this);                  // 返回 Object 多态签名，要强转
READY.compareAndSet(this, 0, 1);
```

* 另外两种工厂：`MethodHandles.arrayElementVarHandle(long[].class)`（数组元素）、`MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN)`（把 `byte[]` 当 `long` 序列读，`TickerCodec` 在用）。
* 访问方法是"签名多态"的（`Object... args`，编译器按实际参数类型生成调用），返回值需手动 cast。

### 2.5 `LongAdder` 对 `AtomicLong`：竞争下的计数

`AtomicLong.incrementAndGet()` 是对**同一内存位置**的 CAS 循环：8 个线程同时来，每轮只有 1 个成功，其余重试，且**每次失败都让该缓存行在核间来回迁移**（2.7）。线程越多越慢。

`LongAdder`（Java 8）把计数器拆成 **一个 `base` + 一个 `Cell[]` 数组**。

```
低竞争：  所有线程 CAS 同一个 base（和 AtomicLong 一样快）
高竞争：  某次 CAS base 失败 -> 线程根据自己的"探针哈希"选一个 Cell[i] 去加 -> 不同线程大概率落在不同 Cell -> 互不干扰
读取：    sum() = base + Σ cells[i]    （不是原子快照：并发更新时可能得到一个"介于前后"的值）
```

每个 `Cell` 用 `@Contended` 填充缓存行，避免 Cell 间伪共享。

选型：

| | `AtomicLong` | `LongAdder` |
|---|---|---|
| 要的是 | 一个**精确的**当前值，要参与 CAS 决策（序号发号、`compareAndSet`、限额检查） | 只写不频繁读的**统计量**（成交笔数、字节数、命中数） |
| 读 | `get()` O(1)，精确 | `sum()` 要遍历 Cell，不是原子快照 |
| 高竞争写 | 差（重试 + 缓存行抖动） | 好（分散） |
| 内存 | 8 字节 | 高竞争下有多个 Cell，更大 |

### 2.6 `ConcurrentSkipListMap`：并发的有序 Map

* **跳表**（skip list）：在有序链表之上叠几层"快车道"链表，每层是下一层的随机抽样，查找从最高层出发跳过大段，期望 `O(log n)`。比平衡树的好处：**插入/删除只改局部指针，容易做成无锁（CAS）**，并发版本不需全局锁。
* `ConcurrentSkipListMap` 是基于跳表的线程安全 `NavigableMap`：有序，`firstEntry/lastEntry/pollFirstEntry/ceilingEntry/headMap/tailMap`……（Java 21 起 `NavigableMap` 继承 `SequencedMap`）。
* 对比：
  * `TreeMap`：有序，**不是线程安全**，多线程要自己加锁；
  * `ConcurrentHashMap`：线程安全，**无序**；
  * `Collections.synchronizedSortedMap(new TreeMap<>())`：一把大锁，竞争大时瓶颈。
* 限制：迭代器**弱一致**（反映创建后的某些修改，不抛 `ConcurrentModificationException`）；`size()` 是 `O(n)`；key/value 不能为 `null`；`merge`、`compute*` 原子。

订单簿的天然选择：key = 价格，按价格有序取最优档，多线程挂单。

### 2.7 伪共享（false sharing）

CPU 缓存按**缓存行**（x86 常见 64 字节，Apple M 系列 128 字节）搬运和保持一致。线程 A 只改 `a`、线程 B 只改 `b`，而 `a`、`b` 恰在**同一缓存行**：A 写一次，该行在 B 的核里失效；B 写一次，又让 A 的失效。两个互不相干的变量在硬件层面**抢同一块东西**，这叫伪共享。解决：让它们相隔至少一条缓存行（**填充**，padding），JDK 内部用 `@jdk.internal.vm.annotation.Contended`（用户类需 `-XX:-RestrictContended`）。

### 2.8 `ReentrantLock`

比 `synchronized` 多出来的能力：

| 能力 | 代码 |
|---|---|
| 尝试获取，不阻塞 | `lock.tryLock()` |
| 带超时 | `lock.tryLock(100, TimeUnit.MILLISECONDS)` |
| 可被中断地等待 | `lock.lockInterruptibly()` |
| 公平锁（先来先得） | `new ReentrantLock(true)` |
| 多个条件队列 | `lock.newCondition()`（`synchronized` 只有一个 `wait/notify`） |
| 非块结构（在不同方法里加/解锁） | `lock()` / `unlock()` 分开调用 |

**铁律：`unlock()` 必须在 `finally` 里**，否则异常路径永远占着锁。**可重入**（reentrant）：同一线程可重复获取，计数记录，`unlock` 同样次数才真正释放。

虚拟线程：`ReentrantLock` 基于 `LockSupport.park`，阻塞时可卸载，**不 pin**；JDK 21 的 `synchronized` 会。JDK 24 起 `synchronized` 也不 pin，那时只按功能选锁。

---

## 3. 编译器和 JVM 到底做了什么

1. **javac 几乎不重排**，重排主要在 **JIT（C2）** 和 **CPU**。`volatile` 字段读写在字节码里只是带 `ACC_VOLATILE` 的 `getfield/putfield`，真正约束由 JIT 生成机器码时落实。
2. **JIT 实现 HB**：在 volatile 读写前后**插入内存屏障**，并禁止编译器跨屏障重排和缓存。1.3 中 JIT 把 `stop` 提出循环，正因它是普通字段，没有屏障阻止。
3. **x86 与 ARM**：x86 是较强的内存模型（TSO），只允许 StoreLoad 重排，volatile 写补一个 StoreLoad 栅栏；ARM 更弱，允许四种重排，没保护的代码更容易现形（1.4 的 98% 就是这么来的）。**x86 开发机"测不出来"的 bug，部署到 ARM（Graviton、Apple Silicon）服务器可能当场爆。**
4. **CAS 是 intrinsic**：`compareAndSet` 被 C2 直接编译成 CPU 原子指令。
5. **`VarHandle` 必须 `static final`**：JIT 知道它是常量才能把整个访问内联成一条机器指令；放普通字段或局部变量会走较慢的通用路径——最容易被忽略的性能前提。
6. **`synchronized`** 在 HotSpot 先是轻量级锁（对象头上 CAS），竞争时膨胀成重量级 monitor（阻塞线程要走内核）。

---

## 4. 例子（由浅入深）

### 例 1（最简单）：可见性与重排序

见 1.3、1.4。结论：**`volatile` 修复可见性，也禁止了那种 StoreLoad 重排**。

### 例 2：计数器——四种写法对比（`J16Ex3Counters.java`）

`int++` 不保护 / `synchronized` / `AtomicLong` / `LongAdder`，每线程加 200 万次（ms，粗糙计时）：

```
threads  int++(丢更新)             synchronized           AtomicLong             LongAdder
1        2ms 值=2000000          6ms                    2ms                    6ms 值=2000000
2        3ms 值=2095019          252ms                  33ms                   7ms 值=4000000
         ^ int++ 期望 4000000，实际 2095019，丢了 1904981
4        4ms 值=2185533          301ms                  55ms                   6ms 值=8000000
         ^ int++ 期望 8000000，实际 2185533，丢了 5814467
8        5ms 值=2074320          573ms                  123ms                  9ms 值=16000000
         ^ int++ 期望 16000000，实际 2074320，丢了 13925680
```

读法：

* `int++` 最快，但**值错得离谱**（期望 400 万，得 209 万）——丢更新（原子性）。**不正确的快没有意义**。
* 单线程时差不多；线程一多，`synchronized` 掉到数百 ms（锁竞争 + 阻塞/唤醒），`AtomicLong` 其次（CAS 重试 + 缓存行抖动），`LongAdder` **几乎不随线程数增长**（各线程写自己的 Cell）。
* 8 线程时 `LongAdder` 比 `AtomicLong` 快 10 倍以上，比 `synchronized` 快 60 倍以上（趋势才是重点）。

### 例 3（贴近真实）：无锁单生产者单消费者队列（`J16Ex4VarHandle.java`）

行情线程（生产者）把消息放进环形队列，策略线程（消费者）取。**只有一个生产者一个消费者**，`head`（只有消费者写）和 `tail`（只有生产者写）各有唯一写者，不需 CAS，只要 release/acquire：

```java
boolean offer(long v) {                          // 生产者
    long t = tail;                               // 自己写的，普通读
    long h = (long) HEAD.getAcquire(this);       // 读对方的进度
    if (t - h == buf.length) return false;       // 满
    buf[(int) (t & mask)] = v;                   // 1. 先写数据
    TAIL.setRelease(this, t + 1);                // 2. release 发布：消费者看到新 tail 就一定看到上面的数据
    return true;
}
long poll() {                                    // 消费者
    long h = head;
    long t = (long) TAIL.getAcquire(this);       // acquire
    if (h == t) return Long.MIN_VALUE;           // 空
    long v = buf[(int) (h & mask)];
    HEAD.setRelease(this, h + 1);                // 归还槽位给生产者
    return v;
}
```

输出：

```
场景 A 读到 price=18950 qty=100
场景 B SPSC: 和=12500002500000 期望=12500002500000 一致=true，约 163 ms（无锁，只用 release/acquire）
```

500 万个数，校验和精确一致。这就是 LMAX Disruptor 的核心思想。

### 例 4：CAS 循环与 ABA（`J16Ex5Cas.java`）

确定性复现：初始栈 `A→B→C`；线程 1 读到 `top=A`、`next=B` 后暂停；线程 2 弹出 A、弹出 B、再把 A 压回；线程 1 恢复做 `CAS(top, A, B)`：

```
正确结果应是 [C ]：A、B 都被弹走过，线程 2 把 A 压回，线程 1 再把 A 弹掉，只剩 C
朴素版 最终栈 = [B C ]   <- B 已被线程 2 弹走，却又回到栈里（线程 1 的 CAS 看到 top 仍是 A 就成功，把 top 设成了过期的 B）
加版本号 最终栈 = [C ]
```

朴素版里 CAS 成功了（`top` 确实还是 A），但 B 早不该在栈里——这就是 ABA。`AtomicStampedReference` 版里线程 2 每次改动戳 +1，线程 1 的 CAS 因戳不同失败，重读后得到正确结果。

### 例 5：并发有序 Map（`J16Ex6Skip.java`）

4 个线程各 5 万次随机挂单到 `ConcurrentSkipListMap<Long, Long>`（价格 18950–19049），用 `merge(price, 1L, Long::sum)` 原子累加该价位数量：

```
价位数 = 100, 总量 = 200000 (期望 200000)
最优卖价 firstEntry = 18950=1988
最高卖价 lastEntry  = 19049=1987
价位 >= 19000 的前 3 个 = [19000=2018, 19001=1998, 19002=1951]
pollFirstEntry(原子取走最优价位) = 18950=1988，之后最优 = 18951
```

总量守恒；`firstEntry` 即最优价；`pollFirstEntry` 一步原子"取走并删除"最优档。

### 例 6：`ReentrantLock` + `Condition` 与 `tryLock`（`J16Ex7Lock.java`）

```java
void put(T x) throws InterruptedException {
    lock.lockInterruptibly();
    try {
        while (count == items.length) notFull.await();     // 用 while 不用 if：防"虚假唤醒"
        ...; notEmpty.signal();
    } finally { lock.unlock(); }
}
```

```
有界缓冲(容量4)传 1..1000，和 = 500500 (期望 500500)
另一个线程 tryLock(100ms) = false（锁被主线程占着，放弃而不是死等）
主线程 isHeldByCurrentThread = true, holdCount = 1
```

生产者消费者跑在**虚拟线程**上，`await()` 时被卸载，不占载体。`tryLock(超时)` 是避免死锁的常用办法：拿不到就退让。

### 例 7：伪共享（`J16Ex8FalseSharing.java`）

两个线程各改 `AtomicLongArray` 的一个元素：下标 (0,1) 相邻（同一缓存行）vs (0,32) 相距 256 字节，每线程 5000 万次：

```
第 1 轮：相邻(下标 0,1) 270 ms  vs  分开(下标 0,32) 161 ms
第 2 轮：相邻(下标 0,1) 294 ms  vs  分开(下标 0,32) 142 ms
第 3 轮：相邻(下标 0,1) 149 ms  vs  分开(下标 0,32) 115 ms
```

相邻的更慢，三轮方向一致，幅度波动（机器有别的负载）。逻辑上两线程毫无关系，纯因共享缓存行变慢。

---

## 5. 坑与限制

1. **`volatile` 不是原子的**：`volatile long n; n++` 照样丢更新；需原子复合操作用 `AtomicLong`/`LongAdder`/锁。
2. **`volatile` 数组**：`volatile int[] a` 只让**引用**可见，元素读写不是 volatile；元素级用 `AtomicIntegerArray` 或 `MethodHandles.arrayElementVarHandle`。
3. **双重检查锁（DCL）必须 `volatile`**：`if (inst == null) synchronized (...) { if (inst == null) inst = new X(); }` 里 `inst` 非 volatile，另一线程可能看到"引用非 null 但对象还没构造完"（构造与赋值被重排）。
4. **`LongAdder.sum()` 不是快照**：别拿它做"达到阈值就触发"的精确判断，也别拿它发序号。
5. **CAS 循环里别做副作用**：失败会重试，副作用重复执行。
6. **ABA**：`compareAndSet` 比较的是引用/值，不是"没人动过"（2.3、例 4）。
7. **`VarHandle` 要 `static final`**，访问方法需强转；错误类型在**运行时**才抛 `WrongMethodTypeException`/`ClassCastException`。
8. **`ReentrantLock` 忘记 `unlock`**：永远 `try { ... } finally { lock.unlock(); }`；`lock()` 放 `try` **外面**（否则 `lock()` 自己失败时 `finally` 会错误解锁）。
9. **伪共享**：只在高频写、多线程、相邻变量时显现；先用 profiler 确认，别预先到处填充。
10. **`ConcurrentSkipListMap.size()` 是 O(n)**；弱一致迭代器；key/value 不许 `null`。
11. **`ReentrantLock` 换 `synchronized` 不是"总是更好"**：JDK 24 起 `synchronized` 在虚拟线程里不再 pin，简单互斥用 `synchronized` 更短且不会漏 `unlock`。
12. **"在我机器上没问题"不是证据**：x86 比 ARM 宽容；JIT 未编译比已编译宽容；低负载比高负载宽容。用 `jcstress`（OpenJDK 并发压力测试工具）才算验证。

---

## 6. 真实代码里的并发原语

**`SharedMean`**（单写者、多读者的队列均值）——2.4 的完整真实例子：

```java
private static final VarHandle PUBLISHED;
private static final VarHandle OWNER;
static { ... PUBLISHED = l.findVarHandle(SharedMean.class, "published", Stat.class);
              OWNER = l.findVarHandle(SharedMean.class, "owner", Thread.class); }

/** 任意线程可调。 */
public Stat read() { return (Stat) PUBLISHED.getAcquire(this); }

private void publish() {
    PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum()));
}

private void claimWriter() {
    Thread me = Thread.currentThread();
    Thread cur = (Thread) OWNER.getAcquire(this);
    if (cur == me) return;
    if (cur != null || !OWNER.compareAndSet(this, null, me)) {
        throw new IllegalStateException("single-writer violated: owned by " + OWNER.getAcquire(this));
    }
}
```

对照：

* **`static final VarHandle`**（2.4、坑 7）。
* **发布不可变快照** `Stat(seq, size, sum)`：写者 `setRelease`，读者 `getAcquire` 读一次引用——读到的一定是某个真实时刻的一致快照，**不会读到"新 sum + 旧 size"这种撕裂值**。这是不可变对象 + release/acquire 的标准配方：对象构造时的所有字段写入都在 `setRelease` 之前，对 `getAcquire` 之后的读可见。
* **`OWNER.compareAndSet(this, null, me)`**：第一个写者用 CAS 抢占"唯一写者"身份，其他线程再写抛 `IllegalStateException`——CAS 做"一次性占位"（2.3）。
* 为什么不用 `volatile Stat published`？可以，更简单；用 release/acquire 是为演示更弱的内存序足够（单写者不需读-改-写原子性，只需发布顺序）。

**`TickerCodec`**：

```java
private static final VarHandle BE_LONG = MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN);
...
long word = (long) BE_LONG.get(buf, off);     // 一次读出 8 字节，大端
```

2.4 的 `byteArrayViewVarHandle`：把 `byte[]` 当 `long` 序列读，不必逐字节拼。这里是 plain `get`，无并发语义，只为"一次读 8 字节"。

**`ConcurrentMerge`**：
* `private final AtomicBoolean closed = new AtomicBoolean();` 与 `close()` 里的 `if (!closed.compareAndSet(false, true)) return;`：CAS 实现**幂等关闭**，多线程同时调 `close()` 只有一个真正执行（2.3 的一次性开关）。
* 数据通道用 `ArrayBlockingQueue`（内部 `ReentrantLock` + `Condition`，即 2.8/例 6 的结构），生产者阻塞在 `put` 时虚拟线程可卸载。

**`OrderBook`**：`SequencedMap<Long, PriceLevel> bids = new java.util.TreeMap<>(Comparator.reverseOrder());`——订单簿价位表。当前设计是**单线程撮合**（Disruptor 式：一个线程独占订单簿，别的线程通过队列投递命令），所以用普通 `TreeMap`。面试官问"多线程共享这个簿怎么办"：先说"单写线程 + 队列"，再说"必须共享就换 `ConcurrentSkipListMap`，但 `PriceLevel` 里 FIFO 和 `total` 的复合更新还需要锁或不可变替换"。

参考实现里没有用 `LongAdder`、`ConcurrentSkipListMap`、`ReentrantLock`、`synchronized`、`volatile`；它们作为概念课出现，是因为面试会问。

---

## 7. 自测题

1. 说出 JMM 的至少 5 条 happens-before 规则。为什么 `volatile` 标志位能发布数据？
2. `volatile int count; void inc() { count++; }` 为什么仍然错？怎么改？
3. 解释 release/acquire，并说明为什么 SPSC 队列里 `tail` 用 `setRelease` 写、`getAcquire` 读就够了，不需 `volatile`。
4. 什么是 ABA？举一个无锁栈的例子，说出两种对策。
5. `LongAdder` 为什么在高竞争下比 `AtomicLong` 快？代价是什么？什么时候不能用？
6. 什么是伪共享？怎么检测、怎么避免？
7. （面试表述）「JDK 21 里为什么在虚拟线程中要用 `ReentrantLock` 而不是 `synchronized`？」

<details><summary>答案</summary>

1. 程序顺序；监视器锁（unlock HB 后续 lock）；volatile（写 HB 后续读）；线程启动；线程终止；传递性；final 字段冻结。volatile 写之前的操作 HB 它之后的读（程序顺序 + volatile 规则 + 传递性），所以先写数据再写标志，读者读到标志后一定看到数据。
2. `count++` 是读-加-写三步，volatile 只保证单次读写可见，不保证复合操作原子；两线程读到同一旧值各写回一次，丢一次更新。改 `AtomicInteger.incrementAndGet()`、`LongAdder.increment()` 或加锁。
3. release 写保证此前的写（含槽位数据）不被重排到它之后；acquire 读保证此后的读不被重排到它之前；消费者 acquire 读到新 tail，就一定看到生产者在 release 前写进槽位的数据。队列正确性不需要"写之后的读不能越过写"（StoreLoad），所以不付 volatile 全栅栏的代价（x86 上尤其明显）。
4. CAS 只比较值：线程 1 读到 A 被暂停，线程 2 把 A→B→A，线程 1 的 CAS 仍成功但中间状态已变（例 4 朴素版栈把已弹出的 B 重新挂回栈顶）。对策：带版本号的 `AtomicStampedReference`/`AtomicMarkableReference`；不复用节点（靠 GC 保证旧引用不指向新对象）；用锁。
5. 热点拆成 base + 多个 Cell，高竞争时不同线程更新不同 Cell（且 Cell 填充过，避免伪共享），避免同一内存位置的 CAS 重试和缓存行抖动。代价：`sum()` 要遍历且不是原子快照，占更多内存；不能用于需要精确当前值参与决策的场合（序号分配、限额 CAS 检查）。
6. 两个互不相关的变量在同一缓存行，不同核写它们会不断使对方缓存行失效。检测：性能剖析看缓存未命中/`perf c2c`，或像例 7 做对照实验。避免：填充或拆到不同缓存行（`@Contended`、手动 padding），或每线程用自己的状态再合并（LongAdder 思路）。
7. JDK 21 里虚拟线程在 `synchronized` 内阻塞会 pin 住载体线程（无法卸载），载体有限，可能耗尽吞吐；`ReentrantLock` 基于 `LockSupport.park`，阻塞时可卸载。JDK 24 修复了 `synchronized` 的 pinning，之后这一理由不再成立。

</details>

---

「延伸」J17 FFM API：堆外内存与原生调用。
