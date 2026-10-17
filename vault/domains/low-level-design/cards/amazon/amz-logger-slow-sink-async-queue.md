---
id: amz-logger-slow-sink-async-queue
node: amazon.amz-logger
type: qa
step: 5
tags: [grown]
---
## Q
在日志框架设计里，磁盘或网络写得慢时，怎样不拖慢业务线程？队列满了怎么办？

## A
做一个 `AsyncHandler` 包住真正的 Handler：业务线程只把 record 放进有界队列（`queue.Queue(maxsize=N)`），后台线程取出来写。队列满的三种策略：丢新日志并计数（默认，业务优先）、丢最旧、阻塞调用方（审计日志不能丢时用）。无界队列会在下游卡住时把内存吃光。关闭时先排空队列再退出线程。
```python
class AsyncHandler:
    def __init__(self, inner, maxsize=1000):
        self.inner, self.dropped = inner, 0
        self._q = queue.Queue(maxsize)

    def handle(self, record):
        try:
            self._q.put_nowait(record)
        except queue.Full:
            self.dropped += 1
```
