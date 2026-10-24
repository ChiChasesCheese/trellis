---
id: pl-sig-rust-intro-fearless-cargo
node: signatures.rust
type: qa
step: 4
---
## Q
Rust 的“无畏并发”（fearless concurrency）靠 `Send`/`Sync` 怎样做到？`cargo` 又是怎样的一体化工具链？

## A
**`Send` 和 `Sync`**：两个标记 trait（没有方法，只表示一种性质），由编译器自动推导：
- `Send`：这个类型的值可以**转移**到另一个线程。
- `Sync`：这个类型的引用 `&T` 可以被**多个线程共享**。

标准库给每个类型标好：`Rc<T>`（非原子引用计数）不是 `Send`，因为计数器不是线程安全的；`Arc<T>`（原子引用计数）是；`Mutex<T>` 让可变数据可以安全共享。`thread::spawn` 要求闭包是 `Send`。

```rust
let r = Rc::new(5);
thread::spawn(move || println!("{}", r));
// error[E0277]: `Rc<i32>` cannot be sent between threads safely
```

把 `Rc` 换成 `Arc<Mutex<_>>`，四个线程各加一千次，真实输出 `4000`。**数据竞争在编译期被拒绝**，而不是靠测试偶然发现。

**无畏的含义**：不是“没有并发 bug”（死锁、逻辑竞争仍然可能），而是**数据竞争不可能出现在安全代码里**，你可以放心地重构并发代码，编译器会拦住不安全的改动。

**`cargo`**：官方的一体化工具：
- `cargo new/build/run/test`：创建、编译、运行、测试。
- `Cargo.toml` 声明依赖，`Cargo.lock` 固定版本，`crates.io` 是中央仓库。
- `cargo fmt`、`cargo clippy`、`cargo doc`、`cargo bench` 内置；文档注释中的代码块会被当作测试运行。
- workspace 支持多 crate 项目；`features` 控制可选功能。

**要记住的一点**：并发安全与工具链体验是 Rust 在系统语言里少见的两张王牌——它给了 C++ 开发者长期缺少的“依赖管理和测试开箱即用”。
