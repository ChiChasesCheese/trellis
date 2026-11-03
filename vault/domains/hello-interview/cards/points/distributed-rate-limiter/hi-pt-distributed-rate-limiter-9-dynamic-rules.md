---
id: hi-pt-distributed-rate-limiter-9-dynamic-rules
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 10
---
## Q
**分布式限流器 · 动态规则下发**｜加分 · 出自：分布式限流器 › 深入 6

分布式限流器的规则要能动态修改、不用发版。轮询和推送两种下发方式各有什么问题，怎么选？

## A
**轮询。** 网关每 30 秒左右拉一次并缓存，简单可靠，但紧急调低限额要等一个周期。
**推送。** ZooKeeper、etcd 的 watch 或 Pub/Sub，秒级到达；要处理断连和部分网关漏收，所以需轮询兜底。
**选择。** 默认轮询加缓存；安全应急要求高再叠加推送。
