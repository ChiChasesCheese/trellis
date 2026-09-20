---
id: problems-notification-service-quiet-hours-and-urgent
node: problems.components.notification-service
type: qa
step: 4
tags: [grown]
---
## Q
通知服务的静默时段（免打扰）怎么建模？一次性验证码撞上静默时段怎么办？被挡下的营销通知是丢掉还是延后？

## A
静默时段是**用户偏好对象上的一段本地时间窗口**（如 22:00–07:00），判断用注入的时钟加用户时区。窗口可以跨午夜，所以不能只写 `start <= hour < end`：

```python
return start <= hour < end if start < end else (hour >= start or hour < end)
```

**URGENT 必须穿透静默时段**——验证码不会因为用户设了免打扰而发不出去。这条规则写在 `decide()` 里，而不是散在每个调用方的 `if` 里，否则迟早有一个调用方漏掉它。

丢还是延后：默认**抑制**并返回一个明确的原因状态，理由是营销通知过夜就没价值了，而且『一觉醒来收到七条积压推送』比一条没收到更糟。但要主动说出延后的代价几乎为零——重试用的延迟堆已经在那里，把那一句 `return` 换成『算出静默结束时刻、压进延迟堆』即可，队列与渠道一行不改。
