---
id: hi-pt-tt-idempotent-transfer-2-in-progress
node: tt.lld.tt-idempotent-transfer.points
type: qa
step: 2
---
## Q
**幂等转账服务 · 进行中占位与合并重复请求**｜必会 · 出自：幂等转账服务 › 深入 1

只在完成后记录键为什么不行？占位记录加事件怎么解决？

## A
**窗口。** 只在完成后记键，两个相同请求同时到达都查不到记录，都执行，转账两次。
**做法。** 第一个请求持有占位记录，其他请求在记录的 `done` 事件上等待，拿到结果就原样返回；等待带超时，超时返回 `StillRunning`（409）。
**对比。** 全局锁会让所有转账串行。
