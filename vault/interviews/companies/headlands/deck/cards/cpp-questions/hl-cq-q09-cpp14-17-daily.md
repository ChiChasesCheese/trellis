---
id: hl-cq-q09-cpp14-17-daily
node: cpp-questions.b-standards
type: qa
step: 15
---
## Q
面试题：C++14 和 C++17 里你每天会用到哪些特性？（`optional`、`variant`、`string_view`、结构化绑定、`if constexpr`、CTAD）
What do C++14 and C++17 add that you'd use every day?

## A
- **14**：泛型 lambda、返回类型推导、`make_unique`、变量模板。
- **17**：
  - `optional`：可能没有值；
  - `variant`：类型安全的 union；
  - `string_view`：不拥有数据的字符串视图；
  - 结构化绑定、`if constexpr`（编译期分支）、类模板参数推导、折叠表达式、保证的复制省略。
