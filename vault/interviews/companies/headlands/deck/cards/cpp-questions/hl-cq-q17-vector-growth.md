---
id: hl-cq-q17-vector-growth
node: cpp-questions.d-containers
type: qa
step: 1
---
## Q
面试题：`std::vector` 怎么增长？什么操作会使迭代器、指针和引用失效？
How does `std::vector` grow? What invalidates iterators, pointers and references?

## A
- `vector` 是**一块连续内存**，`size`（元素个数）≤ `capacity`（已分配容量）。
- 放满后分配约 2 倍的新内存（libc++ / libstdc++ 是 2 倍，MSVC 是 1.5 倍），把元素搬过去，释放旧内存。
- 所以 `push_back` **可能让所有迭代器、指针、引用失效**；知道大小就先 `reserve`。
- 实测容量序列：`1 2 4 8 16 32 64 128`。
- `push_back` 均摊 O(1)：每次翻倍，搬运总量约 2n；但某一次 `push_back` 是 O(n)，延迟敏感路径要 `reserve`。
