---
id: hl-cq-q21-forwarding-refs
node: cpp-questions.e-templates
type: qa
step: 6
---
## Q
面试题：什么是转发引用（forwarding reference）和完美转发？`std::move` 与 `std::forward` 的区别？`emplace_back` 和 `push_back` 呢？
What are forwarding references and perfect forwarding? `std::move` vs `std::forward`; `emplace_back` vs `push_back`?

## A
- 在**被推导的模板参数**上，`T&&` 是**转发引用**，既能绑定左值也能绑定右值。
- 它在函数体里有名字，所以是左值；要保持调用者给的“左值 / 右值”属性，必须写 `std::forward<T>(x)`（完美转发）。
- **`std::move(x)`** 无条件转成右值；**`std::forward<T>(x)`** 只在原本是右值时才转成右值。写通用包装函数用 `forward`，明确放弃一个对象用 `move`。
- **`emplace_back(args...)`** 用转发就地构造，省掉一次临时对象的移动。
