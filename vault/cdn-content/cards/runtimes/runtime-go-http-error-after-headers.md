---
id: runtime-go-http-error-after-headers
node: runtimes.go-http
type: qa
---
## Q
A Go handler writes `200 OK`, starts streaming a large object, then the origin read fails. Why can it no longer return `502`, and what should the design do?

## A
Once headers or body bytes are committed, the status code is on the wire; a later `WriteHeader(502)` cannot replace it. Detect failures before commitment when buffering a small response is affordable. For true streaming, propagate cancellation, terminate the stream, record a distinct metric, and let the client observe a truncated transfer and retry safely. Never cache or mark complete an object until its full body and integrity checks succeed.

## Q zh
Go handler 已写出 `200 OK` 并开始 streaming 大对象，随后读取 origin 失败。为什么此时不能再返回 `502`，设计应该怎么处理？

## A zh
headers 或 body bytes 一旦 committed，status code 就已上网；之后调用 `WriteHeader(502)` 无法替换它。小响应可以在成本可接受时先 buffer，提交前发现错误。真正的 streaming 应传播 cancellation、终止 stream、记录独立 metric，让客户端观察到 truncated transfer 并安全 retry。完整 body 和 integrity check 成功前，绝不能缓存或标记对象完成。
