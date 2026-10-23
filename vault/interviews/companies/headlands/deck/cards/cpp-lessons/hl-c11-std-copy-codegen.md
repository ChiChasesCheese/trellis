---
id: hl-c11-std-copy-codegen
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 9
---
## Q
面试问：编译器怎么优化 `std::copy`？对 `int*` 区间、对 `std::string` 数组各生成什么？
Interview question: How does the compiler optimise `std::copy`?

## A
- 对 `int*` 这种平凡可拷贝类型的连续区间：库用 `is_trivially_copyable` + 连续迭代器分派，整个函数就是**尾调用 `memmove`**（字节数 = `last - first`）。
- 对 `std::string` 数组：逐元素调用 `string::operator=`，不会也不能变成 `memmove`。
- 所以：**平凡类型用 `std::copy` 不比 `memcpy` 慢**，同时对任何类型都正确。
