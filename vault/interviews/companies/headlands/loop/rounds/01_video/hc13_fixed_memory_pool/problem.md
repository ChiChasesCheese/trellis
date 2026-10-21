# hc13 · 定长内存池（Fixed-Size Memory Pool）

## 背景

低延迟系统（行情网关、撮合引擎）不希望在热路径上 `new`：每次 `new` 都在给垃圾回收器（GC）添工作，GC 的停顿会直接变成延迟毛刺。
常见做法是启动时一次性准备好 `capacity` 个等大的块，运行时只在池里「借」和「还」。你要写的就是这个池。

## 读题前你需要知道

最少要先懂：

* **空闲链表（free list）**：把「还没被借走的块」串成一条链，借 = 摘链头，还 = 插链头，都是 O(1)；
* **GC 压力**为什么会变成延迟：分配越快，GC 越频繁；GC 停顿（pause）期间应用线程被挂起，这段时间直接计入请求延迟，表现为偶发的尾延迟毛刺；
* **CAS（compare-and-set）** 和 **ABA 问题**：`CAS(x, expected, new)` 原子地「当 x 仍等于 expected 才写入 new」。ABA 指 x 从 A 变成 B 又变回 A，CAS 看不出中间发生过变化而误判成功；常见解法是给值附一个每次修改都递增的版本号（tag / generation）；
* **堆外内存**与 FFM：用 `Arena` / `MemorySegment` 在 GC 管不到的地方分配一整块内存，GC 看不见它，代价是要手动 `close`、自己做边界与生命周期管理；
* **CPU 缓存**：数据连续排布时，一次读入一条 64 字节的缓存行就带进好几条记录，比跟着指针到处跳快得多。

## 概述

| Part | 类 | 内容 | 新增的难点 |
|---|---|---|---|
| 1 | `IndexPool` | 块 = `int` 编号；`allocate` / `free`；重复归还与非法编号检测；O(1) | 把「是否在用」和「链表指针」塞进同一个 `int[]` |
| 2 | `GenPool` | handle = `long`（高 32 位版本号 + 低 32 位槽位）；检测 use-after-free 与 ABA | 位运算打包、符号扩展、版本号回绕 |
| 3 | `OffHeapOrderPool` | 一块 FFM `MemorySegment`（来自 `Arena`），32 字节定长记录，用 `ValueLayout` / `MemoryLayout` 读写 | 堆外布局、清零、生命周期（`close`） |
| 4 | `ConcurrentPool` | 线程安全：无锁 Treiber 栈 + 带 tag 的 head（`VarHandle` CAS） | ABA、内存序、并发 double-free |

所有类在默认包。`FreeResult`（enum）、`Order`（record）starter 里已给出，不要改。

## 共同约定

```java
public enum FreeResult { FREED, DOUBLE_FREE, INVALID }
public record Order(long id, long px, int qty, int side) { public static final Order ZERO = new Order(0, 0, 0, 0); }
```

* **池满不是错误**：`allocate()` 返回 `NONE`（`IndexPool.NONE = -1`；handle 池的 `NONE = -1L`），不抛异常。
* **归还返回 `FreeResult`**，不抛异常（Part 1 另有 `freeOrThrow`）：
  * `FREED`：成功；
  * `DOUBLE_FREE`：这块当前不在使用中——已经还过，或（Part 2+）handle 已陈旧；
  * `INVALID`：根本不是这个池发出的编号——越界、`NONE`、全零 handle、从没发过的版本号。
* 容量必须在 `[1, 1 << 28]`，否则构造器抛 `IllegalArgumentException`。
* **分配顺序**：初始依次 `0, 1, 2, …`；归还的块插在链头，所以「最后归还的最先被再分配」（LIFO）。这是约定：对缓存友好，并且让测试可以确定地断言。

## Part 1 · `IndexPool`（int 编号 + int 空闲链表）

```java
public final class IndexPool {
    public static final int NONE = -1;
    public static final int MAX_CAPACITY = 1 << 28;
    public IndexPool(int capacity)
    public int capacity()
    public int available()
    public int allocate()                    // 池空 → NONE
    public FreeResult free(int block)        // 越界 → INVALID；当前不在用 → DOUBLE_FREE
    public boolean isAllocated(int block)
    public void freeOrThrow(int block)       // DOUBLE_FREE → IllegalStateException；INVALID → IllegalArgumentException
}
```

