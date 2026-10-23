---
id: hl-cq-q36-arena-and-pool
node: cpp-questions.i-low-latency
type: qa
step: 4
---
## Q
单调竞技场（monotonic arena）怎么分配和释放？适合什么场景？对象池（object pool）是什么，`acquire` / `release` 的复杂度？

## A
- **monotonic arena**：只增不减，分配就是“移动指针”，释放是整块一次完成（`release()`）；适合“每个请求 / 每个消息一块，处理完整体丢弃”。
- **对象池**：预先分配 N 个固定大小对象 + 一条空闲链表，`acquire` / `release` 都是 **O(1)**（“固定内存池”这类题）。
