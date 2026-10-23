---
id: hl-cq-q09-script
node: cpp-questions.b-standards
type: qa
step: 22
---
## Q
用英文 60 秒回答：What do C++14 and C++17 add that you'd use every day? (`optional`, `variant`, `string_view`, structured bindings, `if constexpr`, CTAD)

## A
结构：14 的小件 → 17 的词汇类型（`optional`/`variant`/`string_view`，点出生命周期陷阱）→ 语法糖（结构化绑定、`if constexpr`、CTAD、折叠）→ 复制省略。

- From **C++14** I use generic lambdas, `make_unique`, and relaxed `constexpr`.
- **C++17** gives me **vocabulary types**: `std::optional` instead of sentinel values, `std::variant` with `std::visit` as a type-safe union - cheaper than virtual dispatch because there's no heap or indirect call - and `string_view`, a non-owning pointer-plus-length. The trap with `string_view` is **lifetime**: it dangles if the string dies first.
- Syntax: **structured bindings** for maps and pairs, `if` with an initializer, **`if constexpr`** to pick code at compile time, class template argument deduction, and fold expressions.
- And guaranteed copy elision means returning a temporary does no copy at all.
