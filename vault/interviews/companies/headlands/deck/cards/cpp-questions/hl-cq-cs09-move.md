---
id: hl-cq-cs09-move
node: cpp-questions.cheatsheet
type: qa
step: 9
---
## Q
一句话背诵：`std::move` 的真相、`const` 对象的情形、`noexcept` 与 `vector` 扩容、返回局部变量。

## A
- `std::move` 只是转型。
- 对 `const` 对象会退化成拷贝。
- 移动构造要 `noexcept`，否则 `vector` 扩容时是 **7 次拷贝**而不是 7 次移动。
- `return local;` 不要写 `std::move`。
- C++17 返回临时对象**保证不拷贝**。
