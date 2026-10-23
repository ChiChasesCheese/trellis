---
id: hl-c05-array-sizeof
node: cpp-lessons.c05-stl-containers
type: qa
step: 7
---
## Q
面试问：`std::array` 与 C 数组、与 `vector` 有什么区别？`sizeof` 分别是多少？
Interview question: What is `std::array` and how does it differ from a C array and `vector`?

## A
- `std::array<T,N>`：大小是**类型的一部分**，内联存放，**无堆分配**；`sizeof(std::array<int,4>)` = 16，正好 4 个 `int`，没有头、没有指针。
- 它是带 `size()`、迭代器、拷贝语义的**零开销封装**，不会退化为指针（C 数组会）。
- `sizeof(std::vector<int>)` = 24：三个指针（begin、end、end-of-capacity），元素在堆上。
- 对应 Java 的固定数组 `int[]`，但不在堆上。
