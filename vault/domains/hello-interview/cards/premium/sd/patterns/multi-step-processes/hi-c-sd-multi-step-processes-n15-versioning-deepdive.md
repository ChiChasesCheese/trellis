---
id: hi-c-sd-multi-step-processes-n15-versioning-deepdive
node: sd.patterns.multi-step-processes.notes
type: qa
step: 16
---
## Q
**多步流程 · 追问：怎么更新正在运行的工作流**｜摘要 · 追问

一万个贷款审批工作流正在运行，要加一个合规检查，如何升级而不破坏已启动的执行？

## A
- **难点：** 工作流可能跑几天几周，不能直接部署新代码：旧流程 5 步，新代码 6 步，恢复时对不上。
- **版本化：** 新版本代码单独部署，旧工作流继续跑旧代码，新工作流跑新代码。最简单，但如果变更必须立刻生效就不行，因为不能等旧流程跑完。
- **迁移：** 原地更新定义，让运行中的执行也能采用。
- **声明式系统：** 迁移较少但控制也少。Step Functions 的运行中执行固定在启动时的定义上，更新只影响新执行；运行中需要新步骤就停掉重启，或提前把分支建模进去。
- **持久化执行引擎：** 常用补丁（patch）：`patched("id")` 对新执行（以及首次到达该点的在途执行）返回 true 走新逻辑；历史已走过此点的旧执行返回 false 保持旧行为，一次发布同时服务新旧，且不破坏重放。
- **2026 亮点：** 除了 patch，Temporal 的 Worker Versioning 已 GA：每个 Workflow 类型选 Pinned（在启动时的版本上跑完，不用 patch）或 Auto-Upgrade（切到新版本，仍要 patch 保证重放安全）；长流程可以在 Continue-as-New 的边界升级（这一能力还在 Public Preview）。代价是并行运行多个 Deployment Version，旧版本 worker 要等 Pinned 流程排空才能下线。
