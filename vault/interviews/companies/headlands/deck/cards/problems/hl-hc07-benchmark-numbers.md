---
id: hl-hc07-benchmark-numbers
node: problems.hc07-ticker-hash-map
type: qa
step: 15
---
## Q
几种实现的实测数字（ns/op 和 B/条）是什么？哪些结论被数据支持，哪些没有？

## A
12 核、默认 G1，每项 2000 万次更新取 5 轮最好（ns/op；偏斜 = 90% 更新落在 64 个热门代码）：
| 实现 | 8k 均匀 | 8k 偏斜 | 200 万均匀 | 200 万偏斜 |
|---|---|---|---|---|
| `HashMap<String,Long>.merge` | 7.7 | 4.8 | 55.4 | 20.0 |
| `TickerMap.add(String)` | 7.9 | 3.3 | 45.3 | 12.8 |
| `LongTickerMap.add(long)` | 4.0 | 1.3 | 11.1 | 2.0 |
| `FrozenTickerMap.addAt`（缓存下标） | 0.5 | 0.5 | 1.5 | 0.7 |

另有：`OffHeapTickerMap` 4.1/1.4/11.8/2.1；`FrozenTickerMap.add(long)` 2.5/2.3/13.4/3.6；分离布局 3.8/1.0/10.7/2.6。内存（200 万条，key 对象不计）：`HashMap` 64.4 B，`LongTickerMap` 33.6 B，`OffHeap` 33.5 B，`FrozenTickerMap` 17.0 B。

**读法**：
1. 打包成 `long` 是真金白银的胜利：200 万均匀 55.4 → 11.1（约 5 倍），内存约一半；数据放不进缓存时差距最大（`HashMap` 多次串行未命中）；
2. 数据放得进缓存时差距小得多（7.7 → 4.0）；
3. 完美哈希的**单次 `add`** 没稳定胜出，收益是确定性 + 紧凑 + `addAt` 快一个数量级（「速度来自根本不哈希」）；
4. 交错 vs 分离：运行间噪声大，**不能**宣称交错更快；堆外没更快；
5. 装载因子影响很大（α 0.24→0.49 使 2.3→4.0 ns）；
6. **没测**：多线程、GC 停顿、真实行情分布、其他 CPU、ZGC vs G1。

其他：`SymbolIndex.build` 10 万 key 21–51 ms、200 万 544 ms；预热后 160 万次更新分配：`HashMap.merge` 约 14.8 B/次，其余 < 256 KB。`String("AAPL")` 48 B，`Long` 24 B；10 万随机代码最长探测距离 `TickerMap` 17、`LongTickerMap` 20。
