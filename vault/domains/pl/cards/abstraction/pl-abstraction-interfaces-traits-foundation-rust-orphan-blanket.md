---
id: pl-abstraction-interfaces-traits-foundation-rust-orphan-blanket
node: abstraction.interfaces-traits
type: qa
step: 4
---
## Q
Rust 的孤儿规则（orphan rule）和 blanket impl 是什么？为什么能给别人的类型实现 trait，却又不能随便实现？

## A
Rust 允许事后给已有类型补 trait 实现，但有一条限制：**`impl Trait for Type` 只有在 trait 或 Type 至少一个定义在当前 crate（包）里才合法**，这就是孤儿规则。

```rust
use std::fmt;
impl fmt::Display for Vec<i32> { /* ... */ }
// error[E0117]: only traits defined in the current crate can be
// implemented for types defined outside of the crate
```

`Display` 与 `Vec` 都是标准库的，你无权补。原因是**一致性**（coherence）：如果允许，库 A 和库 B 各给 `Vec<i32>` 实现一遍 `Display`，程序同时依赖两个库时编译器无法选择。孤儿规则保证全局任何类型对任何 trait 至多一份实现，所以不会出现「导入顺序不同行为不同」。绕法是用 newtype（`struct Wrapper(Vec<i32>)`）把类型变成自己的。

**blanket impl**（泛型实现）是一次性给所有满足条件的类型补能力：

```rust
trait Shout { fn shout(&self) -> String; }
impl<T: std::fmt::Display> Shout for T {          // 所有 Display 类型
    fn shout(&self) -> String { self.to_string().to_uppercase() + "!" }
}
// "hey".shout() -> "HEY!"；42.shout() -> "42!"
```

标准库里 `impl<T: Display> ToString for T` 就是这个套路：你实现 `Display`，就白得一个 `to_string()`。
