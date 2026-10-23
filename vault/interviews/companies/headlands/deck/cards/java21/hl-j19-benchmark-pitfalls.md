---
id: hl-j19-benchmark-pitfalls
node: java21.j19-runtime-zgc-jit
type: qa
step: 30
---
## Q
为什么不能用 `System.nanoTime()` 循环当基准？正式测量用什么？

## A
自己写的循环有这些问题：没有预热、死代码被消除（实验用 `sink` 输出结果防止被删）、常量折叠、OSR 干扰。

正式测量用 **JMH**（OpenJDK 微基准工具）。课上的数字是**演示现象**，不是基准结论。

测延迟还要用分位数（p99、p99.9、max），并避免**协同遗漏**（coordinated omission）：测量线程在系统停顿时也停止发请求，漏记了停顿期间本该发生的慢请求。
