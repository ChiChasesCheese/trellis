# hc07 · 股票代码哈希表 —— 讲义

> 读者：会写基本 Java。本篇从零讲清哈希表——哈希函数、冲突、链地址 vs 开放寻址、装载因子、resize、缓存行、装箱——再看「股票代码」这个特殊结构怎样让通用方案更快、更省内存。

---

## 1. 这道题在问什么

行情系统每秒几百万条消息，每条是「某只股票成交了 q 股」。维护**每只股票的累计成交量**：

```
收到 (AAPL, 100)  →  AAPL 的总量 += 100
收到 (MSFT, 50)   →  MSFT 的总量 += 50
收到 (AAPL, 30)   →  AAPL 的总量 += 30        （此时 AAPL = 130）
```

操作只有**按代码查、改、增、删一个数**，即键值映射（map），Java 默认答案 `HashMap<String, Long>`。追问路线：

1. 「自己写一个哈希表。」→ 原理（Part 1）。
2. 「代码最多 8 个大写字母，还能更好吗？」→ **利用输入结构**（Part 2）。
3. 「开盘前就告诉你今天所有代码呢？」→ **完美哈希**（Part 3）。
4. 「怎么知道更快？内存？缓存？」→ **测量**（Part 4）。

### 手算一遍（这张小表贯穿整篇）

**8 个格子**的数组（0..7）放 5 个代码，假设它们的「家」(home slot) 是 `AAPL→3`、`MSFT→6`、`GOOG→2`、`AMZN→3`、`TSLA→7`（怎么算见 2.2）。

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   AAPL   AMZN   空   MSFT   TSLA
                            ↑      ↑
                    AAPL 先到，占了 3；AMZN 的家也是 3，被占了，往后看 4，空 → 住 4
```

查 `AMZN`：家 3 → 是 AAPL，不是我 → 看 4 → AMZN ✓。查 `ZZZZ`（不存在）：家假设是 5 → 空 → 立刻知道不存在。这就是**开放寻址 + 线性探测**的全部直觉。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性；`O(log n)` n 翻倍只多一步；`O(n²)` 每对都处理；`O(1)` 与 n 无关。

### 2.1 为什么需要哈希：数组的下标是「免费」的

数组按下标取值 O(1)（`a[5]` 直接算地址），但只认整数。`List<Entry>` 查一个代码要从头比到尾：8000 个代码平均比 4000 次，每秒几百万条消息就是几十亿次比较。把代码**变成整数**再取余当下标 `a[整数 % 8]` 就又 O(1)。「把任意东西变成整数」的函数叫**哈希函数**（hash function），用其结果当下标的数组叫**哈希表**（hash table）。

### 2.2 哈希函数

确定性函数 `h(key) → 整数`。好的哈希函数：**确定**（同 key 同值）；**相等的 key 得相等的值**（`equals` 与 `hashCode` 的契约：`equals` 的两个对象 `hashCode` 必须相同，反之不要求）；**均匀**（不同 key 尽量散开）；**快**（每次查找都算）。

**`String.hashCode()`**：把字符串当 31 进制的数：

```
hash = s[0]·31^(n-1) + s[1]·31^(n-2) + … + s[n-1]        （int 溢出就自然绕回）
"AAPL" = 65·31³ + 65·31² + 80·31 + 76 = 1936415 + 62465 + 2480 + 76 = 2001436
```

**到格子编号**：`h % 8` 慢（除法）且 `h` 为负时余数也可能为负。**容量取 2 的幂**时用 `h & (容量 - 1)`（容量 8 时只留最低 3 位）：一条与运算，快且非负——这是 `HashMap` 和本题所有实现用 2 的幂容量的原因。

**坑：低位问题**。`h & 7` 只有字符串**最后一两个字符**起作用。五个代码：

```
AAPL  2001436   & 7 = 4
MSFT  2375924   & 7 = 4        ← 撞了
TSLA  2584628   & 7 = 4        ← 撞了
GOOG  2193600   & 7 = 0
AMZN  2013280   & 7 = 0        ← 撞了
```

五个里三个都想住 4 号格。**真实 hashCode 的低位分布并不均匀**，只取低位很危险。两类办法：

* **混合（mix）**：先把高位「搅」进低位，`java.util.HashMap` 用 `h ^ (h >>> 16)`。
* **乘法哈希 / 斐波那契哈希**：乘一个特殊奇数常数，然后**取高位**：

```java
(h * 0x9E3779B9) >>> (32 - 位数)       // 0x9E3779B9 ≈ 2^32 / 黄金比例 1.618…
```

乘法让输入的**每一位**都影响乘积的**高位**，取高位就拿到混合最好的几位。容量 8（3 位）时五个代码得 `AAPL→3, MSFT→6, GOOG→2, AMZN→3, TSLA→7`（第 1 节小表的「家」），只剩一对撞。选黄金比例是因为它让相邻整数（0, 1, 2, …）乘完均匀散布（三距离定理）；对 17576 个三字母代码，最长探测距离只有 0 或 1。

Part 1 的 `home(String)`：

```java
private int home(String key) { return (key.hashCode() * 0x9E3779B9) >>> shift; }   // shift = 32 - log2(容量)
```

`>>>` 是**无符号右移**（高位补 0），保证结果非负且正好在 `0..容量-1`。

### 2.3 冲突（collision）：躲不掉的

两个不同 key 得到同一格子。鸽巢原理躲不掉；即使 key 少于格子，**生日悖论**（23 个人就约一半概率同生日）说冲突来得比直觉早得多：8000 个 ticker 放进 16384 个格子**几乎一定**大量冲突。核心不是「避免冲突」，而是「冲突了怎么办」。

### 2.4 办法一：链地址法（separate chaining）——Java 的 `HashMap`

每个格子（**桶** bucket）是链表的头，冲突的 key 串在同一条链上。

```
桶:  0     1     2     3     4   …
     │           │     │
     ▼           ▼     ▼
   [GOOG]      [X]   [AAPL]──▶[AMZN]──▶ null
     │
     ▼
   [AA]──▶ null
