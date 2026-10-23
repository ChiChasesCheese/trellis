---
id: hft-cpp-containers-vector-vs-list
node: cpp.containers
type: qa
step: 1
---
## Q
为什么在 C++ 里，`std::vector` 遍历和查找通常比 `std::list`、`std::map` 快得多？这和 CPU 缓存有什么关系？

## A
`vector` 的元素在内存里**紧挨着**，而 `list` 和 `map` 的每个节点都是一次单独的堆分配，位置分散，靠指针相连。

CPU 以 64 字节的缓存行（cache line）读内存，并会预取顺序访问的下一行：
- `vector<int>`：一条缓存行装 16 个 `int`（64 ÷ 4），读一行就拿到 16 个元素，预取器还提前取下一行。
- `list<int>`：每个节点还带前后两个指针（共 24 字节），分散在堆里，遍历每走一步都可能是一次缓存未命中（约 80–100 ns）；预取器也猜不到下一个地址。

另一个差别在分配次数：往容器里放 1000 个元素，`vector` 只要十来次扩容（若先 `reserve` 则只要 1 次），`list` 要 1000 次，每次都是一次 `new`。

这就是“理论复杂度相同，实际差一个数量级”的典型例子。
