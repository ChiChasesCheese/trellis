---
slug: event-emitter
---
## Q
**LC 2694 事件发射器**｜Medium

（原题为 JavaScript，这里用 Python。）设计 `EventEmitter`：`subscribe(event, cb)` 订阅并返回带 `unsubscribe()` 的对象；`emit(event, args)` 按订阅顺序调用所有回调（`args` 展开传入），返回结果列表，无订阅者返回 `[]`。

## A
**一句话。** 两层字典 `事件名 -> {订阅编号: 回调}`，`dict` 保持插入顺序即订阅顺序，取消订阅按编号删一项。

```python
class Subscription:
    def __init__(self, release):
        self._release = release

    def unsubscribe(self):
        self._release()

class EventEmitter:
    def __init__(self):
        self._subs = defaultdict(dict)   # 事件 -> {编号: 回调}
        self._next_id = 0

    def subscribe(self, event_name, callback):
        sub_id = self._next_id           # 同一函数订阅两次也能分别取消
        self._next_id += 1
        self._subs[event_name][sub_id] = callback
        subs = self._subs[event_name]
        return Subscription(lambda: subs.pop(sub_id, None))

    def emit(self, event_name, args=None):
        cbs = list(self._subs.get(event_name, {}).values())
        return [cb(*(args or [])) for cb in cbs]
```

**复杂度。** `subscribe`、`unsubscribe` 为 `O(1)`，`emit` 为 `O(订阅数)`。

**易错点。**
- 用列表加 `remove(callback)` 取消：同一回调订阅两次时删错那个，顺序乱掉。
- 直接遍历 `values()` 时回调里取消订阅：抛 `RuntimeError`，所以先复制。
- 调用写成 `cb(args)`：回调收到整个列表，`"1,2,3"` 变成 `"[1, 2, 3]"`，要 `cb(*args)`。

**追问。**
- 回调是异步函数？：`emit` 里 `await asyncio.gather(...)`，保持订阅顺序收集结果。
- 线程安全？：复制回调列表时持锁，调用回调时不持锁，避免死锁。

**同模式。** LC 2695 包装数组、LC 2627 函数防抖、LC 2636 Promise 对象池、LC 1472 设计浏览器历史记录
