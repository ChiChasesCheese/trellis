---
id: hi-pt-tt-idempotent-transfer-6-crash-replay
node: tt.lld.tt-idempotent-transfer.points
type: qa
step: 6
---
## Q
**幂等转账服务 · 崩溃恢复与重放**｜追问 · 出自：幂等转账服务 › 深入 4

占键之后、执行完成之前进程崩溃，键永远停在「进行中」，怎么办？

## A
**做法。** 键记录带开始时间；恢复任务扫描超过阈值的进行中记录，用同一个键重放第二步。
**为什么安全。** 账本分录 ID 由键派生（如 `tr:{client}:{key}`），重放要么发现已记账直接补写结果，要么记账，不会记两次。
