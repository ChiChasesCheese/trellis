---
id: hi-pt-rate-limiter-system-3-fixed-window
node: qb.lld.rate-limiter-system.points
type: qa
step: 3
---
## Q
**限流器（单机类设计） · 固定窗口及其边界突发**｜出自：限流器（单机类设计） › 整体设计

固定窗口算法的状态是什么？它有什么缺陷？

## A
**状态。** 窗口起点和计数；窗口按绝对时间对齐（`now - now % window`），进入新窗口就清零。
**优点。** 状态最小，最便宜。
**缺陷。** 窗口边界允许最多 2N 的突发（上一窗口末尾 N 个加下一窗口开头 N 个）。
