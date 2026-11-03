---
id: craft-retry-backoff-dead-letter-4-dead-letter-is-a-record
node: craft.patterns.retry-backoff-dead-letter
type: qa
step: 4
---
## Q
**重试、退避与死信 · 死信应该记录什么，处理死信本身失败怎么办**｜模式

发布订阅里，订阅者的处理函数有 bug，每次收到事件都抛 `KeyError`。重试用尽以后，这条事件怎么办？直接丢掉、重新抛出、还是别的？死信的接收方自己也可能挂，又怎么办？

## A
**要点。** 重试用尽的事件变成一条**死信记录**返回，而不是异常。记录里至少有：谁（订阅者）、什么事件、为什么（枚举：处理失败、信箱满被挤掉）、试了几次、最后一次的错误。投递循环永远不被订阅者的 bug 打断：订阅者的异常是数据，不是控制流。死信的处理函数也可能失败，同样要吞掉，否则一个坏的死信接收方会杀死整条投递线程。

```python
from dataclasses import dataclass
from enum import Enum

class Reason(Enum):
    HANDLER_FAILED = "handler_failed"    # 重试用尽
    QUEUE_FULL = "queue_full"            # 没机会被处理就被挤掉

@dataclass(frozen=True)
class DeadLetter:
    subscriber: str; event: str; reason: Reason; attempts: int; error: str = ""

class Subscription:
    def __init__(self, name, handler, max_attempts=3):
        self.name, self.handler, self.max_attempts = name, handler, max_attempts
        self.delivered = self.failed = 0

    def deliver(self, event) -> DeadLetter | None:
        error = ""
        for _ in range(self.max_attempts):
            try: self.handler(event)
            except Exception as exc:                      # 订阅者的 bug 不许逃出去
                error = f"{type(exc).__name__}: {exc}"; continue
            self.delivered += 1; return None
        self.failed += 1
        return DeadLetter(self.name, event, Reason.HANDLER_FAILED, self.max_attempts, error)

calls = []
def buggy(e): calls.append(e); raise KeyError("missing field")
sub = Subscription("billing", buggy)
dl = sub.deliver("evt-1")
print(dl)
print("调用次数:", len(calls), " 统计:", (sub.delivered, sub.failed))

def on_dead(dl): raise OSError("dead-letter sink down")      # 死信接收方自己也挂了
try: on_dead(dl)
except Exception: pass                                        # 吞掉：不许炸掉投递线程
print("死信处理失败后，投递线程仍在继续")
```

```
DeadLetter(subscriber='billing', event='evt-1', reason=<Reason.HANDLER_FAILED: 'handler_failed'>, attempts=3, error="KeyError: 'missing field'")
调用次数: 3  统计: (0, 1)
死信处理失败后，投递线程仍在继续
```

**为什么。** 丢掉是悄悄的数据丢失；重新抛出让一个坏订阅者拖垮发布者和其他订阅者。死信把失败变成可查、可重放的数据：修好 bug 后，可以把死信重新投递。原因用枚举区分，是因为处理方式不同：`QUEUE_FULL` 是容量问题（没机会处理），`HANDLER_FAILED` 是代码问题（处理过但失败）。

**代价。** 死信也是一个容器，必须有上限或保留期，否则它自己成了泄漏（见有界容器那一叶）；死信里的事件可能含敏感数据，要和主数据同等对待。

**易错。** 统计计数（delivered / failed / dropped）要和死信同步更新，这样 `delivered + failed + dropped` 等于发出的总数，对账时不会缺口。
