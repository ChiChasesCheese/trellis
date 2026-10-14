# hc04 讲义 · 队列均值与快照：从「每次重新加一遍」到「无锁读」

> 配套题集：[problem.md](../../loop/rounds/01_video/hc04_queue_mean_snapshot/problem.md) · [REPORT.md](../../loop/rounds/01_video/hc04_queue_mean_snapshot/REPORT.md) · 参考解 `loop/rounds/01_video/hc04_queue_mean_snapshot/reference/`
> 读者设定：会写基本 Java（类、方法、循环、`ArrayList`/`HashMap`），没学过数据结构、浮点数、并发。所以每个概念都从零讲。
> 标 **(reconstructed)** 的是我根据题目标题补出来的部分，不是原题（原题证据只有标题和第一句话）。

---

## 1. 这道题在问什么

**第一问**（证据：「实现一个 queue 和三个函数 push、pop 和 get_mean」）：

做一个**队列**（queue）。队列像排队买票：新来的站队尾（`push`），队头的人先走（`pop`），先来的先走，叫「先进先出」（FIFO）。
再加一个函数 `get_mean()`：返回现在队里所有数的**平均数**（mean）。

手算一遍：

```
push 1      队列: [1]
push 2      队列: [1, 2]
push 3      队列: [1, 2, 3]       get_mean → (1+2+3)/3 = 2
push 4      队列: [1, 2, 3, 4]    get_mean → 10/4 = 2.5
pop         返回 1，队列: [2, 3, 4]   get_mean → 9/3 = 3
```

听上去像一道三分钟的题。面试官要看的是**你接下来五十分钟会不会主动发现问题**。我们会发现至少五个问题：

1. 每次 `get_mean` 都把所有数重新加一遍，太慢。
2. 用 `double` 保存「当前总和」，加了又减，结果会悄悄变错。
3. 数很大时 `long` 加法会溢出（变成负数）。
4. 「快照」是什么？保存历史版本要复制多少数据？**(reconstructed)**
5. 一个线程在改队列，另一个线程在读平均数，会不会读到「一半新一半旧」的值？**(reconstructed)**

本讲义按这个顺序一个一个解决。

**第二问**（证据：「第二问是实现一个带有 snapshot 的……」，被截断）：带快照的版本。我把它做成两个层次：
Part 2 是「修正快照」事件流，Part 3 是「可以随时回头看任何历史版本」的持久化队列。都是 **(reconstructed)**。

---

## 2. 前置知识

### 2.1 队列与「环形缓冲」（ring buffer）

**是什么**：队列是一种只能从一端放、从另一端取的数据结构。**环形缓冲**是用一个固定大小的数组实现队列的办法，数组首尾连成一个圈。

**为什么需要**：最直观的办法是用数组，`pop` 时把后面所有元素往前挪一格——要挪 n 个，`O(n)`。
如果不挪，只是把「队头下标」往后移一格，那 `pop` 是 `O(1)`，但前面空出来的格子永远用不上，数组迟早满。解决办法：队尾走到数组末尾后绕回数组开头去用那些空格子。

**怎么工作**（容量 8 的数组，`head` 是队头下标，`size` 是元素个数）：

```
下标:    0   1   2   3   4   5   6   7
内容:   [ ] [ ] [C] [D] [E] [ ] [ ] [ ]      head=2, size=3   队列是 C D E
push F, G, H, I, J：
下标:    0   1   2   3   4   5   6   7
内容:   [I] [J] [C] [D] [E] [F] [G] [H]      head=2, size=8（满）
                                              I 和 J 绕回了开头
```

第 k 个元素（从队头数起，k 从 0 开始）放在 `(head + k) % 容量`。队尾的下一个空位就是 `(head + size) % 容量`。
当容量是 **2 的幂**（8、16、32……），`% 容量` 可以换成 `& (容量 - 1)`（按位与），因为 `x % 8 == x & 7`。位运算比取模快，面试里顺口提一句很加分。

**满了怎么办**：开一个两倍大的新数组，**按逻辑顺序**（从 head 开始，绕回去）把元素抄过去，`head` 归零。
抄的时候要分两段：先抄 `head..末尾`，再抄 `0..head-1`。这一步是常见 bug（见第 8 节）。

**Java 里怎么写**：

```java
long[] buf = new long[16];
int head = 0, size = 0;
void push(long x) {
    if (size == buf.length) grow();
    buf[(head + size) & (buf.length - 1)] = x;
    size++;
}
long pop() {
    long x = buf[head];
    head = (head + 1) & (buf.length - 1);
    size--;
    return x;
}
```

**为什么不用 `ArrayDeque<Long>` 或 `LinkedList<Long>`**：`Long` 是对象，`ArrayDeque<Long>` 里存的是指向对象的引用，每个数是堆上一个单独的小对象（**装箱**，boxing）。
CPU 读数据时要先读引用，再跳到别处读那个对象，叫「指针追逐」。`long[]` 里数据是连续的，CPU 会一口气把相邻数据预取进缓存（cache），快得多。
工作中没有性能要求时，`ArrayDeque` 完全够用，少写代码；面试里说清楚取舍即可。

### 2.2 复杂度、O(1) 与「均摊」（amortized）

**是什么**：复杂度描述「输入变大时，操作要多久」。`O(1)` 表示和 n 无关；`O(n)` 表示和元素个数成正比；`O(log n)` 表示 n 翻倍只多做一步。

**均摊 O(1)**：环形缓冲偶尔扩容要抄 n 个数，这一次是 `O(n)`；但扩容后容量翻倍，要再 push n 次才会下一次扩容。把一次昂贵操作的成本平摊到之前 n 次便宜操作上，平均每次 `O(1)`。这叫均摊。

**为什么重要**：第 3 节的朴素解每次 `get_mean` 是 `O(n)`；100 万次操作 × 2 万元素 = 200 亿步。

### 2.3 浮点数（`double`）为什么会错

