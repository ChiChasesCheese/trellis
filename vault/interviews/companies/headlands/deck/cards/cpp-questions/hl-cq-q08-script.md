---
id: hl-cq-q08-script
node: cpp-questions.b-standards
type: qa
step: 14
---
## Q
用英文 60 秒回答：C++11 in practice: what are `auto`, lambdas, `nullptr`, `enum class`, and brace initialization, and what are the traps?

## A
结构：`auto` 丢 const/引用 → lambda 捕获与悬空 → `nullptr` 与 `enum class` → 花括号 `initializer_list` 优先（2 对 3 个元素）→ 点出移动语义。

- **`auto`** deduces from the initializer but **drops const and references**, so I write `const auto&` when I want a reference.
- **Lambdas** are anonymous function objects with a capture list - by value or by reference; a by-reference capture that outlives the variable is a **dangling reference**.
- **`nullptr`** has its own type, fixing the `NULL`-is-zero overload problem; **`enum class`** is scoped and doesn't convert to int.
- **Brace initialization** forbids narrowing but prefers the `initializer_list` constructor: `vector<int>{3,4}` has two elements, `vector<int>(3,4)` has three.
- And the biggest C++11 change is **move semantics**, which makes returning and passing large objects cheap.