```

查 key：算桶号 → 沿链比较。`java.util.HashMap`：每条目是 `Node` 对象（hash、key、value、next 引用）——**每条目一次堆分配**；装载因子默认 0.75，超过就把桶数翻倍并重新分配所有 Node；Java 8 起链长 ≥ 8（且桶数 ≥ 64）变**红黑树**，防恶意冲突把查找拖成 O(n)。

**代价**（`HashMap<String, Long>` 存一个 ticker 累计量）：

```
table[桶]  ──▶  Node (32 B)  ──▶  key: String (24 B) ──▶ byte[] (24 B)
                     └────────▶  value: Long (24 B)
```

每条目背后 **4 个堆对象**，沿指针层层跳。64 位 HotSpot 下：`Node` 32 B、`Long` 24 B、"AAPL" 这样的 `String` 48 B（对象 24 + byte[] 24）。预分配桶数组的 `HashMap<String,Long>` 在 200 万条目时每条（不含 key 对象）约 **64.4 B**，加 key 字符串 48 B 约 **110 B**，有用信息只有 8 字节 value 和 ≤ 8 字节 key。

### 2.5 办法二：开放寻址（open addressing）和线性探测（linear probing）

不另建链表，所有条目直接放**同一个数组**；冲突时在数组里**往后找下一个空格**。线性探测 = 一格一格往后找（到末尾绕回开头）。

* **插入**：从家出发，往后找第一个空格放进去。
* **查找**：从家出发往后看；**碰到目标就找到，碰到空格就确定不存在**（若存在，插入时一定放在碰到空格之前）。这要求「表里永远有空格」，否则查不存在的 key 无限循环，所以装载因子要限制（2.7）。
* 往后看一格叫一次探测（probe），key 离家多远就探测多少次。

**代价：聚集（clustering）**：冲突的 key 占据连续格子，这片区域像滚雪球越长越大，后来的 key 落进来就要走到片尾。Knuth 给出期望探测次数（装载因子 α = 占用 / 总格子）：

| α | 查找成功平均探测 `(1 + 1/(1−α))/2` | 查找失败平均探测 `(1 + 1/(1−α)²)/2` |
|---|---|---|
| 0.25 | 1.17 | 1.39 |
| 0.50 | 1.50 | 2.50 |
| 0.75 | 2.50 | 8.50 |
| 0.90 | 5.50 | 50.50 |

所以装载因子要**压低**：本实现让占用（含墓碑）不超过 1/2，刚 resize 完只有 1/4，内存换速度。**优点**：**缓存友好**（往后看一格通常在**同一条缓存行**，2.8）；**无每条目分配**。

### 2.6 删除与墓碑（tombstone）

开放寻址里**不能**把被删的格子直接置空。用第 1 节小表：

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   AAPL   AMZN   空   MSFT   TSLA
```

删 AAPL 若把 3 号置空，再查 AMZN：家 3 → 空格 → 「不存在」❌，AMZN 明明在 4 号。AMZN 当初因 3 被占才被挤到 4，删除破坏了「从家到我之间没有空格」这个不变量。

**墓碑**：被删的格子标成「已删除」而不是「空」：

```
格子:   0     1     2      3      4      5     6      7
内容:   空    空   GOOG   ✝墓碑  AMZN   空   MSFT   TSLA
```

* 查找：**碰到墓碑继续往后找**（它不是空格）。
* 插入：可**复用**路上第一个墓碑，但必须先走完整条探测路确认 key 不存在，否则可能重复插入。
* 墓碑会累积，把表撑得「看起来满了」。所以 rehash 时**只搬活条目**，墓碑全消失，触发条件也把墓碑算进装载因子。

另一方案**回移删除**（backward shift）：删除后把后面属于这条探测链的条目往前挪，不留墓碑；更复杂，但无累积（订单簿低分配实现用它）。

### 2.7 装载因子（load factor）与 resize

装载因子 α = 已用 / 总格子。表满时线性探测无限循环，没满时 α 越高探测越多（2.5 表）。所以条目增加时必须扩容并把所有条目**重新哈希**（rehash）——下标由哈希值高位决定，数组大小变了下标全变。

**为什么翻倍**：**摊还分析**（amortized）。翻倍时 C → 2C 搬 C/2 个条目，之前的翻倍搬 C/4、C/8、…，总共 `< C`；插入 n 个条目总搬运 < 2n，摊到每次 O(1)。每次只加 100 格则总搬运 n²/200 级，变 O(n²)。

