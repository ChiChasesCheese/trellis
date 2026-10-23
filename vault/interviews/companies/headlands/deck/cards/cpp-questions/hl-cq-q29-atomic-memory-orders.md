---
id: hl-cq-q29-atomic-memory-orders
node: cpp-questions.g-concurrency
type: qa
step: 7
---
## Q
面试题：`std::atomic` 是什么？解释内存序（`relaxed`、`acquire`/`release`、`seq_cst`）。
What is `std::atomic`? Explain the memory orders.

## A
`std::atomic<T>` 让读-改-写成为不可分割的一步，并规定**内存序**：
- **`seq_cst`**（默认）：所有线程看到同一个全局顺序，最容易推理。
- **`release` 写 + `acquire` 读**：把“写之前的所有内存操作”安全地发布给读到这个值的线程。
- **`relaxed`**：只保证原子性，不保证和其他变量的顺序，适合计数器。
- 拿不准时用 `seq_cst` 或互斥量；不要凭印象选 `relaxed`，除非你能证明它正确。
