# hc13 · 定长内存池 —— 讲义

> 读者：会写基本 Java。本篇从最根本的问题讲起：**Java 有垃圾回收器，为什么还有人要自己管内存？**

---

## 1. 这道题在问什么

假设你在写一个行情网关。每秒钟涌进来几十万条订单消息，每条消息要在内存里放一个小小的结构（订单号、价格、数量、买卖方向），处理完就不要了。

最直白的写法：来一条消息，`new Order(...)`；处理完，不管它，垃圾回收器（GC）会收拾。

面试题问的是另一种写法：**启动时就准备好固定数量（`capacity` 个）的、一样大的"格子"，运行时只"借"和"还"，不再 `new`**。这个装格子的东西叫**内存池**（memory pool）。

题意：实现一个包含 `capacity` 个等大块的池；块用某种"编号"表示；要能分配、归还、校验。返回值约定和后面的四个 Part，是按"一小时电面会怎么递进"来设计的。

### 手算一遍

池有 3 个块，编号 0、1、2。"借"一个，"还"一个：

```
初始            空闲的块: 0 → 1 → 2          （一条链：0 后面是 1，1 后面是 2）
allocate()      摘走链头 0       → 返回 0     空闲: 1 → 2
allocate()      摘走链头 1       → 返回 1     空闲: 2
free(0)         把 0 挂到链头                 空闲: 0 → 2
allocate()      摘走链头 0       → 返回 0     空闲: 2        ← 刚还的最先被借走（LIFO，后进先出）
allocate()      摘走链头 2       → 返回 2     空闲: （空）
allocate()      没有空闲块       → 返回 -1    （池满不是错误，是正常状态）
```

### 四个 Part 怎么递进

面试官不会一上来就问并发。一小时里他会这样一步一步加难度：

1. **Part 1**：块用 `int` 编号。借、还都要 O(1)。"如果我还了同一个块两次呢？还了一个根本不存在的编号呢？"
2. **Part 2**：他问："A 还了块 7，B 借到了块 7，A 手里还有个旧的 7，又还了一次，B 的块就被偷偷还掉了。怎么防？" → 编号里带"版本号"。
3. **Part 3**：他问："这些块在 Java 里是什么？对象数组？能不能让 GC 完全看不见它们？" → 堆外内存（FFM API）。
4. **Part 4**：他问："多线程怎么办？能不能不加锁？" → 无锁栈（Treiber stack）、CAS、ABA。再往后是口头题：每线程缓存。

---

## 2. 前置知识

> 复杂度记号速记：`O(n)` 表示步数随输入规模 n 线性增长；`O(log n)` 表示 n 翻倍只多一步（二分查找、平衡树、堆）；`O(n²)` 表示每一对元素都要处理一次；`O(1)` 表示与 n 无关。

### 2.1 为什么 Java 程序要"池化"？（先回答最根本的问题）

#### 2.1.1 对象住在哪里：堆（heap）

Java 里每次 `new Order(...)`，JVM 在一块叫**堆**的内存里划出一小块，放对象的所有字段，再给你一个引用。你从不 `free` 它。谁来回收？**垃圾回收器**（Garbage Collector，GC）。

GC 的基本工作（以最经典的"标记—清除"思路为例）：

1. 从"根"（线程栈上的局部变量、静态字段）出发，沿着引用一路走，**标记**所有走得到的对象——这些是"活的"；
2. 没被标记到的就是垃圾，把它们占的地方**回收**，供以后的 `new` 使用。

这叫**可达性**（reachability）分析：对象是不是垃圾，由"还有没有人引用它"决定，不由你说了算。

#### 2.1.2 `new` 其实很便宜

很多人以为 `new` 很慢。在 HotSpot 里，每个线程拥有一小块自己专用的堆（**TLAB**，Thread-Local Allocation Buffer）。`new` 一个对象就是把 TLAB 里的"下一个空位指针"往后推一个对象的大小——叫**指针碰撞**（bump the pointer），几条机器指令，不需要锁。我们的 `Order`（一个头 + `long id, long px, int qty, int side`）大约 **40 字节**（对象头 12 字节 + 24 字节字段，凑成 8 的倍数）。

所以池化**不是**为了让分配本身更快（后面的数据会显示：池的借还并不比 `new` 快多少）。

#### 2.1.3 真正的代价在回收

对象不断被创建，堆就不断被填满，填满之后 GC 必须出手：

* **年轻代**（young generation）：新对象先放在这里。大多数对象"朝生夕死"（经验规律，叫**分代假设**），所以 GC 只需要扫描年轻代，把还活着的少数对象**复制**到别处，整块清空——很便宜。
* 复制活对象时，应用线程要**暂停**（stop-the-world，STW）一小会儿，**暂停时间**与"当时活着的对象有多少"相关，而不是与垃圾多少相关。
* 存活足够久的对象被**晋升**到**老年代**（old generation）。老年代满了要做更贵的回收。

"朝生夕死"很便宜，"中年死亡"最糟糕：**对象存活的时间刚好长到会被 GC 复制几次、晋升到老年代，然后才死掉**。我们的订单消息就是这样——它在窗口里存活几十万条消息的时间，足够被复制和晋升。

两个核心量：

| 量 | 含义 | 怎么影响延迟 |
|---|---|---|
| **分配速率**（allocation rate） | 每秒 `new` 了多少字节 | 速率越高，年轻代填满得越快，GC 越频繁 |
| **存活集大小**（live set） | GC 时还活着的对象有多少 | 每次暂停要复制的东西越多，单次暂停越长 |

低延迟系统（撮合、做市）看的是**尾延迟**（tail latency）：不是"平均每条消息 2 微秒"，而是"最慢的那 0.01% 是多少"。一次 5 毫秒的 GC 暂停，对平均值没影响，但对尾延迟是灾难。

#### 2.1.4 数据：池化到底换来什么

场景：窗口里始终有 100 万条在飞的订单，每来一条新消息就顶掉最旧的一条，共 3000 万条消息，`-Xmx256m`。A 组每条 `new Order`；B 组用 `OffHeapOrderPool` 复用堆外槽位（`put(h, id, px, qty, side)` 直接写字段，零分配）。第 3 轮结果（前两轮是预热，同一个 JVM 里依次跑）：

