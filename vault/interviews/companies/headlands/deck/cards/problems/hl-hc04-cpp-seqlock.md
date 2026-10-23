---
id: hl-hc04-cpp-seqlock
node: problems.hc04-queue-mean-snapshot
type: qa
step: 19
---
## Q
C++ 版单写者多读者无锁读用 seqlock，原理和读者协议是什么？与 mutex、原子发布快照、双缓冲相比如何？

## A
**seqlock**：写者把版本号 `version_` 变成**奇数**（「正在写」）→ 改字段 → 变成**偶数**。读者：读到偶数版本号 `v1` → 读字段 → 再读版本号，若仍等于 `v1` 才接受，否则重试；读到奇数就 `yield` 后重试。

要点：
- 字段用 `relaxed` 原子而不是普通变量：普通变量在写者写入的同时被读是数据竞争（UB），`relaxed` 原子保证每个字不撕裂，顺序交给版本号和栅栏；
- 只要「字段在版本号之间」的顺序，所以 `release` / `acquire` 就够，不必 `seq_cst`（全栅栏在 ARM 上开销更明显）；先写 `seq_cst` 版本再优化是合理的；
- 只适合**单写者**；读者重试，所以是 obstruction-free 而不是 wait-free；单写者违规抛 `SingleWriterViolation`。

方案对比：
- `std::mutex`：最简单，读者阻塞写者，面试先说它再说为什么不够；读多写少可 `std::shared_mutex`；
- 原子发布不可变快照（`atomic<shared_ptr<Stat>>`）：一次原子加载，写者每次分配，回收靠引用计数；
- 双缓冲 + 版本号：读者可能被旧缓冲区的复用坑到，要加版本号；
- seqlock：无锁，无分配、无等待写者。

撕裂读实验：写者依次写 `hi`、`lo`（应始终相等），读者会读到 `hi != lo`，是逻辑 bug 不是 UB（用 relaxed 原子避免数据竞争）。
