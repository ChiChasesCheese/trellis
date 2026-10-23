---
id: hl-cq-q15-why-byte-copy-breaks
node: cpp-questions.c-memory-ownership
type: qa
step: 27
---
## Q
对 `std::string` 数组用 `memcpy` 会出什么问题？一个带指向自己内部指针的结构体被 `memcpy` 后会怎样？

## A
- **`std::string` 数组**：两个对象会共享同一块堆缓冲，析构时 **double free**；`std::copy` 则逐个调用字符串的赋值，是正确的。
- **自指结构**：`struct SelfRef { char buf[8] = "abc"; char* p = buf; };` 正确的拷贝构造会让 `p` 重新指向自己的 `buf`；`memcpy` 之后，副本的 `p` 仍然指向**原对象**的 `buf`（实测 `p points into the ORIGINAL: yes (bug)`）。
