# DDIA 速成课：AWS 数据服务设计轮要用到的分布式数据基础（教科书模式）

> 读者设定：写过后端，但《DDIA》（Designing Data-Intensive Applications，Kleppmann）里的东西大部分忘了。
> 目标 bar：senior（SDE II/III）。每一节都按 **是什么 → 为什么需要 → 怎么工作（ASCII 图）→ AWS 哪个服务体现了它 → 回去复习哪张卡/哪篇阅读** 来写，
> 最后有自测题（答案折叠在 `<details>` 里）。
>
> 这个文件**不复制**系统设计 domain 里的内容，只做"重新建立直觉"。细节、数字、追问，一律跳到链接的卡片。
> 卡片库在 `vault/domains/system-design/`（地图 `map/`，卡 `cards/`，阅读 `readings/`，47 题 `drills/problems/`）。

## 0. 来源与可信度（2026-10-15 实际抓取）

| 标记 | 来源 | URL | 本次状态 |
|---|---|---|---|
| [D07] | Dynamo: Amazon's Highly Available Key-value Store, SOSP 2007 | https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf | 已抓取全文并检索 |
| [DDB22] | Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service, USENIX ATC 2022 | https://www.usenix.org/system/files/atc22-elhemali.pdf | 已抓取全文并通读 §2–§6 |
| [AUR17] | Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases, SIGMOD 2017 | https://www.amazon.science/publications/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases | 已抓取 PDF 并检索 §2、§3、§4 |
| [S3-21] | Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3 (ShardStore), SOSP 2021 | https://www.amazon.science/publications/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3 | 已抓取 PDF，读 §1–§2 |
| [KDS] | Kinesis Data Streams quotas and limits | https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html | 已抓取 |
| [DMS] | AWS DMS ongoing replication (CDC) | https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html | 已抓取 |
| [RS] | Redshift columnar storage | https://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html | 已抓取 |
| [GLUE] | AWS Glue concepts | https://docs.aws.amazon.com/glue/latest/dg/components-key-concepts.html | 已抓取 |
| [S3PERF] | S3 request-rate performance guidelines | https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html | 已抓取 |
| [ATH] | Athena: partition your data | https://docs.aws.amazon.com/athena/latest/ug/partitions.html | 已抓取 |

本文件里出现的、**没有**在上表标记来源的 AWS 产品细节（例如 Kinesis 默认保留期、DynamoDB Streams 保留 24 小时、Global Tables 的冲突策略、
Aurora 的隔离级别细节、Redshift RA3 托管存储）是我凭记忆写的，行内会标 `【凭记忆，面试前核对】`。自己的推断标 `推断`。

---

## 1. 存储引擎：B-tree 与 LSM-tree

### 1.1 是什么
数据库最底层要回答一个问题：**"键值对在磁盘上怎么摆，才能让读和写都快？"** 有两大流派：

- **B-tree（原地更新）**：磁盘分成固定大小的**页（page，通常 4–16 KB）**，页组成一棵宽而矮的树。更新 = 找到那一页，原地改。
- **LSM-tree（Log-Structured Merge-tree，追加 + 合并）**：写入先进内存里的**有序表 memtable**，满了就整块顺序写成一个不可变的**有序文件 SSTable**；
  后台不断把小文件**合并（compaction）**成大文件。

### 1.2 为什么需要两种
磁盘（尤其机械盘，SSD 也类似）**顺序写远快于随机写**。B-tree 每次更新是随机写一页；LSM 把随机写变成顺序写，代价是读要查多个文件、后台要做合并。

### 1.3 怎么工作

```
B-tree                                   LSM-tree
                                         写: put(k,v)
        [ root: 30 | 60 ]                   │
         /       |       \                  ▼
   [10|20]    [40|50]   [70|80]         WAL(顺序追加, 崩溃恢复) + memtable(内存有序)
    /  |  \                                 │ 满了 flush(顺序写)
 leaf pages (4–16KB, 原地改)                ▼
 写: 找到叶子页 → 改 → 若满则 split        L0: [SST][SST]        ← 可能互相重叠
 崩溃保护: 先写 WAL 再改页                  L1: [  SST  ][  SST  ]  ← 合并后不重叠
 读: 从根到叶 O(log_B N) 次页读             L2: [ ... 更大 ... ]
                                         读: memtable → L0 逐个 → L1 二分 …
                                             每个 SST 先问 Bloom filter "可能有吗?"
```

**放大（amplification）三角**——任何存储引擎都在这三者之间做取舍：

| 放大 | 含义 | B-tree | LSM（leveled） | LSM（size-tiered） |
|---|---|---|---|---|
| 写放大（write amp） | 1 字节用户数据最终导致多少字节落盘 | 中（整页重写 + WAL 双写） | 高（同一数据被逐层重写多次） | 较低 |
| 读放大（read amp） | 一次读要碰几处磁盘 | 低（一条路径） | 中（每层最多一个文件，加 Bloom） | 高（同层多个文件） |
| 空间放大（space amp） | 磁盘占用 / 逻辑数据量 | 中（页内碎片） | 低 | 高（合并前旧版本并存） |

粗略的教科书量级（`推断`：LSM 文献里的经验值，不是 AWS 公布的数字）：size ratio 为 10 时，leveled 压实下每个字节每下沉一层大约被重写 ~10 次，
所以几层加起来写放大可到 10–30 倍；size-tiered 约等于层数。

**删除**在 LSM 里不是真删，而是写一个**墓碑（tombstone）**，等合并到最底层才真正消失——"删得越多反而越慢"的来源。

**worked example**：每天写 1 TB 新数据、leveled 写放大 ~15 倍 → 磁盘实际承受 ~15 TB/天写入，一块 SSD 的耐久度（DWPD）会被先吃掉。
这就是为什么设计 LSM 系统时要把"写放大"当成容量规划的一等公民，而不只是看 QPS。

### 1.4 AWS 里谁体现了它
- **DynamoDB 存储节点 = B-tree + WAL**。[DDB22] §3 / Figure 2："A replication group consists of storage replicas that contain both the write-ahead logs and the B-tree that stores the key-value data"。
  所以 DynamoDB 的"点查延迟稳定"来自 B-tree 的确定性路径。
- **S3 的 ShardStore = LSM 索引 + 追加写的数据区**。[S3-21] §2："ShardStore's key-value store comprises a log-structured merge tree (LSM tree) but with shard data stored outside the tree"
  （这是 Key-Value Separation，类似 WiscKey）；数据按 chunk 写进**只能顺序追加的 extent**，删除只能留"洞"，要靠**回收（reclamation）**把活的 chunk 搬走再 reset 写指针。
  这和 LSM 的 compaction 是同一个思想，只是搬运的对象是大块对象数据而不是 key。
- **Aurora**：把"页"这一层拆走——数据库只往存储层发 **redo log**，存储节点自己后台把日志"应用"成页（[AUR17] §4）。"The log is the database"。
  这是 B-tree 引擎（InnoDB）+ 把落盘职责下沉的组合，不是 LSM。

