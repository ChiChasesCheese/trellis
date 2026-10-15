# hc07 · 股票代码哈希表 —— 讲义

> 题面：`loop/rounds/01_video/hc07_ticker_hash_map/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/`（`TickerMap`、`TickerCodec`、`LongTickerMap`、`SymbolIndex`、`FrozenTickerMap`、`OffHeapTickerMap`、`Bench`）
> 写法说明见 `study/TEXTBOOK.md`；样板见 `oa01_job_chain.md`（那一篇 2.2 节有一个简短的 `HashMap` 介绍，这里从头重讲并深入）。
> 这篇讲义的任务：**把哈希表从零讲清楚**——哈希函数、冲突、链地址 vs 开放寻址、装载因子、为什么要 resize、缓存行、装箱的代价——
> 然后看「股票代码」这个特殊结构怎样让通用方案再快几倍、再省几倍内存。**所有性能数字都来自本机的实测（在第 4 节和 REPORT 里），没测过的我会明说。**

---

## 1. 这道题在问什么

行情系统每秒收到几百万条消息，每条都是「某只股票成交了 q 股」。你要维护**每只股票的累计成交量**：

```
收到 (AAPL, 100)  →  AAPL 的总量 += 100
收到 (MSFT, 50)   →  MSFT 的总量 += 50
收到 (AAPL, 30)   →  AAPL 的总量 += 30        （此时 AAPL = 130）
```

需要的操作只有：**按股票代码查、改、增、删一个数**。这就是「键值映射」（map）。Java 里默认答案是 `HashMap<String, Long>`。

面试官的路线（我们按「一小时电面里怎么追问」重构的，**(reconstructed)**）：

1. 「先别用 `HashMap`，自己写一个哈希表。」→ 考你懂不懂原理（Part 1）。
2. 「你知道股票代码最多 8 个大写字母。还能做得更好吗？」→ 考你会不会**利用输入的结构**（Part 2）。
3. 「如果开盘前我就告诉你今天所有的代码呢？」→ 考你知不知道**完美哈希**（Part 3）。
4. 「你怎么知道更快？内存呢？缓存呢？」→ 考你会不会**测量**（Part 4）。

### 手算一遍（这张小表贯穿整篇讲义）

假设我们有一个只有 **8 个格子**的数组（编号 0..7）。要放 5 个代码：`AAPL`、`MSFT`、`GOOG`、`AMZN`、`TSLA`。
先别管「怎么算出下标」（第 2.2 节讲），只看结果：假设它们的「家」(home slot) 分别是 `AAPL→3`、`MSFT→6`、`GOOG→2`、`AMZN→3`、`TSLA→7`。

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   AAPL   AMZN   空   MSFT   TSLA
                            ↑      ↑
                    AAPL 先到，占了 3；AMZN 的家也是 3，被占了，往后看 4，空 → 住 4
```

查 `AMZN`：先去它的家 3 → 看到的是 AAPL，不是我 → 往后看 4 → 是 AMZN ✓。
查 `ZZZZ`（不存在）：家假设是 5 → 空 → 立刻知道「不存在」。

这就是**开放寻址 + 线性探测**的全部直觉。后面所有内容都是在回答：怎么算家？撞了怎么办？删除怎么办？满了怎么办？为什么这样排会更快？

---

## 2. 前置知识

### 2.1 为什么需要哈希：数组的下标是「免费」的

**是什么**：数组按下标取值是 O(1)——`a[5]` 直接算出地址（起始地址 + 5 × 元素大小），不用从头数。

**为什么需要哈希**：我们想用「字符串 `AAPL`」当下标，但数组只认整数。

* 如果用 `List<Entry>` 存，查一个代码要从头比较到尾：8000 个代码平均比较 4000 次，每秒几百万条消息 → 每秒几十亿次比较。太慢。
* 如果把代码**变成一个整数**再取余数当下标——`a[变成的整数 % 8]`——就又是 O(1) 了。

「把任意东西变成一个整数」的函数，叫**哈希函数**（hash function）。用哈希函数的结果当下标的数组，叫**哈希表**（hash table）。

### 2.2 哈希函数

**是什么**：一个确定性的函数 `h(key) → 整数`。

**好的哈希函数要满足**：

1. **确定**：同一个 key 永远得到同一个值（否则存进去的找不到）。
2. **相等的 key 必须得到相等的值**：Java 里这就是 `equals` 和 `hashCode` 的契约——两个 `equals` 的对象 `hashCode` 必须相同，反过来不要求。
3. **均匀**：不同的 key 应该尽量**散开**到不同的格子里，别扎堆。
4. **快**：它在最热的路径上，每次查找都要算一遍。

**`String.hashCode()` 怎么算**（Java 的实际算法）：把字符串当成 31 进制的数：

```
hash = s[0]·31^(n-1) + s[1]·31^(n-2) + … + s[n-1]        （int 溢出就自然绕回）
"AAPL" = 65·31³ + 65·31² + 80·31 + 76 = 1936415 + 62465 + 2480 + 76 = 2001436
```

**从 hashCode 到格子编号**（把一个很大的整数缩到 0..容量−1）：

* 取余数：`h % 8`。慢（除法）；而且 `h` 可能是负数，余数也可能是负的。
* **容量取 2 的幂**时：`h & (容量 - 1)`。例如容量 8，`h & 7` 只留最低 3 位。一条与运算就行，比除法快得多，永远非负。这是 `HashMap`、本题所有实现都用 2 的幂容量的原因。

**坑：低位问题**。`h & 7` 只看最低 3 位——也就是只有字符串**最后一两个字符**起作用！看我们的五个代码（hashCode 取自上面的计算）：

```
AAPL  2001436   & 7 = 4
MSFT  2375924   & 7 = 4        ← 撞了
TSLA  2584628   & 7 = 4        ← 撞了
GOOG  2193600   & 7 = 0
AMZN  2013280   & 7 = 0        ← 撞了
```

五个里有三个都想住 4 号格。**真实的 hashCode 低位分布并不均匀**，所以只取低位很危险。解决办法有两类：

* **混合（mix）**：先把高位「搅」进低位。`java.util.HashMap` 的做法是 `h ^ (h >>> 16)`。
* **乘法哈希（multiplicative hashing）/ 斐波那契哈希（Fibonacci hashing）**：乘以一个特殊的奇数常数，然后**取高位**：

```java
(h * 0x9E3779B9) >>> (32 - 位数)       // 0x9E3779B9 ≈ 2^32 / 黄金比例 1.618…
```

乘法让输入的**每一位**都影响乘积的**高位**；取高位就拿到了混合得最好的那几位。对上面五个代码，容量 8（3 位）时得到：`AAPL→3, MSFT→6, GOOG→2, AMZN→3, TSLA→7`——这就是第 1 节小表里的「家」。只剩 AAPL/AMZN 一对撞车，而不是三个扎堆。
选黄金比例是因为它让一串相邻的整数（0, 1, 2, …）乘完之后均匀地散布在整个范围里（数学上叫三距离定理）。本题测试里 17576 个三字母代码（hashCode 近似连续的整数）用它得到的最长探测距离是 0 或 1（本机实测）。

**Java 里怎么写**：本题 Part 1 的 `home(String)`：

```java
private int home(String key) { return (key.hashCode() * 0x9E3779B9) >>> shift; }   // shift = 32 - log2(容量)
```

`>>>` 是**无符号右移**（高位补 0），保证结果非负且正好在 `0..容量-1`。

### 2.3 冲突（collision）：躲不掉的

**是什么**：两个不同的 key 得到同一个格子。

**为什么躲不掉**：鸽巢原理——把 n+1 只鸽子放进 n 个笼子，必有一个笼子有两只。就算 key 数量少于格子数，**生日悖论**也告诉我们冲突来得比直觉早得多：23 个人里就有约一半概率两人同生日（365 天）。
同理，8000 个 ticker 放进 16384 个格子，**几乎一定**有大量冲突。所以哈希表的核心不是「避免冲突」，而是「冲突发生了怎么办」。

两大类办法：

### 2.4 办法一：链地址法（separate chaining）——Java 的 `HashMap`

每个格子（叫**桶**，bucket）是一个链表的头；冲突的 key 串在同一条链上。

```
桶:  0     1     2     3     4   …
     │           │     │
     ▼           ▼     ▼
   [GOOG]      [X]   [AAPL]──▶[AMZN]──▶ null
     │
     ▼
   [AA]──▶ null