**是什么**：`double` 用 64 位表示小数：1 位符号、11 位指数、**52 位尾数**。有效数字大约只有 15–16 位十进制（53 个二进制位）。

**为什么需要懂**：很多人以为 `double` 是「更大的 long」。不是。它能表示很大的数，但**相邻两个能表示的数之间有空隙**，数越大空隙越大。
`10^16` 附近相邻的 `double` 间隔是 2。所以 `1e16 + 1` 的精确结果 `10000000000000001` 表示不出来，只能舍入到相邻的 `1e16` 或 `1e16 + 2`，按规则（四舍五入到偶数）得到 `1e16`。**加的 1 消失了。**

**怎么工作**（演示加了又减）：

```
s = 0.0
s += 1e16   →  1e16
s += 1      →  1e16      （1 被吃掉）
s += 1      →  1e16      （又被吃掉）
s -= 1e16   →  0.0       （正确答案应该是 2）
```

队列里就是这个场景：先 push 一个巨大的数，再 push 两个小数，然后 pop 掉巨大的数——剩下的两个小数的和应该是 2，用 `double` 维护总和得到 0。
这叫**灾难性抵消**（catastrophic cancellation）。解决办法不是「用更好的 double」，而是**别用浮点数存总和**，用整数。

**Java 里**：`double s = 0; s += 1e16; s += 1; s += 1; s -= 1e16;` → `s == 0.0`。（我在本机跑过。）

### 2.4 整数溢出、补码与 128 位累加器

**是什么**：`long` 是 64 位有符号整数，范围 `-2^63 .. 2^63-1`，即 `-9223372036854775808 .. 9223372036854775807`。超出范围时 Java **不报错**，而是「绕回去」：
`Long.MAX_VALUE + 1 == Long.MIN_VALUE`。这叫溢出（overflow）。

**为什么需要处理**：队列里两个 `Long.MAX_VALUE`，和是 `2^64 - 2`，`long` 里存成 `-2`。平均数变成负的——**悄悄错了**，没有任何异常。

**补码**（two's complement）：计算机用补码表示负数：64 位里最高位是符号位，`-1` 是全 1。加法对补码来说和无符号加法是同一个电路，这就是为什么溢出是「绕回」。

**怎么办**：用两个 `long` 拼成一个 128 位整数：`hi`（高 64 位，有符号）和 `lo`（低 64 位，**当无符号数看**）。加一个 `long x`：

```
lo' = lo + x                           （64 位加法，可能绕回）
carry = lo' 比 lo 还小（按无符号比）? 1 : 0   （绕回了就说明向高位进了 1）
hi' = hi + (x 的符号扩展) + carry
```

`x >> 63`（算术右移）：`x` 非负得 0，负数得 -1（全 1）——这是把 64 位 `x` 扩展成 128 位时高 64 位的值。

演示 `MAX + MAX + MAX`（`MAX = 2^63 - 1`）：

```
初始            hi=0, lo=0
+MAX            lo = 2^63-1        hi=0
+MAX            lo = 2^64-2        hi=0     （无符号看 lo 是 2^64-2，没有绕回）
+MAX            lo = (2^64-2)+(2^63-1) = 2^64+2^63-3，绕回成 2^63-3；
                lo' < lo（无符号）→ carry=1 → hi=1
结果 = 1·2^64 + (2^63-3) = 3·(2^63-1)   ✓
```

（我用 Python 验证过：`3 * (2**63 - 1) == 27670116110564327421`，与 `hi*2^64 + lo` 一致。）

**够用吗**：n 个 `long` 之和的绝对值 ≤ n·2^63。队列元素最多 2^31 个，所以和 < 2^94，128 位（范围约 ±2^127）永远放得下。

**Java 里**：`Long.compareUnsigned(a, b)` 按无符号比大小；`Math.addExact(a, b)` 溢出时抛异常（只想「报错」而不是「算对」时用）。

### 2.5 分数与最大公约数（gcd）

**是什么**：平均数 = 总和 / 个数，是一个分数。`6/4` 和 `3/2` 是同一个数，我们约分成最简形式，规定分母恒为正。

**为什么需要**：要比较两个均值是否相等，或要「精确」地给出均值，就不能先除成 `double`。用约分后的分数（`BigInteger` 分子 + `long` 分母）可以精确相等比较，`record` 的 `equals` 自带。

**怎么工作**：`g = gcd(分子, 分母)`，分子分母都除以 g。分子为 0 时 `gcd(0, d) = d`，得到 `0/1`，也是规范形式。

**Java 里**：`BigInteger.gcd`。`BigInteger` 是任意精度整数，不会溢出，但每次运算都要在堆上分配新对象，所以只在**取答案**时用，不在每次 push/pop 里用。

**转成 `double`**：什么时候一次 `a / b` 就是「正确舍入」的？当 `a` 和 `b` 都能被 `double` 精确表示（绝对值 ≤ 2^53）时，IEEE 754 规定除法结果是「精确商舍入到最近」，所以最近的 `double` 就是 `(double)a / b`。
否则先用 `BigDecimal` 做高精度除法再取 `doubleValue()`（会有极小概率的「二次舍入」偏差，在本题的测试中不会出现，面试时提一句即可）。

### 2.6 持久化数据结构（persistent data structure）与「版本」

**是什么**：普通数据结构一改就丢了旧状态。**持久化**数据结构每次修改都生成一个**新版本**，旧版本仍然可读可用。

**为什么需要**：Part 3 要求「保留每个历史版本，随时查任意版本的均值，并从旧版本分叉」。最笨的办法是每个版本复制一份数据：
n 个版本、每份长度 n，总共 `O(n²)` 的时间和空间（本机实测，复制 2 万个版本要 168 ms，而且按平方增长）。

**怎么工作**：让新旧版本**共享**没变的部分，只新建变了的那一点点。最简单的例子是链表：

```
版本 A:  1 → 2 → 3
版本 B = 在 A 前面加 0：   0 → (A 的 1 → 2 → 3)    只新建了一个节点 "0"，后面全部共享
```