`TickerMap` 的策略：

* **触发**：要占用一个**空格**时，若 `(活条目 + 墓碑 + 1) × 2 > 容量`，先 rehash。
* **新容量**：`活条目数 × 4` 向上取 2 的幂。纯插入时新容量 = 旧容量 × 2，α 回到 1/4。
* 墓碑多、活条目少（不停上市退市）时新容量会**小于或等于**旧容量——**清理墓碑**，避免表只增不减。

### 2.8 CPU 缓存、缓存行、局部性（locality）

CPU 比内存快得多，核心旁有几级小而快的**缓存**（L1、L2、L3），读内存时一次读**一整条缓存行**（cache line，常按 64 字节理解，Apple Silicon 是 128）。教科书量级（**非测量值**）：L1 约 1 ns，L2 约 3–5 ns，主内存约 80–100 ns。「读内存拿地址 A，再读 A 拿地址 B……」（**指针追逐**）每一跳都可能缓存未命中，且**不能并行**（下一跳地址要等上一跳读完）。

```
HashMap<String,Long>  查一次：table[桶] → Node → (key String → byte[] 用于 equals) → Long value
                           3~4 次可能的缓存未命中，串行
LongTickerMap          查一次：slots[2i], slots[2i+1]（相邻 16 字节，同一缓存行）
                           1 次缓存未命中（如果要线性探测，下一格通常在同一行）
```

**局部性**：**空间**——访问了 X 很可能马上访问附近（数组连续，读一格顺带拿进后面几格）；**时间**——刚访问的很可能再访问（少数热门股占大部分消息，常驻缓存）。

**交错布局**：key 和 value 放同一个 `long[]`（`slots[2i]=key, slots[2i+1]=value`），一次读缓存行同时拿到两者；分离布局（`keys[]`、`vals[]`）理论上多一次未命中。**但**测量没有稳定支持（第 4 节），别当确定事实说。

### 2.9 装箱（boxing）

泛型集合只能放对象，所以 `long` 要包进 `Long` 对象——装箱（取出叫拆箱）。`Long` 24 字节、堆上分配、GC 管理。`map.merge(key, 1L, Long::sum)` 每次可能分配新 `Long`（不可变，加法结果必是新对象）；`Long.valueOf` 对 −128..127 有缓存池，累计成交量很快超出。

预热后 160 万次 `HashMap<String,Long>.merge` 平均每次分配 **14.8 字节**（不是每次 24，大概是逃逸分析消掉一部分），`LongTickerMap.add` 是 **0**。分配本身不贵，贵的是**积累的垃圾让 GC 更忙**，以及对象散落堆里破坏局部性。

### 2.10 位运算与打包（bit packing）

26 个字母只需 5 比特（2⁵ = 32 ≥ 27，0 留给「没有字符」，1..26 对应 A..Z）。8 个字母 × 5 = 40 比特，一个 `long`（64 比特）装得下。

```java
x << 5            // 左移 5 位 = 乘以 32，给新字符腾位置
x | c             // 按位或：把 c 的比特写进 x 的空位
(x >>> 20) & 0x1F // 先右移 20 位，再只保留最低 5 位 = 取出第 20..24 比特这一个字段
```

`"AAPL"` → A=1, A=1, P=16, L=12；第 i 个字符放在 `[35-5i, 39-5i]` 比特：

```
字符:   A     A     P     L     (空)  (空)  (空)  (空)
字段:  00001 00001 10000 01100 00000 00000 00000 00000
位置:  39..35 34..30 29..25 24..20 19..15 14..10 9..5 4..0

值 = (1<<35) | (1<<30) | (16<<25) | (12<<20) = 35,982,934,016 = 0x860C00000     （脚本算出）
```

好处：不同代码得不同 long（**单射**）；合法代码 > 0，所以 **0 可当「空格」标记**，无需状态数组；比较两个代码 = 比较两个 long，不用 `equals`、不分配。

**注意低位全是 0**：`"AAPL"` 只占高 20 位，低 20 位补 0，所以 `key & mask` 对短代码**完全没用**，全撞同一格。（17576 个三字母代码，`key & mask` 最长探测距离 **17575**；乘法哈希只有 0 或 1。）

### 2.11 完美哈希（perfect hashing）

key 集合**事先固定**（如今天的 8000 个代码）时，可花点启动时间找到对这个集合**零冲突**的哈希函数；**最小**完美哈希更进一步：n 个 key 恰好映射到 `0..n-1`，无空格。

好处：查找确定 O(1)，无探测循环；内存最紧凑（value 放长度恰为 n 的数组）；可把「key → 下标」**缓存起来**——订阅行情时解析一次，之后每条消息直接用下标访问数组，连哈希都省了。**代价**：key 集合不能变（新代码上市要重建）；构造要时间；集合外的 key 要能识别（仍保存原始 key 比较）。算法见 Part 3。

### 2.12 堆外内存（off-heap）与 FFM API

普通对象在**堆**上由 GC 管理；**堆外内存**在 JVM 之外由程序自己申请释放。Java 21 的 **FFM API**（预览，Java 22 转正）用 `Arena`（管生命周期）和 `MemorySegment`（有边界检查）提供安全的堆外访问：

