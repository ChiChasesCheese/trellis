---
slug: logger-rate-limiter
---
## Q
**LC 359 日志速率限制器**｜Easy

设计 `Logger`：`shouldPrintMessage(timestamp, message)` 在同一条消息 10 秒内只让打印一次，打印返回 `true`，否则 `false`。时间戳不递减。

## A
**一句话。** 哈希表存每条消息最早允许再打印的时间，打印成功才把它推到 `timestamp + 10`。

```python
class Logger:
    def __init__(self):
        self.next_ok = {}          # 消息 -> 最早可再打印时间

    def shouldPrintMessage(self, timestamp, message):
        if self.next_ok.get(message, 0) > timestamp:
            return False           # 仍在冷却，不刷新
        self.next_ok[message] = timestamp + 10
        return True
```

**复杂度。** 时间 每次 `O(1)`，空间 `O(M)`。

**易错点。**
- 被拒时也刷新冷却：`(1,"foo")` 后 `(10,"foo")` 被拒，若改成 `20`，`(11,"foo")` 错成 `false`。
- 边界写成 `>=`：`(1,"foo")` 后 `(11,"foo")` 应为 `true`，会被错判。

**追问。**
- 哈希表会无限增长怎么办？：按时间队列存 `(时间, 消息)`，每次先弹出 10 秒前的，同时从集合里删掉。

**同模式。** LC 362 敲击计数器、LC 933 最近的请求次数、LC 146 LRU 缓存
