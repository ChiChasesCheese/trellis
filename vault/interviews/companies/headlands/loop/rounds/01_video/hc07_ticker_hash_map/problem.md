# hc07 · 股票代码哈希表（design an optimized hash map for stock tickers）

股票代码（ticker）是至多 8 个大写字母的短字符串，交易系统要拿它反复查表。这个任务从最普通的 `HashMap<String, Long>` 出发，一步步把它优化成更小更快的表：自己写开放寻址哈希表、把代码打包进一个 `long`、用完美哈希消灭冲突，最后谈堆外内存和怎么测量。key 的结构特殊，这个特点就是优化的突破口。

## 读题前你需要知道

* **哈希表**是怎么做到「几乎 O(1) 查找」的：哈希函数（hash function）、冲突（collision）、链地址法（chaining）vs 开放寻址（open addressing）、装载因子（load factor）、为什么要 resize；
* 线性探测下**删除为什么要留墓碑**（tombstone）；
* **CPU 缓存行**（cache line）和**指针追逐**（pointer chasing）：为什么「把数据排紧」比「少做几次运算」更重要；
* Java 的 `HashMap<String, Long>` 每个条目背后有多少个对象、**装箱**（boxing）是什么；
* **完美哈希**（perfect hashing）：key 集合固定时，能不能做到「零冲突」。


## 背景

行情系统里到处是「按股票代码（ticker）累加/查找」：每个 ticker 的累计成交量、最新价、持仓……每秒几百万次。
Java 里最直接的写法是 `HashMap<String, Long>`。面试官会让你先自己写一个哈希表（证明你懂原理），然后问：**如果 key 是股票代码，你还能做得更好吗？**

股票代码的结构很特别：**至多 8 个大写 ASCII 字母**（`AAPL`、`MSFT`、`BRKB`；真实的 `BRK.B` 这类带点的不在讨论范围）。
这个结构就是优化的突破口。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `TickerMap`（key = `String`，value = `long`） | 手写开放寻址 + 线性探测哈希表：put / get / add / remove，墓碑，resize |
| 2 | `TickerCodec` + `LongTickerMap` | 利用「≤ 8 个大写字母」把代码**打包进一个 `long`**，key 变成原始类型，不分配、不装箱；报文字段直接解析 |
| 3 | `SymbolIndex` + `FrozenTickerMap` | 开盘前就知道全部代码 → **最小完美哈希**，零冲突，value 放进长度恰好 n 的数组 |
| 4 | `OffHeapTickerMap` + `Bench` | 堆外定长表（FFM `Arena`），缓存行对齐；**自己测量**：布局、负载、装箱、缓存 |

所有 value 都是 `long`（比如累计成交量）。签名以 starter 为准，这里只写语义。

## Part 1 · 手写哈希表 `TickerMap`

不许用 `HashMap` / `Map` 做存储。

| 方法 | 语义 |
|---|---|
| `TickerMap()` · `TickerMap(int expectedSize)` | `expectedSize < 0` → `IllegalArgumentException`；预留容量，放 `expectedSize` 条不需要 resize |
| `size()` · `capacity()` · `tombstones()` | 活条目数 · 格子总数 · 墓碑数（诊断用） |
| `containsKey(k)` · `get(k)` → `OptionalLong` | 不存在 `empty`；value 为 0 也是存在 |
| `put(k, v)` → `OptionalLong` | 返回旧值（没有则 `empty`） |
| `add(k, delta)` → `long` | `value += delta`，不存在当作 0，返回新值；溢出 `ArithmeticException` 且表不变 |
| `remove(k)` → `OptionalLong` | 返回被删的值 |
| `forEach(ObjLongConsumer<String>)` | 每个活条目恰好访问一次 |
| `maxProbeLength()` | 所有活 key 里离自己「家」最远的距离（0 = 都在家）；聚集越严重越大 |

* `key == null` → `NullPointerException`；空字符串 `""` 是普通 key。
* 要求：开放寻址 + 线性探测；**（占用 + 墓碑）/ 容量 ≤ 3/4** 在任何操作之后都成立；删除用墓碑，resize 时清掉墓碑；
  反复「插入新 key、删旧 key」时容量不能无限增长，也不能死循环（表里必须始终留有空格）。
