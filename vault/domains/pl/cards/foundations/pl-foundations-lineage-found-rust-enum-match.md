---
id: pl-foundations-lineage-found-rust-enum-match
node: foundations.lineage
type: qa
step: 3
---
## Q
Rust 的 `enum` 和普通枚举有什么不同？`match` 为什么要求处理所有情况？

## A
C 或 Java 的枚举只是一组命名的常量。Rust 的 `enum` 更强：每个变体（variant）可以携带不同形状的数据，一个 `enum` 值在任一时刻恰好是其中一个变体。`match` 按变体分支并取出里面的数据，编译器检查你是否覆盖了所有变体，漏掉一个就是编译错误。

```rust
enum Cmd { Quit, Move(i32, i32) }
for c in [Cmd::Move(1, 2), Cmd::Quit] {
    match c {
        Cmd::Quit => println!("quit"),
        Cmd::Move(x, y) => println!("move {} {}", x, y),
    }
}
```

实际输出：`move 1 2`，然后 `quit`。`Move` 变体带着两个整数，只有在匹配到 `Move` 时才能取出 `x` 和 `y`；`Quit` 不带数据。

这种设计来自 ML 语言家族（1970 年代）。重要的是它的后果：因为「一个值只能是几种形态之一」写在类型里，而且处理必须完整，所以「忘了处理某种情况」这类错误无法编译通过。标准库的 `Option`（有值或没有值）和 `Result`（成功或失败）都只是普通的 `enum`，没有特殊语法。
