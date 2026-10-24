---
id: pl-abstraction-pattern-matching-foundation-rust-match
node: abstraction.pattern-matching
type: qa
step: 2
---
## Q
Rust 的 `match` 是什么样的？解构、守卫和穷尽检查分别怎么工作？

## A
Rust 的 `enum` 每个变体可以携带不同数据，`match` 对它逐个分支匹配，第一个匹配的分支执行，并把数据绑定到变量：

```rust
enum Expr { Num(i64), Add(Box<Expr>, Box<Expr>), Neg(Box<Expr>) }
fn eval(e: &Expr) -> i64 {
    match e {
        Expr::Num(n) => *n,
        Expr::Add(a, b) => eval(a) + eval(b),
        Expr::Neg(inner) => -eval(inner),
    }
}
```

`2 + (-5)` 求值得 `-3`。

- **解构**：`Expr::Add(a, b)` 同时判断「是加法」和取出两个子表达式。模式可以嵌套：`Cmd::Move { x: 0, y }` 要求 `x` 恰好为 0，并把 `y` 绑定出来。
- **守卫**（guard）：分支后面加 `if 条件`，如 `Cmd::Move { x, .. } if x < 0`，条件为假则继续试下一个分支。
- **穷尽检查**：编译器要求所有可能的值都有分支覆盖，漏了就是编译错误，并告诉你漏了哪些值：

```text
error[E0004]: non-exhaustive patterns:
  `Cmd::Move { x: i32::MIN..=-1_i32, .. }` and
  `Cmd::Move { x: 1_i32..=i32::MAX, .. }` not covered
```

注意带守卫的分支不算「覆盖」（编译器不会推理 `x < 0` 的含义），所以上面这类漏洞会被指出来。`match` 是表达式，每个分支返回同一种类型，整个 `match` 就是一个值。