### 1.5 回去复习
- 地图：[map:storage.internals.btree](../../../../domains/system-design/map/storage.internals.btree.md)、[map:storage.internals.lsm](../../../../domains/system-design/map/storage.internals.lsm.md)、[map:storage.internals.tradeoffs](../../../../domains/system-design/map/storage.internals.tradeoffs.md)
- 卡：[storage-btree-vs-lsm](../../../../domains/system-design/cards/storage/storage-btree-vs-lsm.md)、[storage-amplification-triangle](../../../../domains/system-design/cards/storage/storage-amplification-triangle.md)、[storage-lsm-write-path](../../../../domains/system-design/cards/storage/storage-lsm-write-path.md)、[storage-lsm-read-path](../../../../domains/system-design/cards/storage/storage-lsm-read-path.md)、
  [storage-compaction-strategies](../../../../domains/system-design/cards/storage/storage-compaction-strategies.md)、[storage-bloom-filter-properties](../../../../domains/system-design/cards/storage/storage-bloom-filter-properties.md)、[storage-tombstone-deletes](../../../../domains/system-design/cards/storage/storage-tombstone-deletes.md)、[storage-btree-wal-recovery](../../../../domains/system-design/cards/storage/storage-btree-wal-recovery.md)
- 阅读：[lsm-vs-btree-stopford](../../../../domains/system-design/readings/lsm-vs-btree-stopford.md)、[postgres-btree-internals](../../../../domains/system-design/readings/postgres-btree-internals.md)

---

## 2. 复制（Replication）

### 2.1 是什么、为什么
**把同一份数据存多份**，目的有三：容错（一台坏了还有）、就近读（降延迟）、读扩展（分摊读流量）。难点只有一个：**多份副本怎么保持一致**。三种拓扑：

```
单主 (leader/follower)         多主 (multi-leader)              无主 (leaderless / quorum)
 写 ─▶ [Leader] ─▶ F1          写A ─▶ [L-US] ◀──▶ [L-EU] ◀─ 写B   写 ─▶ 同时发给 N 个副本
            └──▶ F2                  (跨区域互相同步)               等 W 个确认就算成功
 读 ◀─ 任意 F (可能旧)           冲突!同一 key 两边同时改            读 ─▶ 问 R 个，取最新版本
```

### 2.2 单主：同步 vs 异步
- **同步**：leader 等 follower 确认才回复客户端。不丢数据，但一个 follower 慢/挂，写就卡住。
- **异步**：leader 写完自己就回复。快，但 leader 挂时还没传出去的写丢了（**复制延迟 = RPO 风险**）。
- **折中（半同步 semi-sync / 法定人数）**：等**多数派**确认。DynamoDB 与 Aurora 都走这条路。

### 2.3 复制延迟带来的三个"异常"（异步 follower 读的时候）
用一个社交例子：Alice 发帖，写到 leader；她刷新页面，读被路由到了还没追上的 follower。

1. **读不到自己的写（read-your-writes 违反）**：Alice 看不到自己刚发的帖。修法：自己的数据读 leader，或带"我写到的位置"去读。
2. **单调读违反（monotonic reads）**：先读到新数据（连到快 follower），再刷新读到旧数据（连到慢 follower）——时间倒流。修法：同一用户固定读同一个副本。
3. **一致前缀读违反（consistent prefix）**：先看到"回答"后看到"问题"，因为两个分区复制速度不同。修法：因果相关的写放同一分区。

### 2.4 多主与冲突
多主（典型场景：多地域写）要面对**写写冲突**：A 地把 title 改成 X，B 地同时改成 Y。常见解法：
**LWW（last-write-wins，按时间戳取最后写）**——简单但会**静默丢数据**（时钟还不准）；
或保留冲突版本交给应用/CRDT 合并。

### 2.5 无主与 Quorum
N 个副本，写要 W 个确认，读问 R 个，**只要 W + R > N，读集合和写集合必有交集**，读到的集合里至少有一个最新值。

```
N=3, W=2, R=2:   写 → {A,B} 成功,C 没收到
                 读 → 问 {B,C} → B 有新值 v2, C 旧值 v1 → 比版本号 → 返回 v2,并 read-repair 把 v2 推给 C
W+R=4>3 ✓.        若 W=1,R=1: W+R=2<3 ✗ → 可能读到 C 的旧值
```
- **sloppy quorum + hinted handoff**：目标副本挂了，写先暂存到别的"临时"节点并带"提示"，等原节点回来再转交。
  好处：写永远能成功（高可用）；代价：**此时 W+R>N 的交集保证作废**，读可能看不到刚写的值。
- **anti-entropy**：后台用 **Merkle tree**（哈希树）比较两个副本，只传不一致的 key 范围——不用全量比对。
- quorum **不等于线性一致（linearizable）**：并发读写、sloppy quorum、部分失败的写都可能让它看到旧值。

### 2.6 AWS 里谁体现了它
- **Dynamo（2007）**：无主 + N/R/W + sloppy quorum + hinted handoff + vector clock + Merkle tree + gossip + 一致性哈希虚拟节点。
  SLA 写的是"99.9% 请求 300 ms 内完成"（[D07] §2.2）；`R + W > N` 得到"类 quorum"（[D07] §4.5）。
  购物车是选它的原因：**宁可合并出重复商品，也不能拒绝加购**。
- **DynamoDB（2012 至今，不是 Dynamo）**：**单主**！每个分区一个 Multi-Paxos 复制组，跨 AZ 3 个副本，**2/3 写 quorum**，只有 leader 服务写和强一致读，
  任意副本可服务最终一致读（[DDB22] §3、§6.1）。别把"DynamoDB = Dynamo 论文"当成面试答案——[DDB22] §2 明说"shared most of the name … but little of its architecture"。
  另外有 **log replica**：只存最近 WAL，不存 B-tree，坏了一个副本时 leader 几秒内加一个 log replica 补齐写 quorum，而重建完整存储副本要几分钟（[DDB22] §5.1、§6.1）。
- **Aurora**：6 副本跨 3 AZ（每 AZ 2 个），**写 quorum 4/6，读 quorum 3/6**。两条规则：`Vr + Vw > V`（读看得到最新写）与 `Vw > V/2`（写之间不冲突）；
  能挂掉整个 AZ 外加一个节点仍不丢数据（AZ+1），挂一个 AZ 仍能写（[AUR17] §2.1）。
  为什么不用 2/3：AZ 整体宕机时，别的 AZ 里的后台随机故障会让 2/3 quorum 破掉。**日常读不需要 quorum**——数据库自己记录哪个 segment 已追上，直接读那一个（[AUR17] §4.2.3）。
- **DynamoDB Global Tables** 是多主跨区域复制，冲突按 last-writer-wins `【凭记忆，面试前核对】`。

### 2.7 回去复习
- 地图：[map:distributed.replication.leader](../../../../domains/system-design/map/distributed.replication.leader.md)、[map:distributed.replication.multi-leader](../../../../domains/system-design/map/distributed.replication.multi-leader.md)、[map:distributed.replication.leaderless](../../../../domains/system-design/map/distributed.replication.leaderless.md)
- 卡：[distributed-sync-vs-async-replication](../../../../domains/system-design/cards/distributed/distributed-sync-vs-async-replication.md)、[distributed-lag-anomalies](../../../../domains/system-design/cards/distributed/distributed-lag-anomalies.md)、[distributed-read-your-writes](../../../../domains/system-design/cards/distributed/distributed-read-your-writes.md)、[distributed-quorum-math](../../../../domains/system-design/cards/distributed/distributed-quorum-math.md)、
  [distributed-quorum-not-linearizable](../../../../domains/system-design/cards/distributed/distributed-quorum-not-linearizable.md)、[distributed-sloppy-quorum-handoff](../../../../domains/system-design/cards/distributed/distributed-sloppy-quorum-handoff.md)、[distributed-lww-danger](../../../../domains/system-design/cards/distributed/distributed-lww-danger.md)、[distributed-read-repair-anti-entropy](../../../../domains/system-design/cards/distributed/distributed-read-repair-anti-entropy.md)、
  [distributed-failover-mechanics](../../../../domains/system-design/cards/distributed/distributed-failover-mechanics.md)
