---
id: reliability-canonical-log-lines
node: reliability.observability
type: qa
---
## Q
What is a canonical log line (Stripe's pattern), and why does one wide structured line per request beat many scattered log lines when you are debugging production?

## A
- **The pattern**: at the end of every request, emit **one structured log line carrying every fact about that request** — request id, authenticated user/merchant, route and method, status code, timings (total, DB, external calls), rate-limit decisions, error class. "Wide" = many key-value fields; "canonical" = the one line you go to first.
- **Why it wins**: debugging becomes a query, not an archaeology dig. You can filter and aggregate across requests SQL-style ("p99 by merchant for this endpoint, last hour, only 429s") because every field lives on the same row. With scattered multi-line logs the same question requires joining fragments by request id and hoping the field you need was logged somewhere.
- **Where it sits**: metrics are pre-aggregated and low-cardinality (cheap, but can't drill to one request); traces show a request's call tree (deep, but sampled and heavyweight). The canonical line is the middle: per-request, cheap enough to keep for all requests, and queryable — the spine the other two hang off.

## Q zh
什么是 canonical log line（Stripe 的模式）？调试生产环境时，为什么每个请求一条宽的结构化日志行胜过许多零散的日志行？

## A zh
- **模式本身**：在每个请求结束时，输出**一条携带该请求所有关键事实的结构化日志行** — request id、已认证的用户/商户、路由与方法、状态码、耗时（总耗时、DB、外部调用）、rate-limit 决策、错误类别。"宽" = 大量键值字段；"canonical" = 你第一个去查的那一行。
- **为什么赢**：调试变成一次查询，而不是考古挖掘。因为所有字段在同一行上，你可以跨请求做 SQL 式的过滤和聚合（"这个端点按商户的 p99，最近一小时，只看 429"）。零散的多行日志要回答同样的问题，得按 request id 拼接碎片，还要祈祷你需要的字段恰好在哪里被打过。
- **它的位置**：metrics 是预聚合、低基数的（便宜，但无法下钻到单个请求）；trace 展示一个请求的调用树（深入，但有采样且笨重）。canonical line 居中：按请求、便宜到可以为所有请求保留、且可查询 — 是另外两者挂靠的脊柱。
