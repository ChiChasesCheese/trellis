---
id: problems-traffic-signal-timing-plan-strategy
node: problems.machines.traffic-signal
type: qa
step: 4
tags: [grown]
---
## Q
交通信号灯（Traffic Signal）的定周期与感应式配时怎么做成可替换的？感应式里最短绿和最长绿各守什么？

## A
把决策收敛成一个布尔问题：**绿灯还要不要再保持一个 tick**。这是策略模式（Strategy）真正挣来的一次应用——两个实现都存在、都带配置状态，而且差别不是一个参数能表达的。

```python
def hold(self, ctx: PhaseContext) -> bool:
    if ctx.elapsed < ctx.phase.min_green:
        return True
    if ctx.elapsed >= ctx.phase.max_green:
        return False
    return ctx.waiting > 0 or ctx.gap_since_arrival <= self._gap
```

**最短绿**是安全参数不是调优参数：绿灯刚亮一格就跳黄，已经起步的司机没有停车距离。**最长绿**是公平上限：没有它，「有车就延长」在早高峰会把支路饿死。中间那一行是**断流**（gap-out）——连续若干 tick 没有新车到达就认为车流断了。

方案拿到的是 `PhaseContext` 这个只读快照（相位、已走时长、排队数、距上次到达几格），不是控制器本身；把 `self` 传给策略是这道题最容易埋下的耦合。
