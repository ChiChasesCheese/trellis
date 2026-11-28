---
id: hi-c-sd-realtime-updates-b02-sse-wire
node: sd.patterns.realtime-updates.beyond
type: qa
step: 3
---
## Q
**实时更新 · SSE 的线上格式与断线补发**｜拓展 · 加分

SSE 在线路上长什么样？服务端怎么用 `Last-Event-ID` 补发，缺口太大时怎么办？

## A
**模式。** 带序号的事件日志加有界缓冲：序号让重连幂等，缓冲决定能补多久。

```python
from collections import deque
from typing import Iterator


class EventLog:
    """服务端：带递增 id 的事件，保留最近 N 条，供断线重连的客户端补发。"""

    def __init__(self, keep: int = 1000) -> None:
        self._buf: deque[tuple[int, str]] = deque(maxlen=keep)   # 环形缓冲：旧的自动丢弃
        self._next = 1

    def publish(self, data: str) -> None:
        self._buf.append((self._next, data))
        self._next += 1

    def stream(self, last_event_id: int | None) -> Iterator[str]:
        """一次 SSE 连接要写出的帧；last_event_id 来自请求头 Last-Event-ID。"""
        oldest = self._buf[0][0] if self._buf else self._next
        if last_event_id is not None and last_event_id + 1 < oldest:
            yield "event: resync\ndata: gap\n\n"                  # 缺口已超出缓冲：让客户端整体重新拉取
        for eid, data in self._buf:
            if last_event_id is None or eid > last_event_id:
                yield f"id: {eid}\ndata: {data}\n\n"              # 空行结束一帧；id 由浏览器自动记住
        yield ": ping\n\n"                                        # 以冒号开头是注释帧，常用作心跳，防止中间设备断开空闲连接


log = EventLog(keep=3)
for m in "abcde":
    log.publish(m)                                                # 缓冲只剩 id 3,4,5
print("".join(log.stream(4)))                                     # 客户端收到 4 之后掉线：补发 5
print("".join(log.stream(1)))                                     # 掉线太久：先通知重新同步
```
- **帧格式：** 每个事件是若干 `字段: 值` 行，以空行结束；`id` 被浏览器记住并在重连时放进 `Last-Event-ID` 请求头；`data` 是内容；以冒号开头的行是注释，常拿来发心跳，让中间设备不因为空闲而断开。
- **有界缓冲的取舍：** 缓冲越大能补的越久，内存越大；缺口超出缓冲就发"重新同步"事件，让客户端整体拉取一次。
- **多机部署：** 缓冲要放到共享存储（Redis Streams、Kafka），否则重连到另一台机器就补不了。
- **代理缓冲：** 设置 `Cache-Control: no-cache`，必要时在代理上关闭响应缓冲，否则流会被卡住。
- **何时不用：** 事件极稀少、重连成本低的场景，直接让客户端重拉全量状态更简单。
