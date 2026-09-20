---
id: problems-key-value-store-merkle-tree-anti-entropy
node: problems.foundations.key-value-store
type: qa
step: 6
tags: [grown]
---
## Q
In a key-value store's background replica-repair (anti-entropy) process, why does comparing Merkle tree roots beat comparing every key between two replicas directly, when only a small fraction of keys have actually diverged?

## A
A full scan-and-compare has to read and transmit both replicas' entire datasets to find the differences, and that cost doesn't shrink even when divergence is tiny — at terabyte scale this makes frequent runs impractical. A Merkle tree hashes each small key range at the leaves and combines hashes up to a single root per replica; two replicas first compare root hashes, and only descend into subtrees whose hashes differ, narrowing down to the actually-diverged key ranges in a number of comparisons proportional to the tree's depth and the fraction diverged, not the size of the dataset. The cost is that the tree must be rebuilt for any key range affected by rebalancing, which is one reason virtual-node counts aren't set arbitrarily high.

## Q zh
在键值存储的后台副本修复（反熵，anti-entropy）过程中，当只有很小一部分 key 真正发生分歧时，为什么比较 Merkle 树根哈希优于直接逐条比较两个副本的全部 key？

## A zh
全量扫描比较需要读取并传输两个副本的全部数据才能找出差异，而且即便分歧很小，这个成本也不会随之下降——在 TB 级数据量下这让频繁运行变得不现实。Merkle 树在叶子节点对每个小 key 范围做哈希，逐层向上合并成每个副本各自的一个根哈希；两个副本先比较根哈希，只在哈希不同的子树里继续往下比较，最终定位到真正分歧的 key 范围，比较次数正比于树的深度和分歧比例，而不是数据集大小。代价是节点重分布影响到的 key 范围对应的树需要重建，这也是虚拟节点数不能设得任意大的原因之一。
