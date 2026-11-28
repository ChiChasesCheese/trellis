---
id: hi-c-lld-coordination-b03-py-async-actor
node: lld.concurrency.coordination.beyond
type: qa
step: 3
---
## Q
**并发协调 · Python：asyncio 版 actor 与回信**｜拓展 · 加分

在 asyncio 里实现 actor 比线程版简单在哪？请求-应答怎么做？

## A
**模式。** 邮箱加顺序处理（mailbox actor）；回信靠消息里带一个 Future。

```python
import asyncio
from dataclasses import dataclass


@dataclass
class Deposit:
    amount: int


@dataclass
class Balance:
    reply: asyncio.Future


class AccountActor:
    def __init__(self, mailbox_size: int = 100) -> None:
        self._box: asyncio.Queue = asyncio.Queue(mailbox_size)   # 有界邮箱：满了发送方等待
        self._bal = 0
        self._task = asyncio.create_task(self._run())

    async def send(self, msg) -> None:
        await self._box.put(msg)

    async def _run(self) -> None:
        while True:
            msg = await self._box.get()
            try:
                match msg:
                    case Deposit(amount):
                        self._bal += amount               # 一次一条，不会交错
                    case Balance(reply):
                        reply.set_result(self._bal)       # 回信
            except Exception as e:                        # 处理器出错不能杀死 actor
                print("handler error", e)
            finally:
                self._box.task_done()


async def main() -> None:
    a = AccountActor()
    await asyncio.gather(*(a.send(Deposit(1)) for _ in range(1000)))
    fut = asyncio.get_running_loop().create_future()
    await a.send(Balance(fut))
    assert await fut == 1000
    a._task.cancel()


asyncio.run(main())
```
- **为什么没有竞态：** 事件循环是单线程，协程只在 `await` 处让出；`_bal += amount` 中间没有 `await`，不可能被切走
- **处理器里 `await` 外部调用：** 同一 actor 仍一次只处理一条消息，状态不会被穿插；但它等待期间其他 actor 在运行，它读到的外部数据可能已过期
- **异常：** 处理器未捕获的异常会终止 `_run`，之后邮箱满了所有发送方永远卡住；必须兜住
- **何时不用：** CPU 密集的处理会卡住整个事件循环，改用线程或进程
