---
id: hl-c01-vector-layout
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 4
---
## Q
`std::vector<Point>`（`Point` 含两个 `int`，`sizeof(Point)` 为 8）和 Java 的 `Point[]` 在内存布局上有什么区别？为什么这决定了性能？

## A
- `vector<Point>` 是**一整块连续内存**，4 个元素共 `4 * 8 = 32` 字节，相邻元素地址差正好 8 字节，每个元素就是 `Point` 本身。
- Java 的 `Point[]` 存的是 4 个**引用**，每个 `Point` 是单独的堆对象，带 12–16 字节对象头，散落在堆里。
- C++ 遍历时顺着缓存行（cache line）读，预取（prefetch）有效；Java 每个元素多一次指针跳转，容易缓存未命中。
- 这就是后面「C++ 为什么快」的根：连续布局、没有对象头、没有间接寻址。