```java
try (Arena arena = Arena.ofShared()) {                       // 出了 try 自动释放
    MemorySegment seg = arena.allocate(1024, 64);           // 1024 字节，64 字节对齐，已清零
    seg.set(ValueLayout.JAVA_LONG, 0, 42L);                 // 在偏移 0 写一个 long
    long v = seg.get(ValueLayout.JAVA_LONG, 0);             // 读回来
}                                                            // 之后再访问 seg 会抛 IllegalStateException
```

用处：布局对齐自控；GC 看不到这块内存（表再大扫描量也不增）；可映射文件/共享内存。**代价**：手动 close、每次访问有边界检查、无自动扩容。

### 2.13 测量（microbenchmark）基本功

「我觉得更快」不是工程结论。Java 微基准的坑（`Bench` 都处理了）：**预热**（JIT 编译需要时间，开头几轮是解释执行；每个测量跑 5 轮取**最好**）；**死代码消除**（结果没被使用 JIT 可能删掉整个计算，所以累加进静态变量并打印）；**同一台机器、同一次运行里比较**；**随机数不放进被测循环**（先把下标存进数组）。要可发表的数字用 **JMH**，`Bench` 只是轻量教学版。

---

## 3. 从最笨的解法开始

### 3.1 最笨：`List<Entry>` 线性查找

```java
for (Entry e : list) if (e.ticker.equals(key)) { e.volume += delta; return; }
list.add(new Entry(key, delta));
```

每条消息平均比较 4000 次 `String.equals`，每秒 300 万条就是 120 亿次比较。

### 3.2 次笨：`HashMap<String, Long>`

```java
map.merge(ticker, qty, Long::sum);
```

对，且已是 O(1)。**慢在**（2.4、2.9）：每条目 4 个堆对象 ~110 字节；查一次沿多层指针跳；每次 `merge` 装箱新 `Long`；key 从报文解析出来时还得先 `new String(...)`（48 字节）才能查——**每秒几百万个短命 String**。8000 个代码均匀访问时 `merge` 约 **7.7 ns/op**，200 万个代码 **55 ns/op**——大部分是缓存未命中。

### 3.3 手写时最容易犯的三个错（Part 1 的陷阱）

1. **用 `hashCode() & mask` 当下标**：低位分布不均，扎堆（2.2）；
2. **删除时把格子置空**：断探测链，后面的 key 找不到（2.6）；
3. **没有 resize，或 resize 不看墓碑**：满了死循环；或不停「插入新 key + 删旧 key」，墓碑撑满表，查不存在的 key 无限循环。

---

## 4. 一步一步改进

### Part 1：手写 `TickerMap`（key = `String`）

1. **数据**：`String[] keys; long[] vals;`（并行数组）。`keys[i] == null` 表示空格；特殊哨兵对象 `TOMB` 表示墓碑；容量是 2 的幂。
2. **家**：`home(key) = (hashCode * 0x9E3779B9) >>> shift`（2.2）。
3. **查找 `find`**：从家出发，`null` → 不存在；`TOMB` → 跳过；`equals` → 找到。
4. **插入 `upsert`**：走完整条探测路并记下**第一个墓碑**；找到相同 key 则更新；走到空格仍没找到，则优先复用墓碑，否则占用这个空格（占用空格前先检查是否需 resize）。
5. **删除**：放墓碑，`size--`，`tombs++`。
6. **rehash**：容量按 `活条目 × 4` 重算，只搬活条目，墓碑消失。
7. **`add` 溢出**：用 `Math.addExact`，它**先算完再写**，抛异常时表未被改动。

期望 O(1)（α ≤ 1/2 时成功查找平均 1.5 次探测）。20 万个代码上做 100 万次 `add` 约 **42–48 ms**（预热后）。

### Part 2：利用 ticker 结构 —— 打包成 `long`

**问题**：Part 1 的瓶颈是 `String`：48 字节、`hashCode()`（首次遍历字符）、`equals()`（逐字节比较）、报文本来没有 `String`（每次要 `new`）。**想法**：代码 ≤ 8 个大写字母 → 40 比特 → 一个 `long`，key 变原始类型，比较 `==`，哈希一次乘法。

1. **`TickerCodec.pack`**：循环，每个字符 `c - 'A' + 1` 放到 `[35-5i, 39-5i]` 比特；校验（空、超 8 个、非 A–Z）。
2. **`parse` 返回 sealed 类型**：`Ticker(long key)` 或 `Invalid(String reason)`。行情流里非法输入是常态，用**值**表示失败不需抓栈（异常很贵），调用者必须处理两种情况（编译器检查）。需要异常处（`pack`）自己转。
3. **`packWire`**：行情报文的 ticker 字段本来就是 **8 字节 + 右侧补空格**。字母 `A..Z` 的 ASCII 是 `0x41..0x5A`，**低 5 位恰好是 1..26**；空格 `0x20` 的**低 5 位恰好是 0**。所以只需把 8 个字节每个的低 5 位拼起来——正是 `Long.compress(word, 0x1F1F1F1F1F1F1F1FL)`（Java 19 加入，对应 x86 PEXT）。用 `VarHandle`（`MethodHandles.byteArrayViewVarHandle(long[].class, BIG_ENDIAN)`）一次读出一个 long，比 8 次 `buf[i]` 拼装快、短。校验用一个 8 次小循环（字母，然后尾部空格）。
4. **`LongTickerMap`**：与 Part 1 同算法，但：
   * `long[] slots` 交错布局（`slots[2i]=key`, `slots[2i+1]=value`）；
   * `0` = 空，`-1` = 墓碑（合法 key 都 > 0，不会混淆）；
   * 哈希 `(key * 0x9E3779B97F4A7C15L) >>> (64 - log2(容量))`（64 位黄金比例常数，取高位）；
   * 比较 `==`；
   * `add` 稳态下**零分配**。

