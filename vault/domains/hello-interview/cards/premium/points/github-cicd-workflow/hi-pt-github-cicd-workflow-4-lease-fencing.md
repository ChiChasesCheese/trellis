---
id: hi-pt-github-cicd-workflow-4-lease-fencing
node: qb.sd.github-cicd-workflow.points
type: qa
step: 4
---
## Q
**CI/CD 平台 · 租约与围栏**｜必会 · 出自：CI/CD 平台 › 深入 2

CI/CD 平台里，执行机领了任务后无声消失，任务会卡在运行中。怎样发现并恢复？如果旧执行机之后又冒出来上报结果，怎么处理？默认该重排还是判失败？

## A
**租约。** 领任务时 leaseUntil = now + 60 s，每 20 s 心跳续租；过期则任务重置为 READY，attempt + 1。

**围栏。** 旧执行机上报带旧 attempt，被拒绝。

**默认。** 步骤可能有副作用（如部署），默认失联即失败，用户可配置重试。
