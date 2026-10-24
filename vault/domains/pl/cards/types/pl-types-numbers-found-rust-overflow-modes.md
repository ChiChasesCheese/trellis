---
id: pl-types-numbers-found-rust-overflow-modes
node: types.numbers
type: qa
step: 3
---
## Q
Rust 的整数溢出在 debug 和 release 构建里分别怎样处理？`cargo build` 的两种 profile 是什么？

## A
Rust 的构建有两种常用的配置（profile）：debug（`cargo build`，默认，不优化，带调试信息，编译快）和 release（`cargo build --release`，开启优化，运行快）。整数溢出的默认行为随配置而变：

- debug：溢出时 panic，程序终止并报告 `attempt to add with overflow`。
- release：不检查，按补码回绕（wrapping），`255u8 + 1` 得 0。

```rust
let n: u8 = std::env::args().count() as u8 + 254;   // 运行时得到 255
println!("{}", n + 1);
```

实际运行：debug 构建输出 `thread 'main' panicked ... attempt to add with overflow`；用 `-O` 编译的 release 构建输出 `0`。

设计理由：溢出几乎总是 bug，所以开发和测试时让它立刻暴露；但每次加法多一次检查有成本，发布时默认关掉。想要的行为可以显式指定，不依赖配置：`checked_add` 返回 `Option`，`wrapping_add` 总是回绕，`saturating_add` 停在上限。也可以在 `Cargo.toml` 的 `[profile.release]` 里设 `overflow-checks = true`，让 release 也检查。

Java 和 Go 没有这种区分：溢出永远回绕，不报错。
