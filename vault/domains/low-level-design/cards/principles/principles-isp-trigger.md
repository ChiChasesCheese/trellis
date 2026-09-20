---
id: principles-isp-trigger
node: principles.solid
type: qa
step: 5
---
## Q
什么信号说明一个接口违反了接口隔离原则（Interface Segregation Principle）？

## A
触发信号：
- 实现者被迫实现一堆自己根本用不到的方法；
- 每个调用方实际只用这个接口的一部分；
- 接口名字里塞了好几个不相关的概念，比如"ReadWriteLock"、"SerializableComparable"；
- 同一个类有多个调用方，各自需要一组不同的方法子集。

症状：写测试替身（fake/mock）时要为用不到的方法硬编造实现；测试里要为跟这个实现者无关的方法做多余的 setup。