```

查 key：算桶号 → 沿链逐个比较。

`java.util.HashMap` 的细节：

* 每个条目是一个 `Node` 对象（hash、key 引用、value 引用、next 引用）——**每个条目一次堆分配**；
* 装载因子默认 0.75：条目数超过「桶数 × 0.75」就把桶数翻倍并重新分配所有 Node；
* Java 8 起，一条链长度 ≥ 8（且桶数 ≥ 64）会变成**红黑树**，防止恶意构造的冲突把查找拖成 O(n)。

**代价**（`HashMap<String, Long>` 存一个 ticker 累计量）：

```
table[桶]  ──▶  Node (32 B)  ──▶  key: String (24 B) ──▶ byte[] (24 B)
                     └────────▶  value: Long (24 B)
```

每个条目背后是 **4 个堆对象**，沿指针一层层跳。在 64 位 HotSpot（默认开压缩指针）下，对象大小：`Node` 32 B、`Long` 24 B、"AAPL" 这样的 `String` 共 48 B（String 对象 24 + 内部 byte[] 24）。
我在本机用 `ThreadMXBean.getThreadAllocatedBytes` 实测了 `new String("AAPL")` = 48 B、`Long.valueOf(1000+i)` = 24 B；预分配好桶数组的 `HashMap<String,Long>` 在 200 万条目时每条（不含 key 对象）约 **64.4 B**。
再加上 key 字符串本身的 48 B，一个条目大约 **110 B**，而它承载的「有用信息」只有 8 字节的 value（和 ≤ 8 字节的 key）。

### 2.5 办法二：开放寻址（open addressing）和线性探测（linear probing）

**是什么**：不另建链表。所有条目直接放在**同一个数组**里；冲突时，在数组里**往后找下一个空格**。线性探测 = 一格一格往后找（到末尾绕回开头）。

**插入**（`put`）：从家出发，往后找到第一个空格放进去。第 1 节的小表就是这样排出来的。
**查找**（`get`）：从家出发，往后看；**碰到目标就找到，碰到空格就确定不存在**（如果它存在，插入时一定会放在碰到空格之前）。
**注意**：这个终止条件要求「表里永远有空格」，否则查找不存在的 key 会无限循环。所以装载因子一定要限制（2.7 节）。

**为什么叫「探测」**：往后看一格叫一次探测（probe）。一个 key 离它的家有多远，就要探测多少次。

**代价：聚集（clustering）**。冲突的 key 占据连续的格子，一片连续被占的格子会像滚雪球一样越长越大——后来的 key 不管家在哪，只要落进这片区域就要走到片尾。
Knuth 给出了线性探测的期望探测次数（装载因子 α = 占用格子数 / 总格子数）：

| α | 查找成功平均探测次数 `(1 + 1/(1−α))/2` | 查找失败平均探测次数 `(1 + 1/(1−α)²)/2` |
|---|---|---|
| 0.25 | 1.17 | 1.39 |
| 0.50 | 1.50 | 2.50 |
| 0.75 | 2.50 | 8.50 |
| 0.90 | 5.50 | 50.50 |

所以线性探测的装载因子要**压低**：本题参考解让占用（含墓碑）不超过 1/2，刚 resize 完时只有 1/4。内存换速度。

**优点**：
* **缓存友好**：往后看一格，通常就在**同一条缓存行**里（2.8 节）——不像链表每跳一步都可能是一次内存访问。
* **没有每条目一次分配**：条目就是数组里的一格。

### 2.6 删除与墓碑（tombstone）

**坑**：开放寻址里**不能**把被删的格子直接置空。用第 1 节的小表：

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   AAPL   AMZN   空   MSFT   TSLA
```

删 AAPL，如果把 3 号置空，再查 AMZN：家是 3 → 看到空格 → 结论「不存在」。❌ 错了，AMZN 明明在 4 号。
原因：AMZN 当初是因为 3 被占才被挤到 4 的；删除破坏了「从家到我之间没有空格」这个不变量。

**墓碑**：被删的格子标成特殊的「已删除」，而不是「空」：

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   ✝墓碑  AMZN   空   MSFT   TSLA
```

* 查找：**碰到墓碑要继续往后找**（它不是空格，不终止）。
* 插入：可以**复用**路上遇到的第一个墓碑（但必须先把整条探测路走完确认 key 不存在，否则可能插入重复的 key）。
* 墓碑会累积，把表撑得「看起来满了」，探测链越来越长。所以 resize/rehash 时**只搬活条目**，墓碑全部消失；并且触发条件把墓碑算进装载因子。

其他删除方案：**回移删除**（backward shift deletion）——删除后把后面属于这条探测链的条目往前挪，不留墓碑。更复杂，但没有墓碑累积的问题（hc05 的 `TickBook` 用了这个）。

### 2.7 装载因子（load factor）与 resize

**是什么**：装载因子 α = 已用格子 / 总格子。

**为什么必须 resize**：表满了，（a）线性探测会无限循环；（b）即使没满，α 越高探测次数越多（见 2.5 的表）。所以条目增加时必须把数组变大，把所有条目**重新哈希**（rehash）进新数组——因为下标 = 哈希值的高位，数组大小变了下标就全变了。

**为什么每次翻倍而不是每次加一点**：**摊还分析**（amortized analysis）。每次翻倍：容量从 C 到 2C，搬 C/2 个条目；之前的翻倍搬的条目数是 C/4、C/8、…，总共 `C/2 + C/4 + … < C`。
所以插入 n 个条目，总搬运次数 < 2n，摊到每次插入是 O(1)。如果每次只加 100 格，总搬运是 n²/200 级别，就变成 O(n²)。

本题参考解的策略（`TickerMap`）：

* **触发**：每次要占用一个**空格**时，如果 `(活条目 + 墓碑 + 1) × 2 > 容量`（占用会超过一半），先 rehash。
* **新容量**：`活条目数 × 4` 向上取 2 的幂。纯插入场景下触发时活条目 = 容量/2，所以新容量 = 旧容量 × 2（正好翻倍），装载因子回到 1/4。
* 如果墓碑很多、活条目很少（比如不停地上市退市），新容量会比旧容量**小或相等**——这是在**清理墓碑**，同时避免表只增不减。

### 2.8 CPU 缓存、缓存行、局部性（locality）

**是什么**：现代 CPU 比内存快得多。为了不让 CPU 总在等内存，CPU 核心旁边放了几级小而快的**缓存**（L1、L2、L3）。CPU 读内存时不是读一个字节，而是一次读**一整条缓存行**（cache line），在 x86 和 Apple Silicon 之间有 64 或 128 字节的区别，常见按 64 字节理解。

**为什么重要**（教科书上的典型量级，**不是本机实测**）：读 L1 缓存约 1 纳秒，L2 约 3–5 纳秒，读主内存约 80–100 纳秒——慢两个数量级。
如果你的数据结构需要「读一次内存拿到地址 A，再读 A 拿到地址 B，再读 B……」（**指针追逐**，pointer chasing），每一跳都可能是一次缓存未命中，而且**不能并行**（下一跳的地址要等上一跳读完才知道）。

**它怎么影响我们**：

```
HashMap<String,Long>  查一次：table[桶] → Node → (key String → byte[] 用于 equals) → Long value
                           3~4 次可能的缓存未命中，串行
