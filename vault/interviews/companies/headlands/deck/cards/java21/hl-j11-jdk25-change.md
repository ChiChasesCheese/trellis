---
id: hl-j11-jdk25-change
node: java21.j11-structured-concurrency
type: qa
step: 16
---
## Q
`StructuredTaskScope` 的 API 在 JDK 25 改成了什么样？JDK 21 的 `ShutdownOnFailure` / `ShutdownOnSuccess` 怎么映射？

## A
**JDK 25**：作用域改用**静态工厂方法**打开，不再用公有构造器；完成策略由 **`Joiner`** 对象表达。默认 `StructuredTaskScope.open()` 的语义是「全部成功才成功，任一失败整体失败」；其他策略传 `open(Joiner)`，内置 joiner 有 `anySuccessfulResultOrThrow()`、`allSuccessfulOrThrow()`、`awaitAll()`、`awaitAllSuccessfulOrThrow()`、`allUntil(...)`，也可自己实现 `Joiner`。

| 想做的事 | JDK 21 | JDK 25+ |
|---|---|---|
| 全部成功才成功 | `new ShutdownOnFailure()` + `join().throwIfFailed()` | `open()` + `join()` |
| 第一个成功收工 | `new ShutdownOnSuccess<T>()` + `join().result()` | `open(Joiner.anySuccessfulResultOrThrow())` |
| 自定义 | 重写 `handleComplete` | 实现 `Joiner` |
