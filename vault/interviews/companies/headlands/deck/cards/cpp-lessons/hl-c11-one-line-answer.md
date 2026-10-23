---
id: hl-c11-one-line-answer
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 1
---
## Q
面试问：`std::copy` 和 `memcpy` 有什么区别？一句话答案是什么？
Interview question: What is the difference between `std::copy` and `memcpy`?

## A
一句话：**`memcpy` 是按字节拷贝的 C 函数，要求不重叠、只能用于平凡可拷贝类型；`memmove` 允许重叠；`std::copy` 是类型感知的，对平凡可拷贝类型优化后就是一次 `memmove`，对其他类型逐元素调用赋值运算符，所以永远对。**

要点：
- `memcpy`/`memmove` 的单位是**字节**，`std::copy` 的单位是**元素**。
- `memcpy` 无类型检查（`void*`），`std::copy` 有。
- 速度：平凡类型下 `std::copy` 不比 `memcpy` 慢。