LongTickerMap          查一次：slots[2i], slots[2i+1]（相邻 16 字节，同一缓存行）
                           1 次缓存未命中（如果要线性探测，下一格通常在同一行）
```

**局部性**的两种形式：
* **空间局部性**：访问了地址 X，很可能马上访问 X 附近。数组连续存放 → 读一格顺带把后面几格拿进缓存；
* **时间局部性**：刚访问过的很可能马上再访问。行情里少数热门股票占了大部分消息（偏斜访问）→ 它们常驻缓存。

**交错布局**：把 key 和 value 放在同一个 `long[]`（`slots[2i]=key, slots[2i+1]=value`），一次读缓存行同时拿到两者。分离布局（`keys[]` 一个数组、`vals[]` 另一个）读完 key 还要再去另一个数组读 value——理论上多一次缓存未命中。
**但**我实测的结果没有稳定地支持这个理论（见第 4 节），所以不要在面试里把它当成确定的事实说。

### 2.9 装箱（boxing）

**是什么**：Java 的 `int`/`long` 是原始类型（直接就是 4/8 字节的数）；泛型集合（`HashMap<String, Long>`）里只能放对象，所以 `long` 要包进一个 `Long` 对象——这叫装箱。取出来再变回 `long` 叫拆箱（unboxing）。

**代价**：`Long` 对象 24 字节（实测）、要在堆上分配、被 GC 管理。`map.merge(key, 1L, Long::sum)` 每次可能分配一个新的 `Long`：因为 `Long` 不可变，加法的结果必须是新对象。
`Long.valueOf` 对 −128..127 有缓存池（不分配），超出范围就分配——累计成交量很快就超出了。
我实测：预热后 160 万次 `HashMap<String,Long>.merge` 平均每次分配 **14.8 字节**（不是每次都 24；我推测是 JIT 的逃逸分析消掉了一部分，没有验证），而 `LongTickerMap.add` 是 **0**。
分配本身不贵（几纳秒），贵的是**积累的垃圾让 GC 更忙**、以及对象散落在堆里破坏局部性。

### 2.10 位运算与打包（bit packing）

**是什么**：一个 `long` 有 64 个比特。26 个字母只需要 5 个比特（2⁵ = 32 ≥ 27，其中 0 留给「没有字符」，1..26 对应 A..Z）。8 个字母 × 5 比特 = 40 比特，一个 `long` 装得下，还多 24 个比特。

**基本操作**：

```java
x << 5            // 左移 5 位 = 乘以 32，给新字符腾位置
x | c             // 按位或：把 c 的比特写进 x 的空位
(x >>> 20) & 0x1F // 先右移 20 位，再只保留最低 5 位 = 取出第 20..24 比特这一个字段
```

**例子**：`"AAPL"` → A=1, A=1, P=16, L=12；第 i 个字符放在 `[35-5i, 39-5i]` 比特：

```
字符:   A     A     P     L     (空)  (空)  (空)  (空)
字段:  00001 00001 10000 01100 00000 00000 00000 00000
位置:  39..35 34..30 29..25 24..20 19..15 14..10 9..5 4..0

