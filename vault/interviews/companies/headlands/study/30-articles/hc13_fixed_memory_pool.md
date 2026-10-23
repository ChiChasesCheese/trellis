# hc13 · 定长内存池 —— 讲义

> 读者：会写基本 Java。从最根本的问题讲起：**Java 有垃圾回收器，为什么还有人要自己管内存？**

---

## 1. 问题是什么

行情网关每秒涌进几十万条订单消息，每条放一个小结构（订单号、价格、数量、买卖方向），处理完就不要了。直白写法：来一条 `new Order(...)`，处理完交给垃圾回收器（GC）。

面试题问另一种：**启动时准备好固定数量（`capacity` 个）等大的"格子"，运行时只"借"和"还"，不再 `new`**——**内存池**（memory pool）。要实现分配、归还、校验，块用某种"编号"表示。

### 手算一遍

池有 3 个块，编号 0、1、2。"借"一个，"还"一个：

| 步骤 | 动作 | 返回 | 空闲链 |
|---|---|---|---|
| 初始 | | | 0 → 1 → 2（一条链：0 后面是 1，1 后面是 2） |
| `allocate()` | 摘走链头 0 | 0 | 1 → 2 |
| `allocate()` | 摘走链头 1 | 1 | 2 |
| `free(0)` | 把 0 挂到链头 | | 0 → 2 |
| `allocate()` | 摘走链头 0 | 0 | 2（刚还的最先被借走，LIFO，后进先出） |
| `allocate()` | 摘走链头 2 | 2 | （空） |
| `allocate()` | 没有空闲块 | -1 | （池满不是错误，是正常状态） |

### 四个 Part 怎么递进

1. **Part 1**：块用 `int` 编号，借、还都 O(1)。"还同一块两次？还不存在的编号？"
2. **Part 2**："A 还了块 7，B 借到 7，A 手里的旧 7 又还一次，B 的块被偷偷还掉。怎么防？" → 编号带"版本号"。
3. **Part 3**："能不能让 GC 完全看不见这些块？" → 堆外内存（FFM API）。
4. **Part 4**："多线程？能不加锁吗？" → 无锁栈（Treiber stack）、CAS、ABA；口头题：每线程缓存。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 为什么 Java 程序要"池化"？

#### 2.1.1 对象住在哪里：堆（heap）

`new Order(...)` 时 JVM 在**堆**里划一小块放对象字段，给你引用；你从不 `free`，由 **GC** 回收。经典"标记—清除"：从"根"（线程栈局部变量、静态字段）沿引用走，**标记**走得到的对象（活的）；没被标记的是垃圾，回收其空间供以后 `new` 使用。这叫**可达性**（reachability）分析：是不是垃圾由"还有没有人引用它"决定。

#### 2.1.2 `new` 其实很便宜

HotSpot 里每个线程有一小块专用堆（**TLAB**，Thread-Local Allocation Buffer），`new` 就是把"下一个空位指针"往后推一个对象大小——**指针碰撞**（bump the pointer），几条机器指令、不需要锁。`Order`（头 + `long id, long px, int qty, int side`）约 **40 字节**（对象头 12 + 字段 24，凑成 8 的倍数）。所以池化**不是**为了让分配更快（后面数据显示池的借还并不比 `new` 快多少）。

#### 2.1.3 真正的代价在回收

堆被填满，GC 必须出手：
* **年轻代**（young generation）：新对象先放这里。多数对象"朝生夕死"（**分代假设**），GC 只扫年轻代，把少数活对象**复制**走，整块清空——便宜。
* 复制时应用线程要**暂停**（stop-the-world，STW），**暂停时间**与"活着的对象有多少"相关，而非垃圾多少。
* 存活够久的对象**晋升**到**老年代**（old generation），老年代满了回收更贵。

"朝生夕死"便宜，"中年死亡"最糟：**存活时间刚好长到被复制几次、晋升后才死**。订单消息在窗口里存活几十万条消息的时间，足够被复制和晋升。

| 量 | 含义 | 怎么影响延迟 |
|---|---|---|
| **分配速率**（allocation rate） | 每秒 `new` 了多少字节 | 越高年轻代填满越快，GC 越频繁 |
| **存活集大小**（live set） | GC 时还活着的对象有多少 | 每次暂停要复制的东西越多，单次暂停越长 |

低延迟系统（撮合、做市）看**尾延迟**（tail latency）：不是"平均 2 微秒"而是"最慢的 0.01% 是多少"。一次 5 毫秒的 GC 暂停对平均值没影响，对尾延迟是灾难。

#### 2.1.4 数据：池化到底换来什么

窗口里始终 100 万条在飞订单，每来一条顶掉最旧的一条，共 3000 万条，`-Xmx256m`。A 组每条 `new Order`；B 组用 `OffHeapOrderPool` 复用堆外槽位（`put(h, id, px, qty, side)` 直接写字段，零分配）。第 3 轮结果（前两轮预热）：

| 收集器 | 方式 | 总耗时 | GC 次数 / 累计耗时 | 单次操作最慢 | 超过 1 ms 的操作 |
|---|---|---|---|---|---|
| G1 | 堆上 `new` | 757 ms | 74 次 / 144 ms | 4.46 ms | 44 个 |
| G1 | 堆外池 | 536 ms | 0 次 / 0 ms | 0.02 ms | 0 个 |
| Parallel | 堆上 `new` | 674 ms | 39 次 / 205 ms | 22.14 ms | 39 个 |
| Parallel | 堆外池 | 536 ms | 0 次 / 0 ms | 0.02 ms | 0 个 |
| 分代 ZGC（`-XX:+UseZGC -XX:+ZGenerational`） | 堆上 `new` | 598 ms | 82 次 / 455 ms（并发线程时间，非暂停） | 0.10 ms | 0 个 |
| 分代 ZGC | 堆外池 | 588 ms | 0 次 / 0 ms | 0.04 ms | 0 个 |

