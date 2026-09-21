---
id: gather-schedules-coroutines-as-tasks
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
把一个裸协程对象（而不是 Task）传给 `asyncio.gather(coro())` 会怎么处理它？

## A
`gather()` 会自动把传入的裸协程对象包装成 `Task` 再调度执行，调用方不需要预先手动 `create_task()`；而结果列表的顺序永远和传入 `aws` 参数的顺序一致，与各任务实际完成的先后顺序无关。
