---
id: amz-emergency-pubsub-followup-topic-and-severity-filter
node: amazon.amz-emergency-pubsub
type: qa
step: 6
tags: [grown]
---
## Q
在应急发布订阅里，面试官追问「消防队只要火灾事件，指挥中心只要 CRITICAL 事件」，要改哪里？

## A
只在 `Subscription` 里加一个判断，总线的路由循环一行不改：
```python
def accepts(self, event):
    return (event.severity >= self._min_severity
            and (self._topics is None or event.topic in self._topics))
```
`Severity` 是 `IntEnum`，所以「至少 WARNING」就是一个 `>=` 比较。`topics=None` 表示全部订阅。事件类型不是固定的枚举而是字符串，新增一种事件不需要改任何类。
