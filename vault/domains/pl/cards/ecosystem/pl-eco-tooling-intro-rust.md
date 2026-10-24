---
id: pl-eco-tooling-intro-rust
node: ecosystem.tooling
type: qa
step: 3
---
## Q
Rust 官方工具链里的 `rustfmt`、`clippy` 和 `cargo test` 各做什么？`clippy` 与编译器的警告有什么区别，一个例子里它抓到什么？

## A
这些工具都由 `cargo` 命令统一调用（`cargo fmt`、`cargo clippy`、`cargo test`），随 `rustup` 官方安装。

**`rustfmt`**：官方格式化器，风格接近唯一，有少量可调选项写进 `rustfmt.toml`。

**编译器自身的检查**已经很严：所有权与借用、类型、未使用变量的警告、穷尽匹配。`clippy` 是**在此之上的风格与惯用写法检查器**，有几百条规则（lint），分级：`correctness`（几乎肯定是 bug，默认报错）、`style`、`perf`、`complexity`、`pedantic`（默认不开）。

一个故意写得不地道的程序，`cargo clippy` 的真实输出（节选）：

```
warning: the loop variable `i` is only used to index `v`
warning: this creates an owned instance just for comparison
warning: called `unwrap` on `x` after checking its variant with `is_some`
```

分别对应：`for i in 0..v.len()` 应该写成 `for x in &v`；`t == "a".to_string()` 白白分配了一个 `String`；先 `is_some()` 再 `unwrap()` 应该用 `if let`。其中有的只是风格，有的会指出性能或潜在 panic。

**`cargo test`**：测试在源文件里的 `#[cfg(test)] mod tests` 模块里，用 `#[test]` 标记；`tests/` 目录放集成测试；文档注释里的代码块**也会被当作测试运行**（doctest），保证文档里的示例不会过期。

**要记住的一点**：Rust 的编译器负责“正确性”，`clippy` 负责“地道性”，二者都随官方工具链，并习惯在 CI 里用 `-D warnings` 把警告当错误。
