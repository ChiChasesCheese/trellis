---
id: hi-c-sd-scaling-reads-b02-coalescing-code
node: sd.patterns.scaling-reads.beyond
type: qa
step: 2
---
## Q
**读扩展 · 请求合并的正确写法**｜拓展 · 加分

把"同一个键只回源一次"写成异步代码，最容易漏的是什么？合并和分布式限流有什么关系？

## A
```python
import asyncio


class Coalescer:
    def __init__(self, fetch) -> None:
        self._fetch = fetch
        self._inflight: dict[str, asyncio.Future] = {}

    async def get(self, key: str):
        fut = self._inflight.get(key)
        if fut is not None:
            return await fut  # 搭便车：等先到的请求
        fut = asyncio.get_running_loop().create_future()
        self._inflight[key] = fut
        try:
            value = await self._fetch(key)
        except BaseException as exc:
            fut.set_exception(exc)  # 异常也要交给等待者，否则它们永远挂起
            fut.exception()  # 无人等待时标记为已取回，避免未取回告警
            raise
        else:
            fut.set_result(value)
            return value
        finally:
            del self._inflight[key]  # 成败都清理，下一波请求重新回源
```
- **最易漏：** 只在成功分支 `set_result`。回源抛异常时等待者永远收不到结果，请求堆积。
- **范围：** 只在进程内生效，所以后端最多被打 N 次（N 为应用服务器数），不是一次。asyncio 单线程调度，检查和登记之间没有 `await`，所以无需锁；多线程实现需要锁。
- **失败风暴：** 回源失败时所有等待者同时失败，调用方仍应有退避和降级，必要时对失败做短时间的负缓存。