| 收集器 | 方式 | 总耗时 | GC 次数 / 累计耗时 | 单次操作最慢 | 超过 1 ms 的操作 |
|---|---|---|---|---|---|
| G1 | 堆上 `new` | 757 ms | 74 次 / 144 ms | 4.46 ms | 44 个 |
| G1 | 堆外池 | 536 ms | 0 次 / 0 ms | 0.02 ms | 0 个 |
| Parallel | 堆上 `new` | 674 ms | 39 次 / 205 ms | 22.14 ms | 39 个 |
| Parallel | 堆外池 | 536 ms | 0 次 / 0 ms | 0.02 ms | 0 个 |
| 分代 ZGC（`-XX:+UseZGC -XX:+ZGenerational`） | 堆上 `new` | 598 ms | 82 次 / 455 ms（并发线程的时间，不是暂停） | 0.10 ms | 0 个 |
| 分代 ZGC | 堆外池 | 588 ms | 0 次 / 0 ms | 0.04 ms | 0 个 |

怎么读这张表（这是最重要的一张表，请逐行看）：

1. **吞吐几乎没差别**（500–800 ms，噪声就有 ±30%，不同轮之间互相超过）。`new` 本来就便宜，池的借还还要多几次内存读写。**别因为"快"去池化。**
2. **尾延迟差几个数量级**：G1 / Parallel 下，`new` 版里有几十个操作被 GC 暂停卡到 1 ms 以上，最慢 4–22 ms；池版最慢 0.02 ms。这就是低延迟系统愿意付出复杂度的原因。
3. **分代 ZGC 把暂停压到了亚毫秒**（0.10 ms），所以在 ZGC 下这个理由大大变弱——代价是 GC 线程在后台吃掉 CPU（455 ms 的累计并发耗时，几乎和应用本身一样多）。池化和选 GC 是同一个问题的两种解法。
4. 还有一个没在表里的事实：池版的 GC 次数是 0，意味着应用线程和 GC 线程不再抢 CPU、不再抢内存带宽。


#### 2.1.5 池化的代价（面试官最爱追问的另一半）

* **复杂度和 bug 面**：你把"谁负责释放"这个问题从 GC 手里接了过来。忘了还 = 泄漏；还两次 = 两个人用同一块；还了还在用 = use-after-free。在 C 里这些是崩溃，在池里它们是**悄悄的数据错乱**，更难查。本题 Part 1–2 就是在防这些。
* **数据泄漏**：上一个主人的数据留在块里，下一个主人能读到。所以 `allocate()` 要清零。
* **在堆上池化对象的陷阱**：池里的对象长期存活 → 被晋升到老年代；之后你每次往老对象里写一个新对象的引用，GC 要通过"写屏障"（write barrier）记下来。池化**堆上的、含引用字段的对象**可能让 GC 更累，不是更轻松。这也是本题的块最终是**堆外、纯数值字段**的原因：GC 完全看不见。
* **现代 JIT 的逃逸分析**（escape analysis）：如果对象没有逃出方法，JIT 可以不分配它（标量替换）。池化会让对象"逃逸"（存进池里），反而失去这个优化。
* **先量，再池化**：用 `-Xlog:gc`、JFR（`jdk.GarbageCollection`、`jdk.ObjectAllocationSample`）确认 GC 是瓶颈再动手。

### 2.2 空闲链表（free list）

**是什么**：把"还没被借走的块"串成一条链。借 = 摘掉链头；还 = 挂到链头。

**为什么需要它**：最朴素的做法是每次借的时候从头扫一遍，找第一个没被借的块——最坏要扫 `capacity` 个，O(n)。空闲链表让借和还都只改一两个变量，O(1)。

**它怎么工作**——最关键的一招是**把链表指针藏在块自己里面**（"侵入式"，intrusive）。空闲的块不需要存数据，所以它的位置可以拿来存"下一个空闲块是谁"。我们用一个 `int[] next`：

```
capacity = 4，初始状态:

 下标      0    1    2    3
 next[ ]  [1]  [2]  [3]  [-1]        head = 0
                                      意思: 0 → 1 → 2 → 3 → 结束(-1)

allocate():  b = head (=0);  head = next[0] (=1);  返回 0
 next[ ]  [?]  [2]  [3]  [-1]       head = 1

free(0):     next[0] = head (=1);  head = 0
 next[ ]  [1]  [2]  [3]  [-1]       head = 0      ← 又挂回去了
```

在用的块的 `next[b]` 没有意义，所以我们拿一个特殊值 `ALLOCATED = -2` 来标记"这块在用"——**一个数字同时承担"链表指针"和"是否在用"两个角色**，因为空闲和在用互斥。这就是 Part 1 检测重复归还的办法，不需要另开 `boolean[]`。

**Java 里怎么写**：见 §5.1。

### 2.3 句柄（handle）、悬空引用与 use-after-free

**是什么**：句柄是"指向某个资源的凭证"。Part 1 里块的 `int` 编号就是一个最简单的句柄。

**为什么会出事**：句柄只是个数字，池收回了块，**数字还在你手里**。三种经典错误：

| 错误 | 怎么发生 | 后果（无防护时） |
|---|---|---|
| **重复归还**（double free） | 对同一个编号 `free` 两次 | 块被挂进空闲链表两次 → 之后同一块被借给两个人 |
| **归还后继续用**（use-after-free） | `free(7)` 之后又读写块 7 | 读到（写坏）别人的数据 |
| **陈旧句柄**（stale handle，ABA 的变种） | A 还了 7；B 借到 7；A 又 `free(7)` | B 的块被 A 还掉了，B 完全不知道 |

第三种是 Part 1 **无法防**的：下标 7 在两个时刻代表"两个不同的所有者"，但数字完全一样。解决办法见 2.4。

### 2.4 版本号（generation）：让同一个下标在不同时刻"长得不一样"

**是什么**：每个槽位带一个计数器；handle 不只是下标，而是 `(版本号, 下标)`。槽位被归还时版本号 +1。handle 里的版本号和槽位当前版本不一致 → 这是个旧 handle。

```
                槽位 7 的版本号      A 的 handle        B 的 handle
初始                 0
A 借到 7             1 (奇数=在用)    (版本1, 下标7)
A 还 7               2 (偶数=空闲)
B 借到 7             3 (奇数=在用)                      (版本3, 下标7)
A 再 free(版本1, 7)  比较: 槽位当前是 3 ≠ 1 → 拒绝（DOUBLE_FREE）
```