队列有「队尾 push、队头 pop」两头变化，不能直接用链表。下面第 4 节会推导出一种用**树**的办法。

**树与父指针**：树是每个节点有一个「父节点」的结构（根没有父）。我们只存「每个节点的父」（父指针），从任何节点沿着父指针往上走，就能走到根，这条路径是唯一的。
多个节点可以有同一个父——这就是「分叉」。

### 2.7 祖先查询（level ancestor）与跳跃指针（jump pointer）

**是什么**：给定树上节点 `v` 和深度 `d`，求 `v` 在深度 `d` 的祖先。深度 = 到根的步数，根深度 0。

**为什么需要**：第 4 节会看到，Part 3 的 `pop` 需要找「队头元素」，它正好是某个节点的「深度为 d 的祖先」。

**朴素做法**：沿父指针一步一步往上走，`O(深度)`。队列长了就慢。

**怎么加速**：每个节点除了存父指针，再多存一个「跳跃指针」`jump`，指向一个更高的祖先。要找深度 `d` 的祖先时：
能跳（跳完深度仍 ≥ d）就跳，不能跳就走一步父指针。关键是 `jump` 怎么选，才能保证总步数是 `O(log n)`。有一个漂亮的规则（Eugene Myers 1983，叫 skew-binary 跳跃指针）：

```
新节点 n，父 p。令 j = jump[p]。
如果 depth[p] - depth[j] == depth[j] - depth[jump[j]]   （p 的跳跃长度等于 j 的跳跃长度）
    jump[n] = jump[j]        （把两段跳合并成一段更长的）
否则
    jump[n] = p
```

直觉：跳跃的长度按 1、1、3、1、1、3、7……这种「近似 2 的幂减 1」的模式增长，长跳的数量是 `log n` 级别。我用代码算出深度 1..16 的 `jump`（所指祖先的深度）：

```
深度:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
jump:  0  1  0  3  4  3  0  7  8  7 10 11 10  7  0 15
```

演示：从深度 8 的节点找深度 5 的祖先。

```
v=8:  jump[8]=7，深度 7 ≥ 5 → 跳到 7
v=7:  jump[7]=0，深度 0 <  5 → 不能跳，走父指针到 6
v=6:  jump[6]=3，深度 3 <  5 → 不能跳，走父指针到 5
v=5:  深度 5 == 5，找到。 共 3 步（朴素要 3 步，差别在深度大时才显现：深度 16 → 深度 1 只要 7 步，朴素要 15 步）
```

只比朴素多存一个 `int` 每节点，不需要「倍增表」那样的 `n log n` 内存。面试时能说出「binary lifting（倍增）也行，`O(n log n)` 内存；jump pointer 是更省内存的版本」就足够。

### 2.8 线程、可见性与「撕裂读」

**是什么**：Part 4 有两个线程：写者线程在改队列，读者线程在读平均数。每个线程有自己的 CPU 缓存和寄存器，编译器和 CPU 还会为了速度**重排**指令顺序。
所以一个线程写入的值，另一个线程**不一定**马上看得到，甚至可能先看到后面的写入、后看到前面的。

**撕裂读**（torn read）：队列有两个状态量 `sum` 和 `size`。写者先更新 `sum` 再更新 `size`。读者在两次写之间读，拿到「新的 sum + 旧的 size」，算出的均值是个根本不存在过的值。
具体：队列里全是 7，size=3，sum=21，均值 7。写者 push 7：先 `sum=28`，再 `size=4`。读者恰好读到 `sum=28, size=3` → 均值 9.33。这个值从未存在过。

**Java 内存模型（JMM）里的 happens-before**：JMM 规定了一些「A 一定在 B 之前、而且 A 的写入对 B 可见」的规则，叫 happens-before。最常用的：
* 同一个线程里，前面的语句 happens-before 后面的。
* 对一个 `volatile` 变量的写 happens-before 之后对它的读。
* 线程 `start()` happens-before 该线程里的所有动作；线程里的所有动作 happens-before 别人 `join()` 它返回。

**怎么解决撕裂读**：把 `(sum, size)` 打包进一个**不可变对象**（所有字段 `final`，建好就不能改），写者每次修改后 `new` 一个新对象并**一次性发布**一个引用。
读者读到的永远是某个完整的对象，要么旧的要么新的。这叫「不可变对象 + 安全发布」。

**发布的几种写法**（越往下越精细）：
| 写法 | 效果 | 代价 |
|---|---|---|
| `synchronized` 读写都加锁 | 最简单，正确 | 读者要排队；在 JDK 21 里虚拟线程在 `synchronized` 里阻塞会「钉住」（pin）载体线程 |
| `volatile Stat published` | 写后读可见 | 每次写有全序屏障，通常够用 |
| `VarHandle.setRelease` / `getAcquire` | 只保证：release 写之前的所有写入，对 acquire 读到该值的线程可见 | 比 `volatile` 更弱更便宜，也更难推理 |
| `StampedLock.tryOptimisticRead` | 读者不加锁，读完检查 stamp，期间有写就重读 | 读者要写重试循环 |

`VarHandle` 是 Java 9 引入的「对字段做精确内存操作」的句柄，`setRelease` 是 release 语义的写，`getAcquire` 是 acquire 语义的读。配对使用就建立了 happens-before：
写者在 `setRelease` 之前做的一切（包括构造 `Stat` 对象的字段初始化），读者 `getAcquire` 读到这个引用之后都看得到。

### 2.9 虚拟线程（一句话，细节见基础课）

虚拟线程（virtual thread，JDK 21 正式）是由 JVM 调度的轻量线程，一个 JVM 可以同时开几十万个；它们跑在少量「载体线程」（carrier thread，数量 = CPU 核数）上。
虚拟线程阻塞（睡眠、等队列）时会让出载体线程。**但纯自旋（`while (!flag) {}`）永远不让出**，如果自旋的虚拟线程数 ≥ 载体线程数，其他虚拟线程（比如本题的写者）就饿死。
这是我在写本题测试时**真的踩到**的坑（读者自旋，写者一直拿不到 CPU，测试挂住），解决办法是自旋里加 `Thread.yield()`。
基础概念的完整讲义计划放在 `study/00-foundations/`（线程 vs 虚拟线程）。

