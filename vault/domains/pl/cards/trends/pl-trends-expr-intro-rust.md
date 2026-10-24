---
id: pl-trends-expr-intro-rust
node: trends.expression-orientation
type: qa
step: 2
---
## Q
Rust 里 `if`、`match`、代码块和 `loop` 为什么都是表达式？末尾分号和单位类型 `()` 有什么作用？

## A
**规则**：Rust 里几乎所有结构都有值。一个**代码块** `{ ... }` 的值是它最后一个**没有分号**的表达式。`if`/`else`、`match`、`loop`（配合 `break 值`）都能放在 `=` 右边。

```rust
let x = { let a = 2; let b = 3; a * b };                      // 6
let label = match x { 0 => "zero", 1..=5 => "small", _ => "big" };  // "big"
let n = loop { break 7; };                                    // 7
fn classify(n: i32) -> &'static str {
    if n < 0 { "neg" } else if n == 0 { "zero" } else { "pos" }   // the value is returned
}
```

真实输出依次为：`classify(-1)` 得 `neg`，`x` 是 6，`label` 是 big，`n` 是 7。函数不需要 `return`：最后一个表达式就是返回值。

**分号的作用**：分号把表达式变成**语句**，丢弃它的值。被丢弃的值的位置上留下**单位类型** `()`（空元组，表示“没有有意义的值”）。块如果以语句结尾，它的值就是 `()`。

**一致性检查**：`if` 的每个分支必须给出同一个类型，否则编译不过：

```rust
let s = if n > 3 { "big" } else { 3 };
// error[E0308]: `if` and `else` have incompatible types
```

这是表达式导向带来的免费检查：值得有统一的类型。`match` 同样要求覆盖所有情形（穷尽性）。

**要记住的一点**：在 Rust 里，“语句”只是“被丢弃了值的表达式”。语言只有一个核心概念：表达式。
