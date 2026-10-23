---
id: hl-cq-q07-cpp14-17-list
node: cpp-questions.b-standards
type: qa
step: 3
---
## Q
C++14 和 C++17 各新增了哪些关键特性？

## A
**C++14**：
- 泛型 lambda（参数写 `auto`）、函数返回类型推导、`make_unique`、变量模板
- 放宽的 `constexpr`（允许循环）
- 数字分隔符 `1'000'000`、二进制字面量 `0b101`

**C++17**：
- 结构化绑定 `auto [k, v]`、`if constexpr`、`if (init; cond)`
- `optional` / `variant` / `any`、`string_view`
- 类模板参数推导（CTAD）、折叠表达式、`inline` 变量
- **保证的复制省略**、`std::filesystem`、并行算法、`[[nodiscard]]`
