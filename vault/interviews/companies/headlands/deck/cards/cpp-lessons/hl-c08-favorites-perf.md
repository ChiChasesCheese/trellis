---
id: hl-c08-favorites-perf
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 17
---
## Q
面试问：你日常最离不开哪几个 C++ 现代特性？这些特性对性能有影响吗？
Interview question: Which modern C++ features do you rely on, and what is their performance impact?

## A
选你真会用的几个：
- 移动语义 + 智能指针（所有权）
- lambda + 算法
- `auto` + 结构化绑定
- `optional` / `string_view`
- `constexpr` / `if constexpr`
- concepts

性能：多数是**零开销**（编译期）；移动语义直接减少拷贝；`string_view`/`span` 避免分配；`constexpr` 把运行期算力挪到编译期；**协程帧可能堆分配**。