我们的版本号约定：**偶数 = 空闲，奇数 = 在用**。每次借、每次还各 +1。好处会在 Part 4 看到：并发时可以用**一次 CAS**同时完成"验证这个 handle 有效"和"把槽位标记为空闲"。

#### 位打包：把两个 32 位数塞进一个 64 位 `long`

handle 要在方法间传、当 map 的 key、存进别的结构，最好是**一个**基本类型的值，不要为它 `new` 对象。`long` 有 64 位，正好放得下 `int generation`（32 位）+ `int index`（32 位）：

```
 63                           32 31                            0
 ┌──────────────────────────────┬──────────────────────────────┐
 │       generation (int)       │         index (int)          │
 └──────────────────────────────┴──────────────────────────────┘

打包:  handle = ((long) generation << 32) | (index & 0xFFFFFFFFL)
拆包:  index = (int) handle;            // 强转取低 32 位
       generation = (int) (handle >>> 32);   // 无符号右移 32 位再取低 32 位
```

最容易犯的错：**符号扩展**（sign extension）。`index` 是 `int`，转成 `long` 时，如果它是负的（最高位 1），Java 会把高 32 位全填成 1，把 generation 污染成 `0xFFFFFFFF`。`& 0xFFFFFFFFL` 先把它当**无符号**数看待，高 32 位清零，才安全。

版本号是 `int`，会溢出回绕（`0xFFFFFFFF + 1 = 0`）。因为 2^32 是偶数，回绕后奇偶性不变，所以"偶空闲/奇在用"的约定在回绕处依然成立。真正的风险是：同一个槽位被借还 2^31 次之后，一个极老的 handle 可能"撞上"当前版本。实际可以忽略；若不能忽略，退役这个槽位（永远不再借出）。

### 2.5 堆外内存与 FFM

Java 21 的外部内存 API（FFM，Foreign Function & Memory，预览）允许在 GC 管不到的地方分配和访问内存。本题用到的几个部件：

* **`Arena.ofShared()`**：负责一块内存的生命周期，`close()` 时整块归还；`ofShared` 允许别的线程访问（`ofConfined` 的内存只允许创建它的线程访问）。
* **`arena.allocate(bytes, 对齐)`**：分配并**清零**。
* **`MemoryLayout.structLayout(...)`**：像 C 的 `struct`，声明每个字段的类型和名字；`byteSize()` 给总大小。
* **`layout.varHandle(sequenceElement(), groupElement("px"))`**：得到一个 `VarHandle`，调用 `PX.get(segment, i)` / `PX.set(segment, i, v)` 读写第 `i` 个槽位的 `px` 字段。偏移由 JDK 算，不写魔法数字。

为什么槽位大小选 **32 字节**：头 8 字节（`gen:int` + `next:int`）+ 载荷 24 字节（`id:long, px:long, qty:int, side:int`）。32 字节是 2 的幂，一条 64 字节的缓存行正好放 2 个槽位，不会有一个槽位横跨两条缓存行（CPU 以缓存行为单位搬运数据，槽位横跨两行就要搬两次）。

### 2.6 并发：竞争、CAS 与"无锁"

并发正确性要同时考虑三件事：**原子性**（一个操作要么全做完、要么没做，别的线程看不到中间状态）、**可见性**（一个线程的写入何时能被别的线程看到）、**有序性**（编译器和 CPU 可能重排指令）。`VarHandle` 是 Java 9 起提供的、对字段做精确内存操作（带指定内存序的读写、CAS）的句柄。

**竞争条件**（race condition）：两个线程都执行"读 head → 改 head"，交错执行就会丢更新。

```
线程1: 读 head=5  ........................... 写 head=next[5]
线程2:           读 head=5, 写 head=next[5]
→ 两个线程都借走了块 5。
```

**CAS**（Compare-And-Set）：`CAS(变量, 期望值, 新值)`——**原子地**检查"变量现在是不是期望值"，是就改成新值并返回 true，不是就什么都不做返回 false。失败的线程重新读、重试。这是所有无锁（lock-free）算法的基石。

**无锁 ≠ 无等待**：无锁保证"总有某个线程在前进"（系统整体不会卡死），但单个线程可能一直 CAS 失败。

### 2.7 Treiber 栈与 ABA

**Treiber 栈**（R. K. Treiber, 1986）：用 CAS 实现的并发栈。栈顶是一个共享变量 `top`：

```
push(x):  loop { t = top;  x.below = t;  if CAS(top, t, x) break; }
pop():    loop { t = top;  if t == null return empty;  n = t.below;  if CAS(top, t, n) return t; }
```

我们的空闲链表本来就是一个栈（LIFO！），所以直接把它做成 Treiber 栈：`top` 就是 `head`，"节点"就是槽位编号，`below` 就是 `next[]` 数组。

**ABA 问题**——这是整个 Part 4 的核心。CAS 只看"值是不是 A"，不看"这期间发生过什么"。

```
初始栈:  A → B → C        (A 在栈顶)

线程 1 开始 pop():   读到 top = A,  读到 A.below = B。 （然后被操作系统切走）
线程 2:              pop() → 拿走 A     栈: B → C
                     pop() → 拿走 B     栈: C        （B 现在在线程 2 手里，正在使用）
                     push(A)            栈: A → C    （A 又回到栈顶）
线程 1 恢复:         CAS(top, 期望 A, 新值 B)  → top 现在确实是 A，CAS 成功！
                     栈变成: B → ???    B 被装回空闲链表，可是线程 2 还在用 B。
```

CAS 成功了（值确实还是 A），但"A"已经不是原来那个"A"——它的 `below` 变了。结果：线程 1 和线程 2 对 B 同时拥有所有权。这是并发池最经典的 bug。

**解法：带 tag 的头指针**（tagged pointer / versioned head）。让 `head` 不只存"栈顶编号"，还存一个**计数器**，每次成功 push/pop 都 +1：

```
 63                32 31                 0
 ┌───────────────────┬────────────────────┐
 │   tag (计数器)     │  栈顶槽位编号(-1=空) │
 └───────────────────┴────────────────────┘
```

CAS 比较的是整个 64 位。线程 2 的 pop、pop、push 让 tag 从 t 变成 t+3；线程 1 的 CAS 期望的是 `(tag=t, A)`，现在是 `(tag=t+3, A)`，不相等 → 失败，重读。

