---
id: hl-c10-pool-benchmark
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 13
---
## Q
创建并销毁 256 个 64 字节订单的实测：`new/delete`、固定池、bump arena、`pmr` monotonic 每个对象各多少纳秒？说明了什么？

## A
- `new / delete`：6.87 ns
- 固定池（free list）：1.78 ns
- bump arena + reset：0.75 ns
- `pmr` monotonic + vector：2.09 ns

读法：热缓存、单线程下 `new/delete` 已经只要几纳秒，池快 3–4 倍，arena 最快（释放是一次 O(1) 的 `reset`）。**真正的收益**在：
- **尾部延迟**：没有偶发的慢分配/系统调用。
- **多线程无争用**。
- **缓存局部性**：对象紧挨着。
