---
id: pl-errors-cost-best-practice
node: errors.cost
type: qa
step: 7
---
## Q
考虑错误处理的性能时，各语言的工程师应该遵循哪些做法？

## A
通用原则：**先区分失败是罕见还是常见，再选机制；其次测量，别凭感觉。**

**Java**
1. 不要用异常表示常见的、预期内的情况（`parseInt` 失败后回退、缓存未命中、迭代结束）。用返回值、`Optional` 或先检查，例如用 `Map.get` 判空，而不是捕获 `NoSuchElementException`。
2. 如果必须在热路径上用异常传递控制，使用预先创建的、不填栈追踪的异常对象（重写 `fillInStackTrace`，或用 `super(msg, cause, false, false)` 构造）。
3. 不要在每次失败时都打印完整栈追踪，日志量和 I/O 成本会放大问题。

**Python**
1. 失败罕见时坚持 EAFP（直接 `try`），不抛时零成本，也避免竞态。
2. 失败很常见时（例如 50% 的键不存在），用 `dict.get`、`in` 检查，或 `setdefault`，比抛异常快数倍。
3. 在热循环里，不要把异常当作控制流退出手段，用 `break`。

**Go**
1. 热路径上返回预先创建的哨兵错误（`var ErrBusy = errors.New(...)`），不要每次 `fmt.Errorf`；包装留给不在热路径上的位置，或在向上传递到日志边界时再加上下文。
2. 不要在高频路径上用 `panic`/`recover` 当控制流，其成本远高于返回错误。

**Rust**
1. `Result` 本身很便宜；真正的成本在错误类型：避免在热路径上构造带 `String` 的错误，用枚举变体承载数据。
2. 需要栈追踪的库（`anyhow`）只在需要时才捕获 backtrace。

**共同**：用基准或 profile 验证，比如 Java 用基准框架 JMH、Go 用 `testing.B`。成本差异常常是数量级，容易测出来。

什么时候违反：不在热路径上的代码，请按清晰度选择机制，不必为纳秒级差异扭曲设计。