---

## 3. 从最笨的解法开始

```java
// 最笨：用 ArrayDeque<Long>，get_mean 每次遍历求和
class NaiveQueueMean {
    private final ArrayDeque<Long> q = new ArrayDeque<>();
    void push(long x) { q.addLast(x); }
    long pop() { return q.removeFirst(); }
    double getMean() {
        double s = 0;
        for (long x : q) s += x;
        return s / q.size();
    }
}
```

**对吗**：小数据对。**复杂度**：`push/pop` 是 `O(1)`，`getMean` 是 `O(n)`（n = 当前队列长度）。

**具体在哪个输入上慢**：队列长度 2 万，每两次 push 求一次均值，共 20 万次 push：约 10 万次 `getMean` × 2 万次加法 = 20 亿次加法。本机实测 **2604 ms**（同样的操作序列，下面改进后的 `QueueMean` 只要 **3 ms**）。

**具体在哪个输入上错**：

* 巨大的数和小数混在一起：`push(10^16), push(1), push(1)` 之后 `pop()`，剩两个 1，均值应为 1。`double` 求和：`10^16 + 1 + 1` 先被吃成 `10^16`；
  如果是「维护总和」的优化版本，减掉 `10^16` 后得 0，均值 0。（遍历版是从头加，剩下 `1+1=2` 是对的，但一旦我们为了加速改成维护总和就错了——见第 4 节。）
* 两个 `Long.MAX_VALUE`：遍历版用 `double` 累加不会溢出，但如果有人用 `long` 累加就变成负数。

---

## 4. 一步一步改进

### 步骤 1：维护「总和」，均值变 O(1)

**发现问题**：`getMean` 每次重新加一遍。
**想法**：总和 `sum` 和个数 `size` 是两个数，`push` 时 `sum += x; size++`，`pop` 时 `sum -= x; size--`，`getMean` 就是 `sum / size`。
**为什么能解决**：均值只依赖总和和个数，而这两个量可以增量更新。
**新复杂度**：三个操作都 `O(1)`。
**新问题**：如果 `sum` 是 `double`，第 2.3 节的漂移出现了。

### 步骤 2：总和用整数，不用浮点数

**发现问题**：`double` 的 `sum` 在加减大小悬殊的数时丢精度。
**想法**：`sum` 用 `long`。整数加减是**精确**的，不存在「吃掉小数」。
**新问题**：`long` 溢出（第 2.4 节）。`push(MAX), push(MAX)` 后 `sum = -2`。

### 步骤 3：128 位总和

**发现问题**：`long` 总和溢出会悄悄给出错答案。
**想法**：用 `hi/lo` 两个 `long` 的 128 位累加器（第 2.4 节）。
**为什么能解决**：n ≤ 2^31 个 `long` 之和绝对值 < 2^94，128 位装得下，永不溢出。
**代码变化**（`QueueMean.push` 的更新部分）：

```java
long l = lo + x;
hi += (x >> 63) + (Long.compareUnsigned(l, lo) < 0 ? 1 : 0);
lo = l;
```

**为什么不用 `BigInteger`**：能用，但每次 push/pop 都要分配新对象。128 位用两个 `long` 字段，零分配。
也可以折中：平时用 `long`，`Math.addExact` 溢出时才转 `BigInteger`；缺点是要写「转回来」的逻辑，不然一旦转了就永远慢。

### 步骤 4：数据存储从 `ArrayDeque<Long>` 换成 `long[]` 环形缓冲

**发现问题**：`ArrayDeque<Long>` 每个元素一个对象（装箱），内存多、指针追逐、GC 压力。
**想法**：`long[]` 环形缓冲（第 2.1 节）。
**新复杂度**：仍是均摊 `O(1)`，常数小很多，内存连续。

### 步骤 5：返回「精确」均值

**发现问题**：`getMean()` 返回 `double` 本身就是舍入过的。面试官问「能不能给精确值？」
**想法**：返回分数 `Mean(numerator, denominator)`，约分；再提供 `toDouble()` 得到最接近的 `double`。
**代码变化**：`record Mean(BigInteger numerator, long denominator)`，紧凑构造器里做 gcd 约分。
**快路径**：绝大多数时候总和在 ±2^53 以内，这时 `(double) lo / size` 已经是正确舍入，不用分配 `BigInteger`。

到这里 Part 1 结束。

### 步骤 6（Part 2）：把「操作序列」做成数据

**发现问题**：题目 (reconstructed) 给的是一串事件：push、pop、query、以及「修正快照」。一堆 `if (cmd.equals("push"))` 容易漏、容易写错。
**想法**：把每种事件建成一个类型，用 `sealed interface Event` 限定只有这四种；处理时用模式匹配 `switch`，编译器会检查你有没有漏掉某种事件。
**修正快照的实现**：它的语义是「丢掉此前整段历史，队列内容就是快照给的列表」。最简单的实现：`q = new QueueMean()`，把列表逐个 push 进去。
**新复杂度**：每个事件 `O(1)`，快照 `O(快照长度)`；总共 `O(输入总大小)`，这是下界（至少要读完输入）。
**健壮性**：文本解析时每种错误（缺参数、不是数字、数字超出 `long`、未知命令）都给出**行号**。`Long.parseLong` 的 `NumberFormatException` 是 `IllegalArgumentException` 的子类，所以一个 `catch` 能同时处理两类，再统一加上 `"line k: "` 前缀。

### 步骤 7（Part 3）：版本化 —— 从复制到共享

**发现问题**：Part 3 要「任何历史版本都能查、能分叉」。
**最笨**：每个版本复制整份内容：`O(n)` 每版本，n 个版本 `O(n²)`（2 万版本实测 168 ms，按平方外推，30 万版本约 37 秒，必超时）。

