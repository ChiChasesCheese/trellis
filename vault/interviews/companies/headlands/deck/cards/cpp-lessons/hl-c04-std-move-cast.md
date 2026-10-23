---
id: hl-c04-std-move-cast
node: cpp-lessons.c04-move-semantics
type: qa
step: 3
---
## Q
面试问：`std::move(x)` 到底做了什么？`std::move(x)` 之后 `x` 处于什么状态？
Interview question: What does `std::move` actually do?

## A
- `std::move(x)` **只是一个类型转换**（`static_cast<T&&>`），把左值 `x` 转成右值引用 `T&&`，**本身不移动任何东西**。
- 真正的移动发生在随后被重载决议选中的**移动构造/移动赋值函数**里。
- 之后 `x` 仍然存在，处于「**有效但未指定**」（valid but unspecified）状态：可以析构、可以赋新值，别读它的值。
- 例：`std::string t = std::move(s);` 后 `s.size()` 通常为 0，但不要依赖；`s = "reuse is fine";` 总是允许。
- 对 `int` 等基础类型 `std::move` 没有意义，移动等于拷贝。
