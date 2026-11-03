---
id: craft-dunder-protocols-that-pay-3-call-makes-objects-observers
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 3
---
## Q
**特殊方法 · 观察者实现 __call__ 与传函数有什么区别**｜写法

事件总线只要求订阅者是「能接收一个事件的可调用对象」。通知记录器需要保存收到的事件、还要提供 `recent()` 查询。写成带 `__call__` 的类，比起传 lambda 或者另写一个适配函数，好在哪里？什么时候反而该用普通函数？

## A
**要点。** 总线依赖的是协议（能被调用），不是类型。类实现 `__call__` 之后，实例可以直接注册，同时它保留自己的状态和其他方法，不需要再包一层。无状态的订阅者（把事件追加到某个列表）直接传绑定方法或函数，就别写类。

```python
class Notifier:
    """既是观察者（可调用），又保存自己收到的事件。"""
    def __init__(self) -> None:
        self._events: list[str] = []
    def __call__(self, event: str) -> None:          # 总线只要求 Callable[[str], None]
        self._events.append(event)
    def recent(self, n: int = 10) -> tuple[str, ...]:
        return tuple(reversed(self._events[-n:]))    # 快照，最新的在前

class Bus:
    def __init__(self) -> None:
        self._subs: list = []
    def subscribe(self, fn) -> None:
        self._subs.append(fn)
    def publish(self, event: str) -> None:
        for fn in self._subs:
            fn(event)

bus, n = Bus(), Notifier()
seen: list[str] = []
bus.subscribe(n)                       # 有状态的对象
bus.subscribe(seen.append)             # 无状态：绑定方法就够
bus.subscribe(lambda e: None)          # 一次性的
bus.publish("a"); bus.publish("b")
print(n.recent(), seen)
print(callable(n), callable(Notifier))
```

实际输出：

```
('b', 'a') ['a', 'b']
True True
```

**为什么。** 总线不需要知道订阅者是什么类型，所以三种写法能混着用；测试时也容易换成假订阅者。最后一行提醒：类本身也是可调用的，调用类就是构造实例，所以总线收到类和收到实例，类型检查都会通过，行为却完全不同。

**代价。** 实例一旦有可变状态，就要想并发：总线在多线程里调用同一个 `Notifier`，`_events` 要加锁。