**改进 A：观察队列的内容是什么**。队列的内容 = 「按顺序 push 进来的元素」去掉最前面已经 pop 的若干个。也就是说，队列 = 一条 push 序列的**一段后缀**（再去掉前缀）。
如果两个版本的 push 序列有公共前缀，那前缀完全可以共享。

**改进 B：把所有 push 过的元素放进一棵树**。每次 `push(version, x)` 新建一个节点：值是 `x`，父亲是这个版本的「队尾节点」。
从根走到某个节点的路径，就是一条 push 序列。从同一个版本 push 两次不同的值，就是同一个节点的两个孩子——**分叉**。

一个版本用三个数描述：
* `tail`：队尾节点；
* `headDepth`：已经弹出了多少个（队头在路径上的深度 = `headDepth + 1`）；
* `sum`：当前队列内容的和（128 位）。

```
push 1, push 2, push 3, pop, push 9 的过程（树 + 版本）

根(0) ─ 1 ─ 2 ─ 3 ─ 9            节点 9 是 push(v4, 9) 新建的，父亲是 3
                                  版本 v3 = (tail=节点3, headDepth=0, sum=6)   队列 [1,2,3]
pop(v3)  → 版本 v4 = (tail=3, headDepth=1, sum=6-1=5)     队列 [2,3]
push(v4, 9) → 新节点 9，父亲是 3 → v5 = (tail=9, headDepth=1, sum=5+9=14)  队列 [2,3,9]
```

**push**：新建一个节点，`sum += x`，`O(1)`。
**mean / size**：`size = depth[tail] - headDepth`，均值 = `sum / size`，`O(1)`。
**pop**：需要知道被弹出的值是多少才能 `sum -= 值`。被弹出的是路径上深度 `headDepth + 1` 的那个节点——正是 **level ancestor** 问题（第 2.7 节）。
朴素走父指针 `O(队列长度)`；用跳跃指针 `O(log n)`。

**新复杂度**：`push` `O(1)`，`mean` `O(1)`，`pop` `O(log n)`，每版本只存三个数，每节点存 4 个原始值（值、父、跳跃、深度）。没有任何复制。

> 为什么不是「银行家队列」（两个栈实现队列，函数式语言里常见）？它的 pop 是**均摊** `O(1)`，但在持久化场景下，同一个旧版本被反复 pop，那次昂贵的「翻转」会被反复触发，均摊论证失效，最坏 `O(n)`。这是一个很好的面试追问点（Okasaki 的书专门讲了）。

**代价**：节点只增不减，永远不回收。要回收就需要引用计数或限制「只保留最近 K 个版本」。

### 步骤 8（Part 4）：并发读 —— 从撕裂到一致

**发现问题**：写者线程不停 push/pop，监控线程想随时读均值。

**尝试 1：直接读 `QueueMean.getMean()`**。`QueueMean` 不是线程安全的：读者可能读到写了一半的 `hi/lo/size`，甚至 `hi` 和 `lo` 之间撕裂。数据竞争，结果未定义。

**尝试 2：整个类加 `synchronized`**。正确，但读者和写者互相阻塞；JDK 21 里虚拟线程在 `synchronized` 内阻塞会钉住载体线程。读多写少时浪费。

**尝试 3：`volatile long sum; volatile int size;`**。每个字段单独看是可见的，但两个字段**分别**读写，读者在两次读之间可能插进写者的更新：撕裂读（第 2.8 节演示）。

**尝试 4（我们的做法）：不可变快照 + 一次发布**：

```java
record Stat(long seq, int size, I128 sum) {}   // 全部 final，建好不变
Stat published;                                // 只通过 VarHandle 访问

// 写者
queue.push(x);
PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum()));

// 读者
Stat st = (Stat) PUBLISHED.getAcquire(this);   // 拿到一个完整的 Stat
```

**为什么正确**：`Stat` 是不可变的；`setRelease` 保证"构造 Stat 的所有写入"先于"引用被别人看到"；`getAcquire` 读到引用就能看到那些写入。读者要么看到旧 Stat 要么看到新 Stat，永远看不到半新半旧。
`seq` 每次 +1，所以同一个读者连续读到的 `seq` 不会倒退（读到旧值后不可能再读到更旧的值，这是 acquire/release 对同一变量的一致性保证）。

**代价**：写者每次分配一个 `Stat`（几十字节）。若写者每秒百万次，可以改为"每 N 次或每 1ms 发布一次"。

**单写者的强制**：`push/pop` 里用 `compareAndSet` 抢占 `owner`，别的线程写就抛 `IllegalStateException`。`compareAndSet` 是原子的"如果当前是 null 就设成我"，同一时刻只有一个线程成功。

---

## 5. 逐段讲参考解

文件在 `loop/rounds/01_video/hc04_queue_mean_snapshot/reference/`。

### 5.1 `QueueMean.I128`

```java
public record I128(long hi, long lo) {
    public I128 plus(long x) {
        long l = lo + x;
        long carry = Long.compareUnsigned(l, lo) < 0 ? 1 : 0;
        return new I128(hi + (x >> 63) + carry, l);
    }
    public I128 minus(long x) {
        long l = lo - x;
        long borrow = Long.compareUnsigned(lo, x) < 0 ? 1 : 0;
        return new I128(hi - (x >> 63) - borrow, l);
    }
    ...
}
```

* `record` 自动有构造器、访问器 `hi()`/`lo()`、`equals`/`hashCode`/`toString`。
* `plus`：见 2.4。`minus` 类似：低位减不够借位（`lo` 比 `x` 小，按无符号比），高位少 1。注意 `x >> 63` 对负数是 -1，所以 `hi - (-1)` 就是 `hi + 1`——符号扩展自动处理了负数。
* 为什么不写 `plus(-x)` 实现 `minus`：`x == Long.MIN_VALUE` 时 `-x` 还是 `Long.MIN_VALUE`（溢出），错。
* `toBigInteger()`：`hi` 有符号、`lo` 当无符号。`BigInteger.valueOf(lo)` 会把它当有符号，`lo < 0` 时要加 `2^64` 补回来。

