---
id: tlc-tops-logger-rate-limiter-0-whole
node: arrays-hashing.logger-rate-limiter
type: qa
---
## Q
**LC 359 日志速率限制器（Logger Rate Limiter）**｜Easy · 全公司热度第 88 名

设计 `Logger` 类，接收一串带时间戳（秒）的消息。每条**不同**的消息最多每 10 秒打印一次：若某条消息在时间戳 `t` 被打印，则同一条消息在 `[t, t + 10)` 内都不能再打印。实现 `Logger()` 初始化对象；`bool shouldPrintMessage(int timestamp, string message)`：消息此刻应当打印则返回 `true`，否则返回 `false`。所有调用的 `timestamp` 按非递减顺序给出。`0 <= timestamp <= 10^9`，`1 <= message.length <= 30`，`shouldPrintMessage` 至多调用 `10^4` 次。例：依次调用 `(1, "foo")`、`(2, "bar")`、`(3, "foo")`、`(8, "bar")`、`(10, "foo")`、`(11, "foo")`，返回 `true, true, false, false, false, true`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 哈希表（hash map）记录状态：每条消息「下一次允许打印的时间」。

**一句话。** 用字典存每条消息最早允许再次打印的时间戳；来了新请求，时间戳没到就拒绝，到了就打印并把允许时间推到 `timestamp + 10`。

**识别。** 「按 key 限频 / 去重」是每个 key 一份小状态的哈希表问题；时间戳非递减，所以只需要记每个 key 最近一次打印的时间，不用保存历史。每次调用 `O(1)`。

**推导。** 把所有打印过的 `(时间戳, 消息)` 存成列表、每次倒着扫：每次调用 `O(n)`，历史越长越慢。其实只有每条消息「最近一次打印」有用，一个字典就够。

```python
class Logger:
    def __init__(self) -> None:
        self.next_ok: dict[str, int] = {}          # 消息 -> 最早允许再次打印的时间戳

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if self.next_ok.get(message, 0) > timestamp:   # 仍在 10 秒冷却期内：不打印，也不刷新冷却
            return False
        self.next_ok[message] = timestamp + 10         # 打印，并从现在起重新冷却 10 秒
        return True
```

运行：示例六次调用依次得到 `[True, True, False, False, False, True]`；`(5, "a")`、`(15, "a")` 得到 `True, True`（`15 = 5 + 10`，刚好允许）。

**复杂度。** 每次调用时间 `O(1)`；空间 `O(M)`，`M` 是不同消息的个数。

**拓展优化。**
- 内存有上限（消息流无限长）：只保留最近 10 秒内打印过的消息。用队列按时间顺序存 `(时间戳, 消息)`，每次调用先把过期的弹出，再用集合判断；每条消息只入队出队一次，仍是均摊 `O(1)`。

```python
from collections import deque


class LoggerBounded:
    def __init__(self) -> None:
        self.window: deque[tuple[int, str]] = deque()   # 按时间戳递增排列的 (时间戳, 消息)，只存最近 10 秒内打印过的
        self.live: set[str] = set()                     # 窗口里出现的消息

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        while self.window and self.window[0][0] <= timestamp - 10:   # 冷却已结束的消息出窗口
            self.live.discard(self.window.popleft()[1])
        if message in self.live:
            return False
        self.live.add(message)
        self.window.append((timestamp, message))
        return True
```

**易错点。**
- 被拒绝时也刷新冷却：`(1, "foo")` 打印后 `(10, "foo")` 被拒，若此时把允许时间改成 `20`，`(11, "foo")` 会错成 `false`（正确 `true`）。只有打印成功才更新。
- 边界写成 `>=`：`(1, "foo")` 后 `(11, "foo")` 应该是 `true`；条件 `next_ok >= timestamp` 会把它错判成 `false`。

**同模式。** LC 362 敲击计数器、LC 933 最近的请求次数、LC 1348 推文计数、LC 146 LRU 缓存。
