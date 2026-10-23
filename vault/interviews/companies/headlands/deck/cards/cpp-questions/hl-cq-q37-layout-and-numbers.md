---
id: hl-cq-q37-layout-and-numbers
node: cpp-questions.i-low-latency
type: qa
step: 9
---
## Q
SPSC 队列里 `head_`、`tail_`、两个缓存索引和数据数组各应怎么对齐？500 万个 `int64` 从一个线程传到另一个线程：每次都读对方索引、缓存索引、`mutex + std::queue` 各是多少？为什么缓存对方索引能快几十倍？

## A
- 对齐：每个成员都 `alignas(128)`，各占独立缓存行；`N` 用 `static_assert((N & (N - 1)) == 0)` 保证是 2 的幂。
- 数字（500 万项）：
  - 每次读对方索引：359 ms（**72 ns/项**）；
  - 缓存对方索引：9 ms（**2 ns/项**）；
  - `mutex + std::queue`：80 ms（16 ns/项，波动大，一般 15–50 ns）。
- 原因：每次 `push` 都读 `head_` 会让持有 `head_` 的缓存行在两个核之间来回传输；缓存副本之后，只有“看起来满 / 空”时才读对方的行，大多数操作只碰自己核上的行。