1. **吞吐几乎没差别**（噪声就有 ±30%）：`new` 本就便宜，池的借还还要多几次内存读写。**别因为"快"去池化。**
2. **尾延迟差几个数量级**：G1 / Parallel 下 `new` 版有几十个操作被 GC 暂停卡过 1 ms，最慢 4–22 ms；池版最慢 0.02 ms。这是低延迟系统愿付复杂度的原因。
3. **分代 ZGC 把暂停压到亚毫秒**，理由大大变弱——代价是 GC 线程后台吃 CPU（455 ms，几乎和应用一样多）。池化和选 GC 是同一问题的两种解法。池版 GC 次数为 0，应用线程和 GC 线程不再抢 CPU 与内存带宽。

#### 2.1.5 池化的代价（面试官最爱追问的另一半）

* **bug 面**：你从 GC 手里接过"谁负责释放"。忘了还 = 泄漏；还两次 = 两人用同一块；还了还在用 = use-after-free。在 C 里是崩溃，在池里是**悄悄的数据错乱**，更难查（Part 1–2 就在防这些）。
* **数据泄漏**：上一个主人的数据留在块里，所以 `allocate()` 要清零。
* **堆上池化对象的陷阱**：长期存活 → 晋升老年代；之后每次往老对象写新对象引用，GC 要经"写屏障"（write barrier）记录。池化**堆上含引用字段的对象**可能让 GC 更累——这也是这里块是**堆外、纯数值字段**的原因。
* **逃逸分析**（escape analysis）：对象没逃出方法时 JIT 可不分配它（标量替换）；池化让对象"逃逸"，反而失去该优化。
* **先量，再池化**：用 `-Xlog:gc`、JFR 确认 GC 是瓶颈再动手。

### 2.2 空闲链表（free list）

把"还没被借走的块"串成链：借 = 摘链头，还 = 挂链头。朴素做法每次从头扫找空块，O(`capacity`)；空闲链表只改一两个变量，O(1)。关键一招是**把链表指针藏在块自己里面**（"侵入式"，intrusive）：空闲块不需存数据，位置可存"下一个空闲块是谁"。用 `int[] next`：

`capacity = 4`，初始状态：`head = 0`，意思是 0 → 1 → 2 → 3 → 结束（-1）。

| 下标 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `next[ ]` | 1 | 2 | 3 | -1 |

* `allocate()`：`b = head (=0)`；`head = next[0] (=1)`；返回 0。此时 `next[0]` 无意义（?），`head = 1`。
* `free(0)`：`next[0] = head (=1)`；`head = 0`。又挂回去了：`next[ ]` 为 1、2、3、-1，`head = 0`。

在用块的 `next[b]` 无意义，用 `ALLOCATED = -2` 标记"在用"——**一个数字同时承担"链表指针"和"是否在用"**（空闲和在用互斥）。这就是 Part 1 检测重复归还的办法，不需另开 `boolean[]`（代码见 §5.1）。

### 2.3 句柄（handle）、悬空引用与 use-after-free

句柄是"指向某资源的凭证"，Part 1 的块 `int` 编号就是最简单的句柄。池收回块后，**数字还在你手里**。三种经典错误：

| 错误 | 怎么发生 | 后果（无防护时） |
|---|---|---|
| **重复归还**（double free） | 对同一编号 `free` 两次 | 块被挂进空闲链表两次 → 同一块借给两个人 |
| **归还后继续用**（use-after-free） | `free(7)` 之后又读写块 7 | 读到（写坏）别人的数据 |
| **陈旧句柄**（stale handle，ABA 的变种） | A 还了 7；B 借到 7；A 又 `free(7)` | B 的块被 A 还掉，B 毫不知情 |

第三种是 Part 1 **无法防**的：下标 7 在两个时刻代表两个不同所有者，数字却一样。解决见 2.4。

### 2.4 版本号（generation）：让同一个下标在不同时刻"长得不一样"

每个槽位带计数器，handle 是 `(版本号, 下标)`，槽位归还时版本号 +1；handle 的版本号与槽位当前版本不一致 → 旧 handle。

| 步骤 | 槽位 7 的版本号 | A 的 handle | B 的 handle |
|---|---|---|---|
| 初始 | 0 | | |
| A 借到 7 | 1（奇数 = 在用） | (版本1, 下标7) | |
| A 还 7 | 2（偶数 = 空闲） | | |
| B 借到 7 | 3（奇数 = 在用） | | (版本3, 下标7) |
| A 再 `free(版本1, 7)` | 比较：槽位当前是 3 ≠ 1 | 拒绝（DOUBLE_FREE） | |

约定：**偶数 = 空闲，奇数 = 在用**，每次借、每次还各 +1。好处在 Part 4：并发时**一次 CAS** 同时完成"验证 handle 有效"和"标记空闲"。

#### 位打包：两个 32 位数塞进一个 64 位 `long`

handle 要在方法间传、当 map key，最好是**一个**基本类型值而不 `new` 对象。`long` 正好放 `int generation` + `int index`：

```
 63          32 31            0
 +-------------+---------------+
 | generation  |     index     |
 +-------------+---------------+
```

高 32 位是 `generation`（int），低 32 位是 `index`（int）。

```java
// 打包
handle = ((long) generation << 32) | (index & 0xFFFFFFFFL)
// 拆包：强转取低 32 位
index = (int) handle;
// 无符号右移 32 位再取低 32 位
generation = (int) (handle >>> 32);
```

最易犯的错：**符号扩展**（sign extension）。`index` 为负（最高位 1）时转 `long`，高 32 位全填 1，污染 generation 成 `0xFFFFFFFF`。`& 0xFFFFFFFFL` 先当**无符号**数处理，高 32 位清零才安全。

版本号 `int` 会回绕（`0xFFFFFFFF + 1 = 0`），2^32 是偶数，回绕后奇偶性不变，"偶空闲/奇在用"依然成立。真正的风险：同一槽位被借还 2^31 次后，极老的 handle 可能"撞上"当前版本；可忽略，不能忽略就退役该槽位。

