---
id: problems-unique-id-generator-lease-coordinator-outage
node: problems.foundations.unique-id-generator
type: qa
step: 7
tags: [grown]
---
## Q
In a unique ID generator design where each node leases a worker id from a coordination service only at startup (never on the generation path), what happens to already-running generator nodes when that coordination service becomes completely unavailable?

## A
Already-running nodes are entirely unaffected for ID generation itself: since GenerateId() never contacts the coordination service, a node that has already leased its worker id keeps generating IDs normally with no dependency on the coordination service's availability. The only thing that breaks is starting new nodes (their initial AcquireWorkerId call fails) and eventually renewing leases — once a lease renewal fails past the lease's expiry, a node should proactively stop generating rather than keep using a worker id that may have been reclaimed and reassigned to another instance, which would risk two nodes producing IDs with the same worker-id segment.

## Q zh
在一个每个节点只在启动时向协调服务申请一次 worker id 租约（从不在生成路径上访问它）的唯一 ID 生成器设计中，当这个协调服务完全不可用时，已经在运行的生成节点会发生什么？

## A zh
已经在运行的节点在 ID 生成本身上完全不受影响：因为 GenerateId() 从不联系协调服务，已经拿到 worker id 租约的节点会继续正常生成 ID，不依赖协调服务的可用性。真正受影响的是启动新节点（它们最初的 AcquireWorkerId 调用会失败）以及之后的租约续约——一旦续约失败超过租约有效期，节点应该主动停止生成，而不是继续使用一个可能已被回收并重新分配给别的实例的 worker id，否则会有两个节点用同一个 worker id 段生成 ID 的风险。
