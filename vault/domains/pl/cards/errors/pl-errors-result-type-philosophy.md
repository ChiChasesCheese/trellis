---
id: pl-errors-result-type-philosophy
node: errors.result-type
type: qa
step: 4
---
## Q
Rust 为什么既有 `Result`，又用 `thiserror` 与 `anyhow` 两套工具？这反映了怎样的设计哲学？

## A
Rust 的错误处理背后的哲学是：**库和应用对错误的需求不同，语言不替你做统一的决定，而是给出组合的工具。**

- **库**的使用者是别的程序员。他们需要根据错误的种类做不同的事：重试、回退、报告。所以库应当暴露一个具体的、可 `match` 的错误类型，通常是一个枚举。`thiserror` 通过派生宏省去手写 `Display` 与 `From` 的样板。库的错误类型是它的 API 的一部分。
- **应用**的使用者是最终用户或运维。顶层只关心「出错了，给出清楚的原因链并退出或返回 500」，不需要逐种类处理。`anyhow::Error` 是一个能装下任何错误的类型，配合 `.context("...")` 逐层加上描述，打印出一条因果链。

```console
reading config: No such file or directory (os error 2)
Error: lookup failed

Caused by:
    key zz not found
```

这是一次真实运行的输出：上面一行是 `{:#}` 格式的单行链，下面是 `main` 返回 `Err` 时的多行格式。

这种分工体现了 Rust 的几个态度：
1. **类型就是文档**：库的错误枚举精确列出了会发生什么。
2. **不替你选**：标准库只给 `Result` 和 `Error` trait，具体怎么封装，生态来补充，库可以随时演进。
3. **成本分摊**：应用层用动态的 `anyhow` 换取方便，付出一次装箱；库保持静态类型，调用者可以零成本匹配。

与 Go 对照：Go 的 `error` 接口既是库的错误类型，又是应用的错误类型，一个统一的开放接口；Rust 把二者拆开，库用封闭的枚举，应用用开放的动态类型，各取所长。
