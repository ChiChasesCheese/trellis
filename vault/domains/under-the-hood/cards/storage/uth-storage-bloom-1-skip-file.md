---
id: uth-storage-bloom-1-skip-file
node: storage.bloom
type: qa
step: 1
---
## Q
**布隆过滤器：这个文件里肯定没有**｜RocksDB · v10.9

按 key 读取时，同一个 key 可能出现在每一层的文件里。怎样不逐个读磁盘就知道“不在”？

## A
**结构。** 每个 SST 带一个布隆过滤器（Bloom filter）：一个位数组加 k 个哈希函数。加入 key 时把 k 个位置 1；查询时只要有一位是 0，就一定不在；全是 1 才是“可能在”。

**细节。**

- 每个 key 约 9.9 位，误判率约 1%（RocksDB 文档）。
- 误判只会多读一个文件，不会漏数据。
- 默认没开：`filter_policy` 默认是 `nullptr`，要自己配 `NewBloomFilterPolicy(10)`。

**为什么。** 位数组约 1.25 字节/key，常驻内存，换掉一次磁盘 I/O。

**坑。** 不支持删除：同一位可能被多个 key 共用。

**对应 LeetCode：** LC 705 设计哈希集合 · LC 217 存在重复元素
