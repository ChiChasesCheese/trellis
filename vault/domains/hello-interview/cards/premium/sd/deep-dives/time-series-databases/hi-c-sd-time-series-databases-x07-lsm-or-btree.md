---
id: hi-c-sd-time-series-databases-x07-lsm-or-btree
node: sd.deep-dives.time-series-databases.exam
type: qa
step: 7
---
## Q
**时序数据库 · LSM 还是 B 树**｜考点 · 必会

(a) 5 万点/秒写入、很少读；(b) 每秒 500 次随机点读、写入很少。各适合 LSM 存储还是 B 树存储？为什么？

## A
- **(a) LSM：** 写入走内存和顺序落盘，吞吐高；读较少，慢一点可以接受。
- **(b) B 树：** 点读只需沿树走一条路径，很快；LSM 的点读可能要翻多个 SSTable，写放大也没有换来收益。
- **LSM 的代价：** 读放大（多个文件）、写放大（压缩时重写）、空间放大（旧版本暂存）。布隆过滤器与压缩策略能缓解读放大，但不能消除。
- **加分：** 说明「写多读少」是前提；如果有 mix，量化后再决定。
