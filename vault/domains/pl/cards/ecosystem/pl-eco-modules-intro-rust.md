---
id: pl-eco-modules-intro-rust
node: ecosystem.modules
type: qa
step: 4
---
## Q
Rust 的 crate、`mod` 树和可见性（`pub`、`pub(crate)`）分别是什么？为什么说 crate 才是编译单位？

## A
**crate**：Rust 的编译单位，也是发布单位。一个 crate 要么是可执行程序（有 `main`），要么是库。所有源文件通过 `mod` 声明连接成**一棵模块树**，作为一个整体一起编译。Cargo 的「package」包含一个或多个 crate，并带一个 `Cargo.toml`。

**`mod`**：模块是 crate 内部的命名空间，可以嵌套，可以对应文件（`mod cart;` 会去找 `cart.rs` 或 `cart/mod.rs`）。路径用 `::` 连接：`shop::cart::total()`。

**可见性默认私有**：不加修饰的条目只在**当前模块及其子模块**内可见。
- `pub`：对外公开（若它的所有父模块也是公开的）。
- `pub(crate)`：只在本 crate 内公开，不对外承诺。
- `pub(super)`、`pub(in path)`：更精细。

```rust
mod shop { pub mod cart {
    pub fn total() -> u32 { discount() * 2 }
    fn discount() -> u32 { 5 }      // private to `cart`
} }
shop::cart::discount();
// error[E0603]: function `discount` is private
```

同一个模块里的 `total` 可以调用私有的 `discount`，外部不行。

**为什么 crate 是编译单位**：编译器一次读入整个 crate 的所有文件，在内部做整体优化（内联、泛型实例化）；改了任何文件，整个 crate 都要重新编译（有增量编译缓解）。因此大项目常被拆成多个 crate（workspace）来缩短编译时间，同时也划出稳定的 API 边界。

**要记住的一点**：Rust 默认私有、逐级公开，`pub(crate)` 这样的中间档让库作者可以在 crate 内自由共享、对外仍然保持小接口。