- 阅读：[dynamo-paper](../../../../domains/system-design/readings/dynamo-paper.md)；整题演练：[design-key-value-store](../../../../domains/system-design/drills/problems/design-key-value-store.md)（题解 [solution-key-value-store](../../../../domains/system-design/readings/problems/solution-key-value-store.md)）

---

## 3. 分区（Partitioning / Sharding）

### 3.1 是什么、为什么
单机放不下或扛不住 → 把数据**切成多块（分区/shard）**，每块在不同机器。副本解决"容错"，分区解决"装不下 + 吞吐"。两者正交：每个分区再各自有若干副本。

### 3.2 哈希分区 vs 范围分区
```
范围分区 (range)                        哈希分区 (hash)
key: a────────m────────z                hash(key) mod / 一致性哈希环
[a–f][g–m][n–s][t–z]                    0 ───────────────────── 2^128
 ✓ 范围扫描高效(同前缀在一处)             ✓ 打散热点,负载均匀
 ✗ 顺序 key(时间戳)全砸最后一片           ✗ 范围扫描要问所有分区(scatter-gather)
```
- **热点（hot key/partition）**：哈希只能打散*不同* key，**同一个 key 太热**（明星账号、爆款商品）仍然压垮一片。办法：给热 key 加随机后缀拆成多份（写时随机选，读时全读再合并），代价是读放大。
- **再平衡（rebalancing）**：加机器时怎么搬数据？`hash mod N` 一加机器几乎全部要搬（灾难）；一致性哈希只搬 ~1/N；
  **固定分区数 + 分区搬家**（先切很多小分区，机器间挪）最常用；**动态分裂**（分区超过阈值就一分为二）最适合范围分区。
- **二级索引**：按 *非分区键* 查怎么办？(a) **本地索引（document-partitioned）**：每个分区只索引自己的数据，写快、读要 scatter-gather；
  (b) **全局索引（term-partitioned）**：索引本身再分区，读快、写要更新别的分区（常常异步 → 索引会陈旧）。

### 3.3 AWS 里谁体现了它
- **DynamoDB**：分区键经过内部哈希函数决定位置；**每个分区承载一段连续、不相交的 key 范围**，所以 sort key 范围查询能在分区内高效完成（[DDB22] §3）。
  Global Secondary Index 是全局索引、异步更新（`【凭记忆，面试前核对】`），Local Secondary Index 与基表同分区。
- **DynamoDB 的"热分区"故事是最好的 senior 素材**（[DDB22] §4）：
  早期把表的预置吞吐**平均分给各分区**，两个问题：(1) *hot partition*——流量集中在少数 key；(2) *throughput dilution*——为存储大小分裂分区后，每个子分区拿到的吞吐被均摊变少。
  解法演进：burst（令牌桶，攒最多 300 秒的闲置容量）→ adaptive capacity（按表级吞吐动态加给热分区）→ **global admission control（GAC，请求路由器本地令牌桶 + 中心 GAC 服务每隔数秒补发令牌）** →
  **按消耗量分裂（split for consumption）**：按观察到的 key 分布挑分裂点，而不是从中间一刀切；并且**单个 item 极热或纯顺序访问的分区分裂也没用，系统会识别出来不分裂**（[DDB22] §4.4）。
- **S3**：按 key 前缀自动分区；每个前缀至少 3,500 写/5,500 读每秒，前缀数无上限；扩容是渐进的，期间可能返回 503 Slow Down（[S3PERF]）。
- **Kinesis**：分片（shard）= 分区；每个 shard 写入至多 1 MB/s 或 1,000 条/s，读取至多 2 MB/s（[KDS]）。按 partition key 哈希到 shard，同 key 有序。
- **Dynamo（2007）**：一致性哈希 + 虚拟节点——每台物理机负责多个环上位置，加减机器时负载均匀迁移（[D07] §4.2）。

### 3.4 回去复习
- 地图：[map:distributed.partitioning.schemes](../../../../domains/system-design/map/distributed.partitioning.schemes.md)、[map:distributed.partitioning.skew](../../../../domains/system-design/map/distributed.partitioning.skew.md)、[map:distributed.partitioning.rebalancing](../../../../domains/system-design/map/distributed.partitioning.rebalancing.md)、[map:distributed.partitioning.indexes](../../../../domains/system-design/map/distributed.partitioning.indexes.md)
- 卡：[distributed-hash-vs-range](../../../../domains/system-design/cards/distributed/distributed-hash-vs-range.md)、[distributed-consistent-hashing](../../../../domains/system-design/cards/distributed/distributed-consistent-hashing.md)、[distributed-vnode-count](../../../../domains/system-design/cards/distributed/distributed-vnode-count.md)、[distributed-hot-key](../../../../domains/system-design/cards/distributed/distributed-hot-key.md)、
  [distributed-hot-key-detection](../../../../domains/system-design/cards/distributed/distributed-hot-key-detection.md)、[distributed-salting-read-cost](../../../../domains/system-design/cards/distributed/distributed-salting-read-cost.md)、[distributed-rebalancing-strategy-choice](../../../../domains/system-design/cards/distributed/distributed-rebalancing-strategy-choice.md)、[distributed-secondary-index-partitioning](../../../../domains/system-design/cards/distributed/distributed-secondary-index-partitioning.md)、
  [distributed-global-index-staleness](../../../../domains/system-design/cards/distributed/distributed-global-index-staleness.md)、[distributed-shard-key-one-way-door](../../../../domains/system-design/cards/distributed/distributed-shard-key-one-way-door.md)、[distributed-scatter-gather-fanout-math](../../../../domains/system-design/cards/distributed/distributed-scatter-gather-fanout-math.md)

---

## 4. 事务与隔离级别（Transactions & Isolation）

### 4.1 是什么、为什么
**事务**：把多个读写打包成一个"要么全做、要么全不做"的单元（ACID 里的 A 原子性）；**隔离（Isolation）** 决定并发事务互相能看到什么。
完美隔离（serializable，等价于一个接一个串行执行）很贵，所以数据库提供一个阶梯，每一级多挡住几种异常：

```
弱 ────────────────────────────────────────────────────────▶ 强
Read Committed   →   Snapshot Isolation(RR)   →   Serializable
挡: 脏读/脏写         再挡: 不可重复读(读到一半       再挡: 写偏斜(write skew)、
                          数据被别人改)                    幻读(phantom)
```

### 4.2 异常用小例子认识
- **脏读（dirty read）**：T1 改了 x 还没提交，T2 读到了；T1 回滚 → T2 读到了从未存在过的值。*Read Committed 挡住。*
- **不可重复读（non-repeatable read）**：T2 在一个事务内读 x 两次，中间 T1 提交了修改，两次结果不同。给一个对账报表读 A 账户、再读 B 账户，中间有转账 → 总额对不上。*Snapshot Isolation 挡住（MVCC：每个事务看一份冻结的快照）。*
- **丢失更新（lost update）**：x=0；T1、T2 各自"读 x → 加 1 → 写回"，最终 x=1 而不是 2。修法：原子 `x = x + 1`、`SELECT … FOR UPDATE`、或 **CAS / 条件写**（`UPDATE … WHERE version = ?`）。
- **写偏斜（write skew）**：规则"至少一个医生值班"。Alice、Bob 同时读到"两人都在值班"，各自把自己改成下班——**各写不同的行**，所以没有写写冲突，Snapshot Isolation 看不出问题，结果 0 人值班。
  只有 serializable（SSI 或 2PL 或串行执行）能挡。
