---
id: pl-types-nominal-structural-found-rust-trait-orphan
node: types.nominal-structural
type: qa
step: 5
---
## Q
Rust 的 `trait` 要怎样显式实现？孤儿规则（orphan rule）禁止的是什么？

## A
Rust 的 `trait` 是一组方法签名（可以带默认实现）。一个类型要满足它，必须有一个显式的 `impl Trait for Type { ... }` 块。和 Java 不同，这个块不必写在类型定义里，可以在别处，因此能为别人的类型补实现。

但有一条限制，叫孤儿规则：`impl` 的 trait 和类型，至少有一个必须定义在当前 crate（Rust 的编译单元）里。你可以给自己的类型实现标准库的 trait，也可以给标准库的类型实现自己的 trait，但不能给标准库的类型实现标准库的 trait。

```rust
use std::fmt;
struct Wrapper(Vec<i32>);                       // 自己的类型，包住别人的
impl fmt::Display for Wrapper {                 // 允许
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "len={}", self.0.len()) }
}
// impl fmt::Display for Vec<i32> { ... }       // 不允许
```

`println!("{}", Wrapper(vec![1, 2]))` 输出 `len=2`。直接写 `impl Display for Vec<i32>` 则编译失败：

```console
error[E0117]: only traits defined in the current crate can be implemented for types defined outside of the crate
```

规则存在的原因是一致性：如果两个库都为 `Vec<i32>` 实现了 `Display`，程序同时依赖它们时编译器无法选择。常用的绕法是新类型包装（newtype），如上面的 `Wrapper`。
