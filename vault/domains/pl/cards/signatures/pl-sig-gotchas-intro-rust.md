---
id: pl-sig-gotchas-intro-rust
node: signatures.gotchas
type: qa
step: 4
---
## Q
Rust 的“陷阱”和别的语言有什么不同？借用检查器的拉锯、整数溢出在调试与发布模式的差异、`Rc` 循环泄漏分别是什么表现？

## A
Rust 的大部分“陷阱”在编译期出现，表现为**摩擦**而不是**惊吓**。真正危险的几处恰恰是编译器**不管**的地方。

**1. 与借用检查器的拉锯（编译期）**。持有引用时修改容器：`let first = &v[0]; v.push(4); println!("{}", first);` 报 `error[E0502]: cannot borrow v as mutable because it is also borrowed as immutable`。编译器是对的（`push` 可能扩容），但初学者会觉得“我只是想读第一个元素”。根源：保守的静态证明。修法：缩短借用、先复制出值、或用索引。

**2. 整数溢出：调试 panic，发布回绕**。

```rust
let x: u8 = 255;
let y = x + args;         // args = 1
```

调试构建运行：`panicked at ... attempt to add with overflow`；用 `-O` 的发布构建运行：输出 `0`，静默回绕（真实输出）。根源：为性能，发布模式默认不检查溢出。修法：需要确定行为时用 `checked_add`、`wrapping_add`、`saturating_add`，或在 `Cargo.toml` 里开启发布模式的 `overflow-checks`。

**3. `Rc` 循环引用泄漏**。两个节点用 `Rc` 互相持有：

```rust
a.borrow_mut().next = Some(b.clone());   // a -> b -> a
// strong counts: 2 2   (never reaches 0, never freed)
```

真实输出：两个强引用计数都是 2，离开作用域后各减一变成 1，永远不释放。根源：引用计数无法回收环，这是**内存安全**的（泄漏不算不安全），所以编译器不管。修法：反向引用用 `Weak`。

**4. 字符串切片落在字符中间会 panic**：`&s[0..1]` 对 `"é"` 在运行时 panic，不是编译错误。

**5. `unwrap()` 的潜在 panic、`RefCell` 的运行时借用违规 panic**：把借用检查推迟到运行时的代价。

**6. 变量遮蔽（shadowing）**：`let x = ...; let x = ...;` 合法，用于转换类型很方便，也可能不小心遮住原值。

**共同点**：Rust 里最安全的一类陷阱是编译错误，最危险的一类是“内存安全但逻辑出错”：溢出、泄漏、panic。防线是 `clippy`、测试和对 `unwrap`/`unsafe` 的审查。