- **幻读（phantom）**：事务按条件 `WHERE room=1 AND time=10:00` 查"没有预订"，然后插入一条；另一事务同时也插入——查询的结果集被"幻影行"改变。

### 4.3 三种实现 Serializable 的办法
1. **真·串行执行**：单线程跑完整事务（Redis、VoltDB），要求事务短、数据在内存。
2. **两阶段锁（2PL）**：读加共享锁、写加排他锁，持有到事务结束；写会阻塞读。能做但并发差、死锁要检测。
3. **SSI（Serializable Snapshot Isolation）**：在快照隔离之上**乐观**地检测"读到的数据被别人改了"，提交时发现冲突就 abort 重试。

### 4.4 分布式事务（跨分区/跨服务）
- **2PC（两阶段提交）**：协调者先问所有参与者"能提交吗（prepare）"，全部 yes 再发 commit。**坏处**：协调者在 prepare 之后挂了，参与者持锁等待（blocking）。
- 所以 senior 答案常常是**避免跨分区事务**：按业务键分区让一个事务只落在一个分区；跨服务用 **Saga**（每步有补偿）+ **Outbox**（本地事务里同时写业务表和"待发送事件"表，再由中继投递），而不是 2PC。

### 4.5 AWS 里谁体现了它
- **DynamoDB**：单 item 操作带条件表达式（`ConditionExpression`，等价 CAS）；还支持跨 item 的 ACID 事务（[DDB22] §3："supports ACID transactions enabling applications to update multiple items … without compromising the scalability, availability, and performance"）。
  事务的内部协议（时间戳排序、无读锁）出自 2023 年 ATC 的另一篇论文，**本次未抓取** `【凭记忆，面试前核对】`。
- **Aurora**：单写者 + 最多 15 个只读副本共享同一份存储卷（[AUR17] §4.2.4）。**不需要 2PC**，因为复制是存储层的 quorum，而不是多个数据库各自提交。
  提交是异步的：事务记录自己的 commit LSN，等 VDL（Volume Durable LSN）追上才回复客户端（[AUR17] §4.2.2）；崩溃恢复一般 10 秒内（[AUR17] §4.3）。
- **S3**：现在对同 key 的 PUT/GET/LIST 提供强读后写一致性（2020-12 公告） `【凭记忆，面试前核对】`；条件写 `If-None-Match` / `If-Match` 可做 CAS，见卡 [storage-s3-conditional-writes](../../../../domains/system-design/cards/storage/storage-s3-conditional-writes.md)。

### 4.6 回去复习
- 地图：[map:distributed.transactions.isolation](../../../../domains/system-design/map/distributed.transactions.isolation.md)、[map:distributed.transactions.concurrency-control](../../../../domains/system-design/map/distributed.transactions.concurrency-control.md)、[map:distributed.transactions.distributed](../../../../domains/system-design/map/distributed.transactions.distributed.md)
- 卡：[distributed-read-committed-anomalies](../../../../domains/system-design/cards/distributed/distributed-read-committed-anomalies.md)、[distributed-isolation-anomalies](../../../../domains/system-design/cards/distributed/distributed-isolation-anomalies.md)、[distributed-mvcc-visibility](../../../../domains/system-design/cards/distributed/distributed-mvcc-visibility.md)、[distributed-lost-update-vs-write-skew](../../../../domains/system-design/cards/distributed/distributed-lost-update-vs-write-skew.md)、
  [distributed-write-skew](../../../../domains/system-design/cards/distributed/distributed-write-skew.md)、[distributed-phantoms-predicate-locks](../../../../domains/system-design/cards/distributed/distributed-phantoms-predicate-locks.md)、[distributed-2pl-vs-ssi](../../../../domains/system-design/cards/distributed/distributed-2pl-vs-ssi.md)、[distributed-actual-serial-execution](../../../../domains/system-design/cards/distributed/distributed-actual-serial-execution.md)、
  [distributed-2pc-mechanics](../../../../domains/system-design/cards/distributed/distributed-2pc-mechanics.md)、[distributed-2pc-blocking-window](../../../../domains/system-design/cards/distributed/distributed-2pc-blocking-window.md)、[distributed-2pc-avoidance](../../../../domains/system-design/cards/distributed/distributed-2pc-avoidance.md)、[correctness-saga-vs-2pc](../../../../domains/system-design/cards/correctness/correctness-saga-vs-2pc.md)、[correctness-outbox-mechanism](../../../../domains/system-design/cards/correctness/correctness-outbox-mechanism.md)
- 阅读：[hermitage-isolation-levels](../../../../domains/system-design/readings/hermitage-isolation-levels.md)、[helland-life-beyond-distributed-transactions](../../../../domains/system-design/readings/helland-life-beyond-distributed-transactions.md)

---

## 5. 共识、租约与 fencing token

### 5.1 是什么、为什么
多个节点要对"**谁是 leader / 下一条日志是什么 / 这把锁归谁**"达成**一致**，哪怕有节点挂、网络慢或分裂。这就是**共识（consensus）**。
没有它：脑裂（split brain）——两个节点都以为自己是 leader，各写各的，数据分叉。

### 5.2 Raft 用大白话（Multi-Paxos 在实践中是同一类东西）
```
角色: Follower ──超时没听到 leader──▶ Candidate ──拿到多数票──▶ Leader
任期 term: 单调递增的"选举轮次编号"(= epoch)。同一 term 至多一个 leader。

写流程:  client ─▶ Leader: 追加日志条目 (term=3, idx=17)
                 Leader ─▶ 并行发给 Followers
                 多数派(含自己)已持久化 ─▶ 该条目 "committed" ─▶ 回复 client
选举规则: 只有日志"至少跟多数派一样新"的节点才能当选 → 已 committed 的条目不会丢
```
三句话记住：(1) 一切写走 leader；(2) 多数派确认才算数（所以 2f+1 个节点容忍 f 个故障）；(3) 任期号让旧 leader 一露面就被识别并退位。
代价：每次写至少一次多数派往返；跨地域部署延迟高；多数派不可达时**拒绝服务**（选 C 不选 A，见 CAP/PACELC）。

### 5.3 租约（lease）与时钟的陷阱
**租约** = 带过期时间的授权："你在未来 10 秒内是 leader，要续约"。好处是 leader 不用每次读都找多数派，只要租约有效就能本地服务**强一致读**。
陷阱：**GC 暂停/进程挂起/时钟漂移**。旧 leader 暂停 20 秒，醒来时还以为自己持有租约，实际上新 leader 已经产生——它的写是"僵尸写"。

### 5.4 Fencing token：让资源端自己拒绝僵尸
每次授权发一个**单调递增的令牌**，受保护的资源（存储）记住见过的最大令牌，**拒绝携带更小令牌的写入**。
客户端自己没法"检查租约仍然有效再写"，因为暂停可以恰好发生在检查与写之间——所以必须在**资源端**执行检查。**没有 fencing 的锁只是建议性锁。**

```
Client1 拿到 lock, token=33 ──(GC 暂停 20s)────────────▶ 写 (token=33) ✗ 被存储拒绝
Client2 租约过期后拿到 lock, token=34 ─▶ 写 (token=34) ✓  存储记下 max=34
```

