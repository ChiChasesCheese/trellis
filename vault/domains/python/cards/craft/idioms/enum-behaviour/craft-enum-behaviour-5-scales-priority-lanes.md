---
id: craft-enum-behaviour-5-scales-priority-lanes
node: craft.idioms.enum-behaviour
type: qa
step: 5
---
## Q
**Enum 的行为 · 从一个等级枚举到分级队列和 SLO**｜写法

通知服务里营销和验证码共用一个发送队列。验证码洪峰时营销永远发不出去，营销积压时验证码又被拖慢。等级枚举怎样同时承担路由、排队和限流的依据？放到多机的消息系统里，同样的思路要换成什么？

## A
**要点。** 一个有序的等级枚举是一把共用的刻度：偏好用 `>=` 过滤，队列按它分道（lane），监控按它分别统计积压。关键的取舍是严格优先级会饿死低等级，所以每一道给一个配额，高等级连续取到配额后必须让位一次。

```python
from collections import deque
from enum import IntEnum

class Priority(IntEnum):
    MARKETING = 10
    URGENT = 30

class Lanes:
    def __init__(self, quota: dict[Priority, int]) -> None:
        self.lanes = {p: deque() for p in Priority}          # 新增等级自动多一条道
        self.quota, self.served = quota, {p: 0 for p in Priority}
    def put(self, p: Priority, item: str) -> None:
        self.lanes[p].append(item)
    def get(self) -> str | None:
        order = sorted(Priority, reverse=True)               # 数值大的先
        for i, p in enumerate(order):
            if not self.lanes[p]:
                continue
            lower_waiting = any(self.lanes[q] for q in order[i + 1:])
            if self.served[p] >= self.quota.get(p, 10**9) and lower_waiting:
                self.served[p] = 0                           # 让位一次
                continue
            self.served[p] += 1
            return self.lanes[p].popleft()
        return None

q = Lanes({Priority.URGENT: 2})
for i in range(5): q.put(Priority.URGENT, f"otp{i}")
for i in range(2): q.put(Priority.MARKETING, f"sale{i}")
print([q.get() for _ in range(7)])
```

实际输出：

```
['otp0', 'otp1', 'sale0', 'otp2', 'otp3', 'sale1', 'otp4']
```

**为什么。** 每取两条紧急就让一条营销，营销有了保底吞吐。`for p in Priority` 让「新增一个等级」自动多出一道队列和一份统计。

**多机。** 单进程的锁和 deque 换成分区主题或每个等级一个独立队列：等级写在消息里，每个队列单独设消费者数量和告警阈值，延迟目标（SLO）按等级分别定义，营销可以慢，验证码不行。等级仍然是同一个数值刻度，只是「配额」变成了消费者数量的分配。
