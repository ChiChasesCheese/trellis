---
id: hl-c05-vector-growth
node: cpp-lessons.c05-stl-containers
type: qa
step: 4
---
## Q
面试问：`std::vector` 扩容怎么工作？复杂度是多少？`reserve` 的作用？
Interview question: How does `std::vector` grow, and what is `reserve` for?

## A
- `vector` 对象本身只有**三个指针**（begin、end、end-of-capacity），`sizeof` 为 24 字节；元素在堆上的连续块里。
- 容量不够时：分配更大的新块（常见增长因子 1.5–2，取决于实现）→ 移动（或拷贝）旧元素 → 释放旧块。所以 `push_back` **摊销 O(1)**，但偶尔整体搬移。
- 实测 1000 次 `push_back`：容量序列 1 2 4 8 … 1024，共 **11 次**重分配；`reserve(1000)` 后重分配 **0 次**。
- 扩容使所有迭代器、指针、引用失效；移动构造 `noexcept` 时才移动元素。
- 已知大小就 `reserve`。