### 5.5 AWS 里谁体现了它
- **DynamoDB**：每个分区 Multi-Paxos 复制组；leader 靠**租约**维持，只有 leader 服务写和强一致读；**新 leader 必须等旧 leader 租约过期**才能服务（"only takes a couple of seconds"）；
  部署时 leader 主动让位，新 leader 不必等租约过期（[DDB22] §3、§6.2、§6.4）。
  失败检测的 senior 细节：follower 想发起选举前，先问其他副本"你们能连上 leader 吗？"，有人说能就放弃——**抑制灰色网络故障（gray failure）造成的误选举**（[DDB22] §6.2）。
- **Aurora**：存储层的恢复用**epoch 编号**给截断范围版本化，防止旧的恢复过程覆盖新的（[AUR17] §4.3）。
- **AWS Builders' Library《Leader election in distributed systems》**（https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/ ，2026-10-15 抓取；本地剪藏 [aws-leader-election](../../../../domains/system-design/readings/aws-leader-election.md)）：原文 "Leases are the most widely used leader election mechanism at Amazon"；推荐用 DynamoDB 或 ZooKeeper 的租约锁客户端（"the easiest and most tested way"）；Kinesis Client Library 用租约保证每个 shard 只有一个消费者 owner；实践要点——**在每次有副作用的操作之前检查剩余租约时间**，不要在后台线程里续租（线程可能在租约过期后还在跑）；慢网络、重试、GC 暂停都会让租约在你以为有效时已过期。

### 5.6 回去复习
- 地图：[map:distributed.consensus](../../../../domains/system-design/map/distributed.consensus.md)、[map:distributed.time.failure](../../../../domains/system-design/map/distributed.time.failure.md)、[map:distributed.time.clocks](../../../../domains/system-design/map/distributed.time.clocks.md)
- 卡：[distributed-raft-guarantees](../../../../domains/system-design/cards/distributed/distributed-raft-guarantees.md)、[distributed-raft-linearizable-reads](../../../../domains/system-design/cards/distributed/distributed-raft-linearizable-reads.md)、[distributed-epoch-numbers](../../../../domains/system-design/cards/distributed/distributed-epoch-numbers.md)、[distributed-fencing-tokens](../../../../domains/system-design/cards/distributed/distributed-fencing-tokens.md)、
  [distributed-consensus-in-practice](../../../../domains/system-design/cards/distributed/distributed-consensus-in-practice.md)、[distributed-failure-detection](../../../../domains/system-design/cards/distributed/distributed-failure-detection.md)、[distributed-process-pause-causes](../../../../domains/system-design/cards/distributed/distributed-process-pause-causes.md)、[distributed-coordination-service-primitives](../../../../domains/system-design/cards/distributed/distributed-coordination-service-primitives.md)、
  [distributed-flp-and-escape](../../../../domains/system-design/cards/distributed/distributed-flp-and-escape.md)
- 阅读：[raft-paper](../../../../domains/system-design/readings/raft-paper.md)、[kleppmann-distributed-locking](../../../../domains/system-design/readings/kleppmann-distributed-locking.md)、[aws-leader-election](../../../../domains/system-design/readings/aws-leader-election.md)；整题演练：[design-lock-service](../../../../domains/system-design/drills/problems/design-lock-service.md)

---

## 6. 流处理：日志、CDC、exactly-once、水位线

### 6.1 日志是核心抽象
**日志（log）** = 只追加、按序编号（offset）的记录序列。三种东西本质都是日志：数据库的 WAL、复制流、消息队列（Kafka/Kinesis）。
把"状态"看成"对日志 fold 的结果"，就得到：**重放日志可以重建任何派生状态**（缓存、搜索索引、数仓、物化视图）。

```
        ┌──────────────── 日志 (有序, 可重放) ─────────────────┐
写入 ─▶ │ e1  e2  e3  e4  e5  e6 …                               │
        └──┬───────────────┬──────────────────┬──────────────────┘
        消费者A(offset=4)  消费者B(offset=2)    新消费者(从 0 重放 → 重建索引)
```

### 6.2 CDC（Change Data Capture）
从源数据库的**事务日志**（MySQL binlog、Postgres WAL、Oracle redo）读取变更，转成事件流发给下游。比"双写"（应用同时写库和队列）强，因为后者在中途崩溃时两边不一致（**dual-write 问题**）。
CDC 要解决三件事：(1) **初始快照 + 增量切换**：先全量拷贝，再接增量，接缝处不丢不重（记下快照时的日志位置）；(2) **有序与幂等**：按主键分区保证同一行的变更有序，下游用主键 upsert 保证重放幂等；(3) **schema 变化**。

### 6.3 exactly-once 的真相
网络上的消息交付语义只有：最多一次（可能丢）、至少一次（可能重）。**"恰好一次"的效果 = 至少一次投递 + 幂等处理**（或把"处理结果 + offset 提交"放进同一个事务）。
```
at-least-once 重试 ─▶ 下游可能收到同一事件两次
        │
        ├─ 幂等 key (event_id / 主键 + 版本号) → 去重表或 upsert → 重复无副作用 ✓
        └─ 事务: 同一个原子操作里 {写结果, 提交 offset} → 崩溃重启要么都有要么都没有 ✓
```
"我的系统是 exactly-once"在面试里是危险话，要立刻补一句"**对哪个边界**、靠什么机制"。

### 6.4 事件时间、处理时间与水位线
- **处理时间（processing time）**：事件到达处理器的时间；**事件时间（event time）**：事件实际发生的时间。手机离线 10 分钟再上传，两者差 10 分钟。
- **窗口（window）**：把无界流切成有界块——滚动窗口（tumbling）、滑动窗口（sliding）、会话窗口（session）。
- **水位线（watermark）**：处理器对"事件时间 ≤ T 的事件大概都到齐了"的**启发式声明**。水位线越过窗口结束时间，窗口关闭输出。晚到的事件怎么办：丢弃、放进侧输出、
  或**更新结果并撤回旧结果（retraction）**。水位线是"延迟 vs 完整性"的旋钮。

### 6.5 AWS 里谁体现了它
- **Kinesis Data Streams**：分片日志，每 shard 写 1 MB/s 或 1,000 条/s、读 2 MB/s（[KDS]）；同 partition key 进同 shard 保序；消费者自己管理检查点 → 至少一次，需要幂等消费。
  默认保留 24 小时、可延长 `【凭记忆，面试前核对】`。
- **AWS DMS**：用各引擎原生接口读事务日志做 CDC（Oracle LogMiner / binary reader，MySQL 要开 row 级 binlog）；文档明确写"**CDC does not provide real-time replication … There are no SLAs for CDC latency**"（[DMS]）。
  面试里讲 DMS 类系统时，要把"没有延迟 SLA"当成需求边界而不是缺陷。
- **DynamoDB Streams**：按 item 的变更日志，24 小时保留，分片有序 `【凭记忆，面试前核对】`。
- **DynamoDB 自己的 PITR**：定期快照 + 归档到 S3 的 WAL，恢复 = 找最近快照 + 重放日志到目标时间点（[DDB22] §5.5）——一个"日志 + 快照"的教科书实例。

