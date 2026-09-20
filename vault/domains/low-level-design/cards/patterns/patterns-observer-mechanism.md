---
id: patterns-observer-mechanism
node: patterns.observer
type: qa
step: 1
---
## Q
Observer 模式的核心机制是什么：subject 内部维护什么，通知（notify）时具体做什么？

## A
subject 维护一份订阅者列表（通常是一组可调用对象），订阅和退订通过 `subscribe()` / `unsubscribe()` 增删这份列表；事件发生时，subject 遍历列表逐个调用，把事件数据传给每一个订阅者。订阅者互不知道彼此，也不需要了解 subject 的内部状态，只依赖约定好的回调签名。

```python
from typing import Callable

class Subject:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[str], None]] = []

    def subscribe(self, fn: Callable[[str], None]) -> None:
        self._subscribers.append(fn)

    def notify(self, event: str) -> None:
        for fn in list(self._subscribers):
            fn(event)
```
