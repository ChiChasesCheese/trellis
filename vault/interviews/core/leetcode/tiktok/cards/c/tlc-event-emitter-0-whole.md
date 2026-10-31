---
id: tlc-event-emitter-0-whole
node: c.event-emitter
type: qa
---
## Q
**LC 2694 事件发射器**｜Medium · LC TikTok 全时段热度 26/100

原题是 JavaScript 题；这里用 Python 解同一个任务，回调是 Python 可调用对象，`emit` 的参数数组用 `*args` 展开，JS 的 `undefined` 对应 `None`。设计一个 `EventEmitter` 类，行为与 Node.js 或 DOM 的 Event Target 相似但有差异，允许订阅和触发事件。两个方法：`subscribe(event_name, callback)`：一个事件可以有多个监听器，触发时按**订阅顺序**依次调用每个回调；返回一个带有 `unsubscribe()` 方法的对象，调用后该回调从订阅列表中移除，`unsubscribe()` 返回 `None`。可以假设传给 `subscribe` 的回调互不引用同一个。`emit(event_name, args=None)`：把可选的参数数组展开传给每个回调，按订阅顺序返回所有回调结果组成的列表；没有订阅者则返回空列表。提示：操作数不超过 10，所有测试用例有效（不会取消不存在的订阅）。例：
```
emitter = EventEmitter()
emitter.emit("firstEvent")                                   # [] 还没有订阅者
emitter.subscribe("firstEvent", lambda: 5)
emitter.subscribe("firstEvent", lambda: 6)
emitter.emit("firstEvent")                                   # [5, 6]

sub = emitter.subscribe("second", lambda *args: ",".join(map(str, args)))
emitter.emit("second", [1, 2, 3])                            # ["1,2,3"]
sub.unsubscribe()                                            # None
emitter.emit("second", [4, 5, 6])                            # []
```

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 `事件名 -> {订阅编号: 回调}` 的两层字典：Python 的 `dict` 保持插入顺序，天然满足「按订阅顺序调用」，取消订阅就是按编号删一项，`subscribe` / `unsubscribe` 都是 `O(1)`，`emit` 是 `O(订阅数)`。

**识别。** 「发布 / 订阅」（观察者模式）：关键是订阅关系的存储和取消。取消要能精确定位到**这一次订阅**，所以用订阅编号而不是回调本身做键（同一个函数可以订阅两次）。

**推导。** 用列表存回调，`unsubscribe` 要 `list.remove(callback)` 线性查找，且同一个函数订阅两次时会删错一个。给每次订阅分配自增编号，返回的对象闭包记住 `(事件名, 编号)`，取消时 `pop` 编号。`emit` 前先复制一份回调列表，回调内部若取消订阅也不会在遍历时修改字典。

```python
from collections import defaultdict
from collections.abc import Callable
from typing import Any


class Subscription:
    def __init__(self, release: Callable[[], None]) -> None:
        self._release = release

    def unsubscribe(self) -> None:
        self._release()                          # 取消这一次订阅；返回 None


class EventEmitter:
    def __init__(self) -> None:
        # 事件名 -> {订阅编号: 回调}；dict 保持插入顺序，等于订阅顺序
        self._subs: defaultdict[str, dict[int, Callable]] = defaultdict(dict)
        self._next_id = 0

    def subscribe(self, event_name: str, callback: Callable) -> Subscription:
        sub_id = self._next_id                   # 编号唯一：同一个函数订阅两次也能分别取消
        self._next_id += 1
        self._subs[event_name][sub_id] = callback
        return Subscription(lambda: self._subs[event_name].pop(sub_id, None))

    def emit(self, event_name: str, args: list[Any] | None = None) -> list[Any]:
        callbacks = list(self._subs.get(event_name, {}).values())   # 先复制：回调里取消订阅不影响本轮遍历
        return [cb(*(args or [])) for cb in callbacks]              # 展开参数，按订阅顺序收集结果
```

运行：`emit("firstEvent")` → `[]`；订阅两个回调后 → `[5, 6]`；`emit("second", [1, 2, 3])` → `["1,2,3"]`，`sub.unsubscribe()` → `None`，再 `emit("second", [4, 5, 6])` → `[]`；订阅 `lambda x: x + 1` 与 `lambda x: x + 2`，取消第一个后 `emit("e", [5])` → `[7]`；同一个函数订阅两次、`emit` 得到两个结果。

**复杂度。** `subscribe`、`unsubscribe` 均摊 `O(1)`；`emit` 为 `O(该事件的订阅数 + 回调本身的耗时)`；空间 `O(订阅总数)`。

**拓展优化。**
- `once`（只触发一次）：订阅时包一层，回调执行后自动 `unsubscribe`。

```python
def subscribe_once(emitter: EventEmitter, event_name: str, callback: Callable) -> Subscription:
    holder: list[Subscription] = []              # 用列表在闭包里延迟拿到 Subscription

    def wrapper(*args: Any) -> Any:
        holder[0].unsubscribe()                  # 先取消，再执行，保证只触发一次
        return callback(*args)

    holder.append(emitter.subscribe(event_name, wrapper))
    return holder[0]
```

**易错点。**
- 用列表加 `list.remove(callback)` 取消订阅：回调序列 `[f, g, f]` 取消第二个 `f` 时，`remove` 删的是第一个，剩下 `[g, f]`，结果顺序与期望的 `[f, g]` 不一致。
- 直接遍历 `dict.values()` 同时回调里取消订阅：抛 `RuntimeError: dictionary changed size during iteration`，所以先复制。
- 把参数数组整个传进去 `cb(args)` 而不是 `cb(*args)`：回调 `lambda *args: ",".join(map(str, args))` 得到 `"[1, 2, 3]"`，而不是 `"1,2,3"`。

**追问。**
- 回调是异步函数（`async`）：`emit` 要 `await` 收集结果，可用 `asyncio.gather` 保持订阅顺序。
- 线程安全：订阅表加锁，`emit` 复制回调列表时持锁、调用回调时不持锁，避免死锁。

**同模式。** LC 2695 包装数组、LC 2627 函数防抖、LC 2636 Promise 对象池、LC 146 LRU 缓存、LC 1472 设计浏览器历史记录。
