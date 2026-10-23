---
id: hl-bs-s1-followups-b
node: behavioral.stories
type: qa
step: 14
---
## Q
被追问结算管线 S1：两个上游任务不同步怎么办？stream 过期怎么办？瓶颈在哪？
Two upstream tasks out of step? Stream staleness? Bottleneck?

## A
- **Two upstream tasks out of step?** `AFTER A, B` 保证两者各自跑过，但不保证是**同一批**；不匹配的进**错误日志**，下一轮**自愈**。
- **Stream staleness?** 无人消费时会**静默**过期。【待补：实际怎么监控】
- **Bottleneck?** 我会量**每阶段耗时**和**每秒行数**；我没有公开的数字。
