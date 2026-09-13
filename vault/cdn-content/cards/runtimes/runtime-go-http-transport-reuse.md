---
id: runtime-go-http-transport-reuse
node: runtimes.go-http
type: qa
---
## Q
A Go proxy creates a new `http.Client` for every origin request. Latency and file-descriptor use climb under load. What is wrong, and what should be long-lived?

## A
Each client usually creates or owns a `Transport`, so per-request construction defeats connection pooling and repeats TCP/TLS setup. Reuse one configured `http.Client` and `Transport` across goroutines; both are concurrency-safe. Always close or fully drain `resp.Body` so the connection can return to the pool. Tune per-host idle limits and timeouts for the origin fan-out, rather than relying blindly on defaults.

## Q zh
Go proxy 为每次 origin 请求都创建新的 `http.Client`。负载升高后 latency 和 file descriptor 一起上涨。问题是什么，哪些对象应该长期复用？

## A zh
每个 client 通常会创建或持有一个 `Transport`，逐请求构造会破坏 connection pooling，并重复支付 TCP/TLS 建连成本。应在 goroutine 之间复用一个配置好的 `http.Client` 和 `Transport`；两者都支持并发安全。必须关闭或完整读完 `resp.Body`，连接才能回到池中。根据 origin fan-out 调整每个 host 的 idle connection 上限和 timeout，不要盲用默认值。
