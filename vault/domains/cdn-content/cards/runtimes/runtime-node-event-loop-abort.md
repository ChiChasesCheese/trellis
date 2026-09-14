---
id: runtime-node-event-loop-abort
node: runtimes.node-event-loop
type: qa
---
## Q
The browser disconnects during a slow origin fetch, but the Node server keeps downloading and transforming the response. What lifecycle signal is missing?

## A
Cancellation is not propagating. Create an `AbortController`, abort it when the inbound request closes or its deadline expires, and pass its `signal` to `fetch`, stream pipelines, and owned async work. Handle `AbortError` as expected cancellation, release buffers and file handles, and avoid starting new stages after abort. A rejected promise alone does not guarantee the underlying I/O stopped unless the API consumes the signal.

## Q zh
浏览器在 slow origin fetch 中途断开，但 Node server 仍继续下载并转换响应。缺少什么 lifecycle signal？

## A zh
缺少 cancellation propagation。创建 `AbortController`，在 inbound request 关闭或 deadline 到期时 abort，并把 `signal` 传给 `fetch`、stream pipeline 和 owned async work。把 `AbortError` 当作预期 cancellation 处理，释放 buffer 与 file handle，abort 后不要启动新阶段。仅有 rejected promise 不代表底层 I/O 已停止，除非 API 实际消费该 signal。
