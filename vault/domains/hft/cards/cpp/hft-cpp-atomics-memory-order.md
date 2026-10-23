---
id: hft-cpp-atomics-memory-order
node: cpp.atomics
type: qa
step: 2
---
## Q
`memory_order_relaxed`、`acquire`、`release`、`seq_cst` 各保证什么？用“生产者发布数据、消费者读取”的例子说明 acquire/release 是怎么配对的。

## A
- **relaxed**：只保证这个操作本身是原子的，对其他内存访问不做任何排序。适合计数器、统计。
- **release**（用于写）：本线程在它**之前**的所有读写，不会被重排到它之后。
- **acquire**（用于读）：本线程在它**之后**的所有读写，不会被重排到它之前。
- **seq_cst**（默认）：在 acquire/release 之上，所有 seq_cst 操作还有一个全局统一的先后顺序。

配对例子：
1. 生产者先写普通变量 `data = 42`；
2. 再 `ready.store(true, release)`；
3. 消费者循环 `while (!ready.load(acquire))`；
4. 一旦读到 `true`，就**保证**能看到 `data == 42`。

如果两边都用 relaxed，消费者可能看到 `ready == true`，却读到旧的 `data`。默认用 `seq_cst`，只在有测量证据时才降级。