期望 O(1)，常数更小，**零分配**。

### Part 3：完美哈希 `SymbolIndex`

**问题**：Part 2 最坏探测长度不确定，且浪费一半格子。代码集合固定时两样都能消灭。**想法**：hash-and-displace（CHD 简化版）。

1. **分桶**：用哈希把 n 个 key 分到 `r ≈ n/4` 个**桶**（每桶平均 4 个）。
2. **从大桶到小桶**：对一个桶，找一个**位移** `d`（0, 1, 2, …），使桶里**每个** key 的 `slot(hash, d)` 都落在**还没被占的格子**且桶内互不相同；找到就占用，记 `disp[桶] = d`。大桶的所有 key 要同时找到空位，最难，趁表还空先放。
3. **单元素桶最后放**：直接给下一个空格子，位移里存 `~slot`（取反成负数，表示「直接指定的格子，不用再算」）。
4. **查询**：算哈希 → 找桶 → 读 `disp` → 算出格子 → **比较 `keys[slot] == key`**。

```
key ─▶ h = hash(key)
        │
        ├─ bucket = fastrange(h 的高 32 位, r)
        │         d = disp[bucket]
        └─ slot = d<0 ? ~d : slot(h, d, n)        keys[slot] == key ? slot : -1
```

**为什么最后要比较 `keys[slot] == key`**：完美哈希只保证**集合内** key 互不冲突；集合外的 key 也会算出某个格子，必须靠比较发现它不是我们的。

**常见坑**：若第 d 个候选格子取「`h + d × 常数` 缩到 [0, n)」，桶内两个 key 的格子差在所有 d 下几乎固定，小表上差不匹配时**不管试多少个 d 都放不进去**。修正：把 d 搅进 h 再乘大奇数，`slot(h, d, m) = high32((h ^ d·K1) · K2) 缩放到 [0, m)`，不同 d 给出看似独立的格子。「等差序列当一族哈希函数」在大表上碰巧能用，在小表上会死。

**`FrozenTickerMap`** = `SymbolIndex` + `long[] values`。热路径：一次混合哈希、读 `disp`、读 `keys`、写 `values`。更快的路径：**订阅时就 `indexOf` 一次，缓存下标**，之后每条消息 `addAt(下标, qty)`——只剩一次数组写。

构造期望 O(n)（10 万个 key 约 21–50 ms，200 万个约 544 ms）；查询 O(1)，**无探测循环**；内存 keys 8 B + values 8 B + disp 约 1 B（n/4 个 int）= **17 B/条**。

### Part 4：堆外 + 测量

**`OffHeapTickerMap`**：同样的线性探测，数据放 `Arena` 分配的 64 字节对齐内存，每槽 16 字节 `[key][value]`，4 槽正好一条缓存行（x86；Apple M 是 128，只是设计意图）。固定容量（槽数 = ≥ 2×maxEntries 的 2 的幂），满了拒绝新 key。

**测量结果**（12 核，默认 G1 GC；每项 2000 万次更新，5 轮取最好；ns/op，越小越好）：

| 实现 | 8,000 代码 均匀 | 8,000 偏斜 | 2,000,000 均匀 | 2,000,000 偏斜 |
|---|---|---|---|---|
| `HashMap<String,Long>.merge` | 7.7 | 4.8 | 55.4 | 20.0 |
| `TickerMap.add(String)` | 7.9 | 3.3 | 45.3 | 12.8 |
| `LongTickerMap.add(long)`（交错） | 4.0 | 1.3 | 11.1 | 2.0 |
| `SplitLongMap.add`（分离两个数组，对照） | 3.8 | 1.0 | 10.7 | 2.6 |
| `OffHeapTickerMap.add` | 4.1 | 1.4 | 11.8 | 2.1 |
| `FrozenTickerMap.add(long)`（完美哈希） | 2.5 | 2.3 | 13.4 | 3.6 |
| `FrozenTickerMap.addAt(缓存的下标)` | 0.5 | 0.5 | 1.5 | 0.7 |

「偏斜」= 90% 更新落在 64 个热门代码上。内存（200 万条目，key 对象不计）：`HashMap<String,Long>` **64.4 B/条**；`LongTickerMap` **33.6 B/条**；`FrozenTickerMap` **17.0 B/条**。

**怎么读这张表**：

