---
id: problems-task-scheduler-no-strategy-class-for-two-modes
node: problems.components.task-scheduler
type: qa
step: 4
tags: [grown]
---
## Q
任务调度器的周期任务只有固定速率和固定延迟两种语义。该不该为它们设计一个 `SchedulingPolicy` 接口，各配一个实现类（策略模式）？

## A
**不该。** 两种语义的区别只有一行："下一次到期时间用『这次的到期时间』算，还是用『真正完成的时刻』算"。一个 `Enum`（`RepeatMode`）加两个 `if` 分支表达的信息和三个类完全一样，却不需要打开三个文件才能看懂总共有几种周期语义。

判据和"观察者该不该用抽象基类"是同一条：策略之间的差异只有一行逻辑，不涉及多个方法要一起变，也不需要 `isinstance` 分派，就不需要一族类。真正值得做成"注入一个函数"的扩展点是后续可能加入的 cron 式日历规则——那时候规则的数量会变、每条规则的计算方式也不同，这才是"多个实现、还会继续增长"的信号，对得上策略模式的适用条件。
