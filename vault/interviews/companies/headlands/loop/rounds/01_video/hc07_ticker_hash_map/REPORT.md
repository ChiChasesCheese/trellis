# hc07 · 思路与追问

## 概要

「为股票代码设计 / 优化哈希表」的原题是 C++ `unordered_map`，Java 版对应 `HashMap<String, Long>`。
面试官真正想看的是四件事：能不能自己写对一个哈希表（冲突 / 删除 / 扩容）；能不能说出通用方案的代价（装箱、指针追逐、每条目几十字节）；能不能利用输入结构（≤ 8 个大写字母 → 一个 `long`）；以及**能不能说出自己怎么测量**。

## 逐 Part 思路

1. **`TickerMap`（String → long）**：并行数组 `String[] keys` / `long[] vals`；容量 2 的幂，下标 = `(hashCode * 0x9E3779B9) >>> shift`（Fibonacci hashing）；`null` = 空格，哨兵对象 `TOMB` = 墓碑（`==` 比较）。
   插入走完整条探测路并记下第一个墓碑；占用空格前检查 `(size + tombs + 1) × 2 > cap` → rehash（新容量 = 活条目 × 4，墓碑消失）。`add` 用 `addExact`，先算后写。
2. **`TickerCodec` + `LongTickerMap`**：5 比特 / 字符，8 个字符放进低 40 比特，尾部补 0，合法 key 恒 > 0（0 = 空格，−1 = 墓碑）；`parse` 返回 sealed `Parsed`；`packWire` 用 `VarHandle` 读 8 字节 + `Long.compress` 拼低 5 位。
   `LongTickerMap` 用交错的 `long[]`、64 位 Fibonacci 哈希、`locateForInsert` 返回 `~插入位置` 把「找没找到」和「位置」装进一个 `int`，稳态 `add` 零分配。
3. **`SymbolIndex` + `FrozenTickerMap`**：hash-and-displace（CHD 简化）。桶数 ≈ n/4，计数排序分桶，按桶大小从大到小为每个桶找位移 `d`，单元素桶最后直接分配剩余格子（位移存 `~slot`）；`indexOf` 末尾比较 `keys[slot] == key` 识别集合外的 key。
   `FrozenTickerMap` = `SymbolIndex` + `long[] values`；`indexOf` / `addAt` 让调用方缓存下标。
4. **`OffHeapTickerMap` + `Bench`**：`Arena.ofShared()` 分配 64 字节对齐的一整块，16 字节槽 `[key][value]`，固定容量（槽数 ≥ 2·maxEntries），满了拒绝新 key；`close()` 幂等。`Bench` 对七种实现做 ns/op 与 B/条测量。

## 隐藏测试会打的坑

* 下标 = `hashCode & mask`；对打包 key 用 `key & mask`（低位全是补的 0，17576 个三字母代码最长探测 17575）。
* 删除置 `null` 断探测链；遇到墓碑就插入造成重复 key；装载因子不算墓碑 → 反复插入 / 删除后表里无空格，查找不存在的 key 死循环。
* 1024 个 `hashCode` 完全相同的字符串（`"Aa"` / `"BB"` 拼接）；删除探测链头部 / 中间后查后面的 key；删除后重插同一个 key 不能增长容量。
* `add` 溢出必须不改表；value = 0 / `Long.MIN_VALUE` 不是「不存在」。
* 位运算：`(c - 'A' + 1) << 35` 没转 `long`（`int` 移位量取模 32）；`packWire` 把前导空格 / 中间空格 / `\0` / 全空格当合法。
* `SymbolIndex`：不比较原始 key（集合外的 key 被误认）；用等差序列做哈希族，小表上永远放不进去；重复 / 非正 key 没拒绝。
* `OffHeapTickerMap`：用 `Arena.ofConfined()`（在别的线程里访问会 `WrongThreadException`）；`close()` 之后没有抛异常；`close()` 第二次抛异常。

## 复杂度

n = 条目数。基准：默认 G1，每项 2000 万次更新，5 轮取最好：

| 实现 (ns/op) | 8,000 代码 均匀 | 偏斜 | 2,000,000 均匀 | 偏斜 | 内存 B/条（200 万，key 对象不计） |
|---|---|---|---|---|---|
| `HashMap<String,Long>.merge` | 7.7 | 4.8 | 55.4 | 20.0 | 64.4（分配字节，预分配） |
| `TickerMap.add(String)` | 7.9 | 3.3 | 45.3 | 12.8 | — |
| `LongTickerMap.add(long)` | 4.0 | 1.3 | 11.1 | 2.0 | 33.6（分配字节，预分配） |
| `SplitLongMap`（对照：分离两个数组） | 3.8 | 1.0 | 10.7 | 2.6 | — |
| `OffHeapTickerMap.add` | 4.1 | 1.4 | 11.8 | 2.1 | 33.5（槽数取 ≥ 2·maxEntries 的 2 的幂 = 4,194,304 × 16 B，算出） |
| `FrozenTickerMap.add(long)` | 2.5 | 2.3 | 13.4 | 3.6 | 17.0（数组大小算出） |
| `FrozenTickerMap.addAt(缓存下标)` | 0.5 | 0.5 | 1.5 | 0.7 | 同上 |

