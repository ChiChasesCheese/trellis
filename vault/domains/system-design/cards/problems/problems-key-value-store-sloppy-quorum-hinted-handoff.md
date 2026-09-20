---
id: problems-key-value-store-sloppy-quorum-hinted-handoff
node: problems.foundations.key-value-store
type: qa
step: 4
tags: [grown]
---
## Q
In a Dynamo-style key-value store, why does a strict quorum (write must land on real preference-list nodes or fail) undermine the goal of never rejecting writes during node failure, and what mechanism fixes it?

## A
A strict quorum rejects a write whenever more than N−W of the key's specific preference-list nodes are unreachable, even if the rest of the cluster is healthy — a single unlucky node failure can block writes for the keys it owns. The fix is a sloppy quorum: when a preferred node is down, the coordinator writes to the next healthy node outside the preference list instead of failing, tagging the data with hinted handoff metadata identifying the true owner. Once the original node recovers, the substitute asynchronously forwards the data to it and deletes its temporary copy. This means any W reachable nodes — not specifically the 'correct' W — are enough for a write to succeed.

## Q zh
在一个 Dynamo 风格的键值存储中，为什么严格 quorum（写入必须落在真正的偏好列表节点上，否则失败）会破坏「节点故障时绝不拒绝写入」这个目标？什么机制解决了它？

## A zh
严格 quorum 会在某个 key 的偏好列表节点中有超过 N−W 个不可达时拒绝写入，哪怕集群其余部分完全健康——一个不走运的节点故障就可能阻塞它所拥有的那些 key 的写入。解法是 sloppy quorum：当某个偏好节点不可达时，协调节点不让写入失败，而是写到偏好列表之外的下一个健康节点，并给这份数据打上标明真正归属节点的 hinted handoff 元数据。原节点恢复后，代管节点异步把数据转交给它并删除本地临时副本。这意味着任意 W 个可达节点——不一定是「正确」的那 W 个——就足以让写入成功。
