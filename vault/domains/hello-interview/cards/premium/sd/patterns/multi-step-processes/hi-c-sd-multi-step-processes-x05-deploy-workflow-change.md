---
id: hi-c-sd-multi-step-processes-x05-deploy-workflow-change
node: sd.patterns.multi-step-processes.exam
type: qa
step: 5
---
## Q
**多步流程 · 发布新版本时的在途工作流**｜考点 · 必会

你要给运行数周的审批工作流加一步合规检查，在途执行有一万个。怎么上线？

## A
- **先分两类需求：** 新检查是否必须立刻对在途流程生效。
- **不必立刻生效：** 版本化，新版本代码单独部署，新启动的走新版，旧的跑完旧版。最简单。
- **必须立刻生效：** 迁移。Temporal 一类引擎用 `patched()` 在代码里分支，历史已越过该点的旧执行走旧逻辑，新的和首次到达的走新逻辑，这样重放不会被破坏。
- **Step Functions：** 在途执行固定在启动时的定义上，要停掉重启，或提前把分支建模进去。
- **2026 亮点：** Temporal 的 Worker Versioning 已 GA，可以大幅减少对满代码的 `patched()` 的依赖：给每个 Workflow 类型标版本策略，Pinned 的流程在启动时的 Deployment Version 上跑完，Auto-Upgrade 的流程切到新版本（仍要靠 patch 保证重放安全）；在下次发布前就能跑完的短流程标 Pinned；跨多次发布又不用 Continue-as-New 的长流程才需要 Auto-Upgrade 加 patch。代价是要同时跑多个版本的 worker（不能滚动发布），旧版本要等 Pinned 流程排空才能下线。
- **要点：** 绝不能直接换掉代码，否则旧历史重放会对不上。
