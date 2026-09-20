---
id: problems-notification-service-priority-lanes-and-quota
node: problems.components.notification-service
type: qa
step: 5
tags: [grown]
---
## Q
通知服务要保证『营销群发不会把一次性验证码（OTP）挤在后面』。落到排队上，『优先级』具体是什么？用一个 `heapq` 够不够？

## A
三种实现：一条 FIFO（没有优先级，直接出局）；一个 `heapq` 存 `(优先级, 序号, 信封)`（代码最短，但低优先级在高优先级持续涌入时会**饿死**，而且『营销积压了多少条』要遍历才算得出来）；**每个优先级一条 `deque`，取时从高到低扫，每条道有连续服务配额**。

选第三种，并把定义说死：*同一优先级内严格先进先出；高优先级优先，但连续 `quota` 条之后必须让低优先级过一条。*

```python
if self._served[priority] >= quota and lower_waiting:
    self._served[priority] = 0   # 让位一次
    continue
```

配额默认无穷大就退化成严格优先级——于是『要不要防饿死』变成一个可配置的取舍而不是隐含行为。额外好处：`depth(priority)` 是 O(1) 的公开属性，积压量可以直接打印。