* 所有操作 **O(1)**，不能为了找空闲块去扫数组；`new IndexPool(1 << 20)` 构造 O(capacity) 可以。
* 重复归还**不能**把块插进链表两次（否则之后同一块会被分配给两个人）。

**面试官的潜台词**：Part 1 做完会问「你怎么知道一个块是不是已经还过？」——答案是不另开 `boolean[]`，用链表数组本身的一个哨兵值。再问「如果 A 还了块、B 借走了同一块、A 又还一次呢？」——Part 1 做不到，这就引出 Part 2。

## Part 2 · `GenPool`（带版本号的 handle，防 use-after-free 与 ABA）

```java
public final class GenPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    public GenPool(int capacity)
    public GenPool(int capacity, int initialGeneration)      // initialGeneration 必须是偶数
    public static long handle(int index, int generation)
    public static int  indexOf(long handle)
    public static int  generationOf(long handle)
    public int capacity()
    public int available()
    public long allocate()
    public FreeResult free(long handle)
    public boolean isLive(long handle)
}
```

* `handle = (long) generation << 32 | (index & 0xFFFFFFFFL)`。
* **版本号规则**：每个槽位有一个 `int` 版本号，初始都是 `initialGeneration`（默认 0）。**偶数 = 空闲，奇数 = 在用**；`allocate` 和 `free` 各把它 `+1`。
  handle 有效 ⇔ 下标在范围内 ∧ handle 里的版本号是奇数 ∧ 等于槽位当前版本号。
* `free` 的判定顺序：下标越界或版本号为偶数 → `INVALID`；版本号为奇数但和槽位当前版本不同 → `DOUBLE_FREE`；否则 `FREED`。
* `0L` 和 `NONE` 永远无效。版本号 32 位回绕后奇偶性不变（2^32 是偶数），不需要特殊处理。
* 为什么选「奇偶」而不是「只涨不管奇偶」：Part 4 里要用**一次 CAS** 完成「在用 → 空闲」的状态切换（并发重复归还只能有一个赢家）。

## Part 3 · `OffHeapOrderPool`（FFM 堆外，定长记录）

```java
public final class OffHeapOrderPool implements AutoCloseable {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    public OffHeapOrderPool(int capacity)
    public int capacity();  public int available();
    public long byteSize();                   // 整块内存字节数（long）
    public static long recordBytes();         // 一个槽位的字节数（含头）
    public long allocate();                   // 返回的记录已清零
    public FreeResult free(long handle);  public boolean isLive(long handle);
    public void put(long handle, long id, long px, int qty, int side);   // 热路径：不创建对象
    public void put(long handle, Order order);
    public long px(long handle);  public int qty(long handle);           // 零分配读
    public Order get(long handle);                                       // 拷贝，会 new
    public void close();                      // 幂等
}
```

* 内存只来自**一个** `Arena.ofShared()` 分配的**一块** `MemorySegment`；每个槽位是定长记录。建议 32 字节：`gen:int, next:int, id:long, px:long, qty:int, side:int`——空闲链表和版本号也放进槽位里，堆上没有 per-slot 对象。字段用 `MemoryLayout.structLayout` + `VarHandle` 读写，别手算偏移。
* handle 规则、`free` 判定与 Part 2 相同（可复用 `GenPool.handle/indexOf/generationOf`）。
* `put/get/px/qty` 遇到非当前有效的 handle 抛 `IllegalStateException`（陈旧、越界、`NONE` 都算）；`put(h, null)` 抛 `NullPointerException`。
* `allocate()` 必须把载荷清零：上一个主人的数据不能漏给下一个。
* `close()` 之后任何访问抛 `IllegalStateException`（`Arena` 自带的行为，不要自己拦）；重复 `close()` 不抛。
* 为什么要有 `put(h, id, px, qty, side)` 这种看起来多余的重载：只提供 `put(h, Order)` 的接口会强迫调用方每次 `new Order`，池就白做了。**API 设计和内存管理是一回事**。

## Part 4 · `ConcurrentPool`（线程安全：无锁 Treiber 栈）

