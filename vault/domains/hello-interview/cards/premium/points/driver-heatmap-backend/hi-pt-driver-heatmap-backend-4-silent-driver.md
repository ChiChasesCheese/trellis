---
id: hi-pt-driver-heatmap-backend-4-silent-driver
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 4
---
## Q
**司机热力图 · 失联过期**｜必会 · 出自：司机热力图 › 深入 2

司机热力图里，司机关掉应用或进了隧道，不再上报位置，他所在格的计数会一直留着。怎么处理？超时该设多长？

## A
**做法。** 每个司机注册一个 lastSeen + 30 s 的定时器，触发时若没有新点，输出（所在格，−1）并删除状态。

**取舍。** 30 秒约 7 个上报周期；太短，进隧道几秒无信号就闪烁消失，太长，图上有"幽灵"司机。
