---
id: pl-eco-compat-intro-rust
node: ecosystem.compatibility
type: qa
step: 4
---
## Q
Rust 的 edition（语言版本）机制是什么？它怎样做到“允许不兼容的语法变化，却不分裂生态”？

## A
**是什么**：Rust 每隔约三年发布一个 edition（2015、2018、2021、2024）。edition 是 crate 级的选择：每个 crate 的 `Cargo.toml` 里写 `edition = "2021"`，编译器按对应规则解析这个 crate。

**允许什么样的变化**：可以改变语法和少量语义，包括引入新关键字、改变路径解析规则、调整某些方法的解析方式。例如 2018 版把 `async` 变成关键字：

```
rustc --edition 2015 e.rs   // let async = 1;  compiles, prints 1
rustc --edition 2018 e.rs   // error: expected identifier, found keyword `async`
```

真实输出如注释：同一行代码，在 2015 下合法，在 2018 下是错误。

另一个例子：`array.into_iter()` 在 2018 下按引用迭代，编译器还会警告“due to backwards compatibility … will resolve to `<[T; N] as IntoIterator>::into_iter` in Rust 2021”；在 2021 下按值迭代。

**不分裂生态的关键**：
1. **互操作**：不同 edition 的 crate 可以互相依赖、链接在一起。edition 只影响一个 crate 自己的**前端解析**，编译后进入同一个中间表示，语义一致。
2. **自动迁移**：`cargo fix --edition` 机械地改写代码，大部分迁移无需人工。
3. **边界清楚**：不允许 edition 改变标准库 API 或类型系统的根基，只改变表面语法与解析。

**与语言版本的区别**：edition 不是新语言，它是“在同一个编译器里，按 crate 选择的一套语法方言”。所有 Rust 编译器的新版本仍支持所有旧 edition。

**要记住的一点**：Rust 用“每个 crate 自己选方言”的办法，把破坏性变化局部化。
