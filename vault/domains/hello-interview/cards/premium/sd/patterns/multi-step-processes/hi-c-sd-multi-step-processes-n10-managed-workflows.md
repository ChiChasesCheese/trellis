---
id: hi-c-sd-multi-step-processes-n10-managed-workflows
node: sd.patterns.multi-step-processes.notes
type: qa
step: 10
---
## Q
**多步流程 · 托管的声明式工作流**｜摘要 · 必会

AWS Step Functions 这类托管工作流怎么描述流程？和 Temporal 比有什么取舍？

## A
- **做法：** 用 JSON、YAML 或专门的 DSL 把工作流写成状态机或 DAG（有向无环图），引擎来运行。最常用的是 AWS Step Functions 和 Google Cloud Workflows。
- **本质相同：** 底层同样在编排工作流、调用 Activity、记录进度以便失败后恢复。
- **优点：** 工作流能画成图，界面直观。
- **代价：** 表达力受限，逻辑要塞进状态机模型，常需写不少自定义代码；不过在 AWS 里很少手写 JSON，AWS CDK 能用真实代码生成同样的状态机，所以"JSON 难看"不是要害，要害是逻辑必须适配状态机模型。
- **2026 亮点：** 托管的持久化执行不止声明式状态机：Cloudflare Workflows（已 GA）用代码写步骤，每个 step 的返回值自动落盘，失败只重试该 step，可配重试次数、延迟、退避和超时，不用自己维护状态机。边界：step 里的外部调用仍要自己做幂等，状态只保留有限期限（免费版 3 天；付费版默认 7 天，最长可配到 30 天），不是长期审计存储。
- **选择：** 声明式还是代码式主要看团队偏好，面试里很少成为争论点，两者都能满足同样的目的。