* 陷阱：1024 个 `hashCode()` **完全相同**的字符串（`"Aa"` 和 `"BB"` 的 hashCode 相等，拼起来仍相等）必须仍然正确（慢一点没关系）。

## Part 2 · 打包进一个 `long`：`TickerCodec` + `LongTickerMap`

### 编码（测试会检查具体的值）

`'A'..'Z'` → `1..26`，每个字符 **5 比特**；第 i 个字符（i 从 0 起）放在第 `[35−5i, 39−5i]` 比特；不足 8 个字符的尾部补 0。结果总是 `> 0` 且 `< 2⁴⁰`。

```
"AAPL" -> 00001 00001 10000 01100 00000 00000 00000 00000   = (1<<35)|(1<<30)|(16<<25)|(12<<20)
```

| 方法 | 语义 |
|---|---|
| `parse(CharSequence)` → `Parsed` | `sealed Parsed permits Ticker(long key), Invalid(String reason)`；null / 空 / 超过 8 个字符 / 含非 A–Z 字符 → `Invalid` |
| `pack(CharSequence)` → `long` | 同 `parse`，非法时抛 `IllegalArgumentException` |
| `isValidKey(long)` · `unpack(long)` → `String` | `unpack` 对非法 key（≤ 0、≥ 2⁴⁰、字段 > 26、第一个 0 字段之后又有字符）抛 `IllegalArgumentException` |
| `packWire(byte[] buf, int off)` → `long` | 行情报文里的代码字段：**8 个字节，大写字母 + 右侧补空格**，如 `"AAPL    "`。非法（全空格、前导空格、中间空格、小写、非字母）→ `IllegalArgumentException`；`off+8 > buf.length` 或 `off < 0` → `IndexOutOfBoundsException` |

### `LongTickerMap`

key 是打包好的 `long`（**必须 > 0**，否则 `IllegalArgumentException`），value 是 `long`。开放寻址 + 线性探测 + 墓碑，装载因子 ≤ 3/4。

`size()` · `capacity()` · `tombstones()` · `containsKey(k)` · `get(k, ifAbsent)` → `long` · `put(k, v)` → `boolean`（`true` = 新 key）· `add(k, delta)` → `long`（溢出 `ArithmeticException` 且不改值）· `remove(k)` → `boolean` · `forEach(LongLongConsumer)` · `maxProbeLength()`。

* **稳态下 `add` / `get` 零分配**（测试用 `ThreadMXBean.getThreadAllocatedBytes` 检查：预热后 160 万次 `add` 分配 < 256 KB；对照 `HashMap<String,Long>.merge` 要分配 > 8 MB）。
* **哈希函数不能写成 `key & mask`**：打包后短代码的低位全是补的 0，几乎所有 key 会落到同一格。测试用全部 17576 个三字母代码检查最长探测距离 ≤ 64。
* 提示：把 key 和 value 放进同一个 `long[]`（交错布局），一次缓存行就拿到两样。

## Part 3 · 完美哈希：`SymbolIndex` + `FrozenTickerMap`

场景：开盘前就知道今天会出现的全部代码（比如 8000 个）。

* `SymbolIndex.build(long[] universe)`：universe 里每个 key `> 0` 且互不相同（否则 `IllegalArgumentException`；空集合合法）。
  `indexOf(key)`：集合内的 key **一一映射到 `0..n−1`**（最小完美哈希），集合外的 key（包括 ≤ 0）返回 `−1`；`keyAt(index)` 是反函数；`size()`。
  必须在 100,000 个 key 上 2 秒内建好；2,000,000 个 key 也能建（参考解约 0.5 秒）。
* `FrozenTickerMap(Collection<String> universe)`：代码按 `TickerCodec` 格式，有非法或重复 → `IllegalArgumentException`。所有 value 初始为 0（**在 universe 里但还没写过 = 0，不是 absent**）。
  `size()` · `indexOf(key)` · `containsKey` · `get(key, ifAbsent)` · `put(key, v)` → `boolean`（不在 universe 里返回 `false`）·
  `add(key, delta)` → `long`（不在 universe 里抛 `IllegalArgumentException`；溢出 `ArithmeticException` 且不改值）·
  **`addAt(int index, long delta)` / `getAt(int)` / `keyAt(int)`**：行情订阅时把代码解析成下标缓存起来，之后每条消息直接用下标。
