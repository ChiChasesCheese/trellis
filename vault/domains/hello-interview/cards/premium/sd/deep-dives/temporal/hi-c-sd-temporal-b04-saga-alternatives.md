---
id: hi-c-sd-temporal-b04-saga-alternatives
node: sd.deep-dives.temporal.beyond
type: qa
step: 4
---
## Q
**Temporal · 补偿（Saga）与同类产品**｜拓展 · 加分

多步骤流程中途失败，已完成的步骤要撤销（退款、释放库存）。在 Temporal 里怎么写？它和 Step Functions 等产品有何区别？

## A
- **补偿写成代码：** 每完成一步，把对应的补偿动作（退款、释放库存）压入一个列表；失败时在 `catch` 里逆序执行这些补偿 Activity。因为 Workflow 是持久的，补偿本身也会在崩溃后继续执行，补偿 Activity 要幂等。这就是 Saga 模式。
- **与 Step Functions：** Step Functions 用状态机定义（声明式 JSON）来描述流程，托管、与 AWS 集成好；Temporal 用通用编程语言写 Workflow，循环、条件、重试都是普通代码，更灵活，需要自己运维或用云服务。
- **谱系：** Temporal 由 Uber 的 Cadence 项目分叉而来；同类的持久化执行产品还有 Restate、Inngest、DBOS 等，核心思想相同：持久记录加重放。
- **选择依据：** 流程复杂度、团队对云厂商的依赖、愿意承担的运维成本。