1. **打包成 `long` 是真金白银的胜利**：200 万代码均匀 55.4 → 11.1 ns/op（约 5 倍），内存 64 B → 34 B（还没算 key 的 48 B String）。数据大到放不进缓存时差距最大——`HashMap` 要多次**串行**缓存未命中，我们只要一次。
2. **数据小、放得进缓存时差距小得多**（8,000 代码 7.7 → 4.0）：剩下的是装箱/比较/哈希的指令数。
3. **完美哈希单次 `add` 不比调好的开放寻址快**：8,000 均匀 2.5 vs 4.0（略胜），200 万均匀 13.4 vs 11.1（略输）——一次查找读三个数组（`disp`、`keys`、`values`），`LongTickerMap` 只读一个。**真正收益：确定的最坏情况、最紧凑的内存（17 B vs 34 B），以及能缓存下标**：`addAt` 比任何 `add` 快 5–10 倍（0.5 / 1.5 ns）。「速度来自根本不哈希」。
4. **交错 vs 分离：数据不支持「交错一定更快」**：200 万均匀 11.1 vs 10.7，偏斜 2.0 vs 2.6（交错略好），8,000 偏斜 1.3 vs 1.0（分离略好），差距在噪声内。
5. **装载因子影响很大，而且会悄悄变化**：resize 容量公式改动后（让纯插入时正好翻倍而非翻 4 倍），8,000 个条目落在 16384 格（α ≈ 0.49，之前 α ≈ 0.24），同样代码从 **2.3 ns 变 4.0 ns**。线性探测对 α 极其敏感（2.5 的 Knuth 表：α 从 0.25 到 0.5，成功查找平均探测 1.17 → 1.5）。
6. **堆外没带来速度**（4.1 vs 4.0；11.8 vs 11.1）。好处是**不占堆、GC 看不见、布局可控**；GC 停顿没测，不对「GC 抖动」下定量结论。
7. **没测的**：多线程、真实行情的访问分布、不同 CPU、GC 停顿、ZGC vs G1。

---

## 5. 逐段讲解法

### 5.1 `TickerMap`：数据与哈希

```java
private static final String TOMB = new String("<deleted>");   // identity sentinel
private String[] keys;
private long[] vals;
private int size, tombs, mask, shift;
```

* `new String("<deleted>")` 保证**独一无二的对象**（字面量会被驻留）；比较用 `k == TOMB`（引用相等）而非 `equals`，所以用户存内容也是 `<deleted>` 的 key 不会被误认为墓碑。
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

`while (true)` 不会死循环：表里至少有一个空格即可，而我们保证 `(size + tombs) × 2 ≤ capacity`。

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

* **走完整条探测路才插入**：墓碑只是候选，key 可能在墓碑**后面**，看到墓碑就插会产生两份拷贝。
* **复用墓碑**不改变 size+tombs，不需检查 resize；**占用空格**使已用 +1，所以先检查。rehash 后新表没有墓碑也没有这个 key，直接找空格。
* `Math.addExact` 先算后写：溢出时 `vals[i]` 还是旧值。

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

* 重新哈希因 `shift` 变了；搬时不需比较（旧表 key 已互不相同）。验证：30 万个 key 依次经过、任何时刻只有 10 个活的，容量应保持 ≤ 1024。

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

* `(long) (c - 'A' + 1) << ...`：**先转 `long` 再移位**！`int` 移位量取模 32，超过 31 位会被截断（`ABCDEFGH` 就会暴露）。
* 接受 `CharSequence` 而非 `String`：`StringBuilder` 可直接传。

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

大端（BIG_ENDIAN）读出，第一个字节在最高位，对应第一个字符——与编码方向一致。

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

* 返回值用「`~位置`」编码：**负数 = 没找到，取反是该插入的位置**，一个 `int` 同时带回两样，避免分配结果对象。
* `add`：`int i = locateForInsert(key); if (i >= 0) { slots[2i+1] = addExact(...) } else insertNew(key, delta, ~i);`——只哈希、探测一次（`TickerMap.add` 先 upsert 再 find，多一次探测，为简单；热路径应像这里）。稳态下无 `new`、装箱、lambda 捕获——**零分配**。

### 5.6 `SymbolIndex.tryBuild`

```java
int r = Math.max(1, (n + 3) / 4);                // 桶数 ≈ n/4
long[] h = new long[n];  int[] count = new int[r + 1];
for (int i = 0; i < n; i++) { h[i] = hash(universe[i], seed); count[bucket(h[i], r) + 1]++; }
```

先算每个 key 的哈希并数每桶几个 key，再用**计数排序**把 key 下标按桶分组到 `members[]`（`start[b]..start[b+1]` 是桶 b 的成员），无对象分配。

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

* "先占着再回滚"：同一个 `used[]` 同时检查「格子被别的桶占用」和「桶内两 key 撞同一格」。
* `cursor` 单调向前：单元素桶最后处理，剩下空格子数 = 剩下 key 数，必有空位。
* 构造失败（极罕见）换 `seed` 重来，最多 64 次。

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

`close()` 之后任何 `seg.get` 都抛 `IllegalStateException`——FFM 的内存安全保证（没有悬空指针）。

---

## 6. Java 21 特性小课

### 6.1 record + sealed + 模式匹配 switch + record 模式

`TickerCodec.Parsed` 是**封闭的结果类型**：

```java
public sealed interface Parsed permits Ticker, Invalid {}
public record Ticker(long key) implements Parsed {}
public record Invalid(String reason) implements Parsed {}

return switch (parse(s)) {
    case Ticker(var key) -> key;
    case Invalid(var reason) -> throw new IllegalArgumentException(reason);
};
```

