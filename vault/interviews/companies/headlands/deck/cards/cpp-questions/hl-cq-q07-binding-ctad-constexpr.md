---
id: hl-cq-q07-binding-ctad-constexpr
node: cpp-questions.b-standards
type: qa
step: 6
---
## Q
追问：什么是结构化绑定（structured binding）、类模板参数推导（CTAD）和 `if constexpr`？
What is a structured binding / CTAD / `if constexpr`?

## A
- **结构化绑定**：把 pair、tuple 等拆开，写成 `auto [k, v]`。
- **CTAD**（Class Template Argument Deduction）：根据构造函数参数推导模板参数，例如 `std::pair p(1, 2.5)` 推出 `pair<int,double>`。
- **`if constexpr`**：编译期选择分支，没被选中的分支甚至不会被实例化。
