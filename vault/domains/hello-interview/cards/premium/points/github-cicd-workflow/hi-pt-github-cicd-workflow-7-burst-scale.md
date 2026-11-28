---
id: hi-pt-github-cicd-workflow-7-burst-scale
node: qb.sd.github-cicd-workflow.points
type: qa
step: 7
---
## Q
**CI/CD 平台 · 突发扩容**｜追问 · 出自：CI/CD 平台 › 深入 4

CI/CD 平台里，10 倍突发之后积压要 23 分钟才能靠空闲余量清掉。工程上怎么处理？看什么指标？

## A
**措施。** 按最老任务的等待时间扩容执行机（暖池加自动伸缩，冷启动约 30 秒，假设）；定时（cron）触发的任务优先级低于推送；租户并发上限保护其他人。

**指标。** 排队等待时间 p99 是头号指标，其次是各池利用率。
