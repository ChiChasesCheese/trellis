---
id: cancel-return-false-if-already-done
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
`task.cancel()` 一定能成功取消任务吗？它的返回值代表什么？

## A
`cancel()` 只是「请求」取消：如果任务已经 done 或已经 cancelled，直接返回 `False`，什么也不做；否则返回 `True` 并安排在下次事件循环周期注入 `CancelledError`——但被注入异常后协程仍可以在 `try/except CancelledError` 里吞掉这个异常来拒绝取消（并不保证真的会被取消），只是官方强烈不建议这么做。