### 5.2 `QueueMean.Mean`

```java
public record Mean(BigInteger numerator, long denominator) {
    public Mean {
        if (denominator <= 0) throw new IllegalArgumentException(...);
        BigInteger g = numerator.gcd(BigInteger.valueOf(denominator));
        if (g.signum() != 0 && !g.equals(BigInteger.ONE)) {
            numerator = numerator.divide(g);
            denominator /= g.longValueExact();
        }
    }
```

**紧凑构造器**（compact constructor）：没有参数列表，直接用参数名；在结尾处编译器自动把（可能被你重新赋值过的）参数赋给字段。所以这里**重新赋值参数**就是约分。
这样不管谁 `new Mean(6, 4)`，得到的都是 `3/2`——record 的 `equals` 才有意义。

### 5.3 `QueueMean` 本体

```java
private long[] buf = new long[16];  // 容量恒为 2 的幂
private int head, size;
private long hi, lo;

public void push(long x) {
    if (size == buf.length) grow();
    buf[(head + size) & (buf.length - 1)] = x;
    size++;
    long l = lo + x;
    hi += (x >> 63) + (Long.compareUnsigned(l, lo) < 0 ? 1 : 0);
    lo = l;
}
```

push 的两件事：把值放进环形缓冲，更新 128 位总和。`pop` 对称：读 `buf[head]`，`head` 前进，总和减去它。

`getMean()` 的快路径：

```java
if (hi == (lo >> 63) && lo >= -(1L << 53) && lo <= (1L << 53)) return (double) lo / size;
return mean().toDouble();
```

`hi == (lo >> 63)` 表示 128 位的值其实能装进一个 `long`（高 64 位只是 `lo` 的符号扩展）。再加上绝对值 ≤ 2^53，分子能精确表示成 `double`；`size` 是 `int`，也能。一次除法 = 正确舍入。否则走慢路径。

`grow()`：

```java
long[] bigger = new long[Math.multiplyExact(buf.length, 2)];
int firstPart = buf.length - head;
System.arraycopy(buf, head, bigger, 0, firstPart);   // head..末尾
System.arraycopy(buf, 0, bigger, firstPart, head);   // 绕回来的 0..head-1
buf = bigger; head = 0;
```

扩容必须按**逻辑顺序**抄，并且把 `head` 复位到 0。用 `Math.multiplyExact` 是为了容量翻倍溢出时抛异常而不是变成负数。

### 5.4 `QueueEvents`

```java
public sealed interface Event permits Push, Pop, Query, Correct {}
public record Correct(List<Long> contents) implements Event {
    public Correct { contents = List.copyOf(contents); }
}
...
switch (e) {
    case Push(var v) -> q.push(v);
    case Pop _ -> q.pop();
    case Query _ -> out.add(q.isEmpty() ? new Empty() : new Value(q.mean()));
    case Correct(var contents) -> { q = new QueueMean(); for (long v : contents) q.push(v); }
}
```

* `sealed ... permits`：只有这四个类能实现 `Event`。`switch` 因此可以**穷尽**：没有 `default` 也能通过编译；将来加第五种事件，这个 `switch` 立刻编译报错，提醒你补处理。
* `List.copyOf` 做**防御性拷贝**并且拒绝 `null` 元素（抛 NPE）。没有它，调用者之后改了原列表，历史就被悄悄改写了。
* `Correct` 里 `for (long v : contents)` 会把 `Long` 拆箱成 `long`。

渲染用嵌套的 record 模式：

```java
case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();
case Value(QueueMean.Mean(var n, var d))              -> n + "/" + d;
case Empty _                                           -> "empty";
```

一行里拆开 `Value` 再拆开里面的 `Mean`；`when d == 1` 是守卫条件。第一个分支不匹配（`d != 1`）就落到第二个。

### 5.5 `VersionedQueue`

数据全部放在原始类型数组里（"数组的结构体"，SoA）：节点用 `val/parent/jump/depth` 四个数组，版本用 `vTail/vHeadDepth/vHi/vLo` 四个数组。好处：没有每节点一个对象，内存紧凑，GC 压力小。

```java
public int push(int version, long x) {
    check(version);
    int node = newNode(vTail[version], x);
    var sum = new QueueMean.I128(vHi[version], vLo[version]).plus(x);
    return newVersion(node, vHeadDepth[version], sum);
}
public int pop(int version) {
    check(version);
    if (size(version) == 0) throw new NoSuchElementException(...);
    int h = vHeadDepth[version] + 1;
    long front = val[levelAncestor(vTail[version], h)];
    var sum = new QueueMean.I128(vHi[version], vLo[version]).minus(front);
    return newVersion(vTail[version], h, sum);
}
```

* `newNode` 里计算跳跃指针，规则见 2.7。节点 0 是**哨兵根**（`parent[0]=jump[0]=0`，深度 0），空队列版本 `EMPTY = 0` 的 `tail` 就是它。
* `levelAncestor(v, d)`：`while (depth[v] > d) v = depth[jump[v]] >= d ? jump[v] : parent[v];`——能跳就跳，否则走一步。
* `correct(contents)`：从根开始连续 `newNode`，产生一条独立的链，`headDepth = 0`。注意它**不**依赖任何旧版本，所以修正快照不影响旧历史。
* 数组满了用 `Arrays.copyOf` 翻倍（均摊 `O(1)`）。
* `check(version)`：未知版本号抛 `IllegalArgumentException`，而不是数组越界——把"调用者错误"和"程序 bug"分开。

### 5.6 `SharedMean`

```java
private static final VarHandle PUBLISHED;  // 指向字段 published
...
public Stat read() { return (Stat) PUBLISHED.getAcquire(this); }
private void publish() { PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum())); }
private void claimWriter() {
    Thread me = Thread.currentThread();
    Thread cur = (Thread) OWNER.getAcquire(this);
    if (cur == me) return;
    if (cur != null || !OWNER.compareAndSet(this, null, me)) throw new IllegalStateException(...);
}
```

