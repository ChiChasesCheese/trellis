---
id: hl-sd03-fu-single-thread
node: system-design.sd03-low-latency-trading
type: qa
step: 35
---
## Q
追问：为什么单线程 run-to-completion，不是多线程流水线？怎么扩展？

## A
线程交接 = 至少一次跨核缓存行传递（约 50–100 ns）+ 排队抖动；3 次交接约 0.3 µs，占 10 µs 预算 3%，且引入尾部；单线程一条消息约 1 µs ⟹ 约 10⁶ msg/s / 核；扩展靠按品种分片（shared nothing），不靠加锁；流水线只用于必须换线程的 I/O 与持久化。局限：一个慢策略会拖慢同分片其他策略 ⟹ 时间预算 + 看门狗。

可以说：「并行度来自品种分片，不来自把一条消息的处理拆给几个线程。」
