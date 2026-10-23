---
id: hl-hc07-cache-boxing
node: problems.hc07-ticker-hash-map
type: qa
step: 8
---
## Q
CPU 缓存行、指针追逐和装箱怎样让 `HashMap<String,Long>` 变慢？交错布局（interleaved）是什么？

## A
CPU 比内存快得多，核心旁有几级小而快的缓存（L1、L2、L3）。读内存一次读**一整条缓存行**（cache line，常按 64 字节理解，Apple Silicon 是 128）。教科书量级（非测量值）：L1 约 1 ns，L2 约 3–5 ns，主内存约 80–100 ns。

**指针追逐**（pointer chasing）：「读地址 A 拿到地址 B，再读 B……」每一跳都可能缓存未命中，且**不能并行**（下一跳地址要等上一跳读完）。
- `HashMap<String,Long>` 查一次：`table[桶]` → `Node` → key `String` → `byte[]`（用于 `equals`）→ `Long` value，3~4 次可能未命中，串行；
- `LongTickerMap`：`slots[2i]`、`slots[2i+1]` 相邻 16 字节在同一缓存行，线性探测下一格通常也在同一行。

**局部性**：空间局部性——访问 X 很可能马上访问附近；时间局部性——刚访问的很可能再访问（少数热门股占大部分消息）。

**装箱**：泛型集合只能放对象，`long` 要包成 24 字节堆上的 `Long`；`merge(key, 1L, Long::sum)` 每次可能分配新 `Long`（不可变）；`Long.valueOf` 只对 −128..127 有缓存池，累计成交量很快超出。预热后 160 万次 `merge` 平均每次分配 **14.8 字节**（逃逸分析消掉一部分），`LongTickerMap.add` 是 **0**。分配本身不贵，贵的是累积的垃圾让 GC 更忙，以及对象散落破坏局部性。key 从报文解析时还要先 `new String`（48 B），每秒几百万个短命 String。

**交错布局**：key 和 value 放同一个 `long[]`（`slots[2i]=key, slots[2i+1]=value`），一次缓存行拿到两者；分离布局理论上多一次未命中。但测量没有稳定支持，不能当确定事实说。
