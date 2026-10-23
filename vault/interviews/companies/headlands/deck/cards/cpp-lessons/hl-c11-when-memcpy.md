---
id: hl-c11-when-memcpy
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 12
---
## Q
什么时候可以直接用 `memcpy`？其他情况用什么？

## A
可以用 `memcpy`：
- **C 接口、网络协议/文件格式缓冲区**（字节数组 ↔ 结构体），且类型平凡可拷贝，写上 `static_assert(std::is_trivially_copyable_v<T>)`。
- **位重解释**：`memcpy(&u, &f, sizeof u)`（等价 `std::bit_cast`），这是合法的别名绕过方式。

其余情况用：容器赋值 `dst = src`、`std::copy`、`std::copy_n`、`vector::insert`、`assign`。
