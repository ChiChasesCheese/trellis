---
id: amz-task-scheduler-delayed-vs-periodic
node: amazon.amz-task-scheduler
type: qa
step: 4
tags: [grown]
---
## Q
在任务调度器设计里，周期任务怎么实现？「固定频率」和「固定间隔」有什么区别？

## A
周期任务不需要新结构：执行完后算下一次到期时间，再入堆。固定频率（fixed rate）：`due += period`，每 5 秒一次，任务耗时 3 秒，仍是 0、5、10 秒开始；任务耗时超过周期会连续追赶。固定间隔（fixed delay）：`due = 完成时间 + period`，两次之间总隔 5 秒，不会追赶。默认选固定间隔，因为不会堆积。
```python
def run(self):
    try:
        self.fn()
    finally:
        if self.period and not self.cancelled:
            self.due = self.sched.clock() + self.period
            self.sched.add(self)
```
