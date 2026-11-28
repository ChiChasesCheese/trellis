---
id: hi-pt-github-cicd-workflow-2-event-idempotent
node: qb.sd.github-cicd-workflow.points
type: qa
step: 2
---
## Q
**CI/CD 平台 · 事件到运行的幂等创建**｜必会 · 出自：CI/CD 平台 › 深入 1

CI/CD 平台里，推送事件经 Kafka（至少一次投递）到达触发服务，触发服务要为每个匹配的工作流创建运行。怎样保证一次推送不会产生两份运行？读工作流文件应该按分支最新还是按提交？

## A
**要点。** Run 带唯一键 (repoId, sha, workflow, eventId)，重复消费插入失败即跳过；Run 和全部 Job 在一个事务里创建。

**为什么按提交。** 处理时分支可能已前进，读最新会让这次推送执行别人的代码，所以按 sha 读文件。

**易错。** 语法错误的工作流要创建一个失败的运行并展示错误，不能静默丢弃。