### 2.5 堆外内存与 FFM

Java 21 的外部内存 API（FFM，预览）可在 GC 管不到的地方分配访问内存：
* **`Arena.ofShared()`** 管一块内存的生命周期，`close()` 整块归还；`ofShared` 允许别的线程访问（`ofConfined` 只允许创建它的线程）。
* **`arena.allocate(bytes, 对齐)`** 分配并**清零**。
* **`MemoryLayout.structLayout(...)`** 像 C 的 `struct`，声明每个字段类型和名字；`byteSize()` 给总大小。
* **`layout.varHandle(sequenceElement(), groupElement("px"))`** 得 `VarHandle`，`PX.get(segment, i)` / `PX.set(segment, i, v)` 读写第 `i` 个槽位的 `px`，偏移由 JDK 算。

槽位 **32 字节**：头 8（`gen:int` + `next:int`）+ 载荷 24（`id:long, px:long, qty:int, side:int`）。32 是 2 的幂，一条 64 字节缓存行正好 2 个槽位，不会有槽位横跨两行（横跨要搬两次）。

### 2.6 并发：竞争、CAS 与"无锁"

并发正确性要考虑：**原子性**（操作要么全做完要么没做，别的线程看不到中间状态）、**可见性**（写入何时被别的线程看到）、**有序性**（编译器和 CPU 可能重排）。`VarHandle`（Java 9）是对字段做精确内存操作（指定内存序的读写、CAS）的句柄。**竞争条件**（race condition）：两线程都"读 head → 改 head"，交错就丢更新。

| 步骤 | 线程 1 | 线程 2 |
|---|---|---|
| 1 | 读 `head=5` | |
| 2 | | 读 `head=5`，写 `head=next[5]` |
| 3 | 写 `head=next[5]` | |

两个线程都借走了块 5。

**CAS**（Compare-And-Set）：`CAS(变量, 期望值, 新值)`——**原子地**检查变量是否为期望值，是就改成新值返回 true，否则什么也不做返回 false；失败的线程重读重试。这是无锁（lock-free）算法的基石。**无锁 ≠ 无等待**：保证"总有某个线程在前进"，但单个线程可能一直 CAS 失败。

### 2.7 Treiber 栈与 ABA

**Treiber 栈**（R. K. Treiber, 1986）：用 CAS 实现的并发栈，栈顶是共享变量 `top`：

```
push(x):  loop { t = top;  x.below = t;  if CAS(top, t, x) break; }
pop():    loop { t = top;  if t == null return empty;  n = t.below;  if CAS(top, t, n) return t; }
```

我们的空闲链表本来就是栈（LIFO），直接做成 Treiber 栈：`top` 就是 `head`，"节点"是槽位编号，`below` 是 `next[]`。

**ABA 问题**——Part 4 的核心。CAS 只看"值是不是 A"，不看"期间发生过什么"。

初始栈：`A → B → C`（A 在栈顶）。

| 步骤 | 线程 | 动作 | 栈 |
|---|---|---|---|
| 1 | 线程 1 | 开始 `pop()`：读到 `top = A`，读到 `A.below = B`（然后被操作系统切走） | |
| 2 | 线程 2 | `pop()`，拿走 A | B → C |
| 3 | 线程 2 | `pop()`，拿走 B（B 现在在线程 2 手里，正在使用） | C |
| 4 | 线程 2 | `push(A)`（A 又回到栈顶） | A → C |
| 5 | 线程 1 | 恢复：`CAS(top, 期望 A, 新值 B)`，top 现在确实是 A，CAS 成功！ | B → ??? |

B 被装回空闲链表，可是线程 2 还在用 B。

CAS 成功（值确实还是 A），但"A"已不是原来那个——`below` 变了，线程 1 和 2 同时拥有 B。这是并发池最经典的 bug。**解法：带 tag 的头指针**：`head` 除栈顶编号外还存一个**计数器**，每次成功 push/pop 都 +1：

```
 63         32 31          0
 +-----------+-------------+
 |    tag    |  top slot   |
 +-----------+-------------+
```

高 32 位 `tag`（计数器）；低 32 位栈顶槽位编号（-1 = 空）。

CAS 比较整个 64 位。线程 2 的 pop、pop、push 让 tag 从 t 变 t+3；线程 1 期望 `(tag=t, A)`，现在是 `(tag=t+3, A)`，不等 → 失败重读。tag 也会回绕（32 位 = 42 亿次）：重现 ABA 要线程 1 在读和 CAS 之间被挂起整整 2^32 次成功操作——可忽略但要注释写明。`AtomicStampedReference` 是同一思想的对象版（每次更新分配 `Pair`，在池里是反面教材）。

### 2.8 每线程缓存（per-thread cache）

所有线程抢同一个 `head`，CAS 失败的线程原地重试，每次都要把 `head` 所在缓存行从别的核心"抢"来（缓存一致性协议 MESI），线程越多越慢。**办法**：每线程手里先攒一小批槽位；借时先从自己的小仓库拿，空了才去共享池**一次拿一批**；还时先放小仓库，满了才**一次还一批**，共享 `head` 只在"补货 / 退货"时碰。无处不在：JVM 的 TLAB、tcmalloc 的 thread cache、jemalloc 的 tcache、slab 分配器的 magazine。数据见 §4.4。

---

## 3. 从最笨的解法开始

最笨的写法（也是白板上的第一版）：

```java
class NaivePool {
    private final boolean[] inUse;
    NaivePool(int capacity) { inUse = new boolean[capacity]; }

    int allocate() {
        for (int i = 0; i < inUse.length; i++) {      // 从头扫，找第一个空的
            if (!inUse[i]) { inUse[i] = true; return i; }
        }
        return -1;
    }
    boolean free(int block) {
        if (block < 0 || block >= inUse.length || !inUse[block]) return false;
        inUse[block] = false;
        return true;
    }
}
```

