---
id: profiling-cprofile-clock-tick-limit
node: performance.profiling
type: qa
source: python-docs
---
## Q
确定性剖析器（如 `cProfile`）的计时精度受限于什么，典型下限在什么量级？这对剖析一个被调用几百万次的极小函数有什么含义？

## A
受限于底层系统时钟的滴答间隔，典型量级在毫秒级（约 0.001 秒）。对调用次数极多、单次极短的函数，每次调用的计时误差会随调用次数累积放大，此时应改用 `timeit` 做批量微基准，而不是逐次信任 `cProfile` 给出的单函数计时。
