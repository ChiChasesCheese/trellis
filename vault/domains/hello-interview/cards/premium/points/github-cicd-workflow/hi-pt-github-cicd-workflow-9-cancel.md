---
id: hi-pt-github-cicd-workflow-9-cancel
node: qb.sd.github-cicd-workflow.points
type: qa
step: 9
---
## Q
**CI/CD 平台 · 取消与自动取消**｜追问 · 出自：CI/CD 平台 › 深入 6

CI/CD 平台里，用户取消一个正在运行的运行，或者同一分支来了新推送要自动取消旧运行。取消如何落到正在执行的任务上？

## A
**做法。** 条件更新运行和任务为 CANCELLING；执行机在心跳响应里收到取消信号，结束进程树；最终态由执行机上报或租约超时落定。

**自动取消。** 同分支新推送取消旧运行，靠并发组（concurrency group）。