tag 也会回绕（32 位 = 42 亿次操作）：要让 ABA 重现，线程 1 必须恰好在读和 CAS 之间被挂起整整 2^32 次成功操作——可以忽略，但要在注释里写明。`AtomicStampedReference` 是 JDK 里同一思想的对象版（但要为每次更新分配一个 `Pair` 对象，在池里是反面教材）。

### 2.8 每线程缓存（per-thread cache）

**问题**：所有线程抢同一个 `head`，CAS 失败的线程在原地重试，每次重试都要把 `head` 所在的缓存行从别的核心"抢"过来（缓存一致性协议，MESI），线程越多越慢。

**办法**：每个线程在自己手里先攒一小批槽位。借的时候先从自己的小仓库拿，空了才去共享池里**一次拿一批**；还的时候先放进自己的小仓库，满了才**一次还一批**回共享池。共享的 `head` 只在"补货 / 退货"时碰一次，而不是每次借还都碰。

这个思路无处不在：JVM 自己的 TLAB 就是每线程的分配缓存；tcmalloc 的 thread cache、jemalloc 的 tcache、Solaris slab 分配器的 magazine（Bonwick 2001）都是它。§4.4 有数据。

---

## 3. 从最笨的解法开始

最笨的写法（也是很多人在白板上的第一版）：

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

它是对的：重复归还、越界都能检测。**错在哪里**：`allocate()` 是 O(`capacity`)。**具体慢在**：池接近满、空位散落在数组中间的时候，每次要扫过前面所有被借走的块才能找到空位。注意这个缺陷很容易被"随机借还"的测试漏掉——如果池里平均只有几百块在用，前几百个格子之后就是空位，扫描很快（（我们实际 300 万次 50/50 随机借还，这个版本 125 ms 就跑完了，看起来没问题！））。所以 `IndexPoolTest.nearFullChurnIsFast` 专门把池填满、再 150 万次"换掉随机一块"：`capacity = 65536` 时，朴素版实际每步约 3.9 微秒，150 万步约 6 秒，超过 2 秒预算（测试红）；链表版同样的负载约 11 毫秒。**教训：测性能要测最坏的形状，不是测"平均看起来随机"的形状。**

另一个常见的"第二笨"写法是 `ArrayDeque<Integer>` 当空闲栈：O(1)，但每个 `Integer` 是个装箱对象（`Integer` 缓存只管 -128..127），借还一次就 `new` 一个对象——**池子本身在制造垃圾**，违背了初衷。

---

## 4. 一步一步改进

### 4.1 Part 1：从扫描到空闲链表

**发现问题**：扫描找空位是 O(n)。
**想法**：别找——让"空位"自己排好队，借的时候直接取队头。
**为什么能解决**：队头就是一个变量；取队头、更新队头都是 O(1)。需要的只是"队里每个元素知道下一个是谁"，即 §2.2 的 `next[]`。
**代码变化**：`boolean[] inUse` → `int[] next` + `int head`；`allocate` 变成 `b = head; head = next[b]`；`free` 变成 `next[b] = head; head = b`。
**新复杂度**：`allocate` / `free` 都是 O(1)；构造 O(capacity)（初始化链表）。空间 `4 × capacity` 字节，比 `boolean[]` 大 4 倍，但换来了 O(1)。

**还差什么——重复归还检测**：只有 `next[]` 的话，`free(3)` 调两次，第二次执行 `next[3] = head; head = 3`——把 3 挂在了链表里它自己的后面，链表出现环或重复。必须能判断"3 现在是不是在用"。
**想法**：用 `next[b] = ALLOCATED (-2)` 标记在用的块（§2.2）。`free` 先看 `next[b] == ALLOCATED`，不是 → `DOUBLE_FREE`；越界 → `INVALID`。
**新复杂度**：仍是 O(1)，不需要额外数组。

### 4.2 Part 2：从下标到带版本号的 handle

**发现问题**：Part 1 无法区分"我手里的 7"和"别人现在手里的 7"（§2.3 的第三种错误）。
**想法**：让 handle 里带版本号（§2.4）。
**为什么能解决**：每次借还让槽位版本号变化；旧 handle 的版本号一定不等于槽位当前版本号。
**代码变化**：多一个 `int[] gens`；`allocate` 里 `gens[i]++`（偶→奇），返回 `handle(i, gens[i])`；`free` 里先拆出 `(index, g)`，校验后 `gens[i] = g + 1`（奇→偶）。
**判定顺序**（`free`）：
1. 下标越界，或 `g` 是偶数（从没发过这种 handle）→ `INVALID`；
2. `gens[index] != g`（奇数但已经过期）→ `DOUBLE_FREE`；
3. 否则 `FREED`。

注意 `NONE = -1`（全 1）永远无效：它的下标是 `0xFFFFFFFF`，当 `int` 是 -1，越界；全零 handle 的版本号是 0（偶数），无效。**漏初始化的 handle 立刻暴露**——这是用偶数表示"空闲"的一个副作用好处。

**新复杂度**：仍是 O(1)；每槽位多 4 字节。

### 4.3 Part 3：从对象到堆外记录

**发现问题**：到目前为止池里放的只是"编号"，真正的数据在哪里？如果用 `Order[]`，数组里存 `capacity` 个引用，每个 `Order` 都是堆上的对象，GC 要扫描它们、晋升它们（§2.1.5）。
**想法**：把数据本身放进一块连续的堆外内存，用 handle 访问。
**为什么能解决**：堆外内存对 GC 不可见（§2.1.1）；连续布局对 CPU 缓存友好。
**代码变化**：`gens` 和 `next` 不再是两个 `int[]`，而是**槽位头部的两个字段**（`gen:int`, `next:int`），后面紧跟载荷（`id, px, qty, side`）。一个 32 字节的 `StructLayout`，`SequenceLayout` 重复 `capacity` 次，一次 `arena.allocate(...)` 拿到。
**要小心的新问题**：
* **清零**：`allocate` 必须把载荷清零，否则上一个主人的数据漏给下一个。`Arena.allocate` 只在第一次分配时清零，**复用**的槽位没人帮你清。
* **生命周期**：`close()` 之后所有访问由 `Arena` 自带检查抛 `IllegalStateException`（不是崩进程）；重复 `close()` 会让 `Arena.close()` 抛异常，所以先判 `arena.scope().isAlive()`。
* **API 设计**：如果只提供 `put(h, Order)` / `Order get(h)`，调用方每次都 `new Order`，等于把池子省下的分配又补了回去。所以多给 `put(h, id, px, qty, side)` 和 `px(h)` / `qty(h)`——**零分配的热路径接口**。`get(h)` 仍提供，但它会 `new`，文档里写明"不在热路径上用"。这说明 API 设计和内存管理是一回事：**API 的形状决定调用方能不能写出零分配的代码**。

