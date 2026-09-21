---
id: future-set-result-twice-raises
node: asyncio.futures
type: qa
source: python-docs
---
## Q
一个 Future 已经通过 `set_result()` 变成 done 状态后，再调用一次 `set_result()` 或 `set_exception()` 会发生什么？

## A
会抛出 `InvalidStateError`：Future 的结果只允许被设置一次，`set_result()`/`set_exception()` 会把 Future 标记为 done 并唤醒所有正在等待它的协程，done 之后状态就固定了，不能再改写结果或异常。
