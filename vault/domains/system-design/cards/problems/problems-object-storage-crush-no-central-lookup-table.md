---
id: problems-object-storage-crush-no-central-lookup-table
node: problems.foundations.object-storage
type: qa
step: 3
tags: [grown]
---
## Q
In an object storage design using CRUSH-style placement, the metadata service stores only a placement-group id for each object, not a literal list of storage node addresses. Why does this let the system add a batch of new storage nodes without rewriting any of the (potentially hundreds of terabytes of) existing metadata records?

## A
CRUSH computes an object's physical node set deterministically from a pseudo-random hash of its placement-group id combined with a shared cluster map describing the current topology - both clients and storage nodes can independently compute the same answer without consulting a central lookup table. Adding new nodes changes the cluster map, and re-running the same deterministic function against the updated map yields the new (mostly unchanged, with only a small fraction remapped) node set for every placement group automatically - the metadata records themselves, which only ever stored the placement-group id, never needed to change. A design that instead stored explicit node lists per object would have to rewrite every affected metadata record whenever topology changed.

## Q zh
在一个采用 CRUSH 风格放置策略的对象存储设计中，元数据服务对每个对象只存一个放置组 id，而不是存具体的存储节点地址列表。为什么这使得系统能在新增一批存储节点时，不需要改写任何一条（可能数百 TB 量级的）已有元数据记录？

## A zh
CRUSH 通过对放置组 id 做伪随机哈希、结合一个描述当前拓扑的共享 cluster map，确定性地计算出对象的物理节点集合——客户端和存储节点都能独立算出同一个答案，不需要查任何中心化查找表。新增节点会改变 cluster map，对更新后的 map 重新跑同一个确定性函数，会自动得到每个放置组的新节点集合（大部分不变，只有小部分重新映射）——元数据记录本身从头到尾只存了放置组 id，根本不需要改。如果改成每个对象直接存显式节点列表，拓扑变化时就必须改写每一条受影响的元数据记录。