值 = (1<<35) | (1<<30) | (16<<25) | (12<<20) = 35,982,934,016 = 0x860C00000     （脚本算出）
```

**这个编码的好处**：

1. 不同的代码得到不同的 long（**单射**）；
2. 合法代码永远 > 0，所以 **0 可以当哈希表的「空格」标记**，不需要额外的状态数组；
3. 比较两个代码 = 比较两个 long，不用 `equals`，不用分配对象。

**注意低位全是 0**：`"AAPL"` 只占高 20 位，低 20 位是补的 0。这意味着 `key & mask`（只看低位）对短代码**完全没用**——所有短代码的低位都是 0，都会撞同一个格子。（本题测试：对全部 17576 个三字母代码，`key & mask` 的最长探测距离是 **17575**——所有 key 住进同一条链；乘法哈希只有 0 或 1。本机实测。）

### 2.11 完美哈希（perfect hashing）

**是什么**：如果 key 的集合**事先固定**（比如今天的 8000 个代码），可以花一点启动时间，找到一个对这个集合**零冲突**的哈希函数。
**最小**完美哈希（minimal perfect hash）更进一步：n 个 key 恰好映射到 `0..n-1`，没有一个空格浪费。

**为什么有用**：

* 查找是确定的 O(1)——没有探测循环，不存在「最坏情况探测很长」；
* 内存最紧凑：value 放进长度恰好 n 的数组，无空格、无墓碑；
* 可以把「key → 下标」的结果**缓存起来**：订阅行情时解析一次，之后每条消息直接用下标访问数组，连哈希都省了。

**代价**：key 集合不能变（新代码上市要重新构造）；构造要花时间；对集合外的 key 要能识别（所以仍要保存原始 key 做比较）。

算法见第 4 节 Part 3。

### 2.12 堆外内存（off-heap）与 FFM API

**是什么**：普通 Java 对象在**堆**（heap）上，由垃圾回收器（GC）管理。**堆外内存**是 JVM 之外、由程序自己申请和释放的一块内存。
Java 21 的 **FFM API**（Foreign Function & Memory，预览特性，Java 22 转正）用 `Arena`（管理内存的生命周期）和 `MemorySegment`（一块有边界检查的内存）提供安全的堆外访问：

```java
try (Arena arena = Arena.ofShared()) {                       // 出了 try 自动释放
    MemorySegment seg = arena.allocate(1024, 64);           // 1024 字节，64 字节对齐，已清零
    seg.set(ValueLayout.JAVA_LONG, 0, 42L);                 // 在偏移 0 写一个 long
    long v = seg.get(ValueLayout.JAVA_LONG, 0);             // 读回来
}                                                            // 之后再访问 seg 会抛 IllegalStateException
```

**为什么用**：布局和对齐由你控制；GC 完全看不到这块内存（表再大，GC 扫描的工作量也不增加）；可以映射文件/共享内存。**代价**：手动 close；每次访问有边界检查；没有自动扩容。

### 2.13 测量（microbenchmark）的基本功

**为什么需要**：「我觉得这样更快」不是工程结论。

**Java 微基准的几个坑**（`Bench` 里都处理了）：

1. **预热**（warm-up）：JIT 编译器把热点代码编译成机器码需要一段时间，一开始的几轮是解释执行，慢得多。我们每个测量跑 5 轮，取**最好**的一轮。
2. **死代码消除**：如果结果没被使用，JIT 可能把整个计算删掉。`Bench` 把结果累加进一个静态变量并在最后打印。
3. **同一台机器、同一次运行里比较**才有意义；换机器/换负载，数字会变。
4. **随机数不要放进被测循环**：先把要访问的下标存进数组，循环里只读数组。
5. 想要可发表的数字：用 **JMH**（OpenJDK 的微基准框架）。`Bench` 只是教学用的轻量版。

---

## 3. 从最笨的解法开始

### 3.1 最笨：`List<Entry>` 线性查找

```java
for (Entry e : list) if (e.ticker.equals(key)) { e.volume += delta; return; }
list.add(new Entry(key, delta));
```

8000 个代码、每条消息平均比较 4000 次 `String.equals`，每秒 300 万条消息就是每秒 120 亿次比较。显然不行。**具体慢在**：每条消息都要线性扫。

### 3.2 次笨：`HashMap<String, Long>`

```java
map.merge(ticker, qty, Long::sum);
```

对，且已经是 O(1)。**慢在**（第 2.4、2.9 节）：

1. 每个条目 4 个堆对象，~110 字节；
2. 查一次沿多层指针跳；
3. 每次 `merge` 装箱一个新 `Long`；
4. 如果 key 是从行情报文里解析出来的，每条消息还得先 `new String(...)`（48 字节）才能查——**每秒几百万个短命的 String**。

本机实测（第 4 节完整表）：8000 个代码、均匀访问时 `HashMap<String,Long>.merge` 约 **7.7 ns/op**；200 万个代码时 **55 ns/op**——此时大部分时间是缓存未命中。

### 3.3 手写时最容易犯的三个错（这就是 Part 1 的陷阱）

1. **用 `hashCode() & mask` 当下标**：低位分布不均匀（2.2 节），会扎堆；
2. **删除时把格子置空**：断掉探测链，后面的 key 找不到（2.6 节）；
3. **没有 resize，或者 resize 不看墓碑**：满了死循环；或者不停地「插入新 key + 删旧 key」，墓碑把表撑满，查找不存在的 key 时无限循环。

---

## 4. 一步一步改进

### Part 1：手写 `TickerMap`（key = `String`）

**目标**：自己实现开放寻址哈希表，跑赢「性能毫无保证」的朴素写法，并且正确（冲突、删除、扩容）。

**步骤**：

1. **数据**：`String[] keys; long[] vals;`（并行数组，`keys[i]` 和 `vals[i]` 是同一条记录）。`keys[i] == null` 表示空格；一个特殊的哨兵对象 `TOMB` 表示墓碑；容量是 2 的幂。
2. **家**：`home(key) = (hashCode * 0x9E3779B9) >>> shift`（2.2 节）。
3. **查找 `find`**：从家出发，`null` → 不存在；`TOMB` → 跳过；`equals` → 找到。
4. **插入 `upsert`**：走完整条探测路，记下**第一个墓碑**；找到相同 key 则更新；走到空格仍没找到，则优先复用墓碑，否则占用这个空格（占用空格之前先检查是否需要 resize）。
5. **删除**：放墓碑，`size--`，`tombs++`。
6. **rehash**：容量按 `活条目 × 4` 重算，只搬活条目，墓碑消失。
7. **`add` 溢出**：用 `Math.addExact`，它**先算完再写**，异常抛出时表没有被改动。

**新复杂度**：期望 O(1)（α ≤ 1/2 时成功查找平均 1.5 次探测）。`TickerMap` 在 20 万个代码上做 100 万次 `add` 约 **42–48 ms**（本机，预热后）。

### Part 2：利用 ticker 结构 —— 打包成 `long`

**发现问题**：Part 1 的瓶颈是 `String`：对象本身 48 字节、`hashCode()`（第一次要遍历字符，之后读缓存字段）、`equals()`（逐字节比较）、行情报文里本来没有 `String`（每次要 `new`）。

**想法**：股票代码 ≤ 8 个大写字母 → 5 比特 × 8 = 40 比特 → 一个 `long`。key 变成原始类型，比较就是 `==`，哈希就是一次乘法。

**步骤**：

1. **`TickerCodec.pack`**：循环，把每个字符 `c - 'A' + 1` 放到 `[35-5i, 39-5i]` 比特。校验（空、超过 8 个、非 A–Z）。
2. **`parse` 返回 sealed 类型**：`Ticker(long key)` 或 `Invalid(String reason)`。为什么不直接抛异常？行情流里非法输入是常态，用**值**表示失败不需要抓栈（异常很贵），调用者必须处理两种情况（编译器检查）。需要异常的地方（`pack`）自己转一下。
3. **`packWire`**：行情报文里的 ticker 字段本来就是 **8 个字节 + 右侧补空格**。字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，**低 5 位恰好是 1..26**；空格 `0x20` 的**低 5 位恰好是 0**。所以只需把 8 个字节每个的低 5 位拼起来——这正是 `Long.compress(word, 0x1F1F1F1F1F1F1F1FL)` 干的事（Java 19 加入的位操作，对应 x86 的 PEXT 指令）。
   读 8 个字节用 `VarHandle`（`MethodHandles.byteArrayViewVarHandle(long[].class, BIG_ENDIAN)`）：一次读出一个 long，比 8 次 `buf[i]` 拼装更快、写起来也短。校验用一个 8 次的小循环（字母，然后尾部空格）。
4. **`LongTickerMap`**：和 Part 1 同一套算法，但：
   * `long[] slots`，交错布局（`slots[2i]=key`, `slots[2i+1]=value`）；
   * `0` = 空，`-1` = 墓碑（合法 key 都 > 0，所以不会混淆）；
   * 哈希：`(key * 0x9E3779B97F4A7C15L) >>> (64 - log2(容量))`（64 位的黄金比例常数，取高位）；
   * 比较：`==`；
   * `add` 在稳态下**没有任何分配**。

**新复杂度**：期望 O(1)，常数更小，**零分配**。

### Part 3：完美哈希 `SymbolIndex`

**发现问题**：Part 2 的最坏情况探测长度不确定；每个条目至少浪费一半的格子（α ≤ 1/2）。如果代码集合固定，这两样都能消灭。

**想法**：hash-and-displace（CHD 算法的简化版）。

1. **分桶**：用哈希把 n 个 key 分到 `r ≈ n/4` 个**桶**里（每桶平均 4 个 key）。
2. **从大桶到小桶**处理：对一个桶，找一个**位移** `d`（0, 1, 2, …），使得桶里**每个** key 的 `slot(hash, d)` 都落在**还没被占的格子**、且桶内互不相同；找到就占用它们，记 `disp[桶] = d`。
   * 为什么大桶先放？大桶的所有 key 要同时找到空位，最难；趁表还空着先放。
3. **单元素桶最后放**：直接给它下一个空格子，位移里存 `~slot`（取反成负数，表示「这是直接指定的格子，不用再算」）。
4. **查询**：算哈希 → 找桶 → 读 `disp` → 算出格子 → **比较 `keys[slot] == key`**。

```
key ─▶ h = hash(key)
        │
        ├─ bucket = fastrange(h 的高 32 位, r)
        │         d = disp[bucket]
        └─ slot = d<0 ? ~d : slot(h, d, n)        keys[slot] == key ? slot : -1
