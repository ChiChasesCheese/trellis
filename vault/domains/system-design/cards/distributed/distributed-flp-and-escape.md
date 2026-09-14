---
id: distributed-flp-and-escape
node: distributed.consensus
type: qa
---
## Q
The FLP result proves consensus is impossible — yet Raft and Paxos clusters reach agreement in production every second. State what FLP actually claims, and the loophole every practical protocol uses.

## A
**The claim is narrower than the slogan**: in a *fully asynchronous* system (no bounds on message delay or processing speed, hence no useful clocks or timeouts), no deterministic algorithm can guarantee consensus **terminates** if even one node may crash. The core: with unbounded delay, a crashed node and a slow node are indistinguishable, and any algorithm can be indefinitely postponed by adversarial scheduling. Safety isn't the issue — *guaranteed liveness* is.

The loophole: real networks aren't fully asynchronous. Practical protocols assume **partial synchrony** and use **timeouts and randomization** — election timeouts to suspect a dead leader, randomized backoff to break repeated split votes. Consequence: Raft/Paxos are engineered so that **safety never depends on timing** (epochs and quorum intersection hold under any delays), while **liveness does** — during pathological network conditions the cluster may keep electing without committing, which is degraded availability, never inconsistency.

## Q zh
FLP 结果证明了共识（consensus）不可能——然而 Raft 和 Paxos 集群每一秒都在生产环境里达成一致。说清 FLP 到底断言了什么，以及所有实用协议利用的那个"漏洞"。

## A zh
**断言比口号窄得多**：在一个*完全异步*的系统中（消息延迟和处理速度没有任何上界，因此没有可用的时钟或超时），只要有一个节点可能崩溃，就没有确定性算法能保证共识**终止**。核心在于：延迟无界时，崩溃的节点和慢的节点无法区分，任何算法都可能被对抗性的调度无限推迟。问题不在安全性——在于*有保证的活性（liveness）*。

漏洞在于：真实网络并非完全异步。实用协议假设**部分同步（partial synchrony）**，并使用**超时与随机化**——用选举超时怀疑 leader 已死，用随机退避打破反复的平票。推论：Raft/Paxos 的工程设计使**安全性永不依赖时序**（epoch 和 quorum 相交在任意延迟下都成立），而**活性依赖时序**——在病态的网络状况下，集群可能不停选举而无法提交，这是可用性降级，绝不是不一致。