旧写法（Java 8）：返回 `long`，非法时 `-1` 或 `0`（「魔数」，易忘检查）；或抛异常（无法选择「不想抓栈」）。新写法：返回类型说明「有两种可能」，`switch` 必须处理两种（不需 `default`）；`case Ticker(var key)` 同时判断类型和取字段。**不该用**：失败罕见、调用者通常无法处理时异常更简洁。这里选值因为非法输入是常态，且 `parse` 在热路径上。

### 6.2 `switch` 表达式与整数/位小工具

`switch` **表达式**产生一个值，分支可直接 `throw`。位工具：`Integer.numberOfTrailingZeros(capacity)`（2 的幂时就是 log₂）、`Integer.highestOneBit(x)`（向上取整到 2 的幂：`highestOneBit(x - 1) << 1`）、**`Long.compress(x, mask)`**（Java 19）把 `x` 中 `mask` 为 1 的比特按顺序拼到低位，例 `Long.compress(0b1010_1100L, 0b1111_0000L)` = `0b1010`。旧写法要手写 8 次「取字节、掩码、移位、或」，现在一条（x86 上 JIT 成 PEXT）。

### 6.3 `VarHandle` 读字节数组

```java
private static final VarHandle BE_LONG = MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN);
long word = (long) BE_LONG.get(buf, off);
```

旧写法 `ByteBuffer.wrap(buf).getLong(off)`（要分配或复用 `ByteBuffer`）或手写 8 次移位。`byteArrayViewVarHandle` 把 `byte[]` 看成 `long[]` 视图，直接读 8 字节，**自带边界检查**，不分配对象，JIT 内联成一次读取。`VarHandle` 还用于并发原子操作（本题未用）。

### 6.4 FFM API：`Arena` / `MemorySegment`（预览）

预览特性，编译运行都要 `--enable-preview`（Java 22 转正，API 小有变化）。旧写法 `sun.misc.Unsafe` 能直接读写内存但**无任何安全检查**，越界即 JVM 崩溃；新写法有边界和生命周期检查，`Arena.close()` 之后访问抛异常而不崩溃。**不该用**：数据能放堆里且 GC 不是瓶颈时，堆内数组更简单（本题测量里堆外并不更快）。

### 6.5 JIT / GC 基础（口头题）

**JIT**：先解释执行，热点方法编译成机器码（后台线程做，所以基准要预热）；**逃逸分析**能把「不逃出方法的对象」优化掉，很可能是 `HashMap.merge` 平均只分配 14.8 字节而非 24 的原因。**Generational ZGC**（JEP 439）是亚毫秒停顿的低延迟 GC；`Bench` 用默认 G1，换 ZGC 数字会不同。

---

## 7. 追问预演

**问：`HashMap` 为什么每次翻倍？为什么容量是 2 的幂？**
* 翻倍 → 摊还 O(1)（2.7）；2 的幂 → 用 `&` 代替 `%`（2.2）。
* 说出口：「翻倍使总搬运量小于 2n，摊到每次插入是常数；2 的幂让取下标变成一次与运算。」

**问：开放寻址和链地址怎么选？**
* 链地址：简单、装载因子可 > 1、删除简单；但每条目一次分配 + 指针追逐，缓存差。开放寻址：连续、缓存友好、无分配；但装载因子要低（≤ 0.5–0.75）、删除麻烦、对哈希质量敏感。
* 说出口：「读多写少、key 小、追求延迟选开放寻址；key 大、写多、删除多或要保证最坏情况，链地址（或树化）更稳。」

**问：删除怎么做？墓碑有什么问题？**
* 不能置空（断探测链）；墓碑累积使探测变长 → 把墓碑算进装载因子触发 rehash 清掉；替代：回移删除。
* 说出口：「留墓碑，查找跳过、插入复用，装载因子把墓碑也算进去，rehash 时清掉。」

**问：怎么测量哈希函数好不好？**
* 看最长/平均探测距离和分布；用真实 ticker 集合而非随机字符串；对连续的三字母代码等结构化输入压测（最易暴露哈希弱点）。

**问：怎么知道你的版本更快？**
* 同机同次运行、预热、多轮取最好、防死代码消除；变化数据规模（放得进缓存 vs 放不进）和访问分布（均匀 vs 偏斜）；报告**没测到**的（多线程、GC、真实数据）；严肃发表用 JMH。
* 说出口：「8000 和 200 万两个规模、均匀和偏斜各测一遍，打包 key 大规模快约 5 倍，小规模只快 2 倍；多线程和 GC 没测。」

**问：完美哈希一定比普通哈希快吗？**
* 不一定：构造耗时、查询读多个数组；收益在最坏情况确定、内存紧凑、可缓存下标，单次 `add` 并没稳定比 `LongTickerMap` 快。
* 说出口：「完美哈希给的是确定性和紧凑，不是魔法加速；真加速来自缓存下标后直接数组访问。」

**问：key 变多了、多线程更新怎么办？**
* 每线程一张表（单写者）+ 定期合并（完美哈希下就是逐下标相加）；或分片加锁；或 `LongAdder` / `VarHandle.getAndAdd` 原子累加（完美哈希下 value 数组固定、不 resize，**很自然**）。热点冲突多时改每线程一张再合并。