```

**为什么最后要比较 `keys[slot] == key`**：完美哈希只保证**集合内**的 key 互不冲突。集合外的 key 也会算出某个格子，必须靠比较发现它不是我们的 key。

**一个我踩过的坑（也是测试 `degenerateUniverses` 抓到的）**：我最初让第 d 个候选格子是「`h + d × 常数` 缩到 [0, n)」——桶内两个 key 的格子差在所有 d 下几乎固定。小表上，桶内两个 key 恰好需要的两个空格的差不匹配时，**不管试多少个 d 都放不进去**。修正：把 d 搅进 h 再乘一个大奇数，`slot(h, d, m) = high32((h ^ d·K1) · K2) 缩放到 [0, m)`，不同的 d 给出看似独立的格子。
教训：「用等差序列当一族哈希函数」在大表上碰巧能用，在小表上会死。

**`FrozenTickerMap`**：`SymbolIndex` + `long[] values`。热路径：一次混合哈希、读 `disp`、读 `keys`、写 `values`。
更快的路径：**订阅时就 `indexOf` 一次，缓存下标**，之后每条消息 `addAt(下标, qty)` —— 只剩一次数组写。

**复杂度**：构造期望 O(n)（100,000 个 key 约 21–50 ms，200 万个 key 约 544 ms，本机）；查询 O(1)，**没有探测循环**；内存：keys 8 B + values 8 B + disp 约 1 B（n/4 个 int）= **17 B/条**。

### Part 4：堆外 + 测量

**`OffHeapTickerMap`**：同样的线性探测，数据放在 `Arena` 分配的 64 字节对齐的内存里，每个槽 16 字节 `[key][value]`，4 个槽正好一条缓存行。（64 字节是 x86 的缓存行大小；Apple M 系列的缓存行是 128 字节，我没有在本机验证过行大小，所以「4 个槽一行」只是设计意图。）固定容量（`maxEntries`，槽数 = ≥ 2×maxEntries 的 2 的幂），满了就拒绝新 key。

**测量结果**（本机 M 系列 Mac，12 核，JDK 21.0.12，默认 G1 GC；`Bench` 每项 2000 万次更新，5 轮取最好；单位 ns/op，越小越好）：

| 实现 | 8,000 代码 均匀 | 8,000 偏斜 | 2,000,000 均匀 | 2,000,000 偏斜 |
|---|---|---|---|---|
| `HashMap<String,Long>.merge` | 7.7 | 4.8 | 55.4 | 20.0 |
| `TickerMap.add(String)` | 7.9 | 3.3 | 45.3 | 12.8 |
| `LongTickerMap.add(long)`（交错） | 4.0 | 1.3 | 11.1 | 2.0 |
| `SplitLongMap.add`（分离两个数组，对照实验） | 3.8 | 1.0 | 10.7 | 2.6 |
| `OffHeapTickerMap.add` | 4.1 | 1.4 | 11.8 | 2.1 |
| `FrozenTickerMap.add(long)`（完美哈希） | 2.5 | 2.3 | 13.4 | 3.6 |
| `FrozenTickerMap.addAt(缓存的下标)` | 0.5 | 0.5 | 1.5 | 0.7 |

「偏斜」= 90% 的更新落在 64 个热门代码上。内存（200 万条目，key 对象不计）：`HashMap<String,Long>` **64.4 B/条**（实测分配字节数，预分配桶数组）；`LongTickerMap` **33.6 B/条**（实测）；`FrozenTickerMap` **17.0 B/条**（数组大小算出）。

**怎么读这张表（诚实版）**：

1. **打包成 `long` 是真金白银的胜利**：200 万代码均匀访问时 55.4 → 11.1 ns/op（约 5 倍），内存 64 B → 34 B（key 对象还没算：再加 48 B 的 String）。这个差距在数据大得放不进缓存时最大——因为 `HashMap` 要多次**串行**的缓存未命中，我们只要一次。（「几次」是我读代码推断的，没有用硬件计数器验证。）
2. **数据小、放得进缓存时差距小得多**（8,000 代码：7.7 → 4.0）。缓存里的访问便宜，剩下的是装箱/比较/哈希的指令数。
3. **完美哈希在「单次 add」上并不比一个调得好的开放寻址表快**：8,000 均匀 2.5 vs 4.0（略胜），200 万均匀 13.4 vs 11.1（略输）。原因：一次查找要读三个数组（`disp`、`keys`、`values`）；`LongTickerMap` 只读一个交错的数组。**完美哈希的真正收益是：确定的最坏情况、最紧凑的内存（17 B vs 34 B），以及——最重要的——让你能缓存下标**：`addAt` 比任何 `add` 都快 5–10 倍（0.5 / 1.5 ns）。「速度来自根本不哈希」。
4. **交错 vs 分离布局：我的数据不支持「交错一定更快」**：`LongTickerMap` 比 `SplitLongMap` 在 200 万均匀时 11.1 vs 10.7（相同）、偏斜时 2.0 vs 2.6（交错略好）、8,000 偏斜 1.3 vs 1.0（分离略好）。差距在运行间的噪声范围内（同一份代码的另一次运行里，8,000 均匀的 `LongTickerMap` 是 2.3 ns，而现在是 4.0 ns——见下一条）。结论：**不要在没有数据的情况下宣称交错布局更快**。
5. **装载因子的影响确实很大，而且会悄悄变化**：我改了 resize 的容量公式后（`size+1` → `size`，让它纯插入时正好翻倍而不是翻 4 倍），8,000 个条目落在 16384 格里（α ≈ 0.49，之前是 32768 格，α ≈ 0.24），同样的代码从 **2.3 ns 变成 4.0 ns**。我没有用 profiler 隔离原因（推测是探测步数变多 + 分支预测失败），但这个测量提醒我们：**线性探测的速度对 α 极其敏感**（对照 2.5 节的 Knuth 表：α 从 0.25 到 0.5，成功查找平均探测次数从 1.17 到 1.5）。
6. **堆外没有带来速度**：`OffHeapTickerMap` 和 `LongTickerMap` 速度相近（4.1 vs 4.0；11.8 vs 11.1）。它的好处不是快，而是**不占堆、GC 看不见、布局可控**。我没有测 GC 停顿，所以不对「GC 抖动」下定量结论。
7. **没测的**：多线程、真实行情的访问分布、不同 CPU、GC 停顿、`-XX:+UseZGC` vs G1 的差异。

---

## 5. 逐段讲参考解

### 5.1 `TickerMap`：数据与哈希

```java
private static final String TOMB = new String("<deleted>");   // identity sentinel
private String[] keys;
private long[] vals;
private int size, tombs, mask, shift;
```

* `new String("<deleted>")` 保证这是一个**独一无二的对象**（字符串字面量会被驻留，任何人写同样的字面量就是同一个对象）；比较用 `k == TOMB`（引用相等），不是 `equals`——所以用户存一个内容也是 `<deleted>` 的 key 不会被误认为墓碑。
* `mask = capacity - 1`，`shift = 32 - log2(capacity)`。

```java
private int home(String key) { return (key.hashCode() * 0x9E3779B9) >>> shift; }
```

### 5.2 `TickerMap`：查找与插入

```java
private int find(String key) {
    int i = home(key);
    while (true) {
        String k = keys[i];
        if (k == null) return -1;                    // 碰到空格：key 不在表里
        if (k != TOMB && k.equals(key)) return i;    // 墓碑要跳过，继续往后
        i = (i + 1) & mask;                          // 到末尾绕回开头
    }
}
```

`while (true)` 会不会死循环？只要表里至少有一个空格就不会：我们保证 `(size + tombs) × 2 ≤ capacity`。

```java
private OptionalLong upsert(String key, long value, boolean accumulate) {
    int i = home(key);
    int firstTomb = -1;
    while (true) {
        String k = keys[i];
        if (k == null) break;
        if (k == TOMB) {
            if (firstTomb < 0) firstTomb = i;        // 记下第一个墓碑
        } else if (k.equals(key)) {
            long old = vals[i];
            vals[i] = accumulate ? Math.addExact(old, value) : value;
            return OptionalLong.of(old);
        }
        i = (i + 1) & mask;
    }
    // key 不在表里 —— 插入
    if (firstTomb >= 0) { /* 复用墓碑: keys/vals 写入; size++; tombs--; */ return OptionalLong.empty(); }
    if ((size + tombs + 1) * 2 > keys.length) {       // 占用空格会让「已用格子」超过一半
        rehash();
        i = home(key);
        while (keys[i] != null) i = (i + 1) & mask;
    }
    keys[i] = key; vals[i] = value; size++;
    return OptionalLong.empty();
}
```

* **为什么要走完整条探测路才插入**：墓碑只是候选；key 可能在墓碑**后面**。如果看到墓碑就插入，会产生同一个 key 的两份拷贝。
* **复用墓碑**时「已用格子」（size+tombs）不变，所以不需要检查 resize。
* **占用空格**会让已用格子 +1，所以先检查；如果触发 rehash，新表里没有墓碑也没有这个 key，直接找空格。
* `Math.addExact` 先算后写：溢出抛 `ArithmeticException` 时 `vals[i]` 还是旧值。

### 5.3 `TickerMap`：删除与 rehash

```java
public OptionalLong remove(String key) {
    int i = find(key);
    if (i < 0) return OptionalLong.empty();
    long old = vals[i];
    keys[i] = TOMB; vals[i] = 0; size--; tombs++;
    return OptionalLong.of(old);
}