* `queue`、`seq` 只有写者线程碰，不需要任何同步。
* 字段 `published` 是**普通字段**（不是 `volatile`），只通过 `VarHandle` 访问，目的是只付 release/acquire 的代价。
* 构造出的 `Stat` 里的字段是 `final`（record），所以 JMM 还额外保证 final 字段的安全发布。
* `compareAndSet(this, null, me)`：原子地"如果 `owner` 是 `null` 就设成 `me`"，返回是否成功。两个线程同时第一次写，只有一个成功，另一个抛异常。

---

## 6. Java 21 特性小课

课本（计划）：`study/10-java21/J01_*.md` 等。这里只讲本题用到的部分。

### J01 `record`（Java 16）

旧写法（Java 8）：一个有两个字段的值类要写字段、构造器、getter、`equals`、`hashCode`、`toString` ≈ 40 行，而且 `equals` 容易漏字段。
新写法：`record Mean(BigInteger numerator, long denominator) {}`，一行全有。`record` 是不可变的（字段 `final`）、不能继承别的类。
**紧凑构造器**让你在构造时校验/规范化参数。**不该用**：需要可变状态、需要继承时。

### J02 `sealed` 接口（Java 17）

旧写法：`interface Event {}`，谁都能实现，`switch` 里永远要 `default`。
新写法：`sealed interface Event permits Push, Pop, Query, Correct {}`，实现者被限定。编译器因此知道"所有可能"，`switch` 可以检查穷尽性。

### J03 `switch` 模式匹配（Java 21）与 J04 record 模式

旧写法：`if (e instanceof Push) { Push p = (Push) e; ... } else if ...`。
新写法见 5.4：`case Push(var v) -> ...`，类型测试 + 强转 + 拆字段一步完成。`when` 守卫写附加条件。
**什么时候不该用**：只有两三种情况且不会增加时，普通 `if` 更直白。

### J05 `switch` 表达式与 `yield`（Java 14）

`events.add(switch (t[0]) { case "push" -> { ...; yield new Push(...); } case "pop" -> ...; default -> throw ...; })`。
`switch` 本身是一个有值的表达式；分支是代码块时用 `yield` 返回值；没有 fallthrough（旧 `case` 忘了 `break` 会"掉进"下一个）。

### J13 未命名模式 `_`（Java 21 预览，需要 `--enable-preview`）

`case Pop _ ->`、`catch (InterruptedException _)`：用 `_` 明说"这个变量我不用"，比起起一个没用的名字，读代码的人不会去找它在哪用了。
预览特性：语法在未来版本可能变，所以只在学习/练习中用。

### J16 `VarHandle`（Java 9）

旧写法：只有 `volatile`（全序，最强也最贵）或 `AtomicReference`（多一层对象）。
新写法：对任意字段拿一个 `VarHandle`，可以选内存序：`getAcquire/setRelease`、`compareAndSet`、`getVolatile` 等。
**不该用**：你说不清楚为什么需要比 `volatile` 更弱的序时，用 `volatile`。这是"榨最后一点性能"的工具，错了很难 debug。

### J10 虚拟线程（Java 21）

测试里 `Executors.newVirtualThreadPerTaskExecutor()` 给每个任务一个虚拟线程。注意第 2.9 节的饥饿陷阱。

---

## 7. 追问预演

**Q1：为什么不用 `ArrayDeque<Long>`？**
* 思考：先承认它也是环形数组，`O(1)`；差异在常数。
* 要点：装箱（每元素一个 `Long` 对象，16–24 字节 + 8 字节引用）、指针追逐、GC 压力；`long[]` 连续内存、缓存友好。
* 可以说："两者复杂度一样。我用 `long[]` 是为了避免装箱和提升缓存局部性；如果没有性能要求，我会直接用 `ArrayDeque`。"

**Q2：`get_mean` 返回 `double`，精度不够怎么办？**
* 思考：精度问题有两个来源——维护总和时的累积误差、最后除法的舍入。
* 要点：总和用整数（精确），最后一步才可能舍入；需要时返回约分分数。`getMean` 保证最近的 `double`。
* 说法："累积误差靠整数总和消除；最后一次除法的舍入我能保证最近 double，因为分子分母都能精确表示时 IEEE 除法本身就是正确舍入的。"

**Q3：128 位够吗？**
* 思考：算上界。n 个 `long` 之和的绝对值 ≤ n·2^63；n ≤ 2^31（Java 数组长度上限）→ < 2^94 < 2^127。
* 要点：给出上界推导；若要任意多元素就用 `BigInteger`。

**Q4：快照怎么存？一定要复制吗？**
* 思考：先说最笨的 O(n)/版本，再问"版本之间有没有共享"。
* 要点：队列内容 = push 序列的一段；push 序列组成树，版本 = (尾节点, 弹出数, 和)，push `O(1)`，pop 找队头需要 level ancestor `O(log n)`。
* 可以补一句："银行家队列在持久化场景下均摊失效。"

**Q5：多个线程读怎么保证一致？**
* 思考：先问"读者要的是什么一致"——这里是 `(sum, size)` 一起。再想"能不能把它们变成一个值"。
* 要点：不可变快照 + 一次发布（release/acquire 或 `volatile`）；对比 `synchronized`、`ReadWriteLock`、`StampedLock` 乐观读。
* 说法："我把状态打成一个不可变对象，写者原子地换引用。读者永远看到完整的某个时刻。"

**Q6：写者也有多个呢？**
* 要点：串行化（把写入投递到一个单线程执行器）；或者 `AtomicReference<Stat>` + CAS 循环：读当前 Stat，算新 Stat，`compareAndSet`，失败重试。但"队列"的 FIFO 语义要求 push/pop 之间有顺序，要先问清楚语义。

