---
id: hi-pt-scheduler-system-design-2-trigger-strategy
node: qb.lld.scheduler-system-design.points
type: qa
step: 2
---
## Q
**任务调度器（定时、周期、带优先级） · Trigger 策略**｜出自：任务调度器（定时、周期、带优先级） › 核心实体与接口

调度器怎样让触发规则可扩展，后续加 cron 不改调度器？Trigger 接口需要哪两个方法？

## A
**接口。** `Trigger.first(now)` 返回第一次触发时间，`after(fired_at, now)` 返回下一次时间或 `None`。
**实现。** `OneShot`、`FixedRate`；扩展点 `CronTrigger`、`FixedDelay`。
**模式。** 策略（Trigger）、命令（Job.fn）、生产者-消费者（计时线程生产，工作线程消费）。
```python
def after(self, fired_at, now) -> float | None: ...
```