**新复杂度**：O(1)；`capacity × 32` 字节，一次分配（`byteSize()` 是 `long`，可以超过 2 GiB，`ByteBuffer` 做不到）。

### 4.4 Part 4：从单线程到线程安全

#### 步骤 A：最简单的正确解——加锁

```java
class LockedPool {
    private final GenPool pool; private final ReentrantLock lock = new ReentrantLock();
    long allocate() { lock.lock(); try { return pool.allocate(); } finally { lock.unlock(); } }
    FreeResult free(long h) { lock.lock(); try { return pool.free(h); } finally { lock.unlock(); } }
}
```

正确、简单、面试里应当**先说出这个**。`ReentrantLock` 而不是 `synchronized`：虚拟线程下 JDK 21 的 `synchronized` 会钉住（pin）载体线程。问题只是：所有线程排队过同一把锁。

#### 步骤 B：想去掉锁——朴素 Treiber 栈（有 bug）

把 `head` 变成一个 `volatile int`（只存栈顶编号），`allocate` 里 `CAS(head, h, next[h])`。看起来对，实际上有 §2.7 的 ABA bug。**这个 bug 是并发池面试的标准考点**。

#### 步骤 C：加 tag 的 head

`head` 变成 `long`：高 32 位 tag，低 32 位编号（§2.7）。代码变化：每次 CAS 的新值是 `pack(tag + 1, 新栈顶)`。
**验证这个修复**：如果把两处 `tagOf(h) + 1` 改成 `tagOf(h)`（去掉 tag），在多线程争用的压力测试里，20 轮就有 7 轮出现"丢了槽位"（空闲链表被弄坏）；加回 tag 后全部通过。这不是证明，但说明压力测试确实抓得到这个 bug。

#### 步骤 D：并发 double-free

单线程的 `free` 是"检查版本 → 改版本 → 压栈"三步。两个线程同时 `free` 同一个 handle，都通过了检查，都压栈 → 同一个槽位进了空闲链表两次 → 之后同一块借给两个人。
**想法**：把"检查 + 改版本"合成**一次 CAS**：`CAS(gens[i], g, g + 1)`。成功的线程拥有"归还这个槽位"的权利，失败的线程看到版本已经变了 → `DOUBLE_FREE`。
**为什么偶/奇约定在这里派上用场**：版本号本身就是状态（奇=在用），CAS 一次完成"状态检查 + 状态切换"，不需要另一个"allocated"标志位和对它的第二次原子操作。
**同样可以验证**：把这个 CAS 换成"先读后写"，并发 double-free 的压力测试就会全面失败（成功归还的次数 2110 > 2000，多归还了）。

#### 步骤 E：内存序——每一处该用什么

| 位置 | 访问方式 | 为什么 |
|---|---|---|
| 读 `head` | `getAcquire` | 要看到别的线程 push 之前对 `next[i]`、`gens[i]` 的写 |
| `head` 的 CAS | `compareAndSet`（volatile 语义，含 release） | push 时发布 `next[i]` 和版本号；pop 成功要成为全序的一环 |
| `next[i]` 读写 | `getOpaque` / `setOpaque` | 读到旧值没关系——那样 `head` 的 tag 已经变了，CAS 会失败；只需要"不撕裂、不被编译器缓存" |
| `gens[i]` 的 CAS（free） | `compareAndSet` | 并发 double-free 的仲裁点 |
| `gens[i]` 在 allocate 里的写 | `setRelease` | 弹出成功后槽位归本线程所有；发布版本号给之后的 `isLive` |
| `inUse` 计数器 | `LongAdder` | 纯统计，不参与正确性；分散热点 |

这里体现的思想："**读到过期数据没关系，只要最后用 CAS 校验**"。这是写无锁算法最常用的省力办法，但只在"CAS 的对象能反映过期"时成立（所以 tag 不能省）。

#### 步骤 F：每线程缓存（口头题，有数据）

基准：65536 个槽位，T 个线程各做 400 万次借还（每批借 16 个再还 16 个），单位百万次操作/秒（alloc 和 free 各算一次）。三种写法：

* `locked`：`ReentrantLock` 包住 `GenPool`；
* `treiber`：我们的 `ConcurrentPool`；
* `cached`：每线程一个 64 格的小仓库，空了从 `ConcurrentPool` 批量借 32 个，满了批量还 32 个。

数据（两次运行；`locked` 在 2 线程时两次分别是 25 和 7——这种波动是真实的，锁的争用结果不稳定）：

| 线程数 | locked | treiber | cached |
|---|---|---|---|
| 1 | 149 – 155 | 106 – 111 | 223 – 239 |
| 2 | 7 – 25 | 9 – 10 | 425 – 432 |
| 4 | 60 – 86 | 14 – 15 | 685 – 707 |
| 8 | 80 – 83 | 3.9 | 1021 – 1028 |

怎么读：

1. **无锁不等于快。** 8 个线程抢同一个 `head` 时，Treiber 栈只有 3.9，比加锁慢 20 倍。每次 CAS 失败都要重新把 `head` 所在的缓存行抢回来，LIFO 又让所有线程总在碰同几个槽位（`gens`、`next` 的同几个缓存行）。`ReentrantLock` 是非公平锁，允许"插队"，一个线程可以连续拿到好几次，反而减少了缓存行的来回搬运。无锁真正的卖点是**不会被挂起的线程拖住别人**（不会优先级反转、不会因为持锁线程被调度出去而全员等待），不是吞吐。
2. **每线程缓存把吞吐翻了几十倍，而且随线程数线性增长**（223 → 1028），因为大多数借还根本没碰共享状态。
3. **代价**（面试官要听的另一半）：
   * **搁浅**（stranding）：槽位躺在某个线程的缓存里，别的线程看池是"空"的（`allocate` 返回 `NONE`），虽然其实有闲置槽位。缓存容量 × 线程数要算进池的总容量。
   * **失去重复归还检测**：缓存里的 handle 在共享池眼里仍是"在用"（版本号是奇数），对它再 `free` 一次，共享池无从发现；要检测只能在每线程缓存里另做一套标记。bench 里的 `Cached` 就没做。
   * **线程退出时要冲刷缓存**；**虚拟线程**下 `ThreadLocal` 缓存是"每个虚拟线程一个"，数量可能几十万——应改成按载体线程 / 按 CPU 分片（striping）的缓存。
   * **LIFO / 公平性语义改变**：刚还的槽位不再是全局下一个被借走的。

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

