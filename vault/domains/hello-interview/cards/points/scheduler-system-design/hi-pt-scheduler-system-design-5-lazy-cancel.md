---
id: hi-pt-scheduler-system-design-5-lazy-cancel
node: qb.lld.scheduler-system-design.points
type: qa
step: 5
---
## Q
**任务调度器（定时、周期、带优先级） · 惰性取消**｜出自：任务调度器（定时、周期、带优先级） › 整体设计

取消任务时要不要从堆里删除？有什么副作用，怎么处理？

## A
**做法。** 只打 `cancelled` 标记，不从堆里删除；旧记录弹出时发现已取消就丢弃。
**副作用。** 取消很多时堆里积累垃圾；已取消条目超过堆大小一半时重建堆。
