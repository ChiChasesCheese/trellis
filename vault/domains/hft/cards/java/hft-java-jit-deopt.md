---
id: hft-java-jit-deopt
node: java.jit
type: qa
step: 3
---
## Q
JIT 为什么要基于运行统计做“投机”优化？投机失败触发去优化（deoptimization）时，延迟会发生什么？

## A
JIT 会赌“过去怎样，将来还怎样”。例如某个调用点运行时 99% 只见到 `ArrayList`，JIT 就直接内联 `ArrayList.get`，前面只放一个“类型真是 ArrayList 吗”的检查。这省掉了虚方法调用，也让后续优化看到更大的代码块，所以更快。

代价是：一旦假设被打破（比如第一次来了 `LinkedList`），检查失败，触发 **uncommon trap**，JVM 丢弃这份编译代码，退回解释器，重新收集统计后再编译（`PrintCompilation` 里会看到 `made not entrant`）。这段时间该方法重新变慢。交易例子：开盘后一直只处理新单，第一次出现撤单消息，该路径的延迟突然抬高。对策是预热覆盖各种路径，并让热路径的调用点类型稳定。
