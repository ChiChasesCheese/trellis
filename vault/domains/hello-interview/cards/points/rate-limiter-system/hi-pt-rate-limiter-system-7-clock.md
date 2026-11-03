---
id: hi-pt-rate-limiter-system-7-clock
node: qb.lld.rate-limiter-system.points
type: qa
step: 8
---
## Q
**限流器（单机类设计） · 单调时钟与时钟注入**｜必会 · 出自：限流器（单机类设计） › 深入 3

限流器该用 `time.time` 还是 `time.monotonic`？测试怎么避免 sleep？

## A
**要点。** 用单调时钟：系统时间被调整（NTP 校时、手工修改）时墙钟会回退，导致令牌为负或窗口错乱。
**测试。** 时钟作为构造参数注入，测试里用可手动拨动的假时钟，不 `sleep`，快且确定。