**问：key 不止 8 个字符（如 `BRK.B`、期权代码）？**
* 扩展字符集或用两个 long（128 位）；或回退到字符串哈希（FNV-1a / xxHash）+ 字节数组比较；热路径始终避免 `new String`。

---

## 8. 常见误区

| 很多人会这样写 | 为什么错 | 正确写法 |
|---|---|---|
| 下标 = `hashCode() & mask` | 低位分布不均，短代码扎堆；打包后的 key 低位全 0，所有 key 撞一格（最长探测 17575） | 乘法哈希（Fibonacci）取高位，或 `h ^ (h >>> 16)` |
| 删除时 `keys[i] = null` | 断探测链，后面的 key 查不到 | 放墓碑；查找跳过；rehash 清理 |
| 遇到墓碑就插入 | key 可能在墓碑后面，导致重复 key | 走完整条探测路，记下第一个墓碑，没找到才复用 |
| 装载因子不算墓碑 | 反复插入/删除后表里没有空格，查不存在的 key 死循环 | `(活 + 墓碑 + 1) × 2 > 容量` 就 rehash |
| `(c - 'A' + 1) << 35`（没转 long） | `int` 移位量取模 32，`<< 35` 实际 `<< 3` | `(long) (c - 'A' + 1) << 35` |
| 用 `0` 当「不存在」返回值 | 累计量本可是 0，分不清 | `OptionalLong` / `containsKey` / `get(k, ifAbsent)` |
| 完美哈希的 `indexOf` 不比较原始 key | 集合外的 key 也算出一个格子，被误认为集合内 | 读出 `keys[slot]` 比较 `== key` |
| 用等差序列 `h + d·c` 当一族哈希函数 | 小表上桶内 key 的格子差固定，永远放不进 | 把 d 搅进 h 再乘大奇数 |
| 微基准只跑一次、不预热、结果不用 | 测到的是解释执行/被 JIT 删掉的代码 | 预热 + 多轮取最好 + 使用结果；严肃测量用 JMH |
| 「堆外一定更快」「交错布局一定更快」 | 测量都没稳定支持 | 先测量再宣称 |

---

## 9. 自测题

1. 线性探测下，α = 0.75 时查找一个**不存在**的 key 平均探测几次？α = 0.5 呢？为什么线性探测的 α 要压得比链地址法低？
2. 容量 8 的表里，`A`（家 3）、`B`（家 3）、`C`（家 4）依次插入，各住哪一格？删除 `A` 后若不用墓碑直接置空，会发生什么？
3. 为什么 resize 必须把所有条目重新哈希，而不能直接把数组复制到更大的数组里？
4. 把 `"AB"` 打包成 `long`，写出十六进制值（本题编码）。再说 `"AB"` 和 `"AB "`（带尾部空格）在 `pack` 与 `packWire` 里分别怎么处理。
5. 若把 `LongTickerMap` 的哈希改成 `(int) key & mask`，对 `"AAPL"` 和 `"AAPM"` 会怎样？
6. 小编程：写 `static int log2(int powerOfTwo)`（不用循环和 `Math.log`），再写 `nextPowerOfTwo(int x)`（≥ x 的最小 2 的幂，x ≥ 1）。
7. `SymbolIndex` 里为什么单元素的桶要最后处理？先处理会怎样？

<details><summary>答案</summary>

1. α = 0.75：`(1 + 1/(1−0.75)²)/2 = 8.5` 次；α = 0.5：2.5 次。线性探测有聚集，α 接近 1 时探测次数按 1/(1−α)² 增长；链地址法冲突只影响同一条链，α = 1 时平均链长也只有 1。
2. `A` 住 3，`B` 家 3 被占 → 住 4，`C` 家 4 被占 → 住 5。删除 `A` 后若置空：查 `C` 从 4 开始（`B` 不是它）→ 5 找到，没出错；但查 `B`：家 3 → 空格 → 误判不存在。有墓碑就不会。
3. 下标由哈希值的**高位**（或低位）决定，数组大小变了 → `shift`/`mask` 变了 → 同一个 key 的下标变了。直接复制，key 待在错误位置，从新的家出发找不到。
4. `'A'=1, 'B'=2` → `(1<<35) | (2<<30)` = `0x800000000 | 0x80000000` = `0x880000000`。`pack("AB ")` → `Invalid`（空格不是 A–Z）；`packWire("AB      ")` 合法，等于 `pack("AB")`（尾部空格是 wire 格式的补位）。
5. `"AAPL"` 与 `"AAPM"` 只差第 4 个字段（`[20..24]` 比特），而 `& mask`（mask 通常 ≤ 2²⁰）只看最低位，这两个 key 的低位全是 0 → 都落在下标 0 → 冲突。所有 ≤ 6 个字符的代码低 10 比特都是 0。
6. `Integer.numberOfTrailingZeros(powerOfTwo)`；`nextPowerOfTwo(x) = x == 1 ? 1 : Integer.highestOneBit(x - 1) << 1`（x ≤ 2³⁰）。
7. 单元素桶的格子是「直接指定」的，放哪都行；大桶需要多个位置**同时**为空，越晚越难（表越满，成功概率按 `(空闲比例)^桶大小` 下降）。先放单元素会吃掉空格子，后面的大桶可能永远找不到合适位移。

</details>

---

「延伸」Sedgewick《算法》第 3.4 节「散列表」。
