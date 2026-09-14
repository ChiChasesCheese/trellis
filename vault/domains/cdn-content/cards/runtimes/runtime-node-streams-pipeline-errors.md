---
id: runtime-node-streams-pipeline-errors
node: runtimes.node-streams
type: qa
---
## Q
An image pipeline manually chains `readable.pipe(resizer).pipe(response)`. One stage fails, but file descriptors remain open. Why prefer `pipeline()`?

## A
Manual `pipe()` does not by itself provide one completion/error boundary for every stage. `pipeline()` forwards backpressure, destroys the connected streams on failure, and resolves or rejects only when the chain settles. Use the promise form with an `AbortSignal`, handle the single terminal error, and ensure temporary outputs are published only after success. This turns partial-stream cleanup into a lifecycle guarantee rather than scattered event handlers.

## Q zh
image pipeline 手动串联 `readable.pipe(resizer).pipe(response)`。某阶段失败后 file descriptor 仍未释放。为什么应优先用 `pipeline()`？

## A zh
手动 `pipe()` 本身不会为所有阶段提供统一 completion/error boundary。`pipeline()` 会传播 backpressure、失败时 destroy 相连 streams，并只在整个 chain settle 后 resolve 或 reject。使用带 `AbortSignal` 的 promise 版本，只处理一个 terminal error，并确保 temporary output 仅在成功后 publish。这样 partial-stream cleanup 成为 lifecycle guarantee，而不是分散的 event handler。