对：重复归还、越界都能检测。**错在**：`allocate()` O(`capacity`)——池接近满、空位散落在数组中间时要扫过前面所有被借走的块。这个缺陷易被"随机借还"测试漏掉：池里平均只有几百块在用时前几百格之后就是空位，扫描很快（300 万次 50/50 随机借还只要 125 ms，看着没问题！）。所以 `IndexPoolTest.nearFullChurnIsFast` 把池填满再 150 万次"换掉随机一块"：`capacity = 65536` 时朴素版每步约 3.9 微秒、共约 6 秒，超 2 秒预算；链表版约 11 毫秒。**教训：测性能要测最坏的形状。**

"第二笨"是 `ArrayDeque<Integer>` 当空闲栈：O(1)，但 `Integer` 是装箱对象，借还一次就 `new` 一个——**池子本身在制造垃圾**。

---

## 4. 一步一步改进

### 4.1 Part 1：从扫描到空闲链表

扫描找空位 O(n)。别找——让"空位"自己排队，借时取队头，队头是一个变量，取、更新都 O(1)；只需每个元素知道下一个是谁，即 `next[]`（§2.2）。`boolean[] inUse` → `int[] next` + `int head`；`allocate` 是 `b = head; head = next[b]`；`free` 是 `next[b] = head; head = b`。都 O(1)，构造 O(capacity)，空间 `4 × capacity` 字节。

**还差：重复归还检测**。只有 `next[]` 时 `free(3)` 调两次，第二次 `next[3] = head; head = 3`——3 挂在自己后面成环。必须判断"3 现在是否在用"：用 `next[b] = ALLOCATED (-2)` 标记在用块；`free` 先看 `next[b] == ALLOCATED`，不是 → `DOUBLE_FREE`；越界 → `INVALID`。仍 O(1)。

### 4.2 Part 2：从下标到带版本号的 handle

Part 1 分不清"我手里的 7"和"别人现在手里的 7"（§2.3 第三种）。handle 带版本号（§2.4）：每次借还版本号变，旧 handle 的版本号必不等于当前。多一个 `int[] gens`；`allocate` 里 `gens[i]++`（偶→奇）返回 `handle(i, gens[i])`；`free` 拆出 `(index, g)`，校验后 `gens[i] = g + 1`（奇→偶）。
**判定顺序**（`free`）：1) 下标越界，或 `g` 是偶数（从没发过）→ `INVALID`；2) `gens[index] != g`（奇数但已过期）→ `DOUBLE_FREE`；3) 否则 `FREED`。

`NONE = -1`（全 1）永远无效（下标当 `int` 是 -1，越界）；全零 handle 版本号为 0（偶数）也无效——**漏初始化的 handle 立刻暴露**。仍 O(1)，每槽位多 4 字节。

### 4.3 Part 3：从对象到堆外记录

池里只放"编号"，真正的数据在哪？用 `Order[]` 则是 `capacity` 个堆对象，GC 要扫描、晋升（§2.1.5）。**想法**：数据放进一块连续堆外内存，用 handle 访问——GC 不可见，缓存友好。`gens` 和 `next` 不再是两个 `int[]`，而是**槽位头部的两个字段**（`gen:int`, `next:int`），后面紧跟载荷（`id, px, qty, side`）：一个 32 字节 `StructLayout`，`SequenceLayout` 重复 `capacity` 次，一次 `arena.allocate(...)`。

**新问题**：
* **清零**：`Arena.allocate` 只在第一次分配时清零，**复用**的槽位没人帮你清，`allocate` 必须清零载荷，否则漏给下一个主人。
* **生命周期**：`close()` 之后访问由 `Arena` 自带检查抛 `IllegalStateException`（不崩进程）；重复 `close()` 会让 `Arena.close()` 抛异常，所以先判 `arena.scope().isAlive()`。
* **API 设计**：只提供 `put(h, Order)` / `Order get(h)`，调用方每次 `new Order`，把省下的分配补回去。所以多给 `put(h, id, px, qty, side)` 和 `px(h)` / `qty(h)`——**零分配热路径接口**；`get(h)` 会 `new`，文档写明不在热路径用。**API 的形状决定调用方能否写出零分配代码**。

O(1)；`capacity × 32` 字节一次分配（`byteSize()` 是 `long`，可超 2 GiB，`ByteBuffer` 做不到）。

### 4.4 Part 4：从单线程到线程安全

#### 步骤 A：最简单的正确解——加锁

```java
class LockedPool {
    private final GenPool pool; private final ReentrantLock lock = new ReentrantLock();
    long allocate() { lock.lock(); try { return pool.allocate(); } finally { lock.unlock(); } }
    FreeResult free(long h) { lock.lock(); try { return pool.free(h); } finally { lock.unlock(); } }
}
```

正确、简单，面试**先说这个**。用 `ReentrantLock` 而非 `synchronized`（虚拟线程下 JDK 21 的 `synchronized` 会钉住载体线程）。问题只是所有线程排队过同一把锁。

#### 步骤 B：去掉锁——朴素 Treiber 栈（有 bug）

`head` 变 `volatile int`，`allocate` 里 `CAS(head, h, next[h])`。看似对，实有 §2.7 的 ABA bug——**并发池面试的标准考点**。

#### 步骤 C：加 tag 的 head

`head` 变 `long`：高 32 位 tag，低 32 位编号；每次 CAS 的新值是 `pack(tag + 1, 新栈顶)`。**验证**：把两处 `tagOf(h) + 1` 改成 `tagOf(h)`（去掉 tag），多线程争用压力测试 20 轮有 7 轮"丢了槽位"；加回 tag 全部通过。

#### 步骤 D：并发 double-free

