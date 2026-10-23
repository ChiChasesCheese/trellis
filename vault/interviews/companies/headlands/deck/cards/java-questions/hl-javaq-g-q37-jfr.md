---
id: hl-javaq-g-q37-jfr
node: java-questions.g-os
type: qa
step: 13
---
## Q
怎么启动 JFR 录制并查看热点方法？JFR 能找出什么？为什么采样型 profiler 在 Java 里可能有偏差？
Why can sampling profilers be biased in Java? How would you find an allocation hotspot?

## A
启动：
```
java -XX:StartFlightRecording=duration=6s,filename=k20.jfr,settings=profile ...
jfr view hot-methods k20.jfr
```
也可运行中 `jcmd <pid> JFR.start`。

- 示例输出：`fib(int)` 占 78.95% 样本，`Random.nextInt(int)` 占 18.42%，正确指出 CPU 热点是热线程和分配线程。
- 其他视图：`gc`、`allocation-by-site`、`contention-by-site`；JFR 开销低到可以在生产常开。
- **采样偏差**：只在 safepoint 处采样会偏（safepoint bias）；JFR 和 async-profiler 不依赖 safepoint 采样。
- **找分配热点**：JFR 的 allocation 事件 / `allocation-by-site`；或 `getThreadAllocatedBytes` 差值。
