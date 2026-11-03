---
id: hi-pt-online-chess-platform-8-clock-server
node: qb.sd.online-chess-platform.points
type: qa
step: 7
---
## Q
**在线国际象棋平台 · 服务端时钟与超时判负**｜必会 · 出自：在线国际象棋平台 › 深入 2

计时为什么不能信客户端，也不能完全按服务端收到消息的时间算？服务端怎么记账，超时怎么检测？

## A
**记账。** 服务端只存这一步开始的服务端时间 `turnStartedAt` 和双方剩余毫秒；收到走子时 `spent = now − turnStartedAt`，可补偿一个上限（如 min(网络延迟估计, 200ms)），`remaining = remaining − spent + increment`。不需要每秒扣减。
**超时。** 所有者为当前轮到的一方设延迟任务，到期先重读时钟再判；每局事件串行，竞态不会产生双重结果。
**展示。** `clock_sync` 周期校正，不是权威。
