---
id: hi-pt-github-cicd-workflow-6-log-streaming
node: qb.sd.github-cicd-workflow.points
type: qa
step: 6
---
## Q
**CI/CD 平台 · 日志分块与实时观看**｜必会 · 出自：CI/CD 平台 › 深入 3

CI/CD 平台有 36,000 个并发任务，用户要近实时地看日志，还要能断线重连。日志通道怎么设计？

## A
**上传。** 执行机每 2 秒把缓冲的行打成块 (jobId, seq, bytes)；36,000 ÷ 2 = 18,000 块/秒，所以先进 Kafka（按 jobId 分区），批量落成对象存储的分段文件，同时推给发布订阅。

**观看。** SSE 带 from=seq 重连；先读已落盘的段，再接实时尾部，用 seq 去重衔接。

**脱敏。** 在执行机端做。