构造：把 `next[i]` 初始化成 `i + 1`，最后一块指向 `NONE (-1)`（链表结束）。`head = 0` 所以第一次 `allocate` 返回 0。`MAX_CAPACITY = 1 << 28` 是为了不让 `new int[...]` 吃掉 1 GiB 以上；超出就明确报错而不是 `OutOfMemoryError`。

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

取链头；链表空（`head == NONE`）就返回 `NONE`，不抛异常——池满是正常状态。取走后把它的 `next` 改成 `ALLOCATED`，这是 §4.1 的"在用标记"。

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

先查范围再查状态（顺序不能反，否则越界直接 `ArrayIndexOutOfBoundsException`）。"不在用"包括"已经还过"和"从没借过"，统一报 `DOUBLE_FREE`——对调用者来说都是"你不该还这块"。

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

switch 表达式：三个分支各产生一个值（要么 `null` 要么异常对象）。漏写 `INVALID` 编译器直接报错（对 `enum` 的穷尽性检查）。这是为什么 `FreeResult` 用 `enum` 而不是 `int` 常量：新增一种结果时，所有 `switch` 都会编译失败，不会悄悄漏处理。

### 5.2 `GenPool`（Part 2）

```java
public static long handle(int index, int generation) {
    return ((long) generation << 32) | (index & 0xFFFFFFFFL);
}
public static int indexOf(long handle) { return (int) handle; }
public static int generationOf(long handle) { return (int) (handle >>> 32); }
```

就是 §2.4 的打包 / 拆包。`>>>`（无符号右移）而不是 `>>`：虽然后面又 `(int)` 强转，两者结果相同，但 `>>>` 表达了"这里不关心符号"的意图。

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

* `index < 0`：低 32 位当 `int` 是负数（比如 `0x0000_0001_8000_0000`）——必须检查，否则 `gens[index]` 抛异常。
* `(g & 1) == 0`：偶数版本号 = 从没发过 → `INVALID`。
* 这里不再需要 `ALLOCATED` 哨兵：版本号的奇偶就是状态。`next[]` 只在空闲链表里有意义。

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

`SLOT` 声明一个槽位的字段（32 字节，8 字节对齐，没有隐式填充：4+4+8+8+4+4）。`SLOTS` 是 `MAX_CAPACITY` 个槽位的序列——**它只是一个描述，不分配任何内存**。用它生成 `static final` 的 `VarHandle`：JIT 对 `static final` 的 `VarHandle` 能把读写内联成一条加载 / 存储指令。如果按实际 `capacity` 在构造器里生成 `VarHandle`（实例字段），JIT 不能把它当常量折叠，会慢。每个 `VarHandle` 的坐标是 `(MemorySegment, long 槽位下标)`。

```java
this.seg = arena.allocate(SLOT.byteSize() * capacity, 64);
for (int i = 0; i < capacity; i++) NEXT.set(seg, (long) i, i + 1 < capacity ? i + 1 : END);
```

一次分配 `capacity × 32` 字节，64 字节对齐（缓存行）。分配出来全零，所以 `gen = 0`（全部空闲，偶数）不用初始化；`next` 要显式写成 `i + 1`。

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

和 `GenPool.allocate` 一模一样，多了"清零载荷"。`VarHandle.get` 返回 `Object`（签名多态），所以要 `(int)` 强转。注意下标一律转 `long`：`(long) index`——传 `int` 会让 `VarHandle` 调用点的静态类型不匹配，运行时才报 `WrongMethodTypeException`。

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

幂等关闭。此后任何 `seg` 访问抛 `IllegalStateException("Already closed")`，由 FFM 运行时保证，我们不用自己检查。

### 5.4 `ConcurrentPool`（Part 4）

```java
private static long pack(int tag, int index) { return ((long) tag << 32) | (index & 0xFFFFFFFFL); }
private static int tagOf(long h) { return (int) (h >>> 32); }
private static int indexOf(long h) { return (int) h; }
```

和 handle 同样的打包，但这里高 32 位是 tag。

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

逐行：
1. `getAcquire` 读 `head`（含 tag）。
2. 空 → 返回 `NONE`。
3. 读 `next[index]`——这是"如果我成功弹出，新栈顶是谁"。此时它可能已经过期（别的线程正在改），没关系，下一步的 CAS 会验证。
4. `compareAndSet(this, h, pack(tag + 1, below))`：`head` 还完全等于刚才读到的 `h`（包括 tag）才成功。
5. 成功后这个槽位归本线程所有，没人会同时修改它的版本号（别的线程拿着的旧 handle 的 `free` 会因为版本号不匹配失败），所以直接 `get`+`setRelease` 就行，不需要 CAS。
6. 失败：`Thread.onSpinWait()`（给 CPU 的提示：我在自旋，可以省电 / 让出超线程资源），回到循环。

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

先 CAS 版本号（§4.4 步骤 D）。**赢了这次 CAS 的线程独占"把槽位压回栈"的权利**，之后的压栈循环只会和别的线程的 push / pop 竞争 `head`，不会和"另一个想压同一个槽位的线程"竞争。压栈：把当前 `head` 的栈顶写进 `next[index]`，再 CAS `head` 指向 `index`，tag + 1。

`available()`：`capacity - inUse.sum()`。`LongAdder.sum()` 在并发更新时是近似值，静止后精确。

---

## 6. Java 21 特性小课

本题用到的特性：

