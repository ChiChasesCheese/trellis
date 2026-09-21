---
id: taskgroup-cancels-siblings-on-error-gather-does-not
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
同样是并发跑一组任务，`asyncio.TaskGroup`（3.11 起）相比 `asyncio.gather` 提供了什么更强的安全保证？

## A
在 `TaskGroup` 里，只要有一个子任务（或它调度出的孙任务）抛出异常，`TaskGroup` 会主动取消组内其它还未完成的任务，再统一收尾退出；而 `gather` 默认（`return_exceptions=False`）遇到异常只会向外传播，并不会取消其它还在跑的可等待对象，容易留下「孤儿」任务继续消耗资源。
