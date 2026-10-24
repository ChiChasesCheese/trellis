---
id: pl-errors-result-type-foundation-thiserror-anyhow
node: errors.result-type
type: qa
step: 4
---
## Q
`thiserror` 和 `anyhow` 是什么？为什么 Rust 生态里有这两个库？

## A
两个都是社区的第三方库（crate），不是标准库，解决 `Result` 用起来的两类样板：

**`thiserror`**：用一个派生宏（derive macro，编译期自动生成代码的标注）为你的错误枚举生成 `Display`（错误的可读文字）和 `From`（从底层错误转换）的实现。

```rust
#[derive(thiserror::Error, Debug)]
enum StoreError {
    #[error("key {0} not found")]
    NotFound(String),
    #[error("io failure")]
    Io(#[from] std::io::Error),
}
```

用于**库**：调用者可以对枚举 `match`，区分不同失败。

**`anyhow`**：提供一个能装下任何错误的类型 `anyhow::Error`，和 `.context("...")` 方法给错误加说明。

```rust
let s = std::fs::read_to_string("/nope").context("reading config")?;
```

用于**应用**：顶层不需要区分种类，只需要一条完整的因果链。本机实测，`get("zz").context("lookup failed")?` 在 `main` 里失败时打印：

```console
Error: lookup failed

Caused by:
    key zz not found
```

要记住的一个事实：库返回具体的枚举让调用者能 `match`，应用用 `anyhow` 图方便并保留因果链。
