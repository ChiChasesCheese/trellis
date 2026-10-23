---
id: hl-c11-selftest
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 15
---
## Q
自测：在哪种情况下 `memcpy` 与 `std::copy` 生成的机器码几乎相同？为什么不能 `memcpy` 一个含 `std::string` 成员的 struct？

## A
- 元素类型**平凡可拷贝**且迭代器**连续**（指针、`vector` 迭代器）时，`std::copy` 就是一次 `memmove`。
- 含 `std::string` 成员的 struct 不是平凡可拷贝：按位复制得到两个共享同一堆缓冲区的字符串，析构时 **double free**。
