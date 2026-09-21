---
id: shield-protects-inner-task-not-outer-await
node: asyncio.cancellation
type: qa
source: python-docs
---
## Q
`await asyncio.shield(task)` 能保证外层协程被取消时，`task` 本身完全不受影响、外层也不会看到任何异常吗？

## A
`shield()` 只保护被包裹的 `task` 本身不因为外层协程的取消而被取消（`task` 会继续在后台跑完）；但外层这条 `await shield(task)` 语句仍然会因为收到取消请求而抛出 `CancelledError`——如果想让外层完全感知不到取消，需要额外用 `try/except CancelledError` 包一层去吞掉它（官方不推荐这样做）。