**Q7：C++ 怎么写？**（原题是 C++ 面试）
* 要点：`std::vector<int64_t>` 或 `std::deque`；总和用 `__int128`（GCC/Clang 扩展）；均值 `long double` 或自己做分数；并发发布用 `std::atomic<std::shared_ptr<const Stat>>`（C++20）。

---

## 8. 常见误区

1. **用 `double` 存总和。**
   * 错在哪：加减大小悬殊的数丢精度（第 2.3 节），而且错误是**静默**的。
   * 对应测试：`noFloatDriftFromARunningDoubleSum`。
   * 正确：总和用整数。

2. **用 `long` 存总和，以为"题目的数不会那么大"。**
   * 错在哪：`Long.MAX_VALUE` 是合法输入；溢出后均值变负，无异常。
   * 对应测试：`sumOverflowingLongIsExact`。
   * 正确：128 位，或 `Math.addExact` 至少报错（但"报错"不等于"算对"，要和面试官确认期望）。

3. **环形缓冲扩容时 `Arrays.copyOf(buf, 2 * n)`。**
   * 错在哪：`head` 不在 0 时，元素的逻辑顺序被打乱——队头之前绕回的部分排到了错误的位置。
   * 对应测试：`ringBufferWrapsAndGrowsInFifoOrder`（专门让 head 停在 10 再扩容）。
   * 正确：分两段 `arraycopy`，`head` 归零。

4. **`Mean` 没约分，或分母可以为负。**
   * 错在哪：`6/4 != 3/2`，`3/-2 != -3/2`，record 的 `equals` 判不相等。
   * 对应测试：`meanIsReducedFractionWithPositiveDenominator`。

5. **`Correct(List)` 直接存传入的列表引用。**
   * 错在哪：调用者之后 `add` 一个元素，事件的内容变了。
   * 对应测试：`correctEventCopiesItsContents`。
   * 正确：`List.copyOf`。

6. **版本化时每个版本 `new long[]` 复制。**
   * 错在哪：O(n²)。对应测试 `deepChainsAndWideBranchingUnderTwoSeconds`（30 万深度链 + 20 万随机分叉）。

7. **并发读时用两个 `volatile` 字段。**
   * 错在哪：每个字段单独可见，但两个字段的组合不原子，撕裂读（第 2.8 节）。
   * 对应测试：`readersAlwaysSeeAConsistentMean`（全 7 的不变量：均值必须恰好是 7）。

8. **测试里用纯自旋的读者跑在虚拟线程上，写者被饿死，测试挂住。**
   * 这是我写本题时真实遇到的。解决：自旋循环里 `Thread.yield()`，或读者用平台线程。

---

## 9. 自测题

**1.（概念）** 为什么环形缓冲的容量选 2 的幂？
<details><summary>答案</summary>
可以用 `& (容量-1)` 代替 `% 容量`，位与比取模快；并且扩容 ×2 自然保持 2 的幂。
</details>

**2.（概念）** `push(10^16), push(1), push(1), pop()` 后，用 `double` 维护的总和是多少？应该是多少？
<details><summary>答案</summary>
`double` 里 `1e16 + 1 = 1e16`（1 被舍掉），再 `+1` 同样，最后减 `1e16` 得 0。正确是 2（剩下 1 和 1）。
</details>

**3.（计算）** 用 `hi/lo` 方案，`lo = 0xFFFF_FFFF_FFFF_FFFF`（无符号最大），`hi = 0`，加 `x = 1`，结果是什么？
<details><summary>答案</summary>
`l = lo + 1 = 0`（绕回）；`compareUnsigned(0, 0xFFFF…F) < 0`，所以 carry = 1；`x >> 63 = 0`；`hi = 0 + 0 + 1 = 1`。结果 `hi=1, lo=0`，即 2^64。
</details>

**4.（设计）** 版本 v 的 `tail` 节点深度是 9，`headDepth` 是 4。队列有几个元素？队头在路径上的深度是多少？
<details><summary>答案</summary>
元素个数 = 9 − 4 = 5；队头是深度 5 的祖先（`headDepth + 1`）。`pop` 之后 `headDepth` 变 5。
</details>

**5.（并发）** 把 `Stat` 的字段改成非 `final` 的普通类（有 setter），并且写者"修改同一个对象再重新发布"，会出什么问题？
<details><summary>答案</summary>
读者可能拿到的是"正在被修改"的同一个对象，读到半新半旧的字段（撕裂读），不可变性的保证就没了。必须每次 `new` 一个新对象。
</details>

**6.（小编程）** 写出不用 `BigInteger`、判断两个 `long` 相加是否溢出的表达式。
<details><summary>答案</summary>
`long r = a + b; boolean overflow = ((a ^ r) & (b ^ r)) < 0;`（两个加数符号相同、而结果符号与它们不同就是溢出）。或者直接 `Math.addExact(a, b)` 捕获 `ArithmeticException`。
</details>

---

## 10. 延伸阅读

* Goldberg, *What Every Computer Scientist Should Know About Floating-Point Arithmetic*（ACM Computing Surveys 1991）——讲清楚 `double` 为什么有空隙、什么是正确舍入。
* Okasaki, *Purely Functional Data Structures*（Cambridge, 1998）第 5 章——持久化队列、摊还分析为什么在持久化下会失效。
* Myers, "An Applicable Random-Access Stack"（Information Processing Letters, 1983）——skew-binary 跳跃指针的出处。
* JLS（Java 语言规范）§17.4 Memory Model——happens-before 的正式定义。
* Doug Lea, "Using JDK 9 Memory Order Modes"——`VarHandle` 的 plain/opaque/acquire-release/volatile 四档，为什么这样分。
* JEP 395（Records）、JEP 409（Sealed Classes）、JEP 441（Pattern Matching for switch）、JEP 440（Record Patterns）、JEP 444（Virtual Threads）——每个特性的设计动机。
* Goetz et al., *Java Concurrency in Practice* 第 3 章（共享对象）与第 16 章（Java 内存模型）——不可变对象与安全发布。
