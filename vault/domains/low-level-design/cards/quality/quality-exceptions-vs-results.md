---
id: quality-exceptions-vs-results
node: quality.errors
type: qa
---
## Q
Exceptions vs result types (`Result`/`Either`/`Optional`) — what's the decision rule, and what failure of each style should you name?

## A
Rule: model by **expectedness at the call site**.

- **Expected domain outcomes** the caller must handle every time — insufficient funds, seat already booked, validation failure — return a **result type**: the compiler forces handling, and outcomes are values you can log, map, and test.
- **Exceptional conditions** the immediate caller can't fix — connection lost, invariant broken, bug — **throw**, and let a boundary handler translate (crashing on a programmer error beats limping on).

Failure modes to name: exceptions for expected cases become **control flow** — invisible in signatures, easy to forget, expensive; results for truly unrecoverable errors force `.map/.flatMap` plumbing through code that could do nothing anyway. Never signal failure with `null` or sentinel values — that's the worst of both.

## Q zh
什么时候应该使用异常而不是返回结果对象？

## A zh
**使用异常**：
- 不可恢复的错误（null 指针、系统故障）
- 意外情况（违反前置条件）
- 编程错误（应该从不发生）

**使用结果对象**（Result、Option、Either）：
- 预期的故障模式（用户不存在、余额不足）
- 业务逻辑的一部分
- 调用者需要以不同的方式处理成功/失败
- Kotlin 的 `Result<T>`、Rust 的 `Result<T, E>`、Java 的 Optional

权衡：
- 异常：调用者无法忽略错误，但会隐藏流程
- 结果：显式处理，但调用者可能忽视失败情况

现代趋势：对预期的故障使用结果，对编程错误使用异常。
