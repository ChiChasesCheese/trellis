---
id: hi-c-lld-patterns-b01-observer-weak
node: lld.in-a-hurry.patterns.beyond
type: qa
step: 1
---
## Q
**设计模式 · Python：观察者的弱引用与失败隔离**｜拓展 · 加分

Observer 在长期运行的系统里最常见的泄漏和故障是什么？Python 里怎么防？

## A
**模式。** 观察者加弱引用（weak reference）。

```python
import weakref


class Stock:
    def __init__(self) -> None:
        self._subs: weakref.WeakSet = weakref.WeakSet()   # 订阅者没人用就自动消失

    def attach(self, obs) -> None:
        self._subs.add(obs)

    def set_price(self, p: float) -> list[str]:
        errors = []
        for obs in list(self._subs):                      # 遍历快照：通知时允许退订
            try:
                obs.update(p)
            except Exception as e:                        # 一个失败不影响其他观察者
                errors.append(repr(e))
        return errors


class Display:
    def __init__(self) -> None:
        self.seen: list[float] = []

    def update(self, p: float) -> None:
        self.seen.append(p)


class Broken:
    def update(self, p: float) -> None:
        raise RuntimeError("boom")


s, d, b = Stock(), Display(), Broken()
s.attach(b)
s.attach(d)
assert len(s.set_price(1.0)) == 1 and d.seen == [1.0]
del d
import gc
gc.collect()
assert len(s._subs) == 1                                  # Display 已回收，不会泄漏
```
- **失效监听者（lapsed listener）：** 强引用列表让订阅者永远活着，忘记退订就是内存泄漏
- **弱引用的坑：** 绑定方法和 lambda 自己没有强引用会立刻被回收，需存对象本身，或用 `WeakMethod`
- **不要用时：** 订阅关系必须由系统持有时（后台任务回调），用强引用并显式退订
- 跨线程通知需要锁或把事件放进队列
