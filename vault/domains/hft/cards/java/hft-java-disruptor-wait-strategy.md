---
id: hft-java-disruptor-wait-strategy
node: java.disruptor
type: qa
step: 2
---
## Q
Disruptor 的等待策略（wait strategy）有哪几种？怎样在延迟和 CPU 占用之间选择？

## A
消费者等待生产者发布新序号时，可以用不同的等待方式：

| 策略 | 做法 | 取舍 |
|---|---|---|
| BusySpin | 死循环不停读序号 | 延迟最低，独占一个核 100% CPU |
| Yielding | 自旋一阵后 `Thread.yield()` | 延迟低，CPU 略省 |
| Sleeping | 自旋、让出、再 `parkNanos` 睡眠 | CPU 占用低，延迟抖动更大 |
| Blocking | 用锁和条件变量等待 | CPU 最省，延迟最高（默认） |

交易热路径常用 BusySpin，并配合绑核（把线程固定到独占的核），否则自旋会和别的任务抢 CPU。后台、非关键的消费者用 Sleeping 或 Blocking，把核让出来。
