---
id: pl-errors-result-type-best-practice
node: errors.result-type
type: qa
step: 8
---
## Q
Rust 里使用 `Result` 和 `Option` 的最佳实践是什么？

## A
1. **库返回具体的错误枚举，应用用 `anyhow`**。库的错误用 `thiserror` 定义，每个变体对应调用者可能想区分的情形，并用 `#[from]` 自动转换底层错误。应用的 `main` 和高层函数返回 `anyhow::Result<T>`，在每一层用 `.context("正在做什么")` 加描述。不要在库的公共 API 里返回 `anyhow::Error`，那会让调用者无法 `match`。
2. **在生产代码里避免 `unwrap()`**。它在 `None`/`Err` 时 panic，信息还很少。必须用时写 `expect("为什么这里一定成功")`，让这条信息说明不变量，而不是复述错误。测试和原型里用 `unwrap` 没问题。
3. **用组合器和 `?` 把成功路径写成直线**；`ok_or` / `ok_or_else` 把 `Option` 转成 `Result`；`map_err` 转换错误类型；遍历时 `collect::<Result<Vec<_>, _>>()` 一次收集所有结果，遇到第一个错误就停止。
4. **`main` 返回 `Result`**：失败时进程以非零状态码退出，并打印错误。
5. **不要用 `Result<T, String>`**。字符串无法被程序区分，也不实现 `Error` trait。至少用自定义类型。
6. **错误携带数据，不仅是消息**：把导致失败的值（文件名、键）放在变体里，调用者可以据此决定动作。
7. **区分「预期的失败」与「bug」**：前者返回 `Err`，后者（违反不变量）用 `panic!`/`assert!`/`expect`。
8. **`#[must_use]` 与 lint**：保持 `unused_must_use` 警告开启，CI 里用 `-D warnings`，不丢弃结果。

在 C++ 里的对应做法：返回 `std::expected`（C++23，装着值或错误的结果类型）的函数一律标 `[[nodiscard]]`（丢弃返回值时警告）；取值前先检查 `has_value()`，或用 `value_or`、`transform`、`and_then` 组合，不要直接写 `*r`（失败时是未定义行为，标准不规定后果）；错误类型用枚举或带数据的结构，不用 `std::string`（同样无法被程序区分）。
什么时候违反：快速的 CLI 或脚本里，直接用 `anyhow` 和 `?` 一路到 `main`，足够好。
