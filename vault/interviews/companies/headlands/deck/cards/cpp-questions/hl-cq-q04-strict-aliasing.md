---
id: hl-cq-q04-strict-aliasing
node: cpp-questions.a-why-fast
type: qa
step: 22
---
## Q
追问：什么是严格别名规则（strict aliasing）？要做类型双关（type punning）该用什么？
What is strict aliasing?

## A
- 规则：通过一个**不相关类型**的指针访问对象是未定义行为。
- 好处：编译器因此可以假设 `int*` 和 `float*` 不指向同一块内存，从而放心优化和重排。
- 做类型双关用 **`memcpy`** 或 **`std::bit_cast`**（C++20），不要用指针强转。
