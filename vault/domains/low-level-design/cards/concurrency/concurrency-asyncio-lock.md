---
id: concurrency-asyncio-lock
node: concurrency.asyncio
type: qa
step: 3
---
## Q
```python
async def reserve(key):
    if key not in taken:
        await notify_external_service(key)
        taken.add(key)
```
两个协程并发调用 `reserve("A")`，为什么还是会出现两次都通过了检查的竞态？怎么修？

## A
检查 `key not in taken` 和写入 `taken.add(key)` 之间隔了一次 `await`，而 `await` 正是协程的让出点：第一个协程检查完、发起网络调用后把控制权交还给事件循环，第二个协程这时候运行，同样检查到 `key not in taken`（还没被加入），于是两个协程都真的去调用了外部服务——这和 `threading` 里的 check-then-act 是同一类 bug，只是让出点从"任意字节码之间"变成了"每一个 `await`"。

修法是用 `asyncio.Lock`（专门给协程用，不是给线程用的）把跨 `await` 的检查和写入整体包起来：

```python
lock = asyncio.Lock()
async def reserve(key):
    async with lock:
        if key not in taken:
            await notify_external_service(key)
            taken.add(key)
```
`async with lock` 在等锁的时候本身也是一个让出点，不会阻塞整个事件循环。
