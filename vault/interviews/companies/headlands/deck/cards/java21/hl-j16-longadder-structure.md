---
id: hl-j16-longadder-structure
node: java21.j16-concurrency-primitives
type: qa
step: 19
---
## Q
`LongAdder`（Java 8）为什么在高竞争下比 `AtomicLong` 快？内部结构和读取方式是什么？

## A
`AtomicLong.incrementAndGet()` 是对**同一内存位置**的 CAS 循环：8 个线程同时来，每轮只有 1 个成功，其余重试，且每次失败都让该缓存行在核间来回迁移，线程越多越慢。

`LongAdder` 把计数器拆成 **一个 `base` + 一个 `Cell[]` 数组**：
- 低竞争：所有线程 CAS 同一个 `base`，和 `AtomicLong` 一样快；
- 高竞争：某次 CAS `base` 失败 → 线程按自己的「探针哈希」选一个 `Cell[i]` 去加 → 不同线程大概率落在不同 Cell，互不干扰；
- 读取：`sum() = base + Σ cells[i]`，**不是原子快照**。

每个 `Cell` 用 `@Contended` 填充缓存行，避免 Cell 间伪共享。
