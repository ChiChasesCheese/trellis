---
id: problems-elevator-tick-not-sleep
node: problems.machines.elevator
type: qa
step: 1
tags: [grown]
---
## Q
在电梯系统（Elevator System）设计里，为什么要把时间建模成一个 `step()` 推进一拍的 tick，而不是给每部电梯开一个线程、在循环里 `time.sleep(3)` 模拟运行一层？

## A
因为这道题考的是调度逻辑，不是定时器。tick 让一拍只做一件事（关门、走一层、或开门），于是“下一站去哪”“此刻处于哪个状态”都能被逐拍断言，整套测试不需要睡眠、也不会在 CI 上飘。线程加 sleep 则把调度算法和线程生命周期纠缠在一起，测试只能靠等待和运气，出了错分不清是算法错还是竞态。真实时间仍然需要（事件要带时间戳，用于统计等待时长），所以时钟是构造时注入的 `Callable[[], datetime]`，测试里“过了三秒”就是把假时钟往前拨，而不是真的等三秒。