其他数据（预热后）：`SymbolIndex.build` 10 万 key 21–51 ms、200 万 key 544 ms；`TickerMap` 20 万个代码上 100 万次 `add` 42–48 ms；
预热后 160 万次更新的分配量：`HashMap<String,Long>.merge` 约 14.8 B/次（≈ 24 MB），`LongTickerMap.add` / `FrozenTickerMap.add` / `OffHeapTickerMap.add` 都 < 256 KB。
`String("AAPL")` = 48 B、`Long` = 24 B；最长探测距离：10 万个随机代码，`TickerMap` 17、`LongTickerMap` 20（容量 262144）。

**怎么读这些数字、哪些结论没有被数据支持**：
* 打包成 `long` 是实打实的胜利（大数据下约 5 倍、内存约一半）；
* 完美哈希的**单次 `add`** 没有稳定地比调好的开放寻址快，它的收益是确定性 + 紧凑 + 可缓存下标（`addAt` 快一个数量级）；
* 交错 vs 分离布局：运行间噪声大，**不能**宣称交错更快；堆外没有更快；
* 装载因子影响显著：同一份 `LongTickerMap` 代码，仅因 resize 公式改动使 8000 条目的 α 从 0.24 变到 0.49，ns/op 从 2.3 变到 4.0；
* **没测**：多线程、GC 停顿、真实行情分布、其他 CPU。

## Java 21 特性

| 特性 | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| record | `TickerCodec.Ticker(long key)` / `Invalid(String reason)` | 不可变值对象，`equals` 白送，测试直接 `assertEquals(new Ticker(…), parse("AAPL"))` |
| sealed | `Parsed permits Ticker, Invalid` | 「合法 / 非法」封闭成一个类型，调用方必须处理两种；比返回 `-1` 魔数或抛异常更诚实 |
| 模式匹配 switch + record 模式 | `pack`：`case Ticker(var key) -> key; case Invalid(var reason) -> throw …` | 判断类型 + 取字段 + 穷尽性检查一步完成，无 `default` |
| switch 表达式 | 同上，分支直接 `throw` / 产生值 | 无 fallthrough |
| 位工具与数学 | `Long.compress`（拼 wire 字段的低 5 位）、`Integer.numberOfTrailingZeros` / `highestOneBit`（2 的幂容量与 log₂）、`Math.addExact`（累加溢出） | `compress` 一条代替 8 次移位掩码；`addExact` 溢出抛异常而不是回绕 |
| `VarHandle` | `TickerCodec.packWire`：`byteArrayViewVarHandle(long[].class, BIG_ENDIAN)` | 把 `byte[]` 当 `long[]` 读，自带边界检查，不分配 `ByteBuffer` |
| FFM `Arena` / `MemorySegment`（预览） | `OffHeapTickerMap`：`Arena.ofShared()`、`allocate(bytes, 64)`、`get/set(JAVA_LONG, offset)` | 堆外、对齐可控、有边界与生命周期检查（`close` 后访问抛异常，而不是 `Unsafe` 那样直接崩溃） |
| 运行时 | `Bench` 的预热 / 取最好 / 防死代码消除；`ThreadMXBean` 分配量测试；逃逸分析与 Generational ZGC 的口头讨论 | 用测量回答「更快吗」 |

## 面试官可能的追问

1. **链地址 vs 开放寻址怎么选？** 开放寻址：连续内存、缓存友好、无逐条目分配，但装载因子要低、删除要墓碑 / 回移、对哈希质量敏感；链地址：实现和删除简单、能容忍高装载因子，但指针追逐。读多写少、key 小、要低延迟选开放寻址。
2. **删除怎么做？墓碑的问题？** 不能置空（断探测链）；墓碑 + 装载因子把墓碑算进去 + rehash 时清理；替代方案是回移删除（不留墓碑，更复杂）。
3. **为什么容量是 2 的幂、为什么每次翻倍？** `&` 代替 `%`；翻倍使总搬运 < 2n（摊还 O(1)）。
4. **怎么证明你的哈希函数好？** 测最长 / 平均探测距离，用真实代码集合和结构化输入（连续的三字母代码、打包后低位全 0 的 key），不要只用随机串。
5. **打包 key 以后 `key & mask` 为什么不行？** 低 20 位在 ≤ 4 个字符时全是补的 0，所有短代码落同一格；用乘法哈希取高位。
6. **完美哈希一定更快吗？** 不一定（单次 `add` 没有稳定胜出）；收益是最坏情况确定、内存紧凑、可缓存下标。
7. **多线程更新怎么办？** 每线程一张表 + 合并；完美哈希下 value 数组固定、不 resize，可以用 `VarHandle`（`arrayElementVarHandle`）对元素原子累加；热点冲突时再分片。
8. **key 不止 8 个字符 / 含 `.` 和数字？** 扩字符集或用两个 `long`；或字符串哈希（FNV-1a / xxHash）+ 字节比较；热路径避免 `new String`。
9. **堆外比堆内快吗？** 没有；它的好处是 GC 不可见、布局可控，代价是手动 `close`、无自动扩容。
