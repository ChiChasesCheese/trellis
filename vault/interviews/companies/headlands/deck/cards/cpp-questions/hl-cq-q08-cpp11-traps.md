---
id: hl-cq-q08-cpp11-traps
node: cpp-questions.b-standards
type: qa
step: 9
---
## Q
面试题：C++11 里的 `auto`、lambda、`nullptr`、`enum class`、花括号初始化各是什么，有哪些陷阱？
C++11 in practice: what are `auto`, lambdas, `nullptr`, `enum class`, and brace initialization, and what are the traps?

## A
- **`auto`**：从初始化表达式推导类型，**会丢掉 `const` 和引用**；想保留引用写 `auto&` / `const auto&`。
- **lambda**：带捕获的匿名函数对象。
- **`nullptr`**：有自己的类型，不会被当成整数。
- **`enum class`**：作用域枚举，不隐式转 `int`。
- **花括号初始化**：禁止窄化，但会**优先选 `initializer_list` 构造函数**。
