---
id: hl-c07-concepts-overload
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 11
---
## Q
```cpp
void print_kind(std::integral auto) { /* integral */ }
void print_kind(std::floating_point auto) { /* floating */ }
void print_kind(auto) { /* generic */ }
```
调用 `print_kind(1)`、`print_kind(2.5)`、`print_kind("x")` 各选哪个？规则是什么？

## A
- `print_kind(1)` → integral 版；`print_kind(2.5)` → floating 版；`print_kind("x")` → generic 版。
- 规则：**约束更强的重载优先**（`integral` 版本胜过无约束 `auto`）。
- 传错类型时，错误信息直接指出违反的约束：如 `twice(std::string("oops"))` 报 `candidate template ignored: constraints not satisfied [with T = std::string]`，原因链 `'std::string' does not satisfy 'Numeric'` → `'integral'`。
