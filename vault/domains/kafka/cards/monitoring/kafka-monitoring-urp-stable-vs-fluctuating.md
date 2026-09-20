---
id: kafka-monitoring-urp-stable-vs-fluctuating
node: monitoring.broker-metrics
type: qa
step: 2
source: kafka-2e
---
## Q
发现集群的非同步分区（URP）数量持续维持在一个稳定不变的数值，和这个数值一直在上下波动，这两种表现分别通常指向什么完全不同的根因？

## A
如果 URP 数量长期稳定不变，很可能是集群中有某个 broker 已经彻底离线：整个集群的 URP 数量恰好等于这个离线 broker 上的分区数量，因为离线的 broker 不会再产生任何指标，它负责的这些分区就会一直停留在「非同步」状态，直到这个 broker 的硬件、操作系统或 Java 层面的问题被解决并重新上线。如果 URP 数量在波动，或者虽然稳定但确认并没有 broker 离线，则说明是集群本身出现了性能问题（比如资源过度消耗），这类问题原因繁多、更难定位，需要进一步检查具体是哪个（或哪些）broker、以及是 CPU、磁盘 IO 还是网络的瓶颈。