### 6.6 回去复习
- 地图：[map:async.log](../../../../domains/system-design/map/async.log.md)、[map:async.streaming.cdc](../../../../domains/system-design/map/async.streaming.cdc.md)、[map:async.streaming.processing](../../../../domains/system-design/map/async.streaming.processing.md)、[map:async.delivery.exactly-once](../../../../domains/system-design/map/async.delivery.exactly-once.md)
- 卡：[async-log-vs-queue](../../../../domains/system-design/cards/async/async-log-vs-queue.md)、[async-cdc-mechanism](../../../../domains/system-design/cards/async/async-cdc-mechanism.md)、[async-cdc-initial-snapshot](../../../../domains/system-design/cards/async/async-cdc-initial-snapshot.md)、[correctness-dual-write-problem](../../../../domains/system-design/cards/correctness/correctness-dual-write-problem.md)、[async-exactly-once-myth](../../../../domains/system-design/cards/async/async-exactly-once-myth.md)、
  [async-idempotent-producer](../../../../domains/system-design/cards/async/async-idempotent-producer.md)、[async-kafka-transactions-eos](../../../../domains/system-design/cards/async/async-kafka-transactions-eos.md)、[async-eos-boundary-choice](../../../../domains/system-design/cards/async/async-eos-boundary-choice.md)、[async-event-time-watermarks](../../../../domains/system-design/cards/async/async-event-time-watermarks.md)、[async-late-event-policy](../../../../domains/system-design/cards/async/async-late-event-policy.md)、
  [async-window-types](../../../../domains/system-design/cards/async/async-window-types.md)、[correctness-idempotent-consumer-patterns](../../../../domains/system-design/cards/correctness/correctness-idempotent-consumer-patterns.md)
- 阅读：[the-log-jay-kreps](../../../../domains/system-design/readings/the-log-jay-kreps.md)、[confluent-exactly-once-kafka](../../../../domains/system-design/readings/confluent-exactly-once-kafka.md)、[treat-exactly-once-delivery](../../../../domains/system-design/readings/treat-exactly-once-delivery.md)、[turning-the-database-inside-out](../../../../domains/system-design/readings/turning-the-database-inside-out.md)；整题演练：[design-ad-click-aggregation](../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)、[design-message-queue](../../../../domains/system-design/drills/problems/design-message-queue.md)

---

## 7. 批处理 vs 流处理（以及数据湖/数仓）

### 7.1 是什么
- **批（batch）**：输入有界（"昨天的全部日志"），算完输出，延迟分钟到小时，吞吐高、容易重算和修 bug。
- **流（stream）**：输入无界，持续输出，延迟秒级，要面对乱序、状态、恢复。
- **Lambda 架构**：批 + 流两套代码并行（批保准确、流保时效），代价是写两遍逻辑。**Kappa**：只保留流，需要重算时从日志起点重放。

### 7.2 为什么数据服务岗位会反复问
AWS Data Services 的产品几乎都是这几块的托管版：**对象存储（S3）→ 目录（Glue Data Catalog）→ 批 ETL（Glue/EMR，Spark）→ 查询（Athena/Redshift）+ 流（Kinesis）+ CDC（DMS）**。
关键直觉：

```
行存 (OLTP): 一行的所有列相邻        列存 (OLAP): 一列的所有值相邻
 [id,name,age][id,name,age]…          [id,id,id…][name,name…][age,age,age…]
 读一整行快, 聚合某一列要读全部        只读需要的列, 同类型数据压缩比高, 向量化执行
```
- **列存省 I/O**：只读查询涉及的列；同列数据类型一致，压缩（字典、游程）效果好（[RS]：同一块能装下约三倍的列值，因而 I/O 约为三分之一，这是文档里的简化示意）。
- **分区裁剪（partition pruning）**：目录按 `year=2026/month=10/day=15/` 布局，`WHERE` 命中分区键时只扫对应前缀（[ATH]）。
- **小文件问题**：对象存储每个请求有固定开销，几百万个小文件会让查询被 `LIST` 和 `GET` 次数拖死（[ATH] 也提醒大量未分区对象会触到 S3 请求速率限制）。解法：合并（compaction）成 128 MB–1 GB 左右的文件 `推断：常见经验区间`。
- **表格式（Iceberg/Delta/Hudi）**：在对象存储上用元数据文件+快照实现 ACID、时间旅行、增量合并（见卡 [analytics-table-formats](../../../../domains/system-design/cards/analytics/analytics-table-formats.md)）。

### 7.3 AWS 里谁体现了它
- **S3**：对象存储，11 个 9 的设计耐久度（[DDB22] §5.1 引用）；高吞吐靠并行化前缀与多实例聚合（[S3PERF]）。
- **Glue**：Data Catalog（元数据，**不含数据本身**）+ Crawler（推断 schema 建表）+ Spark ETL Job + Trigger（[GLUE]）。
- **Redshift**：列存 MPP 数仓（[RS]）；排序键/分布键决定裁剪与 join 的数据搬运 `【凭记忆，面试前核对】`。
- **Athena**：无服务器 SQL 查询 S3 上的数据——官方文档原话 "serverless, so there is no infrastructure to set up or manage, and you pay only for the queries you run"（https://docs.aws.amazon.com/athena/latest/ug/what-is.html ，2026-10-15 抓取）；"按扫描的字节数计费"是公开定价模型，但定价页是动态页面、本次没读到具体价格 `【凭记忆，面试前核对】`。在这个模型下，列存格式+分区裁剪直接等于省钱（[ATH]）。

### 7.4 回去复习
- 地图：[map:analytics.batch](../../../../domains/system-design/map/analytics.batch.md)、[map:analytics.olap](../../../../domains/system-design/map/analytics.olap.md)、[map:analytics.warehouse](../../../../domains/system-design/map/analytics.warehouse.md)、[map:analytics.derived](../../../../domains/system-design/map/analytics.derived.md)
- 卡：[analytics-batch-vs-stream](../../../../domains/system-design/cards/analytics/analytics-batch-vs-stream.md)、[analytics-lambda-vs-kappa](../../../../domains/system-design/cards/analytics/analytics-lambda-vs-kappa.md)、[analytics-row-vs-column-layout](../../../../domains/system-design/cards/analytics/analytics-row-vs-column-layout.md)、[analytics-columnar-compression](../../../../domains/system-design/cards/analytics/analytics-columnar-compression.md)、
  [analytics-lake-vs-warehouse-vs-lakehouse](../../../../domains/system-design/cards/analytics/analytics-lake-vs-warehouse-vs-lakehouse.md)、[analytics-table-formats](../../../../domains/system-design/cards/analytics/analytics-table-formats.md)、[analytics-lakehouse-compaction](../../../../domains/system-design/cards/analytics/analytics-lakehouse-compaction.md)、[analytics-idempotent-reruns](../../../../domains/system-design/cards/analytics/analytics-idempotent-reruns.md)、
  [analytics-shuffle-mechanics](../../../../domains/system-design/cards/analytics/analytics-shuffle-mechanics.md)、[analytics-skew-stragglers](../../../../domains/system-design/cards/analytics/analytics-skew-stragglers.md)
- 阅读：[iceberg-table-format](../../../../domains/system-design/readings/iceberg-table-format.md)、[spark-rdd-paper](../../../../domains/system-design/readings/spark-rdd-paper.md)、[clickhouse-vldb-paper](../../../../domains/system-design/readings/clickhouse-vldb-paper.md)

---

## 8. 编码与 schema 演进（Encoding & Schema Evolution）

### 8.1 是什么、为什么
数据要在**进程之间、时间之间**流动：写进磁盘/消息队列的字节，会被**不同版本**的代码读到（滚动升级时新旧版本共存；日志里有三年前的数据）。
所以 schema 必须能演进：
- **向后兼容（backward）**：新代码能读旧数据。
- **向前兼容（forward）**：旧代码能读新数据（忽略不认识的字段）。

### 8.2 怎么做
| 格式 | 机制 | 要点 |
|---|---|---|
| JSON | 字段名随数据一起存 | 灵活但大；数字精度/类型模糊 |
| Protobuf / Thrift | 字段**编号（tag）** 而非名字 | 只能加可选字段、不能复用编号、不能随便改类型 |
| Avro | 写入 schema 与读取 schema **分开**，读时做 schema resolution | 新增字段必须有默认值；适合 Kafka + schema registry |

