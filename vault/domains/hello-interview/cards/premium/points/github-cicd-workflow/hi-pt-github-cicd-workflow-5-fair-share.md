---
id: hi-pt-github-cicd-workflow-5-fair-share
node: qb.sd.github-cicd-workflow.points
type: qa
step: 5
---
## Q
**CI/CD 平台 · 租户公平**｜必会 · 出自：CI/CD 平台 › 深入 2

CI/CD 平台里，一个租户一次推送触发了 10 万个任务。怎样做到不饿死其他租户？

## A
**做法。** 每个租户一个子队列，用赤字轮转（deficit round robin）出队，再加每租户并发上限（假设免费 20、企业 500）。

**效果。** 大租户只占自己的份额，别的租户的任务照常出队。

**对应。** 单机的令牌桶限速，在这里变成并发上限加公平出队。