| id | 用在哪 | 老写法 | 新写法 / 为什么 |
|---|---|---|---|
| `record` | `Order(long id, long px, int qty, int side)` + `Order.ZERO` | 一个类 + 4 个字段 + 构造器 + 访问器 + `equals`/`hashCode`/`toString`（约 30 行，容易漏改） | 一行；`equals` 逐字段比较，所以可以直接比较 `new Order(1,2,3,4)` 和 `pool.get(h)`。 |
| record 模式 | `put(long, Order)` 里 `case Order(long id, long px, int qty, int side) ->` | `long id = o.id(); long px = o.px(); ...` 四行 | 一次解构；编译器检查 record 的组件个数与类型。**不该用**的场合：只用一个字段时，直接 `o.px()` 更清楚。 |
| switch 表达式 | `freeOrThrow`：`RuntimeException failure = switch (free(block)) {...}` | `switch` 语句 + 每个分支赋值 + `break`（漏 `break` 就 fall through） | 每个分支是一个值；对 `enum` **穷尽性检查**，新加一个 `FreeResult` 值，这里编译不过。 |
| `var` | `var pool = new IndexPool(3)` | `IndexPool pool = new IndexPool(3)` | 右边已经写了类型；**不该用**：右边看不出类型时（如 `var x = foo()`）。 |
| 虚拟线程 | `Executors.newVirtualThreadPerTaskExecutor()` 开 2000 个并发任务 | 线程池大小要调参，2000 个平台线程会吃掉大量内存 | 2000 个任务就开 2000 个虚拟线程，几乎没成本；自旋型任务**不该**用虚拟线程（会占住载体线程）。这里的任务是短小的借还、不阻塞。 |
| `VarHandle` / `LongAdder` | `ConcurrentPool` 的 `HEAD`、`NEXTS`、`GENS`，`inUse` | `AtomicReferenceFieldUpdater` / `Unsafe` / 每个槽位一个 `AtomicInteger`（`capacity` 个对象） | `arrayElementVarHandle(int[].class)` 对普通 `int[]` 的元素做 CAS / opaque / release，不需要为每个槽位建一个原子对象；`findVarHandle` 对普通 `long` 字段做 CAS。 |
| FFM | `OffHeapOrderPool` 的 `Arena` / `MemorySegment` / `StructLayout` / `SequenceLayout` | `ByteBuffer.allocateDirect`（容量 `int`、无确定性释放、偏移全靠手算） | 容量 `long`、`close()` 确定性释放、字段按名字访问。**JDK 21 是预览特性**（`--enable-preview`），JDK 22 起转正，`allocateUtf8String` 等名字会变。 |

本题的位运算打包（`& 0xFFFFFFFFL`、`>>>`）属于基础，不在特性矩阵里；`Math.addExact` / `Math.clamp` 等小工具本题没有用到。

---

## 7. 追问预演

### 追问 1：为什么要自己做内存池？Java 不是有 GC 吗？

**思考过程**：先承认 `new` 很快（TLAB 指针碰撞），池化不是为了快；再说真实的代价在 GC，具体是暂停（尾延迟）和 GC 线程抢 CPU；最后给"什么时候该用"的判据。
**答案要点**：分配速率高 + 存活集大 + 对尾延迟敏感；先用 `-Xlog:gc` / JFR 量；现代 GC（分代 ZGC）已经把暂停压到亚毫秒，所以先试换 GC 再考虑池化。
**可以说出口的一段话**：「`new` 本身很便宜，我池化不是为了更快，是为了让热路径上没有分配，GC 就没有活干，延迟曲线上就没有毛刺。我会先用 JFR 确认 GC 暂停确实是尾延迟的来源，因为池化会引入 use-after-free 这类逻辑 bug，是有成本的。」

### 追问 2：怎么知道一个块是不是已经还过？

**思考过程**：O(1) 的话不能扫；需要每块一个"状态"；最省的办法是复用已有的 `next[]`。
**答案要点**：`next[b] == ALLOCATED` 哨兵；`free` 先检查；不额外开数组。
**一段话**：「空闲块的 `next` 是下一个空闲块的编号（≥ -1），在用块的 `next` 我设成 -2。`free` 时看到不是 -2 就说明它不在用，直接返回 DOUBLE_FREE，不会动链表。」

### 追问 3：A 还了块 7，B 借到了 7，A 又还一次——怎么防？

**思考过程**：问题根源是下标没有"身份"；需要让同一下标在不同借用期里不相等；自然想到版本号。
**答案要点**：handle = (generation, index)；每次借还版本号变；`free` 比较版本号。
**一段话**：「把 handle 做成 long，高 32 位是槽位的版本号，低 32 位是下标。槽位每次归还版本号加一，旧 handle 里的版本号就永远追不上当前版本，所以 A 的第二次 free 会被识别出来而不会动到 B 的块。」

### 追问 4：版本号溢出了怎么办？

**思考过程**：32 位版本号 2^32 种取值，每次借还 +2（我们用奇偶）所以 2^31 次借还才回到同一个值；回绕后奇偶性不变。
**答案要点**：回绕后一个 2^31 次借还之前的 handle 可能"撞上"；可忽略，若不可忽略，槽位达到上限后退役（不再借出）；或者用 64 位版本号 + 128 位 handle。
**一段话**：「版本号 32 位，同一个槽位要被借还二十亿次，旧 handle 才可能碰巧又有效。实际上不会发生；如果是长期运行的关键系统，我会在版本号接近上限时把槽位永久退役。」

### 追问 5：多线程怎么做？

**思考过程**：先说最简单正确的（锁），再说为什么想去掉锁，再说无锁的陷阱（ABA）、解法（tag），再说并发 double-free。
**答案要点**：见 §4.4 全部。
**一段话**：「最简单是一把 ReentrantLock。如果要无锁，空闲链表本来就是个栈，可以用 Treiber 栈，但单纯对栈顶下标做 CAS 有 ABA 问题，所以我把 head 做成 long，高 32 位是每次成功操作都加一的 tag。另外 free 要用一次 CAS 把槽位版本号从奇数推到偶数，这样两个线程同时 free 同一个 handle 只会有一个赢。」

### 追问 6：tag 也会溢出吧？

**思考过程**：tag 32 位；ABA 要求某线程在读 head 和 CAS 之间，别的线程做了恰好 2^32 的整数倍次成功操作。
**答案要点**：理论上存在，实践中需要一个线程被挂起足够久且别的线程做 42 亿次操作；要消除就用 64 位 tag + 128 位 CAS（`cmpxchg16b`；Java 里没有直接支持）或 hazard pointers / epoch 回收。
**一段话**：「会回绕，但要重现 ABA 需要一个线程被挂起期间别人恰好完成 2 的 32 次方次操作。我接受这个风险，并在注释里写明。更严的做法是 hazard pointer，或者缩小问题，用每线程缓存减少共享栈的操作次数。」

### 追问 7：无锁一定比锁快吗？

