---
id: uth-compose-event-bus-3-invariants-code
node: compose.event-bus
type: qa
step: 3
---
## Q
**不变量与最小实现**｜Guava EventBus · 33.5.0

写一个最小的事件总线，说清登记和发布各自先后做什么、为什么发布期间有人退订也不会出错。

## A
**不变量。**

- 每个事件类型对应的订阅者集合从不被原地修改：读者拿到的永远是完整的一份，增删只发生在新副本上。
- 同一个订阅者重复登记只留一份。
- 一个订阅者出错，不能影响同一次发布里后面的订阅者。

**顺序。** 登记或退订：拿锁 → 复制旧集合 → 改副本 → 整体换上。发布：不拿锁 → 展开事件的类和父类 → 每个类型取当时的集合 → 逐个调用。

```python
import threading
from collections.abc import Callable
from typing import Any

Handler = Callable[[Any], None]


class EventBus:
    def __init__(self) -> None:
        self.subs: dict[type, tuple[Handler, ...]] = {}      # 事件类型 -> 订阅者；元组不可变，当快照用
        self.lock = threading.Lock()                         # 只在注册 / 注销时用

    def register(self, event_type: type, handler: Handler) -> None:
        with self.lock:                                      # 写时复制：造一个新元组，再整个换上去
            old = self.subs.get(event_type, ())
            if handler not in old:                           # 同一个订阅者重复注册只算一次
                self.subs[event_type] = (*old, handler)

    def unregister(self, event_type: type, handler: Handler) -> None:
        with self.lock:
            old = self.subs.get(event_type, ())
            self.subs[event_type] = tuple(h for h in old if h != handler)

    def post(self, event: object) -> None:
        for cls in type(event).__mro__:                      # 事件的类、父类，一直到 object
            for handler in self.subs.get(cls, ()):           # 读不加锁：拿到的元组再也不会被改
                try:
                    handler(event)
                except Exception as exc:                     # 一个订阅者出错不能连累后面的
                    print("handler failed:", exc)
```

**坑。** 发布期间有人退订，这一次发布仍会通知到他，因为集合是发布开始时拿到的快照；订阅者在自己的处理函数里退订自己，也不会崩。

**对应 LeetCode：** 无直接对应的题
