---
id: hl-c04-move-ctor-code
node: cpp-lessons.c04-move-semantics
type: qa
step: 4
---
## Q
为拥有 `char* data_` 和 `size_t n_` 的 `Buffer` 类写出移动构造函数，并说明它和拷贝构造的复杂度差别。

## A
```cpp
Buffer(Buffer&& o) noexcept : data_(o.data_), n_(o.n_) {
    o.data_ = nullptr;
    o.n_ = 0;
}
```
- **移动**：偷走指针，把源置空（`nullptr`、0），**O(1)**。源对象析构时 `delete[] nullptr` 安全。
- **拷贝构造**：`new char[o.n_]` 再 `memcpy`，**O(n)**。例：1 MiB 缓冲区拷贝一次复制 1048576 字节，移动只拷两个字段。
- 必须标 `noexcept`（见 `vector` 扩容规则）。
