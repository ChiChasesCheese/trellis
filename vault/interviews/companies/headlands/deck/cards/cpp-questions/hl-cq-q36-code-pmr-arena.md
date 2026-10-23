---
id: hl-cq-q36-code-pmr-arena
node: cpp-questions.i-low-latency
type: qa
step: 3
---
## Q
补全代码：在栈上放一块 64 KB 缓冲区，用它建立一个 `std::pmr::monotonic_buffer_resource`（上游设为 `null_memory_resource`），再创建一个用它分配的 `std::pmr::list<Order>`。

## A
```cpp
alignas(std::max_align_t) std::array<std::byte, 64 * 1024> buf;
std::pmr::monotonic_buffer_resource arena(
    buf.data(), buf.size(), std::pmr::null_memory_resource());
std::pmr::list<Order> l(&arena);
```
- 链表节点（以及 `pmr::string` 的缓冲）都从栈上这块 `buf` 里切。
- 上游用 `null_memory_resource`：用完了会**抛异常**而不是悄悄回退到堆，适合测试“确实没有堆分配”。