```java
public final class ConcurrentPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    public ConcurrentPool(int capacity)
    public int capacity()
    public int available()            // 并发进行中可以是近似值；所有线程静止后必须精确
    public long allocate()
    public FreeResult free(long handle)
    public boolean isLive(long handle)
}
```

* handle 规则与 Part 2 相同；单线程下行为必须和 `GenPool` 一致（含 LIFO）。
* 空闲链表是 **Treiber 栈**：`head` 是一个 `long` 字段，**高 32 位 tag（每次成功 push/pop 都 +1）、低 32 位栈顶槽位**（`-1` = 空），用 `VarHandle.compareAndSet` 更新。不允许用 `synchronized` / `Lock` / `AtomicReference` 配对象节点。
* **并发 double-free**：两个线程同时 `free` 同一个 handle，恰好一个返回 `FREED`，另一个返回 `DOUBLE_FREE`，槽位只能进空闲链表一次。提示：用 CAS 把槽位版本号从 `g` 推到 `g+1`。
* 任意线程可以 `allocate`、任意线程可以 `free`（分配和归还可以发生在不同线程）。
* **口头追问（不写代码）**：每线程缓存（per-thread cache）、批量补货；它为什么能让吞吐翻几十倍，又丢掉了什么保证。

## 样例

```java
var p = new IndexPool(2);
p.allocate();                // 0
p.allocate();                // 1
p.allocate();                // -1 (NONE)
p.free(0);                   // FREED
p.free(0);                   // DOUBLE_FREE
p.free(7);                   // INVALID
p.allocate();                // 0   （LIFO）

var g = new GenPool(1);
long a = g.allocate();       // 0x0000_0001_0000_0000   index 0, generation 1
g.free(a);                   // FREED
long b = g.allocate();       // 0x0000_0003_0000_0000   同一槽位，generation 3
g.free(a);                   // DOUBLE_FREE  （旧 handle 动不了新主人的块）
g.isLive(b);                 // true
```

## 边界清单（隐藏测试会打）

| 类别 | 例子 |
|---|---|
| 容量 | `0`、负数、`MAX_CAPACITY + 1`；`capacity == 1` |
| 编号 | `-1`、`capacity`、`Integer.MIN_VALUE`、`Integer.MAX_VALUE` |
| 打包 | 版本号为负（高位 1）；下标 `Integer.MAX_VALUE`；忘了 `& 0xFFFFFFFFL` 的符号扩展 |
| handle | `0L`、`-1L`、版本号偶数、低 32 位当 `int` 是负数、`Long.MIN_VALUE` / `MAX_VALUE` |
| 状态 | 池满后再分配；重复归还三次；归还从没分配过的块；归还后又重新分配同一槽位（ABA） |
| 回绕 | `new GenPool(1, -2)`：版本号从 `0xFFFFFFFE` 起，分配得到 `-1`，归还后回绕为 `0` |
| 堆外 | 极值 `Long.MIN_VALUE` / `Integer.MIN_VALUE` 往返；相邻记录互不覆盖；复用记录是零；`close` 后访问；重复 `close` |
| 并发 | 小池 + 8 线程反复借还不能出现两个主人；三个线程同时 `free` 同一批 handle；跨线程借 / 还；大量虚拟线程 |
| 性能 | 300 万次随机借还 < 2 s；**池几乎一直是满的**时 150 万次「换掉随机一块」< 2 s（O(n) 扫描空位的写法死在这里）；100 万记录的堆外池 < 2 s；4 线程各 5 万轮 × 16 次借还 < 2 s |

## 相关变体

* 把「编号」换成 `ByteBuffer` 切片（`ByteBuffer.slice()`）——Java 老办法，容量 `int`、无 `close`；
* 块大小可变（slab / buddy allocator）——这里的块都是等大小，不做；
* "池里有 N 个对象，`acquire()` 阻塞等待、`release()` 唤醒"——`Semaphore` + 栈的阻塞版，注意它和这里的非阻塞语义不同；
* C++ 版本里同题会追问 placement new / alignment / `std::pmr`。

## 考什么

不是某个算法，而是**把「借」和「还」的所有失败模式想全**：池满、重复归还、归还别人的块、编号被复用、并发下两个人拿到同一块；
然后能解释**为什么**要池（GC 压力），以及池自己会引入什么新问题（use-after-free 变成逻辑错误而不是崩溃、ABA、数据泄漏、碎片）。
