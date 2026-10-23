---
id: hl-c04-move-assign-copy-swap
node: cpp-lessons.c04-move-semantics
type: qa
step: 5
---
## Q
`Buffer` 的拷贝赋值和移动赋值怎么写？copy-and-swap 是什么？为什么要处理自赋值？

## A
```cpp
Buffer& operator=(const Buffer& o) {
    if (this != &o) { Buffer tmp(o); swap(tmp); }
    return *this;
}
Buffer& operator=(Buffer&& o) noexcept {
    if (this != &o) {
        delete[] data_;
        data_ = o.data_; n_ = o.n_;
        o.data_ = nullptr; o.n_ = 0;
    }
    return *this;
}
```
- **copy-and-swap**：先拷贝出临时对象，再和它 `swap`；临时对象离开作用域时带走旧资源。天然异常安全（强保证）。
- **自赋值**：`a = std::move(a)` 如果不判断，会先 `delete[] data_` 释放自己，再读自己已释放的指针，出错。
- `swap` 用 `std::swap` 交换两个成员，标 `noexcept`。
