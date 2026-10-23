---
id: hl-cq-q08-lambda-compiles-to
node: cpp-questions.b-standards
type: qa
step: 12
---
## Q
追问：lambda 编译后是什么？`auto&&` 和 `decltype(auto)` 分别是什么？
What does a lambda compile to? What's `decltype(auto)` / `auto&&`?

## A
- lambda 被编译成**编译器生成的类**：有 `operator()`，每个捕获对应一个成员；**不捕获**的 lambda 可以转换成函数指针。
- `auto&&` 是**转发引用**（forwarding reference）。
- `decltype(auto)` 保留表达式的**精确类型**，包括引用。
