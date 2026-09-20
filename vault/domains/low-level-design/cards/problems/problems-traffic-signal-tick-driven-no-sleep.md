---
id: problems-traffic-signal-tick-driven-no-sleep
node: problems.machines.traffic-signal
type: qa
step: 2
tags: [grown]
---
## Q
交通信号灯（Traffic Signal）控制器里为什么不能写 `time.sleep(green_duration)` 加后台线程？替代方案是什么？

## A
`sleep` 让整份设计**不可测**：要验证「紧急车辆抢占之后确实经过了全红」，你只能真的等几秒；要跑一万个 tick 的随机演练，要等几小时。职责也错了——控制器不该知道「一秒有多长」，那是驱动它的那一层的事。

替代方案是**按 tick 推进**：控制器提供 `step()`，推进一格仿真时间；真实时间只通过注入的时钟进入时间戳，逻辑里一处 `sleep` 都没有。谁来每秒调一次 `step()` 是部署问题（实时循环、仿真器、或者测试里的一个 `for`）。

收益是可以写出精确到格的期望，比如 `[GREEN, GREEN, GREEN, CLEARANCE, CLEARANCE, ALL_RED, GREEN]`；整套测试含四千 tick 的随机演练跑完只要几十毫秒。附带好处：控制器内部没有线程，于是**根本不需要锁**——这是要主动说出口的设计选择，不是遗漏。
