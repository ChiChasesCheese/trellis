---
id: pl-eco-packages-intro-rust
node: ecosystem.package-managers
type: qa
step: 5
---
## Q
Rust 的 Cargo 怎样解析依赖？`Cargo.toml` 的 semver 约束、`Cargo.lock` 和「同一个库的多个主版本共存」分别是什么？

## A
**Cargo** 是 Rust 官方的构建工具兼包管理器，依赖来自 crates.io（中央仓库）。`Cargo.toml` 声明依赖，写 `serde = "1.0"` 默认的含义是**脱字符约束**（caret）：`>=1.0.0, <2.0.0`，即任何与 1.0 兼容的版本。`Cargo.lock` 记录求解结果，应用必须提交，库不必。

**解析策略**：取满足所有约束的**最新兼容版本**。生成锁文件之后，`cargo build` 一直用锁里的版本，除非运行 `cargo update`。

**多个主版本共存**：Cargo 把不同主版本视为不同的包。如果 `b` 依赖 `d` 1.x，`c` 依赖 `d` 2.x，Cargo 会把两个版本**都**编译进来，各用各的，不是冲突。真实输出（用本地路径模拟）：

```
$ cargo tree -d      # duplicated packages
d v1.0.0  <- b v0.1.0  <- app
d v2.0.0  <- c v0.1.0  <- app
```

`cargo run` 输出 `d 1.0.0 d 2.0.0`，两个版本同时在同一个二进制里工作。

**同一主版本内只保留一份**：如果两个约束都落在 1.x，Cargo 统一选一个满足两边的 1.x 版本。

**代价**：
1. 二进制变大，编译变慢。
2. 两个版本的类型不互通：`d1::Config` 与 `d2::Config` 是两个不同的类型，传给对方会报类型不匹配，这在公共 API 里暴露某个依赖的类型时特别痛。

**特性开关**（features）：crate 可以声明可选功能，依赖方选择开启哪些；解析时同一个 crate 的所有特性取**并集**，所以一个依赖开启的特性会影响所有人。

**要记住的一点**：Cargo 用「允许多版本共存」绕开了菱形依赖，把成本转移到二进制体积和类型互通上。
