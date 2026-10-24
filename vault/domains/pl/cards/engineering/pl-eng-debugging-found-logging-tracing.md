---
id: pl-eng-debugging-found-logging-tracing
node: engineering.debugging
type: qa
step: 5
---
## Q
结构化日志（structured logging）和分布式追踪（distributed tracing）是什么？为什么线上排障要给每个请求带一个 ID，各语言怎样做？

## A
**结构化日志**：每条日志不是一段自由文本，而是一个事件，带有机器可解析的键值字段（通常是 JSON）。好处是可以按字段查询和聚合：“`req_id = r-42` 的所有日志”“`err = card_declined` 每分钟多少次”。

Go 1.21 起标准库就有 `log/slog`：
```go
log := base.With("req_id", "r-42", "user", 7)   // attach once
log.Info("charge started", "amount_cents", 1299)
log.Error("charge failed", "err", "card_declined", "attempt", 2)
```
输出：
```
{"level":"INFO","msg":"charge started","req_id":"r-42","user":7,"amount_cents":1299}
{"level":"ERROR","msg":"charge failed","req_id":"r-42","user":7,"err":"card_declined","attempt":2}
```
`With` 绑定的字段出现在之后的每一行。Java 用 SLF4J + Logback，靠 `MDC`（线程绑定的键值）达到同样效果；Python 的 `logging` 加 `contextvars` 或 `structlog`；Rust 的 `tracing` 用**跨度**（span）：

```rust
let span = info_span!("request", req_id = "r-42", user = 7);
let _guard = span.enter();
info!("charge started");            // request{req_id="r-42" user=7}: charge started
```
进入跨度之后的所有事件都自动带上它的字段。

**分布式追踪**把同样的想法扩展到跨服务：请求进入系统时生成一个**追踪 ID**（trace id），每经过一个服务/操作产生一个**跨度**（有开始、结束、父子关系），并通过 HTTP 头往下游传递。标准格式是 W3C 的 `traceparent: 00-<32位十六进制trace id>-<16位span id>-01`。OpenTelemetry 是跨语言的统一标准，四门语言都有 SDK。

**为什么必须有请求 ID**：线上一个用户请求会经过多个服务、多个线程/协程，日志在时间上交错。没有 ID，就只能按时间猜；有了它，一条查询就能还原一个请求的完整经过。
