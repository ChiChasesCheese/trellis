---
id: hi-c-sd-multi-step-processes-n07-workflow-orchestration
node: sd.patterns.multi-step-processes.notes
type: qa
step: 7
---
## Q
**多步流程 · 工作流系统与持久化执行**｜摘要 · 必会

工作流编排想要什么？工作流系统和持久化执行引擎各是什么？

## A
- **目标：** 描述一个可靠的、长时间运行的流程（workflow），能扛住服务器崩溃或重启，从中断处继续而不是丢失全部进度，且不用自己搭基础设施。
- **工作流系统与持久化执行引擎：** 既有事件驱动的好处，又自带持久的 saga 协调者。类比 Flink 给流处理提供高层描述方式，它们让你描述系统的高层流程，由引擎负责编排。
- **持久化执行（durable execution）：** 写长时间运行的代码，可以在机器之间迁移并扛住故障和重启；崩溃后在新机器上从上一个成功的步骤继续。多数引擎用代码描述流程：你写一个函数代表工作流，引擎负责编排它。
- **两派区别：** 流程如何描述和管理，代码式（如 Temporal）与声明式（如 Step Functions）。
- **Temporal 的来历：** 2019 年从 Cadence 分叉，Cadence 由其创始人在 Uber 构建（此前做过 AWS 简单工作流服务）；成熟、开源、被许多大公司使用。
