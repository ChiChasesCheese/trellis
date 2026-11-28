---
id: hi-c-lld-elevator-b03-py-inbox
node: lld.problem-breakdowns.elevator.beyond
type: qa
step: 3
---
## Q
**电梯系统 · Python：用收件箱队列让 `step` 独占状态**｜拓展 · 加分

并发呼叫时不加锁，怎么让多个线程安全地交请求？这样为什么正确？

## A
**模式。** 单写者（single writer）：状态只被一个线程修改，其他线程通过消息队列提交意图。

```python
import queue
import threading
from dataclasses import dataclass


@dataclass(frozen=True)
class Req:
    floor: int


class Elevator:
    def __init__(self) -> None:
        self._inbox: queue.SimpleQueue[Req] = queue.SimpleQueue()   # 线程安全，无界
        self.requests: set[Req] = set()                             # 只有 step 所在线程碰它

    def add(self, r: Req) -> None:          # 任意线程可以调用
        self._inbox.put(r)

    def step(self) -> None:
        while True:                         # 每拍开头把收件箱倒空，再用普通集合工作
            try:
                self.requests.add(self._inbox.get_nowait())
            except queue.Empty:
                break
        # ... 之后的 SCAN 逻辑只读写 self.requests


e = Elevator()
ts = [threading.Thread(target=lambda b=b: [e.add(Req(b * 1000 + k)) for k in range(500)])
      for b in range(4)]
for t in ts:
    t.start()
while any(t.is_alive() for t in ts):
    e.step()                                # 与写入线程同时运行
for t in ts:
    t.join()
e.step()
assert len(e.requests) == 2000              # 一个都没丢，也没有锁
```
- **为什么正确：** 队列内部处理了并发入队和出队；`requests` 集合从头到尾只被调用 `step` 的那个线程碰，没有并发访问就没有竞态。
- **与加锁相比：** 呼叫线程不会被 `step` 阻塞；代价是新请求要等下一拍才被看见，多了最多一拍的延迟。
- **仍要注意：** "选哪部电梯"依赖电梯当前的方向和位置，这些由 `step` 线程修改，读到的是略旧的快照；要精确就把派发也放进同一个线程的消息循环。
- **何时不用：** 单线程模拟不需要；强一致派发（读到的状态必须最新）时还是锁或单线程事件循环更直接。
