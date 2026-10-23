---
id: hft-cpp-no-alloc-arena-vs-pool
node: cpp.no-alloc
type: qa
step: 3
---
## Q
arena（也叫 bump allocator，指针递增分配器）和固定大小对象池有什么区别？各适合什么场景？C++17 的 `std::pmr` 又是什么？

## A
- **arena**：一大块内存加一个“已用位置”指针。分配 = 把指针往前推 n 字节（对齐后），不能单独释放；用完后 `reset()` 一次性把指针拨回起点，全部回收。适合**同生命周期**的一批对象，例如处理完一条行情消息就整体丢弃的临时数据。一次实测中它最快，约 0.7 ns / 对象。
- **对象池**：槽大小固定，每个对象可以**在不同时间**单独归还。适合订单这类“各自生死”的同类对象。

选择标准：对象是否同时死亡。能同时死亡就用 arena（释放几乎免费）；不能就用池。

`std::pmr`（polymorphic memory resources）让标准容器可以在运行时指定内存来源，例如 `monotonic_buffer_resource` 就是一个 arena，于是 `vector`、`string` 也能把内存放在预先给定的缓冲区里，不用每个容器写自己的分配器。
