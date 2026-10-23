---
id: hl-cq-q10-cpp20-23-use
node: cpp-questions.b-standards
type: qa
step: 23
---
## Q
面试题：C++20 和 C++23 新增了什么，你会用哪些？（concepts、ranges、span、`<=>`、coroutines、`std::expected`）
What's new in C++20 and C++23, and which of it would you use?

## A
- C++20 四大件：**concepts**（给模板写约束，错误信息变可读）、**ranges**（惰性管道）、**coroutines**、**modules**。
- 常用小件：`span`、`<=>`、`jthread`、`format`、`<bit>`、`consteval`。
- C++23 的 `std::expected`、`std::print`、显式 `this` 已经能用。
- 即插即用的收益：concepts、`span`、`<bit>`、`expected`；协程和 modules 是更大的投入，面试时要如实说明哪些写过、哪些只了解概念。
