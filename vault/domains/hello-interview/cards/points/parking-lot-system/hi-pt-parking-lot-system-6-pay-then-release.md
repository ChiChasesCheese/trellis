---
id: hi-pt-parking-lot-system-6-pay-then-release
node: qb.lld.parking-lot-system.points
type: qa
step: 6
---
## Q
**停车场管理系统 · 先缴费后释放**｜必会 · 出自：停车场管理系统 › 深入 3

离场时为什么必须先缴费成功再释放车位？缴费失败怎么办？

## A
**为什么。** 释放车位意味着可再分配；若缴费失败而车位已释放，车辆仍在场内，就出现一个车位对应两辆车。
**失败。** 抛异常，车位保持占用，用户可重试。
