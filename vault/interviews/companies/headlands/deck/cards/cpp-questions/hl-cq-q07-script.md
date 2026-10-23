---
id: hl-cq-q07-script
node: cpp-questions.b-standards
type: qa
step: 8
---
## Q
用英文 60 秒回答：What are the differences between C++11, 14, 17 and 20?

## A
结构：11 最大（移动语义等）→ 14 打磨 → 17 词汇类型与结构化绑定 → 20 第二次大改，23 补 `expected` → 实践：以 17 为基线，热路径避开异常/RTTI/`shared_ptr`。

- **C++11** is the big one: **move semantics**, `auto`, **lambdas**, smart pointers, `std::thread` and atomics with a real memory model, `constexpr`, `nullptr`, range-for.
- **C++14** polishes it: generic lambdas, return type deduction, `make_unique`, and relaxed `constexpr`.
- **C++17** adds vocabulary types - `optional`, `variant`, `string_view` - plus **structured bindings**, `if constexpr`, **guaranteed copy elision**, and `std::filesystem`.
- **C++20** is the second big release: **concepts**, **ranges**, coroutines and modules, plus `std::span`, the spaceship operator, `jthread`, and `std::format`. C++23 adds `std::expected`, `std::print` and deducing `this`.
- In practice I write C++17 as a baseline and use C++20 where the compiler allows; in latency-critical code I avoid exceptions, RTTI and `shared_ptr` on the hot path.
