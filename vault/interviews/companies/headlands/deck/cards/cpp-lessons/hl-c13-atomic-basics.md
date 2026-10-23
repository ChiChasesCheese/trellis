---
id: hl-c13-atomic-basics
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 3
---
## Q
`std::atomic<T>` 保证什么？常用操作有哪些？`atomic` 和 `mutex` 怎么选？

## A
- `atomic<T>` 保证对它的读、写、读改写是**不可分割**的，并附带内存序语义。
- 常用操作：`load`、`store`、`exchange`、`fetch_add/sub/and/or`、`compare_exchange_weak/strong`（CAS）。
- `fetch_add` 是原子读改写，不会丢更新（`++` 在 `atomic` 上也是）；`mutex` 版本同样正确但更重（阻塞、内核介入）。
- 选择：`atomic` 针对**单个变量**的不可分割操作，无锁，延迟低；`mutex` 保护一段任意临界区（**多变量不变式**），会阻塞。一个不变式涉及多个变量就用 `mutex`。
