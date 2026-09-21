---
id: future-done-callback-scheduled-not-sync
node: asyncio.futures
type: qa
source: python-docs
---
## Q
用 `future.add_done_callback(cb)` 注册的回调，是在 Future 变成 done 的那一刻同步立即执行的吗？

## A
不是。即使调用 `add_done_callback()` 时 Future 已经是 done 状态，回调也不会被同步立即调用，而是通过 `loop.call_soon()` 排进事件循环的下一轮调度——这保证了回调总是异步触发，行为一致，不会因为「注册时机早晚」而产生同步执行的意外情况。
