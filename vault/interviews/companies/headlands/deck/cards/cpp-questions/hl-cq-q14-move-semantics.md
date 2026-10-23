---
id: hl-cq-q14-move-semantics
node: cpp-questions.c-memory-ownership
type: qa
step: 19
---
## Q
面试题：什么是移动语义？`std::move` 到底做了什么？编译器什么时候做复制省略？
What is move semantics? What does `std::move` really do? When does the compiler elide copies?

## A
- **移动** = “偷”临时对象或即将销毁对象的内部资源（指针换手），而不是复制。
- **`std::move` 本身不移动任何东西，只是把表达式转成右值引用**；真正的移动由移动构造函数完成。
- 被移走的对象处于“**有效但未指定**”状态：可以安全销毁或重新赋值，不要读它的值（实测 `a.size()` 变成 0，`b` 得到 40）。
- `noexcept` 的移动才会被 `vector` 增长时使用。
- 返回局部变量**不要写 `std::move`**，因为会阻止复制省略。
