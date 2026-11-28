---
id: hi-c-sd-chatgpt-b04-slow-client
node: sd.problem-breakdowns.chatgpt.beyond
type: qa
step: 4
---
## Q
**ChatGPT · 拓展：客户端读得慢，谁来承担积压**｜拓展 · 加分

手机网络很差，SSE 写不出去，聊天服务内存里会堆积 token。怎样避免一个慢客户端拖垮实例？

## A
**模式。** 拉取式读取加有界缓冲：消费者按自己的速度拉，生产者不被阻塞也不无限堆积。

```python
import asyncio


async def relay(read_batch, write, max_buffer: int = 64) -> None:
    """read_batch(last_id) -> (entries, new_last_id)；write(entry) 在客户端慢时会挂起。"""
    buf: asyncio.Queue = asyncio.Queue(max_buffer)         # 有界：满了 put 会挂起，读取随之放缓

    async def reader() -> None:
        last = "0"
        while True:
            entries, last = await read_batch(last)         # 相当于阻塞的 XREAD
            for e in entries:
                await buf.put(e)                           # 背压：不会一直读到内存里

    async def writer() -> None:
        while True:
            await write(await buf.get())

    r, w = asyncio.create_task(reader()), asyncio.create_task(writer())
    done, pending = await asyncio.wait({r, w}, return_when=asyncio.FIRST_EXCEPTION)
    for p in pending:
        p.cancel()                                          # 任一边失败（客户端断开）就收尾
    for d in done:
        d.result()
```
- **为什么：** 用 Redis Stream 读时，积压留在 Stream（有 `MAXLEN` 上限），而不是留在聊天服务的进程里；慢客户端只会让自己的读取推迟，不影响工作者生成，也不影响其他连接。
- **纯 pub/sub 推送的对比：** 订阅者回调里堆积，慢客户端会把积压变成实例内存增长。
- **客户端落后太多：** 要么追上（直接跳到最新并告知），要么断开让它用 `Last-Event-ID` 重连。
- **代价：** 比直接转发多一层队列和任务，延迟略增；`maxsize` 要按"可容忍的落后 token 数"选。
