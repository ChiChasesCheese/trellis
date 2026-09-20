---
id: problems-notification-service-idempotency-key-and-scope
node: problems.components.notification-service
type: qa
step: 8
tags: [grown]
---
## Q
通知服务的幂等键由谁提供？作用粒度应该是『一次请求』还是『一次请求 × 一个渠道』？

## A
**由调用方提供**。服务自己 `uuid4()` 的话，调用方超时重发永远是一条新消息，幂等形同虚设——只有调用方知道『这两次调用是不是同一件事』（订单号、事件 id）。所以请求对象里的 `notification_id` 是必填参数。

粒度是 **`(notification_id, channel)`**。一次请求扇出到邮件和短信：邮件成了、短信超时要重试，用请求级的键会让短信的重试撞上邮件留下的记录。把它写成信封上的一个属性：

```python
@property
def idempotency_key(self) -> str:
    return f"{self.notification_id}|{self.channel}"
```

去重表还必须有 TTL 和 `purge()`：一个只写不删的去重表是一个保证会 OOM 的组件。