滚动发布规律：**expand → migrate → contract**（先加新字段/新读取能力，再迁移数据与写入，最后删旧的）。
任何"先部署只读新格式的代码，等全部节点都能读，再开始写新格式"的两阶段发布，都是在避免新旧版本不兼容。

### 8.3 AWS 里谁体现了它
- **DynamoDB 的 read-write deployment**：第一步先部署"能读新消息格式"的软件；全部节点都能读之后，第二步才部署"开始发送新消息"。回滚时两种格式仍可共存（[DDB22] §6.4）。
  这就是 forward compatibility 的运维版，也是 Builders' Library《Ensuring rollback safety during deployments》的核心。
- **Glue Schema Registry**（Avro/JSON Schema/Protobuf 的兼容性检查） `【凭记忆，面试前核对】`。
- DMS/Kinesis/Glue 表之间传的都是"带 schema 的行"，列加减就是 schema 演进问题。

### 8.4 回去复习
- 地图：[map:storage.encoding](../../../../domains/system-design/map/storage.encoding.md)、[map:architecture.services](../../../../domains/system-design/map/architecture.services.md)
- 卡：[storage-encoding-compat-directions](../../../../domains/system-design/cards/storage/storage-encoding-compat-directions.md)、[storage-avro-schema-resolution](../../../../domains/system-design/cards/storage/storage-avro-schema-resolution.md)、[storage-avro-evolution-defaults](../../../../domains/system-design/cards/storage/storage-avro-evolution-defaults.md)、[storage-protobuf-tag-rules](../../../../domains/system-design/cards/storage/storage-protobuf-tag-rules.md)、
  [storage-rolling-upgrade-compat](../../../../domains/system-design/cards/storage/storage-rolling-upgrade-compat.md)、[infra-two-phase-format-rollout](../../../../domains/system-design/cards/infra/infra-two-phase-format-rollout.md)、[infra-rollback-safety](../../../../domains/system-design/cards/infra/infra-rollback-safety.md)、[architecture-expand-contract](../../../../domains/system-design/cards/architecture/architecture-expand-contract.md)
- 阅读：[kleppmann-schema-evolution](../../../../domains/system-design/readings/kleppmann-schema-evolution.md)、[aws-rollback-safety](../../../../domains/system-design/readings/aws-rollback-safety.md)

---

## 9. 把它们串起来：一次 `PutItem` 的旅程（DynamoDB，[DDB22] §3）

```
client ──▶ request router ──(查 metadata: key→分区→leader)──▶ 分区 leader (Multi-Paxos 组长)
                                                              │ 1. 条件检查(ConditionExpression)
                                                              │ 2. 生成 WAL 记录,发给另外 2 个副本(跨 AZ)
                                                              │ 3. 收到 ≥1 个 follower 持久化确认(共 2/3) → 应用到 B-tree
                                                              ▼
                                                           ack 给 client
后台: WAL 定期归档到 S3 (带 checksum + manifest) → 用于 PITR、备份、scrub 校验
```
把本文每一节对应上去：分区（§3，哈希+连续范围）、复制与 quorum（§2，2/3 写 quorum）、共识与租约（§5，leader lease）、
存储引擎（§1，B-tree+WAL）、日志/快照/PITR（§6）、协议演进（§8，read-write deployment）。
**面试里讲任何 AWS 数据服务，都可以用这条骨架把各个机制挂上去。**

---

## 10. 论坛实证：面试里真正被问到的"DDIA 零件"（校准你的复习重点）

来源：`../catalog/raw/forums.md` §1（2026-10-15）。结论：**不问原理推导**（没有人被要求推 Raft/2PC/vector clock），**但会问"在具体系统里怎么选这个零件"，senior 档会追到内部机制**。
面试官的原话（官方 HLD 视频，official.md §4.5）："if you are going to rely on something like Leader election it would be better if you know how it works, but at the very least be aware of its limitations"；"candidates asking about some esoteric features from these databases … I usually ask them to design that part in detail"。
**推断**：你嘴里说出的每个零件名，都可能被要求当场设计出来——所以只说你能讲到第二层的。

| 报告里被点名的零件（ID）| 本文哪一节 | 你应该能说到的第二层 |
|---|---|---|
| LSM tree vs B-tree、Cassandra 内部（LC6841317，SDE2 Twitter 设计）| §1 | 写放大/读放大、compaction、Bloom filter、墓碑；为什么写多选 LSM |
| Consistent hashing、sharding vs replication、倾斜分区/名人问题（LC6841317、LC8420230）| §3 | 虚拟节点、再平衡搬多少数据、热 key 加盐的读代价 |
| Read-after-write consistency（LC6841317）| §2.3 | 读自己的写：读 leader / 带位点读；quorum 为什么也不保证 |
| Kafka / **ISR** / consistent hashing（LC8537984，**SDE1** 现场，面试官看简历后问）| 见下 | ISR 是什么、为什么 `acks=all` 加 `min.insync.replicas` |
| 同步冲突解决，"我先说 last-write-wins，他追问"（RD1wyeq0k）| §2.4 | LWW 为什么丢数据；版本向量/应用层合并/CRDT |
| 主备 DB 故障检测、自动切换、副本同步、一致性（JC-bqt2ha，DB group）| §2、§5 | fencing、租约、灰色故障、RPO/RTO → 新题 `problems/managed_db_control_plane.md` |
| DynamoDB 分区键选择（LC8528370）| §3 | 高基数、避免热分区、访问模式驱动键设计 → `hld_sketches.md` S4 |
| OpenSearch + CDC（LC8315111）| §6 | CDC 快照衔接、幂等 upsert → `problems/cdc_replication_pipeline.md` |
| 分布式限流的 central leasing service（LC8428653，SDE3）| §5 | 租约、令牌批量预取、失败时退化策略 |
| OT vs CRDT（LC8286346）| 本文未展开 | 见卡 `distributed-crdt-convergence`、`problems-google-docs-ot-vs-crdt-tradeoff`、题库 [design-google-docs](../../../../domains/system-design/drills/problems/design-google-docs.md) |

**Kafka ISR（本文其余部分没讲，补一段）** `【凭记忆，面试前核对；官方文档见 [kafka-docs](../../../../domains/system-design/readings/kafka-docs.md)】`
- **是什么**：一个分区的副本集合里，"跟得上 leader 的那些副本"叫 ISR（In-Sync Replicas）。
- **为什么**：全同步等所有副本会被最慢的拖垮；全异步 leader 挂了会丢数据。ISR 是折中：**只等"跟得上的"副本**，落后太久的被踢出 ISR（不再等它）。
- **怎么工作**：生产者 `acks=all` 时，leader 等 **ISR 中所有副本**都写入才确认；再配 `min.insync.replicas=2`，ISR 少于 2 个时拒绝写入（宁可不可用也不丢数据）。leader 挂了从 ISR 里选新 leader（不会丢已确认数据）；若 ISR 为空且允许"不干净选举"（unclean leader election），可能选出落后的副本，**用丢数据换可用性**。
- **复习**：[problems-message-queue-isr-quorum-f-plus-1-tradeoff](../../../../domains/system-design/cards/problems/problems-message-queue-isr-quorum-f-plus-1-tradeoff.md)、[confluent-exactly-once-kafka](../../../../domains/system-design/readings/confluent-exactly-once-kafka.md)、[design-message-queue](../../../../domains/system-design/drills/problems/design-message-queue.md)。

