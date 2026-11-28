---
id: hi-c-lld-bookmyshow-b03-py-idempotency
node: lld.problem-breakdowns.bookmyshow.beyond
type: qa
step: 1
---
## Q
**电影票预订 · 网络重试会不会订两次**｜拓展 · 追问

客户端请求超时后自动重发订座请求，服务端其实已经成功。怎么避免订两笔？

## A
**模式。** 幂等键（idempotency key）：同一个请求重复提交，结果只生效一次。

```python
import threading
import uuid


class Sys:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._taken: set[str] = set()
        self._by_key: dict[str, str] = {}      # 幂等键 -> 已生成的确认号

    def book(self, key: str, seats: tuple[str, ...]) -> str:
        with self._lock:                       # 查键、检查座位、登记在同一个临界区
            if key in self._by_key:
                return self._by_key[key]       # 重发：返回同一个确认号，不再占座
            if self._taken & set(seats):
                raise ValueError("taken")
            self._taken |= set(seats)
            rid = uuid.uuid4().hex
            self._by_key[key] = rid
            return rid


s = Sys()
first = s.book("k1", ("A5",))
assert s.book("k1", ("A5",)) == first          # 重试得到同一个结果
try:
    s.book("k2", ("A5",))                      # 另一个请求要同一座位：正常失败
except ValueError:
    pass
```
- **为什么需要：** 网络里"没收到回复"不等于"没成功"；客户端只能重试，服务端必须让重试无害。
- **键由谁生成：** 由客户端在发起一次"意图"时生成（如打开结账页时），同一次意图的所有重试带同一个键。
- **键要保存多久：** 要覆盖客户端可能重试的时间窗口，之后可清理；存储随之增长，所以要有过期。
- **注意：** 检查键和执行必须原子，否则两个并发重试都认为键不存在，各占一次。
- **何时不用：** 内存里的单进程演示不需要；有真实网络和支付时必须有。
