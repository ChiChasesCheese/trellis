---
id: problems-logger-two-level-thresholds
node: problems.components.logger
type: qa
step: 1
tags: [grown]
---
## Q
在日志框架（Logging Framework）设计里，级别阈值为什么要有两层——logger 一层、每个 handler（输出目的地）各自再一层？只留一层不行吗？

## A
两层各有各的职责，缺一个就答不出常见需求。**logger 的阈值是省开销**：它在造记录之前判一次，被关掉的 `debug()` 调用只花一次整数比较，不会构造 `LogRecord` 对象、不会走分发路径。**handler 的阈值是分流**：同一条记录，控制台全收、文件只收 ERROR、告警通道只收 CRITICAL，这只能由每个目的地自己说了算。只留 logger 一层，就做不到不同目的地不同门槛；只留 handler 一层，被关掉的 DEBUG 仍然要构造对象并遍历所有 handler，高频日志路径上这笔开销很可观。