单线程 `free` 是"检查版本 → 改版本 → 压栈"三步。两线程同时 `free` 同一 handle，都通过检查、都压栈 → 同一槽位进空闲链表两次。**想法**：把"检查 + 改版本"合成**一次 CAS** `CAS(gens[i], g, g + 1)`：成功的线程拥有"归还这个槽位"的权利，失败的看到版本已变 → `DOUBLE_FREE`。**偶/奇约定在此派上用场**：版本号本身就是状态（奇=在用），一次 CAS 完成"状态检查 + 切换"，不需另一个标志位。**验证**：换成"先读后写"，并发 double-free 压力测试全面失败（成功归还 2110 > 2000）。

#### 步骤 E：内存序——每一处该用什么

| 位置 | 访问方式 | 为什么 |
|---|---|---|
| 读 `head` | `getAcquire` | 要看到别的线程 push 之前对 `next[i]`、`gens[i]` 的写 |
| `head` 的 CAS | `compareAndSet`（volatile 语义，含 release） | push 时发布 `next[i]` 和版本号；pop 成功要成为全序的一环 |
| `next[i]` 读写 | `getOpaque` / `setOpaque` | 读到旧值没关系——那样 `head` 的 tag 已变，CAS 会失败；只需不撕裂、不被编译器缓存 |
| `gens[i]` 的 CAS（free） | `compareAndSet` | 并发 double-free 的仲裁点 |
| `gens[i]` 在 allocate 里的写 | `setRelease` | 弹出成功后槽位归本线程所有；发布版本号给之后的 `isLive` |
| `inUse` 计数器 | `LongAdder` | 纯统计，不参与正确性；分散热点 |

思想：「**读到过期数据没关系，只要最后用 CAS 校验**」——只在"CAS 的对象能反映过期"时成立（所以 tag 不能省）。

#### 步骤 F：每线程缓存（口头题，有数据）

65536 个槽位，T 个线程各做 400 万次借还（每批借 16 再还 16），单位百万次操作/秒。`locked`（`ReentrantLock` 包住 `GenPool`）；`treiber`（`ConcurrentPool`）；`cached`（每线程 64 格小仓库，空了从 `ConcurrentPool` 批量借 32 个，满了批量还 32 个）。两次运行数据（`locked` 2 线程时分别 25 和 7，锁争用不稳定）：

| 线程数 | locked | treiber | cached |
|---|---|---|---|
| 1 | 149 – 155 | 106 – 111 | 223 – 239 |
| 2 | 7 – 25 | 9 – 10 | 425 – 432 |
| 4 | 60 – 86 | 14 – 15 | 685 – 707 |
| 8 | 80 – 83 | 3.9 | 1021 – 1028 |

1. **无锁不等于快。** 8 线程抢同一个 `head`，Treiber 栈只有 3.9，比加锁慢 20 倍：每次 CAS 失败都要把 `head` 所在缓存行抢回来，LIFO 又让所有线程总碰同几个槽位。`ReentrantLock` 是非公平锁，允许"插队"，一个线程可连续拿好几次，减少缓存行搬运。无锁真正的卖点是**不会被挂起的线程拖住别人**（无优先级反转），不是吞吐。
2. **每线程缓存把吞吐翻了几十倍且随线程数线性增长**（223 → 1028），因大多数借还根本没碰共享状态。
3. **代价**（面试官要听的另一半）：
   * **搁浅**（stranding）：槽位躺在某线程缓存里，别的线程看池是"空"的（`NONE`），其实有闲置槽位；缓存容量 × 线程数要算进池总容量。
   * **失去重复归还检测**：缓存里的 handle 在共享池眼里仍是"在用"（奇数版本），再 `free` 一次无从发现；要检测只能在缓存里另做标记。
   * **线程退出要冲刷缓存**；**虚拟线程**下 `ThreadLocal` 缓存可能几十万个——应改按载体线程 / 按 CPU 分片（striping）。
   * **LIFO / 公平性改变**：刚还的槽位不再是全局下一个被借走的。

---

## 5. 逐段讲解法

### 5.1 `IndexPool`（Part 1）

```java
public IndexPool(int capacity) {
    if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
    next = new int[capacity];
    for (int i = 0; i < capacity - 1; i++) next[i] = i + 1;
    next[capacity - 1] = NONE;
    head = 0;
    available = capacity;
}
```

构造：`next[i] = i + 1`，最后一块指向 `NONE (-1)`；`head = 0`。`MAX_CAPACITY = 1 << 28` 避免 `new int[...]` 吃掉 1 GiB 以上，超出明确报错而非 `OutOfMemoryError`。

```java
public int allocate() {
    int block = head;
    if (block == NONE) return NONE;
    head = next[block];
    next[block] = ALLOCATED;
    available--;
    return block;
}
```

取链头；链表空返回 `NONE` 而不抛异常——池满是正常状态。取走后 `next` 改成 `ALLOCATED`。

```java
public FreeResult free(int block) {
    if (block < 0 || block >= next.length) return FreeResult.INVALID;
    if (next[block] != ALLOCATED) return FreeResult.DOUBLE_FREE;
    next[block] = head;
    head = block;
    available++;
    return FreeResult.FREED;
}
```

先查范围再查状态（不能反，否则越界直接抛 `ArrayIndexOutOfBoundsException`）。"不在用"含"已还过"和"从没借过"，统一报 `DOUBLE_FREE`——都是"你不该还这块"。

```java
public void freeOrThrow(int block) {
    RuntimeException failure = switch (free(block)) {
        case FREED -> null;
        case DOUBLE_FREE -> new IllegalStateException("block not allocated (double free?): " + block);
        case INVALID -> new IllegalArgumentException("block out of range: " + block);
    };
    if (failure != null) throw failure;
}
```

switch 表达式三个分支各产生一个值（`null` 或异常对象），漏写 `INVALID` 编译器直接报错。`FreeResult` 用 `enum` 而非 `int` 常量：新增结果时所有 `switch` 编译失败，不会悄悄漏处理。

### 5.2 `GenPool`（Part 2）

