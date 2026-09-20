---
id: problems-rate-limiter-local-first-hybrid-enforcement
node: problems.foundations.rate-limiter
type: qa
step: 3
tags: [grown]
---
## Q
In a rate limiter spanning 20 gateway nodes, why does a design that splits each key's limit into a static 'limit/20' share per node, enforced purely locally with no cross-node communication, produce incorrect throttling — and what does a local-first hybrid design do instead?

## A
If a key's traffic happens to concentrate on fewer nodes than the fleet size (e.g. due to sticky client routing), those nodes hit their static limit/20 share and start rejecting requests even though the key's global quota is nowhere near exhausted elsewhere in the fleet — an under-admission error caused purely by how traffic happened to be distributed, not by actual overuse. A local-first hybrid design instead starts from the static split but has each node periodically (e.g. every 100ms) report its observed share of a key's traffic to a central store, which recomputes and redistributes each node's local share to match real traffic patterns; local checks stay in-process (no network call) for the common case, only falling back to a synchronous central-store check when a node's local state looks close to its (dynamically adjusted) share.

## Q zh
在一个横跨 20 台网关节点的速率限制器里，为什么把每个 key 的限额静态切成 'limit/20' 份、每个节点纯本地执行、互不通信的方案会产生错误的限流？'本地优先'的混合方案又是怎么做的？

## A zh
如果某个 key 的流量恰好集中在少数几个节点上（例如客户端连接粘性导致），这几个节点会先撞上自己静态的 limit/20 份额并开始拒绝请求，即使这个 key 在集群其它地方的全局配额远未用完——这是纯粹由流量分布方式造成的错误拒绝（under-admission），而不是真的用量超标。本地优先的混合方案从静态切分出发，但让每个节点周期性地（例如每 100ms）向中心存储上报自己观测到的该 key 流量份额，中心重新计算并下发各节点应得的份额，使其匹配真实流量分布；大多数情况下本地判定完全在进程内完成（不发网络请求），只有当某节点的本地状态逼近它（动态调整后）的份额时，才退化为一次同步的中心存储核验。
