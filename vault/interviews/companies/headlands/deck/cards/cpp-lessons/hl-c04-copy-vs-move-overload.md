---
id: hl-c04-copy-vs-move-overload
node: cpp-lessons.c04-move-semantics
type: qa
step: 6
---
## Q
```cpp
std::vector<Buffer> v; v.reserve(3);
v.push_back(Buffer(8));
v.push_back(b);
v.push_back(std::move(b));
```
三次 `push_back` 各调用移动还是拷贝？为什么？

## A
- `push_back(Buffer(8))`：实参是**右值**（临时对象），选中 `push_back(T&&)`，走**移动**。
- `push_back(b)`：`b` 是**左值**，选中 `push_back(const T&)`，走**拷贝**（`COPY`）。
- `push_back(std::move(b))`：`std::move` 把左值转为右值引用，走**移动**，之后 `b` 为空。
- 机制就是重载决议：传临时对象或 `std::move` 的结果选 `T&&` 版本，其他选 `const T&` 版本。