* 热路径零分配；2000 万次 `add` < 2 秒。
* 提示：hash-and-displace（CHD 的简化）；**别忘了在 `indexOf` 里比较 `keys[slot] == key`**——完美哈希只保证集合内的 key 不冲突，集合外的 key 也会被映射到某个格子。

## Part 4 · 堆外与测量：`OffHeapTickerMap` + `Bench`

* `OffHeapTickerMap(int maxEntries)`（`AutoCloseable`）：用 FFM 的 `Arena` / `MemorySegment` 在堆外分配一整块，**64 字节对齐**，每个槽位 16 字节 `[key:8][value:8]`，`key == 0` 表示空格。
  固定容量：槽位数 = 不小于 `2·maxEntries` 的 2 的幂；`maxEntries` 个 key 放满之后，再插入**新** key → `IllegalStateException`，已有 key 仍可更新。没有 `remove`、没有 `resize`。
  `size()` · `capacity()` · `maxEntries()` · `containsKey` · `get(k, ifAbsent)` · `put(k, v)` → `boolean` · `add(k, delta)` → `long` · `close()`（可重复调用；之后任何访问 → `IllegalStateException`）。
  `key ≤ 0` → `IllegalArgumentException`；`maxEntries ∉ [1, 2²⁸]` → `IllegalArgumentException`。必须能从**别的线程**访问（所以用 `Arena.ofShared()`）。
* `Bench`：把同一串更新（8,000 个 ticker 和 2,000,000 个 ticker；均匀访问和偏斜访问）喂给 `HashMap<String,Long>` / `TickerMap` / `LongTickerMap` / 分离布局的对照实现 / `OffHeapTickerMap` / `FrozenTickerMap`（查表 / 缓存下标），打印 ns/op 和每条记录的字节数。
  **面试里被问「你怎么知道更快」时，要能说出怎么测、测到了什么、哪些结论没有测。**

## 边界清单（隐藏测试多半打这些）

空表、`""` 作 key、value 为 0 / 负数 / `Long.MIN_VALUE`；`null` key；同一 `hashCode` 的一大批字符串；删除探测链的**中间**和**头部**之后查后面的 key；删除后重新插入同一个 key（复用墓碑）；
一直插入新 key + 删除旧 key（墓碑清理）；resize 之后所有 key 仍在；`add` 溢出且不改值；`Long.MAX_VALUE` 作 key；
打包：1 个字符 / 8 个字符 / 9 个字符 / 小写 / 数字 / 全角字母；报文字段里的前导空格 / 中间空格 / 全空格 / `\0`；
完美哈希：0、1、2 个 key；全部 17576 个三字母代码（结构化输入）；集合外的 key；重复 key。

## 相关变体

* C++ 版：`std::unordered_map` 的链地址法（每个桶一个链表，节点单独分配）→ 追问冲突与内存开销 → 换成开放寻址 / `flat_hash_map`（和 Part 1、2 同构）；
* 「key 不止 8 个字符怎么办？」→ 128 位 key（两个 `long`）、或者 FNV / xxHash 之类的字符串哈希 + 字节比较；
* 「多线程更新同一张表怎么办？」→ 分片（每个线程一张表，最后合并）、`LongAdder`、或者无锁的原子 CAS；这里不含；
* 「你怎么证明你的哈希函数好？」→ 看最长探测距离、平均探测次数、用真实数据（而非随机数据）测。

## 考什么

不是背 `HashMap` 的源码，而是**从原理出发的工程判断**：能不能把冲突处理、装载因子、删除、扩容讲清楚并写对；
能不能指出通用方案的代价（装箱、指针追逐、每个条目几十字节）；能不能利用输入的结构（≤ 8 个大写字母 → 一个 `long`）；
知道「key 集合固定」是一个可以再榨一次的条件（完美哈希）；以及最重要的——**说出自己怎么测量，而不是凭感觉**。