private void rehash() {
    String[] oldKeys = keys; long[] oldVals = vals;
    allocate(capacityFor(size, 4));                  // 按活条目数重算，墓碑不计
    for (int j = 0; j < oldKeys.length; j++) {
        String k = oldKeys[j];
        if (k == null || k == TOMB) continue;
        int i = home(k);
        while (keys[i] != null) i = (i + 1) & mask;
        keys[i] = k; vals[i] = oldVals[j]; size++;
    }
}
```

* 重新哈希是因为 `shift` 变了，旧下标不再有意义；搬的时候不需要比较（旧表里的 key 已经互不相同）。
* 对应的测试：`tombstoneChurnDoesNotBloatTheTableOrLoopForever`（30 万个 key 经过、任何时刻只有 10 个活的 → 容量必须 ≤ 1024）。

### 5.4 `TickerCodec`

```java
public static Parsed parse(CharSequence s) {
    if (s == null) return new Invalid("null");
    int n = s.length();
    if (n == 0) return new Invalid("empty ticker");
    if (n > MAX_LEN) return new Invalid("ticker longer than " + MAX_LEN + ": " + s);
    long key = 0;
    for (int i = 0; i < n; i++) {
        char c = s.charAt(i);
        if (c < 'A' || c > 'Z') return new Invalid("not an uppercase ASCII letter at " + i + ": " + s);
        key |= (long) (c - 'A' + 1) << (BITS * (MAX_LEN - 1 - i));
    }
    return new Ticker(key);
}
```

* `(long) (c - 'A' + 1) << ...`：**先转成 `long` 再移位**！`c - 'A' + 1` 是 `int`，`int` 左移超过 31 位会被截断（Java 对 `int` 的移位量取模 32）。这是位运算最经典的坑：测试里的 `ABCDEFGH` 会抓到。
* 接受 `CharSequence` 而不是 `String`：`StringBuilder` 也能直接传，不必先 `toString()`。

```java
public static long pack(CharSequence s) {
    return switch (parse(s)) {
        case Ticker(var key) -> key;
        case Invalid(var reason) -> throw new IllegalArgumentException(reason);
    };
}
```

`packWire`：

```java
long word = (long) BE_LONG.get(buf, off);          // 一次读 8 字节（大端），越界抛 IndexOutOfBoundsException
// 校验：字母…尾部空格；首字节不能是空格（不能是空字段）
return Long.compress(word, 0x1F1F1F1F1F1F1F1FL);   // 每个字节的低 5 位拼成连续的 40 比特
```

大端（BIG_ENDIAN）读出来，第一个字节在最高位，对应第一个字符——和我们的编码方向一致。

### 5.5 `LongTickerMap`

```java
private int home(long key) { return (int) ((key * GOLDEN) >>> shift); }   // GOLDEN = 0x9E3779B97F4A7C15L, shift = 64 - log2(cap)

private int locateForInsert(long key) {          // 找到返回 >=0；找不到返回 ~(应该插入的位置)
    int i = home(key);
    int firstTomb = -1;
    while (true) {
        long k = slots[2 * i];
        if (k == key) return i;
        if (k == EMPTY) return ~(firstTomb >= 0 ? firstTomb : i);
        if (k == TOMB && firstTomb < 0) firstTomb = i;
        i = (i + 1) & mask;
    }
}
```

* 返回值用「`~位置`」编码：**负数 = 没找到，取反就是该插入的位置**。这样一个 `int` 同时带回了「找没找到」和「位置」，避免分配结果对象。
* `add`：`int i = locateForInsert(key); if (i >= 0) { slots[2i+1] = addExact(...) } else insertNew(key, delta, ~i);`——只哈希、探测一次，不像 `TickerMap.add` 那样先 upsert 再 find（那个多一次探测，是为了代码简单；热路径上你应该像这里一样）。
* 稳态下 `add` 里没有 `new`，没有装箱，没有 lambda 捕获——**零分配**。

### 5.6 `SymbolIndex.tryBuild`

```java
int r = Math.max(1, (n + 3) / 4);                // 桶数 ≈ n/4
long[] h = new long[n];  int[] count = new int[r + 1];
for (int i = 0; i < n; i++) { h[i] = hash(universe[i], seed); count[bucket(h[i], r) + 1]++; }
```

先算每个 key 的哈希，数每个桶有几个 key。然后**计数排序**（counting sort）把 key 的下标按桶分组到 `members[]`（`start[b]..start[b+1]` 是桶 b 的成员）——不用 `List<List<…>>`，没有对象分配。

```java
long[] order = new long[r];
for (int b = 0; b < r; b++) order[b] = ((long) (start[b + 1] - start[b]) << 32) | b;
Arrays.sort(order);                                // 按（大小，桶号）排序，从后往前 = 从大到小
```

把「桶大小」和「桶号」打包进一个 long 排序，省掉比较器。

```java
if (size == 1) { while (used[cursor]) cursor++; used[cursor] = true; slotKeys[cursor] = ...; disp[b] = ~cursor; continue; }
for (int d = 0; d < MAX_DISPLACEMENT && !placed; d++) {
    int ok = 0;
    for (int p = from; p < to; p++) {
        int s = slot(h[members[p]], d, n);
        if (used[s]) break;
        used[s] = true;                            // 先占着：桶内两个 key 撞同一格也能发现
        tmp[ok++] = s;
    }
    if (ok == size) { /* 登记 */ disp[b] = d; placed = true; }
    else for (int p = 0; p < ok; p++) used[tmp[p]] = false;     // 回滚，换下一个 d
}
if (!placed) return null;                          // 这个 seed 不行，build 换种子重来
```

* "先占着再回滚"：用同一个 `used[]` 同时检查「格子已被别的桶占用」和「桶内两个 key 撞同一格」。
* `cursor` 单调向前：单元素桶最后处理，此时剩下的空格子数 = 剩下的 key 数，必然有空位。
* 构造失败（极罕见）时换 `seed` 重来最多 64 次。

### 5.7 `FrozenTickerMap` 与 `OffHeapTickerMap`

`FrozenTickerMap`：

```java
public int indexOf(long key) { return key <= 0 ? -1 : index.indexOf(key); }
public long add(long key, long delta) {
    int i = indexOf(key);
    if (i < 0) throw new IllegalArgumentException("unknown ticker key: " + key);
    return addAt(i, delta);
}
public long addAt(int index, long delta) { return values[index] = Math.addExact(values[index], delta); }
```

`OffHeapTickerMap`（关键几行）：

```java
this.arena = Arena.ofShared();                              // 允许别的线程访问（JUnit 的超时断言会换线程）
this.seg = arena.allocate(capacity * SLOT_BYTES, 64);       // 已清零；64 字节对齐
private long keyAt(int slot)   { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES); }
private long valueAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES + 8); }
public void close() { if (arena.scope().isAlive()) arena.close(); }
```

`close()` 之后任何 `seg.get` 都抛 `IllegalStateException`——这是 FFM 的内存安全保证（没有悬空指针），测试 `accessAfterCloseFailsAndCloseIsIdempotent` 检查。

---

## 6. Java 21 特性小课

### 6.1 record（J01）+ sealed（J02）+ 模式匹配 switch（J03）+ record 模式（J04）

`TickerCodec.Parsed` 是一个**封闭的结果类型**：

```java
public sealed interface Parsed permits Ticker, Invalid {}
public record Ticker(long key) implements Parsed {}
public record Invalid(String reason) implements Parsed {}

