---
id: pl-types-algebraic-data-types-found-rust-enum-data
node: types.algebraic-data-types
type: qa
step: 2
---
## Q
Rust 里 `struct` 和带数据的 `enum` 分别表示什么？为什么说它们是积与和？

## A
`struct` 把几个字段放在一起，一个值同时拥有所有字段：这是积（product）。`enum` 列出几个变体，一个值在任一时刻恰好是其中一个，每个变体可以带自己的数据：这是和（sum）。

```rust
struct Point { x: i32, y: i32 }           // 同时有 x 和 y
enum Cmd { Quit, Move(i32, i32) }         // 是 Quit，或者是 Move
let p = Point { x: 1, y: 2 };
let c = Cmd::Move(p.x, p.y);
match c {
    Cmd::Quit => println!("quit"),
    Cmd::Move(a, b) => println!("{} {}", a, b),
}
```

实际输出 `1 2`。`Move` 变体的数据只有在 `match` 到 `Move` 时才能取出；`Quit` 不带数据。`match` 必须覆盖全部变体，漏一个编译失败。

数一数取值个数就能理解「积」和「和」的名字：`Point` 的每个字段有 2³² 种取值，整体是 2³² × 2³² 种（相乘）；`Cmd` 的取值是 `Quit` 的 1 种，加上 `Move` 的 2³² × 2³² 种（相加）。

这件事的实用价值是：每个变体只带它自己需要的数据，不存在「`Quit` 却带着一个无意义的坐标」这种状态。如果用一个结构体加标志字段来模拟，这些无意义的组合是可以构造出来的。