**思考过程**：用数据说话：§4.4 的表。
**答案要点**：不一定；争用高时 Treiber 栈每次 CAS 失败都有缓存行搬运；无锁的价值是进度保证（不会被挂起的线程卡住）；真正提升吞吐的是减少对共享状态的访问（每线程缓存）。
**一段话**：「我测过：8 个线程抢同一个 Treiber 栈，吞吐比一把 ReentrantLock 还低很多；加每线程缓存、批量补货之后快了几十倍。所以无锁的价值主要是进度保证，不是吞吐，吞吐靠降低争用。」

### 追问 8：每线程缓存有什么代价？

**思考过程**：缓存把状态藏在线程里，凡是需要全局视角的功能都会受影响。
**答案要点**：搁浅、重复归还检测变弱、线程退出冲刷、虚拟线程下 `ThreadLocal` 的数量、LIFO 语义变化。见 §4.4 步骤 F。

### 追问 9：池满了怎么办？

**思考过程**：三个选择，各有适用场景；选择是产品决策，不是技术问题。
**答案要点**：(1) 返回 `NONE`（拒绝 / 背压，调用方决定）；(2) 阻塞等待（`Semaphore` + 栈）；(3) 扩容（链接新的块组，但会打破"固定容量"的保证、引入分配）。低延迟系统通常选 (1) 并告警：池满意味着容量规划错了。

### 追问 10：为什么用堆外而不是 `Order[]` 预分配？

**答案要点**：`Order[]` 里的 `Order` 是堆对象，被晋升到老年代；之后每次往它们里写引用要写屏障；GC 每次完整回收都要遍历它们。堆外的纯数值记录 GC 看不见。代价：手动 `close`、固定容量、边界检查（JIT 能消掉大部分）、JDK 21 里是预览特性。

---

## 8. 常见误区

### 误区 1：打包 handle 时忘了 `& 0xFFFFFFFFL`

```java
// 很多人这样写
long handle = ((long) generation << 32) | index;       // index 是 int
```

`index` 非负时没问题，但 `index` 是 `int`，一旦为负（比如 `0x8000_0000`），`(long) index` 的高 32 位全是 1，把整个 `generation` 位 OR 成 `0xFFFFFFFF`。**正确**：`| (index & 0xFFFFFFFFL)`。

### 误区 2：重复归还只"忽略"，不检查

```java
void free(int b) { next[b] = head; head = b; }       // 没检查
```

连续 `free(3)` 两次，`next[3] = 3`（自己指向自己），之后 `allocate` 永远返回 3。**正确**：先看 `next[b] == ALLOCATED`。

### 误区 3：以为 `volatile` 能修好 ABA

把 `head` 声明成 `volatile int` 只解决可见性，不解决 ABA——ABA 是"值相同但历史不同"，`volatile` 不记历史。**正确**：加 tag（或 `AtomicStampedReference`）。来自 §2.7。

### 误区 4：`free` 先检查再修改，没有原子化

```java
if (gens[i] == g) { gens[i] = g + 1; push(i); }       // 两步，之间可以被别的线程插入
```

并发下两个线程都通过 `if`。**正确**：`CAS(gens[i], g, g+1)` 把检查和修改合成一次。

### 误区 5：复用槽位忘了清零

`allocate()` 返回的记录里还留着上一个主人的 `px`、`qty`。这既是 bug 来源（"我没写 qty，为什么不是 0"）也是信息泄漏。**正确**：`allocate` 里写零（或约定调用方必须写全）。

### 误区 6：池要被多个线程用，却用 `Arena.ofConfined()`

`ofConfined` 的 segment 只允许创建它的线程访问，别的线程访问会抛 `WrongThreadException`（带超时的测试框架常把测试体放到另一个线程里运行，同样会触发）。**正确**：`ofShared()`。

### 误区 7：把 `available()` 当并发中的精确值

并发进行中，`inUse` 和 `head` 的更新不是同一个原子操作，`available()` 可能暂时偏差几个。**正确**：把它当近似值，只在所有线程静止后断言精确。

---

## 9. 自测题

1. 一个 `IndexPool(4)`，依次执行 `allocate, allocate, allocate, free(1), allocate, free(1), free(1)`，每一步的返回值是什么？
2. 为什么 `GenPool` 用"奇偶"表示空闲 / 在用，而不是另开一个 `boolean[]`？至少说出两个好处。
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
5. 代码题：`ConcurrentPool.free` 里，如果先 `push` 再 CAS 版本号（颠倒这两步），会出什么 bug？给出一个具体的交错。

<details><summary>答案</summary>

1. 容量 4：`allocate`=0, `allocate`=1, `allocate`=2, `free(1)`=FREED, `allocate`=1（LIFO），`free(1)`=FREED，`free(1)`=DOUBLE_FREE。
2. (a) 版本号本来就必须有，奇偶白送，不增加空间；(b) 并发时可以一次 CAS 同时完成"校验 handle + 切换状态"，如果用独立的 `boolean`，就需要对两个变量做原子操作；(c) 全零 handle 的版本号是 0（偶数），自动无效，漏初始化的 handle 能被发现。
3. `long handle = ((long) generation << 32) | (index & 0xFFFFFFFFL);` `index` 是 `int`，负数转 `long` 会符号扩展，高 32 位变成全 1，把 `generation` 位全部 OR 成 1；`& 0xFFFFFFFFL` 先当无符号处理，高 32 位清零。
4. ABA：线程 1 读到 `h = A`、`next[A] = B` 后被切走；线程 2 弹 A、弹 B、再压 A；线程 1 的 CAS 看到 head 还是 A 就成功，把已被线程 2 占用的 B 装回栈顶。改法：`head` 改成 `long`，高 32 位是 tag，每次成功操作 +1，CAS 比较整个 64 位（用 `VarHandle` 或 `AtomicLong`）。
5. 线程 1、2 同时 `free(h)`。线程 1 先 push 槽位 i（栈里有了 i），然后被切走；线程 2 也 push 槽位 i，此时 i 被压了两次（`next[i]` 指向自己或形成环），之后 `allocate` 把同一个槽位发给两个线程。颠倒后，"谁有权压栈"没有仲裁，必须先用 CAS 版本号选出唯一赢家。

</details>

---

「延伸」Herlihy & Shavit《The Art of Multiprocessor Programming》（Treiber 栈与 ABA）。
