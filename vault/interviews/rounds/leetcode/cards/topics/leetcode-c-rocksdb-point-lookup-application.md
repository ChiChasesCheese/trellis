---
id: leetcode-c-rocksdb-point-lookup-application
node: topics.uncategorised
type: qa
anki: 1787359913594
tags: [algorithm::binary-search, algorithm::bloom-filter, algorithm::lsm-tree, algorithm::skip-list, application, case, case::rocksdb-point-lookup, category::storage-databases, leetcode, system::rocksdb]
---
## Q
RocksDB 的 point lookup 中，LSM、Bloom Filter 和二分分别负责什么？二分具体出现在哪三层？

## A
LSM 把数据组织成 MemTable 与多层有序 SST；Bloom Filter 先排除肯定不含 key 的候选文件；二分依次用于定位 L1+ 的候选 SST、SST 内的 data block、以及 data block 内的 key。WAL 属于写入恢复路径，不参与这三层二分。

**Evidence**

RocksDB 官方 MultiGet Read Path 明确描述 L1+ 文件元数据、SST index block 和 data block 三处 binary search，以及中间的 Bloom Filter probe。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FRocksDB%20%E7%82%B9%E6%9F%A5%E4%B8%AD%E7%9A%84%20LSM%E3%80%81Bloom%20Filter%20%E4%B8%8E%E4%B8%89%E5%B1%82%E4%BA%8C%E5%88%86)
