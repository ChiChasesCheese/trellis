---
id: hl-cq-cs15-templates-forwarding
node: cpp-questions.cheatsheet
type: qa
step: 15
---
## Q
一句话背诵：模板与泛型的区别、concepts 的价值、完美转发和 `emplace_back` 的效果。

## A
- 模板按类型实例化、无装箱，错误出现在实例化处；concepts 把错误挪到调用处（"constraints not satisfied … because 't.price()' would be invalid"）。
- **完美转发**：`T&&` 是转发引用，要 `std::forward<T>`。
- `emplace_back` 就地构造：**0 次移动**，`push_back` 是 **1 次**。
