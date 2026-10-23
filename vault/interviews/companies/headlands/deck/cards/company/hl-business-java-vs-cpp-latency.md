---
id: hl-business-java-vs-cpp-latency
node: company.business
type: qa
step: 15
---
## Q
Headlands 的 Java 岗和延迟的关系是什么？岗位描述里和延迟直接相关的是哪一条？

## A
Java 岗**不在交易热路径上**，毫秒以下的交易引擎是 C++ 岗。

岗位描述里与延迟直接相关的只有一条：改善**系统内部组件之间**的网络通信，以达到最优延迟和吞吐。

"exchange connectivity""lock-free""profiling"这些热路径词出现在 C++ 岗的描述里。Java 岗更偏研究平台与基础设施：研究平台、分布式存储、计算集群、监控。