```java
public static long handle(int index, int generation) {
    return ((long) generation << 32) | (index & 0xFFFFFFFFL);
}
public static int indexOf(long handle) { return (int) handle; }
public static int generationOf(long handle) { return (int) (handle >>> 32); }
```

§2.4 的打包 / 拆包。用 `>>>` 而非 `>>`，表达"这里不关心符号"。

```java
public long allocate() {
    int index = head;
    if (index == END) return NONE;
    head = next[index];
    int g = ++gens[index];            // 偶 → 奇
    available--;
    return handle(index, g);
}

public FreeResult free(long handle) {
    int index = indexOf(handle);
    int g = generationOf(handle);
    if (index < 0 || index >= gens.length || (g & 1) == 0) return FreeResult.INVALID;
    if (gens[index] != g) return FreeResult.DOUBLE_FREE;
    gens[index] = g + 1;              // 奇 → 偶
    next[index] = head;
    head = index;
    available++;
    return FreeResult.FREED;
}
```

* `index < 0`：低 32 位当 `int` 是负数（如 `0x0000_0001_8000_0000`）——必须检查，否则 `gens[index]` 抛异常。
* `(g & 1) == 0`：偶数版本号 = 从没发过 → `INVALID`。
* 不再需要 `ALLOCATED` 哨兵：版本号奇偶就是状态；`next[]` 只在空闲链表里有意义。

### 5.3 `OffHeapOrderPool`（Part 3）

```java
private static final StructLayout SLOT = MemoryLayout.structLayout(
        JAVA_INT.withName("gen"), JAVA_INT.withName("next"),
        JAVA_LONG.withName("id"), JAVA_LONG.withName("px"),
        JAVA_INT.withName("qty"), JAVA_INT.withName("side"));
private static final SequenceLayout SLOTS = MemoryLayout.sequenceLayout(MAX_CAPACITY, SLOT);
private static final VarHandle GEN = SLOTS.varHandle(sequenceElement(), groupElement("gen"));
...
```

`SLOT` 声明一个槽位的字段（32 字节，8 字节对齐，无隐式填充：4+4+8+8+4+4）。`SLOTS` 是 `MAX_CAPACITY` 个槽位的序列——**只是描述，不分配内存**。用它生成 `static final` 的 `VarHandle`，JIT 能把读写内联成一条加载 / 存储指令；若在构造器里按实际 `capacity` 生成（实例字段），JIT 不能当常量折叠，会慢。坐标是 `(MemorySegment, long 槽位下标)`。

```java
this.seg = arena.allocate(SLOT.byteSize() * capacity, 64);
for (int i = 0; i < capacity; i++) NEXT.set(seg, (long) i, i + 1 < capacity ? i + 1 : END);
```

一次分配 `capacity × 32` 字节，64 字节对齐。全零，所以 `gen = 0`（空闲，偶数）不用初始化；`next` 要显式写成 `i + 1`。

```java
public long allocate() {
    int index = head;
    if (index == END) return NONE;
    head = (int) NEXT.get(seg, (long) index);
    int g = (int) GEN.get(seg, (long) index) + 1;
    GEN.set(seg, (long) index, g);
    ID.set(seg, (long) index, 0L);  PX.set(seg, (long) index, 0L);
    QTY.set(seg, (long) index, 0);  SIDE.set(seg, (long) index, 0);
    available--;
    return GenPool.handle(index, g);
}
```

与 `GenPool.allocate` 一样，多了"清零载荷"。`VarHandle.get` 返回 `Object`（签名多态），要 `(int)` 强转；下标一律转 `long`——传 `int` 会让调用点静态类型不匹配，运行时才 `WrongMethodTypeException`。

```java
public void put(long handle, Order order) {
    switch (order) {
        case Order(long id, long px, int qty, int side) -> put(handle, id, px, qty, side);
    }
}
```

record 模式：一行把 `Order` 拆成四个局部变量，再调用零分配的四参数版本。`order` 为 `null` 时 `switch` 抛 `NullPointerException`。

```java
public void close() { if (arena.scope().isAlive()) arena.close(); }
```

幂等关闭。此后任何 `seg` 访问抛 `IllegalStateException("Already closed")`，由 FFM 运行时保证，不用自己检查。

### 5.4 `ConcurrentPool`（Part 4）

```java
private static long pack(int tag, int index) { return ((long) tag << 32) | (index & 0xFFFFFFFFL); }
private static int tagOf(long h) { return (int) (h >>> 32); }
private static int indexOf(long h) { return (int) h; }
```

与 handle 同样的打包，但高 32 位是 tag。

```java
public long allocate() {
    while (true) {
        long h = (long) HEAD.getAcquire(this);
        int index = indexOf(h);
        if (index == EMPTY) return NONE;
        int below = (int) NEXTS.getOpaque(next, index);
        if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, below))) {
            int g = (int) GENS.get(gens, index) + 1;
            GENS.setRelease(gens, index, g);
            inUse.increment();
            return GenPool.handle(index, g);
        }
        Thread.onSpinWait();
    }
}
```

1. `getAcquire` 读 `head`（含 tag）；空 → 返回 `NONE`。
2. 读 `next[index]`——"若我成功弹出，新栈顶是谁"。可能已过期，没关系，下一步 CAS 会验证。
3. `compareAndSet(this, h, pack(tag + 1, below))`：`head` 还完全等于读到的 `h`（含 tag）才成功。
4. 成功后槽位归本线程所有，没人会同时改它的版本号（别人旧 handle 的 `free` 会因版本号不匹配失败），所以直接 `get`+`setRelease`，不需 CAS。
5. 失败：`Thread.onSpinWait()`（提示 CPU 在自旋，可省电 / 让出超线程资源），回到循环。

