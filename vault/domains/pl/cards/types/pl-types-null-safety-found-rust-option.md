---
id: pl-types-null-safety-found-rust-option
node: types.null-safety
type: qa
step: 3
---
## Q
Rust 没有 `null`，`Option<T>` 是怎样表示「没有值」的？编译器怎样强制你处理它？

## A
`Option<T>` 是标准库里的一个普通 `enum`，只有两个变体：`Some(值)` 表示有，`None` 表示没有。「可能没有」是类型的一部分：`Option<&str>` 和 `&str` 是不同的类型，不能混用。要取里面的值，必须先说明没有时怎么办。

```rust
use std::collections::HashMap;
let mut m = HashMap::new();
m.insert("a", "x");
for k in ["a", "b"] {
    match m.get(k) {
        Some(v) => println!("{} -> {}", k, v.to_uppercase()),
        None => println!("{} -> missing", k),
    }
}
println!("{}", m.get("b").map(|v| v.len()).unwrap_or(0));
```

`HashMap::get` 返回 `Option`，实际输出：`a -> X`、`b -> missing`、`0`。`match` 必须同时写 `Some` 和 `None` 两个分支，漏掉一个就编译失败；`map` 在有值时变换，`unwrap_or(0)` 在没有时给默认值。

如果把 `Option<&str>` 直接传给要 `&str` 的函数，编译器拒绝：`expected &str, found Option<&str>`。所以空指针错误在安全的 Rust 里无法写出来。

常用的几个操作：`?` 在 `None` 时让函数提前返回 `None`；`unwrap()` 在 `None` 时 panic（只用于你确信有值的地方）；`expect("原因")` 同样会 panic，但带说明。
