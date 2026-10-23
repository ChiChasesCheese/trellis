---
id: hl-j19-tail-latency
node: java21.j19-runtime-zgc-jit
type: qa
step: 1
---
## Q
为什么交易系统看尾部延迟（tail latency）而不是平均延迟？Java 有哪两个别的语言没有的尾部延迟成因？

## A
交易系统关心 p99、p99.9、最大值：绝大多数订单 50 µs 处理完，但每一万个里有一个用了 100 ms，就足以错过行情，平均值几乎不变却掩盖了它。

Java 的两个特有成因：
1. **垃圾回收暂停**（GC pause）；
2. **JIT 预热与「去优化」**（deoptimization）。

为什么「平均延迟 50 µs」不能说明系统适合低延迟交易：平均值被大量快的请求稀释，应看 p99/p99.9/max，并检查测量是否有协同遗漏（coordinated omission）。