```java
public FreeResult free(long handle) {
    ...
    if (!GENS.compareAndSet(gens, index, g, g + 1)) return FreeResult.DOUBLE_FREE;
    inUse.decrement();
    while (true) {
        long h = (long) HEAD.getAcquire(this);
        NEXTS.setOpaque(next, index, indexOf(h));
        if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, index))) return FreeResult.FREED;
        Thread.onSpinWait();
    }
}
```

先 CAS 版本号（步骤 D）。**赢者独占"把槽位压回栈"的权利**，之后的压栈循环只与别线程的 push / pop 竞争 `head`。压栈：把当前 `head` 的栈顶写进 `next[index]`，再 CAS `head` 指向 `index`，tag + 1。`available()` 是 `capacity - inUse.sum()`（`LongAdder.sum()` 并发时近似，静止后精确）。

---

## 6. Java 21 特性小课

| id | 用在哪 | 老写法 | 新写法 / 为什么 |
|---|---|---|---|
| `record` | `Order(long id, long px, int qty, int side)` + `Order.ZERO` | 类 + 4 字段 + 构造器 + 访问器 + `equals`/`hashCode`/`toString`（约 30 行，易漏改） | 一行；`equals` 逐字段比较，可直接比较 `new Order(1,2,3,4)` 和 `pool.get(h)` |
| record 模式 | `put(long, Order)` 里 `case Order(long id, long px, int qty, int side) ->` | `long id = o.id(); ...` 四行 | 一次解构；编译器检查组件个数与类型。**不该用**：只用一个字段时直接 `o.px()` 更清楚 |
| switch 表达式 | `freeOrThrow`：`RuntimeException failure = switch (free(block)) {...}` | `switch` 语句 + 每分支赋值 + `break`（漏 `break` 就 fall through） | 每分支是一个值；对 `enum` **穷尽性检查**，新加 `FreeResult` 值这里编译不过 |
| `var` | `var pool = new IndexPool(3)` | `IndexPool pool = new IndexPool(3)` | 右边已写类型；**不该用**：右边看不出类型时（`var x = foo()`） |
| 虚拟线程 | `Executors.newVirtualThreadPerTaskExecutor()` 开 2000 个并发任务 | 线程池要调参，2000 个平台线程吃大量内存 | 几乎没成本；自旋型任务**不该**用（占住载体线程）。这里任务短小、不阻塞 |
| `VarHandle` / `LongAdder` | `ConcurrentPool` 的 `HEAD`、`NEXTS`、`GENS`，`inUse` | `AtomicReferenceFieldUpdater` / `Unsafe` / 每槽位一个 `AtomicInteger`（`capacity` 个对象） | `arrayElementVarHandle(int[].class)` 对普通 `int[]` 元素做 CAS / opaque / release，不需每槽位一个原子对象；`findVarHandle` 对普通 `long` 字段做 CAS |
| FFM | `OffHeapOrderPool` 的 `Arena` / `MemorySegment` / `StructLayout` / `SequenceLayout` | `ByteBuffer.allocateDirect`（容量 `int`、无确定性释放、偏移手算） | 容量 `long`、`close()` 确定性释放、字段按名字访问。**JDK 21 预览**（`--enable-preview`），JDK 22 转正，`allocateUtf8String` 等名字会变 |

---

## 7. 追问预演

### 追问 1：为什么要自己做内存池？Java 不是有 GC 吗？

承认 `new` 很快，池化不为快；真实代价在 GC 暂停（尾延迟）和 GC 线程抢 CPU。判据：分配速率高 + 存活集大 + 对尾延迟敏感；先用 `-Xlog:gc` / JFR 量；分代 ZGC 已把暂停压到亚毫秒，先试换 GC 再池化。
说：「池化不是为更快，是让热路径无分配、GC 没活干、延迟曲线没有毛刺。我先用 JFR 确认 GC 暂停确是尾延迟来源，因为池化会引入 use-after-free 这类 bug，有成本。」

### 追问 2：怎么知道一个块是不是已经还过？

O(1) 不能扫；复用 `next[]`：`next[b] == ALLOCATED` 哨兵，`free` 先检查，不额外开数组。
说：「空闲块的 `next` 是下一个空闲块编号（≥ -1），在用块设成 -2；`free` 时不是 -2 就直接返回 DOUBLE_FREE，不动链表。」

### 追问 3：A 还了块 7，B 借到 7，A 又还一次——怎么防？

根源是下标没有"身份"→ 版本号：handle = (generation, index)，每次借还版本号变，`free` 比较版本号。
说：「handle 是 long，高 32 位槽位版本号，低 32 位下标。槽位每次归还版本号加一，旧 handle 的版本号追不上当前版本，所以 A 的第二次 free 会被识别，动不到 B 的块。」

### 追问 4：版本号溢出了怎么办？

借还一轮 +2，所以 2^31 次借还才回到同一值，回绕后奇偶性不变；一个 2^31 次借还之前的 handle 可能"撞上"。可忽略，不可忽略就在版本号接近上限时退役该槽位，或用 64 位版本号 + 128 位 handle。

### 追问 5：多线程怎么做？

先最简单正确的（锁），再无锁陷阱（ABA）与解法（tag），再并发 double-free（§4.4）。
说：「最简单是一把 ReentrantLock。要无锁，空闲链表本是栈，用 Treiber 栈，但对栈顶下标 CAS 有 ABA，所以 head 做成 long，高 32 位是每次成功操作加一的 tag。free 用一次 CAS 把版本号从奇推到偶，两个线程同时 free 同一个 handle 只一个赢。」

### 追问 6：tag 也会溢出吧？

ABA 要求某线程在读 head 和 CAS 之间别人恰好做了 2^32 整数倍次成功操作。理论存在，实践需线程挂起足够久且别人做 42 亿次操作；要消除就用 64 位 tag + 128 位 CAS（Java 无直接支持）或 hazard pointers / epoch 回收。我接受并在注释写明；也可用每线程缓存减少共享栈操作次数。

### 追问 7：无锁一定比锁快吗？

