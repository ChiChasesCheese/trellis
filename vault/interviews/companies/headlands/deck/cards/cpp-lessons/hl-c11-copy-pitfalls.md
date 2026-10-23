---
id: hl-c11-copy-pitfalls
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 14
---
## Q
拷贝相关有哪六个常见的坑？

## A
1. `memcpy` 的第三个参数是**字节数**，忘了乘 `sizeof(T)` 只拷贝一部分。
2. 对 `std::vector<T>`、`std::string` 对象本身 `memcpy`：拷贝的是它们内部的三个指针。
3. `std::copy` 目标区间太小：它不会扩容；先 `resize` 或用 `back_inserter`。
4. `std::copy` 重叠且目标在源区间内部：UB，用 `copy_backward`。
5. 对含指针成员的结构体 `memcpy` 得到的是**浅拷贝**。
6. 把 `memcpy` 当类型转换用（`float` → `int` 位）是对的，但用 `*(int*)&f` 是 UB（严格别名）。
