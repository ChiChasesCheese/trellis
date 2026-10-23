---
id: hl-c13-memory-order-table
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 6
---
## Q
面试问：解释 `memory_order_relaxed`、`acquire`、`release`、`acq_rel`、`seq_cst` 各保证什么。
Interview question: Explain the C++ memory orders.

## A
- `relaxed`：只保证这个操作本身原子，不对其他内存访问排序；适合计数器、统计。
- `release`（store）：本线程在这条 store **之前**的所有读写，不会被重排到它之后。
- `acquire`（load）：本线程在这条 load **之后**的所有读写，不会被重排到它之前。
- `acq_rel`：读改写操作兼有两者。
- `seq_cst`（默认）：在 acq/rel 之上，所有 `seq_cst` 操作有**一个全局总顺序**。

比 `seq_cst` 便宜：在弱序 CPU（如 ARM）上尤其明显；x86 上 acq/rel 本来就是免费的。
