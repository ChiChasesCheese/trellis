---
id: hi-c-sd-temporal-n06-what-is
node: sd.deep-dives.temporal.notes
type: qa
step: 6
---
## Q
**Temporal · 一句话讲清它的编程模型**｜摘要 · 必会

Temporal 是什么？Workflow、Activity、历史、定时器、Signal 如何一起构成它的模型？

## A
- **定义：** 围绕持久化执行构建的工作流编排系统。
- **Workflow：** 可重放的编排逻辑。**Activity：** 与外界交互的操作。
- **执行历史（Event History）：** Temporal 把工作的结果记录进持久历史，这样出故障后可以重放 Workflow 并重建状态。
- **必然的约束：** 因为要重放，Workflow 代码必须确定性。
- **能力：** 计时器让 Workflow 不占 worker 等待；Signal 让外部系统向在运行的 Workflow 送信息。
- **结果：** 订单流程几乎能写成最初想要的那种顺序代码：扣款、占库存、发货、等送达、发邮件。
