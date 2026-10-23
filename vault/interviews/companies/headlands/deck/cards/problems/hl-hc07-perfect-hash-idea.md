---
id: hl-hc07-perfect-hash-idea
node: problems.hc07-ticker-hash-map
type: qa
step: 12
---
## Q
完美哈希（perfect hashing）和最小完美哈希是什么？适用条件、好处与代价是什么？

## A
key 集合**事先固定**（如开盘前就知道今天的 8000 个代码）时，可花启动时间找到对这个集合**零冲突**的哈希函数；**最小**完美哈希更进一步：n 个 key 恰好映射到 `0..n−1`，无空格。

好处：
- 查找确定 O(1)，无探测循环（最坏情况确定）；
- 内存最紧凑：value 放长度恰为 n 的数组；200 万条目约 17 B/条，对比 `LongTickerMap` 33.6 B、`HashMap` 64.4 B；
- 可把「key → 下标」**缓存**：订阅行情时 `indexOf` 一次，之后每条消息 `addAt(下标, qty)` 直接访问数组，连哈希都省了。

代价：key 集合不能变（新代码上市要重建）；构造要时间（10 万 key 约 21–51 ms，200 万约 544 ms）；集合外的 key 要能识别（仍保存原始 key 比较）。

`SymbolIndex` API：`build(long[] universe)`（每个 key > 0 且互不相同，否则 `IllegalArgumentException`；空集合合法），`indexOf(key)` 集合内一一映射到 `0..n−1`、集合外（含 ≤ 0）返回 −1，`keyAt(index)` 反函数，`size()`。

`FrozenTickerMap(Collection<String> universe)`：非法或重复 → `IllegalArgumentException`；**在 universe 里但还没写过 = 0，不是 absent**；`put` 不在 universe 返回 `false`；`add` 不在 universe 抛 `IllegalArgumentException`；`addAt/getAt/keyAt(int)`。热路径零分配，2000 万次 `add` < 2 秒。

注意：完美哈希的单次 `add` 并没有稳定地比调好的开放寻址快（一次查找读 `disp`、`keys`、`values` 三个数组），收益是确定性 + 紧凑 + 可缓存下标。
