---
id: hl-hc07-what-asked
node: problems.hc07-ticker-hash-map
type: qa
step: 1
---
## Q
股票代码哈希表题（design an optimized hash map for stock tickers）的追问路线和四个 Part 是什么？

## A
场景：行情系统每秒几百万条消息，按股票代码（ticker，**至多 8 个大写 ASCII 字母**，如 `AAPL`）累加 / 查找成交量。默认答案 `HashMap<String, Long>`。追问路线：
1. 「自己写一个哈希表」→ 原理（Part 1）：`TickerMap`，开放寻址 + 线性探测，`put/get/add/remove`，墓碑，resize；装载因子（占用 + 墓碑）/ 容量 ≤ 3/4；
2. 「代码最多 8 个大写字母，还能更好吗」→ 利用输入结构（Part 2）：`TickerCodec` + `LongTickerMap`，打包进一个 `long`，不分配、不装箱；
3. 「开盘前就知道今天所有代码呢」→ 完美哈希（Part 3）：`SymbolIndex` + `FrozenTickerMap`，最小完美哈希，零冲突；
4. 「怎么知道更快、内存、缓存」→ 堆外与测量（Part 4）：`OffHeapTickerMap` + `Bench`。

所有 value 是 `long`。`TickerMap` 要求：`null` key → `NullPointerException`，`""` 是普通 key；`get` 返回 `OptionalLong`（value 为 0 也是存在）；`add` 溢出抛 `ArithmeticException` 且表不变；1024 个 `hashCode` 完全相同的字符串（`"Aa"` 和 `"BB"` 拼接）必须仍然正确。

考的不是背 `HashMap` 源码，而是从原理出发的工程判断：写对冲突 / 删除 / 扩容；指出通用方案的代价（装箱、指针追逐、每条目几十字节）；利用输入结构；key 集合固定是可再榨一次的条件；最重要的是**说出自己怎么测量**。
