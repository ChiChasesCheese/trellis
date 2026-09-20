---
id: problems-task-scheduler-fixed-rate-vs-fixed-delay
node: problems.components.task-scheduler
type: qa
step: 2
tags: [grown]
---
## Q
在任务调度器（task scheduler）设计里，周期任务有固定速率（fixed rate）和固定延迟（fixed delay）两种语义。如果某一次执行超过了一个周期才跑完，两者接下来的行为分别是什么？

## A
**固定速率**：下一次到期 = **这一次的到期时间** + 周期，与这次实际跑了多久无关。一旦落后，它会在恢复正常之后**连续追赶**——一次批量检查里可能连续补跑好几次，直到追上当前时间为止。长期平均频率精确（比如一小时正好跑 60 次），但会扎堆。

**固定延迟**：下一次到期 = **这一次真正跑完的时刻** + 周期。任意两次执行之间**永远隔着至少一个完整周期**，不会追赶、不会扎堆，但长期平均频率会随每次执行耗时的抖动而漂移。

代码上的分水岭在"下一次到期在哪一步被算出来"：

```python
# 取出（还没执行）的那一刻：只有固定速率在这里重排
if meta.mode is FIXED_RATE:
    push(entry.id, entry.due + meta.period)

# 真正执行完之后：只有固定延迟在这里重排
if meta.mode is FIXED_DELAY:
    push(task_id, finished_at + meta.period)
```