return switch (parse(s)) {
    case Ticker(var key) -> key;
    case Invalid(var reason) -> throw new IllegalArgumentException(reason);
};
```

旧写法（Java 8）：返回 `long`，非法时返回 `-1` 或 `0`（「魔数」，容易被调用者忘记检查）；或者抛异常（调用者无法选择「我不想抓栈」）。
新写法：返回类型本身就说明「有两种可能」，`switch` 必须处理两种（编译器检查，不需要 `default`）；`case Ticker(var key)` 同时完成类型判断和取字段。

什么时候**不该**用：失败很罕见、且调用者通常无法处理时，异常更简洁。这里选值是因为行情流里非法输入是常态，而且 `parse` 可能在热路径上。

详细课本：`study/10-java21/J02_sealed.md`、`J03_pattern_switch.md`、`J04_record_patterns.md`（待写）。

### 6.2 `switch` 表达式（J05）与整数/位小工具（J15）

`pack` 里的 `switch` 是**表达式**：它产生一个值，分支可以直接 `throw`。
位工具：`Integer.numberOfTrailingZeros(capacity)`（容量是 2 的幂时就是 log₂）、`Integer.highestOneBit(x)`（≤ x 的最大 2 的幂，用于向上取整到 2 的幂：`highestOneBit(x - 1) << 1`）、
**`Long.compress(x, mask)`**（Java 19）：把 `x` 中 `mask` 为 1 的那些比特，按顺序拼到低位。例：`Long.compress(0b1010_1100L, 0b1111_0000L)` = `0b1010` = 10。
旧写法要手写 8 次「取字节、掩码、移位、或」，现在是一条（x86 上会被 JIT 编译成 PEXT 指令，本机 ARM 上是一小段指令序列——我没有验证 JIT 具体生成了什么）。

### 6.3 `VarHandle` 读字节数组（J16）

```java
private static final VarHandle BE_LONG = MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN);
long word = (long) BE_LONG.get(buf, off);
```

旧写法：`ByteBuffer.wrap(buf).getLong(off)`（要分配一个 `ByteBuffer` 对象，或复用同一个），或手写 8 次移位。
`byteArrayViewVarHandle` 把 `byte[]` 看成 `long[]` 视图，直接读 8 个字节，**自带边界检查**（越界抛 `IndexOutOfBoundsException`），不分配对象，JIT 能内联成一次读取（加上必要的字节序转换）。
`VarHandle` 还用于并发（原子操作 `compareAndSet` 等）——本题没有用到，但是同一个类。

### 6.4 FFM API：`Arena` / `MemorySegment`（J17，预览）

见 2.12 节。关键点：

* 预览特性：编译和运行都要 `--enable-preview`（`jtest.py` 已经带上）；Java 22 转正，API 小有变化（所以课本里的写法以 Java 21 为准）。
* 旧写法 `sun.misc.Unsafe`：能直接读写内存，但**没有任何安全检查**——越界就是 JVM 崩溃（segfault）。
* 新写法：每次访问有边界检查和生命周期检查；`Arena.close()` 之后访问会抛异常而不是崩溃。
* 什么时候**不该**用：数据能放堆里且 GC 不是瓶颈时，堆内数组更简单（本题测量里堆外并不更快）。

### 6.5 JIT / GC 基础（J19，口头题）

* **JIT**（just-in-time 编译）：JVM 先解释执行，发现热点方法后编译成机器码；编译是后台线程做的，所以基准要预热。**逃逸分析**能把「不逃出方法的对象」优化掉（栈上分配/标量替换）——这很可能就是 `HashMap.merge` 平均每次只分配 14.8 字节而不是 24 的原因（推测，没有用 `-XX:-DoEscapeAnalysis` 对照验证）。
* **Generational ZGC**（JEP 439）：低延迟垃圾回收器，停顿目标亚毫秒；`jtest.py` 的测试用它跑。**本讲义的 `Bench` 用的是默认 G1**，所以 `Bench` 数字和测试里用 ZGC 的时间没有直接可比性。

---

## 7. 追问预演

**问：`HashMap` 为什么每次翻倍？为什么容量是 2 的幂？**
* 思考：翻倍 → 摊还 O(1)（2.7）；2 的幂 → 用 `&` 代替 `%`（2.2）。
* 说出口：「翻倍使总搬运量小于 2n，摊到每次插入是常数；2 的幂让取下标变成一次与运算。」

**问：开放寻址和链地址怎么选？**
* 答要点：链地址——实现简单、装载因子可以 > 1、删除简单；但每个条目一次分配 + 指针追逐，缓存差。开放寻址——数据连续、缓存友好、无分配；但装载因子要低（线性探测 ≤ 0.5–0.75）、删除麻烦（墓碑或回移）、对哈希质量敏感。
* 说出口：「读多写少、key 小、追求延迟，我选开放寻址；key 大、写多、删除多或者要保证最坏情况，链地址（或带树化）更稳。」

**问：删除怎么做？墓碑有什么问题？**
* 答要点：不能置空（断探测链）；墓碑 + rehash 时清理；问题：累积使表变「脏」、探测变长 → 把墓碑算进装载因子触发 rehash；替代：回移删除。
* 说出口：「我留墓碑，查找跳过它、插入时复用它，装载因子把墓碑也算进去，rehash 时清掉。」

**问：怎么测量你的哈希函数好不好？**
* 答要点：最长探测距离 / 平均探测次数 / 用真实 ticker 集合而不是随机字符串；对结构化输入（连续的三字母代码）做压力测试；看桶（或探测）长度的分布。
* 说出口：「我会拿真实的代码集合跑，统计探测距离的分布，尤其是最大值；还会用连续、相近的代码试，因为这是最容易暴露哈希弱点的输入。」本题测试 `hashSpreadsPackedKeysWhoseLowBitsAreAllZero` 就是这样做的。

**问：你怎么知道你的版本更快？**
* 答要点：同一台机器、同一次运行、预热、多轮取最好、防止死代码消除；改变数据规模（放得进缓存 vs 放不进）和访问分布（均匀 vs 偏斜）；报告**没测到**的（多线程、GC、真实数据）；真要发表用 JMH。
* 说出口：「我用 8000 和 200 万两个规模、均匀和偏斜两种访问各测了一遍，打包 key 在大规模下快约 5 倍，小规模只快 2 倍。多线程和 GC 停顿我没测。」

**问：完美哈希一定比普通哈希快吗？**
* 答要点：不一定。构造时间、查询要读多个数组；它的收益在最坏情况确定、内存紧凑、可以缓存下标。我们的实测里单次 `add` 并没有稳定地比 `LongTickerMap` 快。
* 说出口：「完美哈希给的是确定性和紧凑，不是魔法加速。真正的加速来自把下标缓存起来，直接数组访问。」

**问：key 变多了、多线程更新怎么办？**
* 答要点：每个线程一张表（单写者）+ 定期合并（完美哈希下合并就是逐下标相加）；或分片加锁；或对 value 用 `LongAdder` / `VarHandle.getAndAdd` 做原子累加（完美哈希下 value 数组固定，**原子累加很自然**，因为不用 resize）。
* 说出口：「完美哈希加固定数组的好处是不会 resize，所以可以直接用 `VarHandle` 对数组元素做原子累加；热点冲突多时改成每线程一张再合并。」

**问：key 不止 8 个字符怎么办（比如 `BRK.B`、期权代码）？**
* 答要点：扩展字符集或用两个 long（128 位）；或者回退到字符串哈希（FNV-1a / xxHash）+ 字节数组比较；热路径上始终避免 `new String`。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 下标 = `hashCode() & mask` | 低位分布不均，短代码扎堆；打包后的 key 低位全是 0，所有 key 撞一格（实测最长探测 17575） | 乘法哈希（Fibonacci）取高位，或 `h ^ (h >>> 16)` 混合 |
| 删除时 `keys[i] = null` | 断了探测链，后面的 key 查不到 | 放墓碑；查找跳过墓碑；rehash 时清理 |
| 遇到墓碑就插入 | key 可能在墓碑后面，导致重复 key | 走完整条探测路，记下第一个墓碑，没找到才复用 |
| 装载因子不算墓碑 | 反复插入/删除后表里没有空格，查找不存在的 key 死循环 | `(活 + 墓碑 + 1) × 2 > 容量` 就 rehash |
| `(c - 'A' + 1) << 35`（没转 long） | `int` 移位量取模 32，`<< 35` 实际是 `<< 3` | `(long) (c - 'A' + 1) << 35` |
| 用 `0` 当「不存在」的返回值 | 累计量本来就可以是 0，分不清「没有」和「是 0」 | `OptionalLong` / `containsKey` / `get(k, ifAbsent)` |
| 完美哈希的 `indexOf` 不比较原始 key | 集合外的 key 也会算出一个格子，被误认为是集合内的 | 读出 `keys[slot]` 比较 `== key` |
| 用等差序列 `h + d·c` 当一族哈希函数 | 小表上桶内 key 的格子差固定，永远放不进去 | 把 d 搅进 h 再乘大奇数 |
| 微基准只跑一次、不预热、结果不用 | 测到的是解释执行/被 JIT 删掉的代码 | 预热 + 多轮取最好 + 使用结果；严肃测量用 JMH |
| 「堆外一定更快」「交错布局一定更快」 | 本题实测都没有稳定地支持 | 先测量再宣称 |

---

## 9. 自测题

1. 线性探测下，α = 0.75 时查找一个**不存在**的 key 平均要探测几次？α = 0.5 呢？为什么线性探测的 α 要压得比链地址法低？
2. 一个容量 8 的表里，`A`（家 3）、`B`（家 3）、`C`（家 4）依次插入，各住哪一格？删除 `A` 后，如果不用墓碑直接置空，查 `C` 会发生什么？
3. 为什么 resize 时必须把所有条目重新哈希，而不能直接把数组复制到更大的数组里？
4. 把 `"AB"` 打包成 `long`，写出十六进制的值（用本题的编码）。再说出 `"AB"` 和 `"AB "`（带尾部空格）在 `pack` 与 `packWire` 里分别怎么处理。
5. 判断：如果把 `LongTickerMap` 的哈希改成 `(int) key & mask`，对 `"AAPL"` 和 `"AAPM"` 会怎样？
6. 小编程：写一个 `static int log2(int powerOfTwo)`，不用循环和 `Math.log`。再写 `nextPowerOfTwo(int x)`（≥ x 的最小 2 的幂，x ≥ 1）。
7. 为什么在 `SymbolIndex` 里单元素的桶要最后处理？如果先处理会怎样？

<details><summary>答案</summary>

1. α = 0.75：`(1 + 1/(1−0.75)²)/2 = 8.5` 次；α = 0.5：2.5 次。线性探测有聚集（冲突的 key 占据连续的格子，滚雪球），α 接近 1 时探测次数按 1/(1−α)² 增长；链地址法冲突只影响同一条链，α = 1 时链长平均也只有 1。
2. `A` 住 3，`B` 家是 3 被占 → 住 4，`C` 家是 4 被占 → 住 5。删除 `A` 后若置空：查 `C` 从 4 开始（`B` 不是它）→ 5（是 `C`）→ 找到，这个例子没出错；但查 `B`：家 3 → 空格 → 误判不存在。有墓碑就不会。
3. 下标由哈希值的**高位**（或低位）决定，数组大小变了 → `shift`/`mask` 变了 → 同一个 key 的下标变了。直接复制，key 会待在错误的位置，查找时从新的家出发找不到。
4. `'A'=1, 'B'=2` → `(1<<35) | (2<<30)` = `0x800000000 | 0x80000000` = `0x880000000`。`pack("AB ")` → `Invalid`（空格不是 A–Z）；`packWire("AB      ")` → 合法，等于 `pack("AB")`（尾部空格是 wire 格式的补位）。
5. `"AAPL"` 与 `"AAPM"` 只差第 4 个字段（`[20..24]` 比特），而 `& mask`（mask 通常 ≤ 2²⁰）只看最低位，这两个 key 的低位全是 0 → 都落在下标 0 → 冲突。实际上所有 ≤ 6 个字符的代码低 10 比特都是 0（第 7 个字符才用到低 10 位）。
6. `Integer.numberOfTrailingZeros(powerOfTwo)`；`nextPowerOfTwo(x) = x == 1 ? 1 : Integer.highestOneBit(x - 1) << 1`（对 x ≤ 2³⁰）。
7. 单元素桶的格子是「直接指定」的，放哪都行；大桶需要多个位置**同时**为空，越晚越难（表越满，成功概率按 `(空闲比例)^桶大小` 下降）。先放单元素会把空格子吃掉，后面的大桶可能永远找不到合适的位移。

</details>

---

## 10. 延伸阅读

* Sedgewick《算法》第 3.4 节「散列表」—— 链地址和线性探测的标准入门，含 Knuth 的探测次数公式的推导。
* Knuth《计算机程序设计艺术》卷 3 第 6.4 节「Hashing」—— 线性探测的探测次数公式的原始来源；乘法哈希（Fibonacci hashing）的出处。
* `java.util.HashMap` 源码与 Javadoc（https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html ）—— 看 `hash()`（`h ^ (h >>> 16)`）、`putVal`、`resize`、`treeifyBin`。
* Belazzougui, Botelho, Dietzfelbinger《Hash, displace, and compress》(ESA 2009) —— CHD 完美哈希算法的原论文，本题 `SymbolIndex` 是它的简化版。
* JEP 442 Foreign Function & Memory API (Third Preview)（https://openjdk.org/jeps/442 ）—— Java 21 里 `Arena` / `MemorySegment` 的设计文档。
* `java.lang.invoke.VarHandle` 与 `MethodHandles.byteArrayViewVarHandle` Javadoc；`Long.compress` Javadoc —— 本题用到的两个位/字节工具。
* Ulrich Drepper《What Every Programmer Should Know About Memory》—— 缓存行与局部性的经典长文（读第 3 章「CPU Caches」）。
* OpenJDK JMH（https://github.com/openjdk/jmh ）—— 严肃的 Java 微基准框架；README 的「Pitfalls」一节值得读。
