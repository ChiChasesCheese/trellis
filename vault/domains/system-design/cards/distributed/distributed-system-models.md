---
id: distributed-system-models
node: distributed.time.failure
type: qa
---
## Q
Crash-stop vs crash-recovery vs Byzantine fault models — what does each assume, and which (plus which timing model) do mainstream datacenter systems design for?

## A
- **Crash-stop**: a faulty node halts and never returns — clean but unrealistic.
- **Crash-recovery**: nodes may crash and come back, keeping **stable storage** across the outage but losing memory — what Raft, Kafka, and databases actually assume.
- **Byzantine**: nodes may lie or act arbitrarily (bugs, compromise). Tolerating f liars needs **3f+1** nodes plus signed messages — the cost is why datacenter systems skip it and instead handle *weak* corruption with checksums, TLS, and input validation. BFT lives where participants distrust each other (blockchains, some aerospace).

Timing: **partial synchrony** — the network usually behaves, but delays are occasionally unbounded — which is why timeouts can trigger recovery but must never be the sole proof of death ([[distributed-failure-detection]]).

## Q zh
Crash-stop、crash-recovery、拜占庭这三种故障模型——各自假设什么？主流数据中心系统按哪一种（再加哪种时序模型）来设计？

## A zh
- **Crash-stop**：出故障的节点停下来就再也不回来了——干净但不现实。
- **Crash-recovery**：节点可能崩溃后又恢复，在故障期间**稳定存储**得以保留，但内存丢失——这才是 Raft、Kafka 和数据库真正的假设。
- **拜占庭**：节点可能撒谎或任意行动（bug、被攻破）。容忍 f 个说谎者需要 **3f+1** 个节点，外加签名消息——这个代价正是数据中心系统跳过它、转而用校验和、TLS、输入校验来处理*弱*损坏的原因。BFT 用在参与者互相不信任的场景（区块链、部分航天系统）。

时序：**部分同步（partial synchrony）**——网络通常表现正常，但延迟偶尔会无界——这就是为什么超时可以触发恢复流程，但绝不能作为死亡的唯一证据（[[distributed-failure-detection]]）。