**复习优先级建议**（按上表证据）：§3（分区/热点）≥ §2（复制/一致性/冲突）> §5（租约/故障切换）> §1（LSM vs B-tree）> §6（CDC）> §4（事务）。

---

## 11. 自测题（先自己答，再展开）

1. 写放大、读放大、空间放大各是什么？为什么 leveled compaction 读更快但写更贵？
<details><summary>答案</summary>写放大：1 字节用户数据导致的总落盘字节；读放大：一次读要访问的磁盘位置数；空间放大：磁盘占用/逻辑数据量。
Leveled 保证每层 key 范围不重叠，一次读每层至多查一个文件（读快、空间低），但为维持这种不重叠，数据在下沉每一层时都要与下层重叠文件合并重写（写贵）；size-tiered 反之。</details>

2. 为什么 LSM 的删除要写墓碑？墓碑什么时候才能真正清除？
<details><summary>答案</summary>旧版本散落在多个不可变文件中，没法原地删，只能写一条"此 key 已删除"的新记录盖住旧的。只有当合并到包含该 key 所有旧版本的最底层（并且超过保留/复制宽限期）时才能丢弃；否则旧值会"复活"。</details>

3. N=3、W=2、R=2 时为什么读一定能看到最新写？如果启用 sloppy quorum 呢？
<details><summary>答案</summary>W+R=4>3，任何写集合与读集合至少交一个节点，该节点有最新版本。sloppy quorum 下写可能落在"目标副本以外"的临时节点，读去问的是目标副本，交集保证失效，可能读到旧值（等 hinted handoff 补齐后才恢复）。</details>

4. Aurora 为什么选 V=6、Vw=4、Vr=3，而不是 3 副本 2/3？
<details><summary>答案</summary>要在"整个 AZ 故障 + 另一个节点随机故障（AZ+1）"下不丢数据，且"整个 AZ 故障"时仍能写。Vr+Vw=7>6 保证读看得到最新写，Vw=4>3 保证两个写必相交。2/3 在 AZ 故障叠加背景故障时会失去 quorum。（[AUR17] §2.1）</details>

5. DynamoDB 的写 quorum 是多少？一个副本无响应时 leader 怎么保持写可用？
<details><summary>答案</summary>3 副本跨 AZ，2/3 构成写 quorum；leader 立即加入一个 log replica（只复制最近 WAL，几秒钟），保证写 quorum 仍能满足，而重建完整存储副本需要几分钟。（[DDB22] §5.1、§6.1）</details>

6. 描述"读不到自己的写"和"单调读违反"的区别，各给一个修法。
<details><summary>答案</summary>前者：用户写完后自己读不到（读了落后副本）——修：用户自己的数据读 leader，或带写入位置去读。后者：连续两次读，第二次反而更旧（两次连到不同落后程度的副本）——修：同一用户粘到同一副本。</details>

7. 热分区和吞吐稀释各是什么？DynamoDB 最终怎么解决？
<details><summary>答案</summary>热分区：流量集中在少数 item，所在分区被限流而整表吞吐有余。稀释：为存储分裂分区后，吞吐被均摊给子分区，每个子分区能用的变少。演进：burst → adaptive capacity → GAC（请求路由器本地令牌桶+中心补发）→ 按消耗分裂（按观察到的 key 分布选分裂点；单 item 极热或顺序访问则不分裂）。（[DDB22] §4）</details>

8. 写偏斜是什么？为什么 Snapshot Isolation 挡不住？举例并给一个修法。
<details><summary>答案</summary>两个事务读同一前提、各写不同的行，合起来破坏不变量（值班医生例子）。没有写写冲突，所以快照隔离不报错。修法：串行化隔离、对前提行加 `FOR UPDATE`、或把不变量物化成一行并加唯一约束/条件写（"物化冲突"）。</details>

9. 为什么 2PC 在实践中常被避免？senior 答案怎么绕开跨分区事务？
<details><summary>答案</summary>协调者在 prepare 后宕机，参与者持锁阻塞；延迟高、可用性取决于所有参与者。绕开：让一个事务只涉及单分区（按业务键分区）；跨服务用 Saga + 补偿 + Outbox；或在设计里允许最终一致并用对账兜底。</details>

10. Raft 里"任期号"解决什么问题？为什么只有日志足够新的节点才能当选？
<details><summary>答案</summary>任期号是逻辑时钟，旧 leader 看到更大任期就退位，防止脑裂时旧 leader 继续提交。只让日志不落后于多数派的节点当选，保证已 committed 的条目一定在新 leader 日志里，不会丢。</details>

11. 解释 fencing token，以及为什么客户端自己检查租约没用。
<details><summary>答案</summary>每次授权给单调递增令牌，资源端记住最大令牌并拒绝更小的。客户端"检查租约再写"不是原子的，GC 暂停可以恰好发生在检查与写之间，所以必须由资源端校验。</details>

12. 为什么说"exactly-once"其实是"至少一次 + 幂等（或事务）"？给出两种实现方式。
<details><summary>答案</summary>交付层面只能保证最多/至少一次。要让效果恰好一次：(1) 幂等：事件带唯一 id/主键+版本，下游去重或 upsert；(2) 事务：把"写结果"与"提交 offset"放进同一原子事务（如 Kafka 事务、数据库事务）。必须说清是在哪个边界。</details>

13. CDC 为什么比应用双写更可靠？初始快照与增量的接缝怎么处理？
<details><summary>答案</summary>双写在两次写之间崩溃会不一致；CDC 只以数据库事务日志为唯一事实来源。接缝：开始快照前先记录日志位置（LSN/binlog 位点），全量拷贝后从该位点开始应用增量，重复的变更靠主键 upsert 幂等吸收。</details>

14. 水位线是什么？水位线推进过快/过慢各有什么后果？
<details><summary>答案</summary>对"事件时间 ≤T 的事件已大致到齐"的启发式声明，用来决定何时关闭窗口。过快：晚到事件被丢或需要撤回修正；过慢：结果延迟高、状态占内存久。</details>

15. 为什么列存适合分析、行存适合 OLTP？分区裁剪和小文件问题分别是什么？
<details><summary>答案</summary>OLTP 一次读写整行，行存相邻；分析常只聚合少数列，列存只读需要的列且同类型易压缩。分区裁剪：按目录前缀布局分区，条件命中分区键就跳过无关前缀。小文件：每个对象请求有固定开销，海量小文件使 LIST/GET 次数与元数据成为瓶颈，需要合并。</details>

16. 滚动升级时新旧版本共存，为什么要"先读后写"两阶段发布？
<details><summary>答案</summary>新代码先上线"能读新格式"，等所有节点都能读后再让它"写新格式"。否则新节点写出旧节点读不懂的数据，回滚也会失败。DynamoDB 的 read-write deployment 就是这个模式。（[DDB22] §6.4）</details>

17. （senior 综合）用本文的机制，讲清 DynamoDB 写一条数据时为什么"单个副本宕机不影响写、一个 AZ 宕机也不丢"。
<details><summary>答案</summary>分区的 3 个副本分在不同 AZ，写只需 2/3 持久化 WAL；一个副本宕机 → leader 加 log replica 补足 quorum；整个 AZ 宕机 → 其余两个 AZ 仍有 2 个副本（若 leader 在故障 AZ，其它副本等旧租约过期后选新 leader）；WAL 还会归档到 S3 做第二道保险。（[DDB22] §3、§5.1、§6.1）</details>
