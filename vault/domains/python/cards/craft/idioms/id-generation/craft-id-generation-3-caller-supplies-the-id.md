---
id: craft-id-generation-3-caller-supplies-the-id
node: craft.idioms.id-generation
type: qa
step: 3
---
## Q
**ID 生成 · 为什么幂等的请求 ID 要由调用方给**｜写法

通知服务收到「给用户发一条验证码」的请求，网络超时后调用方会重发。如果 `notification_id` 由服务端用计数器或 UUID 生成，重发会怎样？应该由谁决定这个 ID？

## A
**要点。** 能判断「这两次调用是不是同一件事」的只有调用方。服务端自己发的 ID 每次都是新的，重发就永远是新消息，幂等（重复提交效果等于一次）无从谈起。所以请求 ID 由调用方生成并随请求带来；服务端只负责用它去重。服务端生成的 ID 用于它自己创建的实体（对局、订单），那是另一类 ID。

```python
import itertools
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Notification:
    notification_id: str          # 调用方给：只有它知道「是不是同一件事」
    user_id: str

class Service:
    def __init__(self) -> None:
        self.sent: dict[str, Notification] = {}
        self._ids = itertools.count(1)
    def submit(self, n: Notification) -> str:
        if n.notification_id in self.sent:         # 重发：认得出
            return "duplicate"
        self.sent[n.notification_id] = n
        return "sent"
    def submit_server_id(self, user_id: str) -> str:
        nid = f"n{next(self._ids)}"                # 服务自己编号：每次都是新的
        self.sent[nid] = Notification(nid, user_id)
        return "sent"

s = Service()
n = Notification("otp-482913", "u1")
print(s.submit(n), s.submit(n))
s2 = Service()
print(s2.submit_server_id("u1"), s2.submit_server_id("u1"), len(s2.sent))
```

实际输出：

```
sent duplicate
sent sent 2
```

**为什么。** 第一行重发被识别，第二行同一个用户发了两条。两种 ID 的分工：调用方给的是「这件事」的身份，服务端发的是「这个对象」的身份。

**易错。** 调用方给 ID 就要约定怎么生成：随机 UUID 每次重试必须复用同一个，而不是每次重试重新生成；业务上有天然键（订单号 + 事件类型）时优先用它。
