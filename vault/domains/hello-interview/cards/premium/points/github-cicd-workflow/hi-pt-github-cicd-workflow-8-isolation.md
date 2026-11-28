---
id: hi-pt-github-cicd-workflow-8-isolation
node: qb.sd.github-cicd-workflow.points
type: qa
step: 8
---
## Q
**CI/CD 平台 · 隔离与密钥**｜追问 · 出自：CI/CD 平台 › 深入 5

CI/CD 平台要执行用户仓库里的任意脚本，其中有不可信代码。隔离和密钥该怎么处理？

## A
**隔离。** 每个任务一个新的 microVM 或带用户态内核的容器，跑完销毁，不复用。

**密钥。** 控制平面按任务签发短期令牌，运行时才注入；来自 fork 的拉取请求不给密钥。

**其他。** 出站网络按策略限制；用配额和异常检测对付挖矿滥用。