不一定（§4.4 表）：争用高时 Treiber 栈每次 CAS 失败都有缓存行搬运；无锁的价值是进度保证，提升吞吐靠减少对共享状态的访问（每线程缓存）。
说：「我测过：8 个线程抢同一个 Treiber 栈，吞吐比一把 ReentrantLock 低很多；加每线程缓存批量补货后快了几十倍。」

### 追问 8：每线程缓存有什么代价？

搁浅、重复归还检测变弱、线程退出冲刷、虚拟线程下 `ThreadLocal` 数量、LIFO 语义变化（§4.4 步骤 F）。

### 追问 9：池满了怎么办？

产品决策：(1) 返回 `NONE`（拒绝 / 背压）；(2) 阻塞等待（`Semaphore` + 栈）；(3) 扩容（打破"固定容量"、引入分配）。低延迟系统通常选 (1) 并告警：池满意味着容量规划错了。

### 追问 10：为什么用堆外而不是 `Order[]` 预分配？

`Order[]` 里的 `Order` 是堆对象，会晋升老年代，写引用要写屏障，GC 完整回收要遍历；堆外纯数值记录 GC 看不见。代价：手动 `close`、固定容量、边界检查（JIT 消掉大部分）、JDK 21 预览。

---

## 8. 常见误区

### 误区 1：打包 handle 时忘了 `& 0xFFFFFFFFL`

```java
// 很多人这样写
long handle = ((long) generation << 32) | index;       // index 是 int
```

`index` 为负（如 `0x8000_0000`）时 `(long) index` 高 32 位全 1，把 `generation` 位 OR 成 `0xFFFFFFFF`。**正确**：`| (index & 0xFFFFFFFFL)`。

### 误区 2：重复归还只"忽略"，不检查

```java
void free(int b) { next[b] = head; head = b; }       // 没检查
```

连续 `free(3)` 两次，`next[3] = 3`，之后 `allocate` 永远返回 3。**正确**：先看 `next[b] == ALLOCATED`。

### 误区 3：以为 `volatile` 能修好 ABA

`volatile int head` 只解决可见性，不解决 ABA（"值相同但历史不同"）。**正确**：加 tag（或 `AtomicStampedReference`）。

### 误区 4：`free` 先检查再修改，没有原子化

```java
if (gens[i] == g) { gens[i] = g + 1; push(i); }       // 两步，之间可以被别的线程插入
```

并发下两个线程都通过 `if`。**正确**：`CAS(gens[i], g, g+1)` 把检查和修改合成一次。

### 误区 5：复用槽位忘了清零

`allocate()` 返回的记录里还留着上一个主人的 `px`、`qty`：既是 bug 来源也是信息泄漏。**正确**：`allocate` 里写零（或约定调用方写全）。

### 误区 6：池要多线程用，却用 `Arena.ofConfined()`

`ofConfined` 的 segment 只允许创建它的线程访问，别的线程抛 `WrongThreadException`（带超时的测试框架常在另一线程跑测试体）。**正确**：`ofShared()`。

### 误区 7：把 `available()` 当并发中的精确值

并发进行中 `inUse` 和 `head` 的更新不是同一个原子操作，`available()` 可能暂时偏差几个。**正确**：当近似值，只在所有线程静止后断言精确。

---

## 9. 自测题

1. 一个 `IndexPool(4)`，依次执行 `allocate, allocate, allocate, free(1), allocate, free(1), free(1)`，每步返回值是什么？
2. `GenPool` 为什么用"奇偶"表示空闲 / 在用，而不另开 `boolean[]`？至少说两个好处。
3. 写出把 `(int generation, int index)` 打包进 `long` 的代码，并解释为什么 `index` 要 `& 0xFFFFFFFFL`。
4. 下面的无锁弹出为什么错？怎么改？
   ```java
   int pop() {
       while (true) {
           int h = head.get();                  // AtomicInteger，存栈顶编号
           if (h == -1) return -1;
           if (head.compareAndSet(h, next[h])) return h;
       }
   }
   ```
5. 代码题：`ConcurrentPool.free` 里，如果先 `push` 再 CAS 版本号（颠倒这两步），会出什么 bug？给一个具体交错。

<details><summary>答案</summary>

1. 容量 4：`allocate`=0, `allocate`=1, `allocate`=2, `free(1)`=FREED, `allocate`=1（LIFO），`free(1)`=FREED，`free(1)`=DOUBLE_FREE。
2. (a) 版本号本来就必须有，奇偶白送，不增空间；(b) 并发时可一次 CAS 同时完成"校验 handle + 切换状态"，独立 `boolean` 则要对两个变量做原子操作；(c) 全零 handle 版本号是 0（偶数）自动无效，漏初始化的 handle 能被发现。
3. `long handle = ((long) generation << 32) | (index & 0xFFFFFFFFL);` `index` 是 `int`，负数转 `long` 会符号扩展，高 32 位变全 1，把 `generation` 位全 OR 成 1；`& 0xFFFFFFFFL` 先当无符号处理，高 32 位清零。
4. ABA：线程 1 读到 `h = A`、`next[A] = B` 后被切走；线程 2 弹 A、弹 B、再压 A；线程 1 的 CAS 看到 head 还是 A 就成功，把已被线程 2 占用的 B 装回栈顶。改法：`head` 改 `long`，高 32 位 tag，每次成功操作 +1，CAS 比较整个 64 位（`VarHandle` 或 `AtomicLong`）。
5. 线程 1、2 同时 `free(h)`。线程 1 先 push 槽位 i，然后被切走；线程 2 也 push 槽位 i，i 被压了两次（`next[i]` 指向自己或成环），之后 `allocate` 把同一槽位发给两个线程。颠倒后"谁有权压栈"没有仲裁，必须先用 CAS 版本号选出唯一赢家。

</details>

---

## 延伸阅读

* Herlihy & Shavit《The Art of Multiprocessor Programming》（Treiber 栈与 ABA）。
