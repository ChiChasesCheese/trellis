# Redis 八股：分布式锁、数据结构、持久化、高可用

Redis 是一个把数据放在内存里的键值数据库（key-value store），用单线程执行命令，常被拿来做缓存、计数器、排行榜和分布式锁。面试官通常从「你们项目里 Redis 干什么」开始，沿着一条线往下挖：数据结构 → 持久化 → 主从与集群 → 分布式锁 → 锁的各种失效场景。答题顺序固定为 **机制 → 为什么 → 数字或取舍 → 追问**，每个问题都要能在 60–90 秒内讲完。缓存三大问题和缓存一致性在 [[tiktok-cache-problems]]，幂等和分布式事务在 [[tiktok-idempotency-transactions]]。

## 速记：这一页的 13 个问题

| # | 问题 | 一句话答案 |
|---|---|---|
| 1 | 单线程为什么还快 | 内存 + epoll 多路复用 + 简单结构，瓶颈是网络不是 CPU |
| 2 | 五种基本结构的底层 | SDS / quicklist / listpack+hashtable / intset+hashtable / listpack+skiplist |
| 3 | ZSet 怎么用、为什么是跳表 | 排行榜、延迟队列；范围查询简单、实现简单 |
| 4 | RDB 与 AOF | RDB 快照恢复快但丢数据多；AOF 丢 ≤1 秒但文件大 |
| 5 | 过期与淘汰 | 惰性 + 定期删除；内存满了按 maxmemory-policy 淘汰 |
| 6 | 主从、哨兵、Cluster | 异步复制会丢写；Cluster 16384 个槽 |
| 7 | SET NX 分布式锁 | `SET k token NX PX`，释放用 Lua 比较 token 再删 |
| 8 | 锁过期了业务没完 | 看门狗续期；真正正确要靠 fencing token |
| 9 | RedLock 与批评 | 5 个独立主节点多数派；Kleppmann 指出时间假设不成立 |
| 10 | Redis 锁 vs ZooKeeper vs 数据库 | 效率型用 Redis，正确性型用共识系统或数据库约束 |
| 11 | 事务、Lua、pipeline | MULTI 不回滚；Lua 原子；pipeline 只省网络往返 |
| 12 | KEYS 与 SCAN | KEYS 阻塞全库；SCAN 增量但可能重复 |
| 13 | 去重与计数 | Bitmap、HyperLogLog（12KB，误差约 0.81%）、Set |

## Q1. Redis 是单线程的，为什么还能这么快？

- **机制**：命令执行在一个主线程里串行完成，没有锁竞争和上下文切换；数据在内存里，大多数操作是 O(1) 或 O(log N)；网络层用 epoll 多路复用（IO multiplexing）让一个线程同时管几万个连接。
- **为什么**：Redis 的瓶颈是内存带宽和网络，不是 CPU，所以多线程执行命令换不来多少，反而带来锁的复杂度。
- **数字**：单实例通常 8–10 万 ops/s（简单命令），用 pipeline 能到几十万。Redis 6.0 起可以开 I/O 线程（`io-threads`）并行读写 socket，**命令执行仍然是单线程**。
- **追问 · 单线程的代价？** 任何慢命令都会堵住所有人：`KEYS *`、大集合的 `SMEMBERS`、删除百万元素的大 key、耗时的 Lua。对策：用 `SCAN` 代替 `KEYS`，用 `UNLINK`（4.0+，后台线程释放内存）代替 `DEL`，拆大 key。
- **追问 · 所以 Redis 只用一个核？** 一台机器上跑多个实例，或用 Cluster 分片；持久化的 fork 子进程、I/O 线程、后台线程也会用到别的核。

## Q2. 五种基本数据结构的底层编码是什么？

| 类型 | 小数据时 | 大数据时 | 备注 |
|---|---|---|---|
| String | embstr / int | raw（SDS，简单动态字符串） | SDS 记录长度，O(1) 取长度，二进制安全；单值上限 512MB |
| List | listpack | quicklist（链表，每个节点是一个 listpack） | 3.2 起 quicklist，7.0 起 listpack 取代 ziplist |
| Hash | listpack | hashtable | 阈值默认 128 个字段、单值 64 字节 |
| Set | intset（全整数）/ listpack | hashtable | 元素全是整数且少时用 intset |
| ZSet | listpack | skiplist + dict | dict 做 member 到 score 的 O(1) 查找，跳表做排序和范围 |

- **为什么**：小数据用紧凑的连续内存省空间、对 CPU 缓存友好；数据大了再换成指针结构保证 O(1) 或 O(log N)。
- **追问 · 为什么 listpack 取代 ziplist？** ziplist 的每个节点记录前一个节点长度，改一个节点可能引起后面一连串更新（连锁更新，cascade update）；listpack 每个节点只记自己的长度，没有连锁更新。
- **追问 · rehash 怎么不卡？** 渐进式 rehash（incremental rehash）：同时保留两张哈希表，每次增删查顺带搬一个桶，加上后台定时搬，避免一次搬完阻塞。

## Q3. ZSet 常见用法？为什么用跳表而不是红黑树或 B+ 树？

- **用法**：排行榜（`ZADD` / `ZREVRANGE 0 99` / `ZRANK`）、延迟队列（score = 到期时间戳，轮询 `ZRANGEBYSCORE -inf now`）、滑动窗口限流（score = 请求时间戳，`ZREMRANGEBYSCORE` 删窗口外的）。
- **复杂度**：`ZADD`、`ZREM`、`ZRANK` 是 O(log N)；`ZRANGE` 是 O(log N + M)，M 是返回的个数。
- **为什么跳表**：范围查询只要找到起点再顺着最底层链表走；实现比红黑树简单得多（插入不用旋转）；每层的 span 让 `ZRANK` 也能 O(log N)。Redis 作者的原话是「实现和调试更简单，范围操作不比平衡树慢」。B+ 树是为磁盘页设计的，内存里没有这个收益。
- **追问 · 同分怎么排？** 同 score 按 member 字典序。要「同分先到先得」，把时间编进 score：`score * 2^20 + (MAX_TS - ts)`，注意 score 是 double，只有 53 位有效整数精度，别溢出。
- **追问 · 亿级用户的排行榜？** 单个 ZSet 放不下的话按用户 ID 或分数段分片，每片取 Top-K，再在应用层归并；全局名次只对前几千名精确，其余用分段区间估算。

## Q4. RDB 和 AOF 有什么区别？怎么选？

- **RDB**（快照）：`fork` 子进程，利用写时复制（copy-on-write, COW）把某一时刻的内存写成二进制文件。恢复快、文件小；缺点是两次快照之间的数据会丢（分钟级）。
- **AOF**（append-only file）：把每条写命令追加到日志。`appendfsync` 三档：`always`（每条都刷盘，最安全最慢）、`everysec`（默认，最多丢约 1 秒）、`no`（交给操作系统，通常 30 秒以内）。文件会变大，所以有 AOF 重写（rewrite）：按当前内存状态重新生成最短的命令序列。
- **混合持久化**（4.0 起 `aof-use-rdb-preamble yes`）：重写时前半部分是 RDB 格式、后面追加增量命令，兼顾恢复速度和数据完整。7.0 起 AOF 拆成「基础文件 + 增量文件 + 清单」（multi-part AOF）。
- **选择**：只做缓存可以都关；要保数据用 AOF everysec + 混合；极致不丢数据 Redis 本身做不到，要落到数据库。
- **追问 · fork 有什么风险？** fork 要复制页表，实例越大越慢（10GB 级可能阻塞几十到上百毫秒）；快照期间写入多会触发大量 COW，内存峰值最坏接近翻倍。对策：单实例控制在 10–20GB 内，关闭透明大页（THP），预留内存，在从库上做备份。
- **追问 · 重启时先读哪个？** 开了 AOF 就读 AOF（它更完整），没开才读 RDB。

## Q5. 过期键怎么删？内存满了怎么办？

- **过期删除**：惰性删除（访问时才检查，过期就删）+ 定期删除（每秒 10 次，每次从设了过期时间的键里随机抽 20 个，删掉过期的，如果过期比例超过 25% 就继续抽）。两者都不保证过期键立刻消失，内存不会精确释放。
- **淘汰**（`maxmemory` 达到上限时按 `maxmemory-policy`）：默认 `noeviction`（写入报错）；常用 `allkeys-lru`、`allkeys-lfu`、`volatile-lru`、`volatile-ttl`、`allkeys-random`。
- **近似 LRU**：不维护全局链表，随机抽 `maxmemory-samples`（默认 5）个键，淘汰其中最久未访问的；样本越大越接近真 LRU，CPU 越多。
- **LFU**：8 位计数器，对数递增，随时间衰减；能抵抗一次性扫描把热数据挤掉的问题。
- **追问 · 缓存场景选哪个？** 通常 `allkeys-lru` 或 `allkeys-lfu`；Redis 里还存了不能丢的数据（比如锁、会话）就别混用，拆实例。
- **追问 · 主从下谁负责过期？** 只有主库删，主库向从库发 `DEL`；从库读到过期键时（3.2+）返回空但不自己删。

## Q6. 主从复制、哨兵、Cluster 是怎么保证高可用的？

- **主从复制**：从库 `PSYNC replid offset`；偏移量还在主库的复制积压缓冲区（`repl-backlog-size`，默认 1MB）里就增量同步，否则全量同步（主库 `bgsave` 生成 RDB 发过去）。**复制是异步的**，主库宕机时没传出去的写会丢。
- **哨兵**（Sentinel）：监控主从，多个哨兵投票判断主观下线 → 客观下线（达到 `quorum`），再选一个哨兵 leader（要多数派同意）执行故障转移，挑复制偏移量最大、优先级高的从库升主。
- **Cluster**：16384 个哈希槽（hash slot），`CRC16(key) mod 16384` 决定槽，每个主节点负责一段槽；客户端被重定向用 `MOVED`（槽永久迁走）和 `ASK`（迁移中临时重定向）；节点之间用 gossip 交换状态，主节点宕机由其从节点发起选举。
- **为什么是 16384**：心跳包里要带槽位图，16384 位只有 2KB；更多的槽让心跳包变大，而集群规模建议不超过约 1000 个节点，这个数量足够分布均匀。
- **限制**：多键命令（`MGET`、事务、Lua）的键必须在同一个槽；用哈希标签 `{user:1}:cart` 强制落到同一槽。
- **追问 · 脑裂（split brain）？** 主节点被网络隔离但仍在接受写，哨兵把从库升了主，旧主恢复后变成从库，隔离期间的写全部丢失。缓解：`min-replicas-to-write 1` 和 `min-replicas-max-lag 10`，让旧主在联系不到从库时拒绝写。这只是缩小窗口，不是消除。

## Q7. 怎么用 Redis 实现分布式锁？

加锁一条命令，释放一段 Lua：

```text
SET lock:order:123 <uuid> NX PX 30000
```

```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])
else
  return 0
end
```

- **NX**：只在键不存在时设置，保证互斥。**PX**：设过期时间，持有者崩溃时锁能自动释放，避免死锁。**两者必须在同一条命令里**，分开写（先 `SETNX` 再 `EXPIRE`）中间崩溃就永远死锁。
- **value 是随机唯一值**：释放时要确认「锁还是我的」。不比较直接 `DEL`，会出现：A 的锁过期 → B 拿到锁 → A 执行完 `DEL`，把 B 的锁删了。
- **释放用 Lua**：`GET` 比较和 `DEL` 要原子；否则 A 刚 `GET` 完发现是自己的，锁恰好过期被 B 拿走，A 的 `DEL` 又删了 B 的锁。
- **可重入**：用 Hash，字段是线程标识，值是重入次数（Redisson 就是这么做的）；加锁次数加一，释放减一，到 0 才删键。
- **加锁失败怎么办**：快速失败，或带超时的自旋重试（加随机退避），或用 Pub/Sub 等释放通知（Redisson 的做法），不要无限忙等。
- **追问 · 为什么不用 `SETNX` + 业务时间戳？** 依赖各机器时钟，时钟不一致会让锁被提前抢走，且无法原子地检查并替换。

## Q8. 锁过期了业务还没执行完怎么办？看门狗是什么？

- **问题**：TTL 设短了会提前释放，设长了持有者崩溃后别人要等很久。TTL 没有对所有情况都合适的值。
- **看门狗**（watchdog，Redisson 实现）：加锁时没指定 `leaseTime`，默认锁时长 `lockWatchdogTimeout = 30s`，后台每 10 秒（1/3 周期）检查持有线程还活着就续期到 30 秒。进程崩溃 → 续期停止 → 最多 30 秒后锁自然过期。
- **注意**：指定了 `leaseTime` 就不会续期；看门狗只证明「线程还活着」，不证明「它还有资格操作」。
- **它防不住什么**：持有者发生长时间 GC 停顿（stop-the-world）或整个进程被挂起，续期线程也停了，锁过期，别人拿到锁，原持有者醒来后以为自己还持有，继续写数据。**任何基于租约（lease）的锁都有这个问题。**
- **根治：fencing token**。锁服务每次发放锁时返回一个单调递增的数字，持有者每次写下游时带上它，下游（数据库或存储）拒绝比已见过的 token 小的请求：

```sql
UPDATE account SET balance = balance - 100, fence = 42
WHERE id = 7 AND fence < 42;
```

- **追问 · Redis 怎么发 token？** 单实例 `INCR` 就行，但主从切换后计数可能回退，所以 Redis 做不到严格的 fencing；ZooKeeper 的 zxid 或节点序号、etcd 的 revision 才是天然单调的。
- **追问 · 不想引入 fencing 怎么办？** 让被保护的操作本身幂等，或用数据库乐观锁（版本号 `WHERE version = ?`）。锁只负责「大多数时候别重复干活」，正确性由下游约束兜底。

## Q9. RedLock 是什么？为什么被批评？

- **算法**：N = 5 个互相独立的 Redis 主节点（没有主从关系）。客户端记下开始时间 T1；依次对 5 个节点 `SET NX PX`，每个请求用远小于 TTL 的超时；**至少 3 个成功**，且 `有效时间 = TTL − (T2 − T1) − 时钟漂移 > 0`，才算拿到锁；失败则向所有节点发释放。
- **为什么要它**：单实例 Redis 锁在主从切换时会丢：A 在主库拿到锁，主库宕机，锁还没复制到从库，从库升主，B 也拿到同一把锁。RedLock 想用多数派解决这个问题。
- **Kleppmann 的批评**（2016）：
  1. 它**假设**网络延迟、进程停顿、时钟漂移都有上界，这在真实系统里不成立（GC 停顿、时钟跳变、包延迟）；
  2. 没有 fencing token，所以即使算法正确，持有者暂停后仍会出现两个客户端同时认为自己持有锁；
  3. 如果你只需要「效率」（偶尔重复没关系），一个单实例锁就够了，RedLock 过重；如果你需要「正确性」，RedLock 又不够，应该用有共识算法的系统。
- **Antirez 的回应**：时钟问题可以靠单调时钟和多数派检查缓解，进程停顿发生在加锁之后的话，任何锁都有同样问题。
- **结论（要说的一句话）**：效率型场景用单 Redis 锁加合理 TTL；正确性型场景用 ZooKeeper / etcd 加 fencing token，或把正确性交给数据库约束和幂等。业界实践里，RedLock 用得并不多。
- **追问 · 5 个节点挂了 2 个还能工作吗？** 能，多数派 3 个存活即可；挂 3 个就加不上锁。

## Q10. Redis 锁、ZooKeeper 锁、数据库锁怎么选？

| | Redis | ZooKeeper / etcd | 数据库（唯一键或行锁） |
|---|---|---|---|
| 一致性 | 异步复制，切换可能丢锁 | 共识（ZAB / Raft），线性一致 | 单库强一致 |
| 性能 | 最高，单机数万 QPS | 低一个数量级，写要过半数 | 受连接数和行锁影响 |
| 死锁处理 | 靠 TTL 过期 | 临时节点 / 租约，会话断开自动释放 | 事务超时 |
| 公平 / 通知 | 要自己做 | 临时顺序节点 + watch，天然公平 | 无 |
| 适合 | 高并发、容忍极小概率重复 | 选主、配置、要求正确性的互斥 | 业务本身就在这个库里 |

- **说法**：先问「重复执行的代价是什么」。代价是多发一条通知，用 Redis；代价是重复扣款，用数据库唯一键或状态机更新，锁只是优化。
- **追问 · 乐观锁和悲观锁？** 乐观锁用版本号（`UPDATE ... WHERE version = ?`，影响行数 0 就重试），冲突少时吞吐高；悲观锁（`SELECT ... FOR UPDATE`）冲突多时更稳，但持锁时间长会拖垮连接池。

## Q11. Redis 事务、Lua 脚本、pipeline 分别保证什么？

- **事务**（`MULTI` / `EXEC`）：命令入队，`EXEC` 时连续执行不被打断，但**没有回滚**：某条命令运行时出错，其他命令照样执行。`WATCH` 实现乐观锁：被监视的键在 `EXEC` 前被改过，整个事务放弃。
- **Lua 脚本**：整个脚本在单线程里原子执行，可以带逻辑（读—判断—写），是实现「比较并删除」「限流」「扣库存」的标准办法。风险：脚本执行太久会阻塞全库，超过 `busy-reply-threshold`（默认 5 秒）后其他客户端收到 `BUSY` 错误。Cluster 下脚本里的所有键必须在同一个槽。
- **pipeline**：把多条命令一次发出、一次读回，省的是网络往返（RTT），**不保证原子性**，中间可以穿插别的客户端的命令。
- **追问 · 扣库存怎么写？** 一段 Lua：`if tonumber(redis.call('get', k)) >= n then return redis.call('decrby', k, n) else return -1 end`。不要「先 GET 再 SET」，会超卖。

## Q12. 为什么线上不能用 KEYS？SCAN 有什么特点？

- **KEYS pattern** 是 O(N) 遍历整个键空间，单线程下阻塞所有请求，千万级键会堵几秒。
- **SCAN cursor MATCH pattern COUNT n**：游标式增量遍历，每次只扫一小段。特点：**可能返回重复键**（rehash 时），**不保证快照**（遍历期间新增或删除的键可能出现也可能不出现），`COUNT` 只是提示不是精确返回数；但在遍历开始到结束一直存在的键一定会返回。
- **用法**：扫描用 `SCAN`，大集合用 `SSCAN` / `HSCAN` / `ZSCAN`；业务代码要对结果去重、要能容忍重复处理。
- **追问 · 批量删除某前缀的键？** 在从库上 `SCAN` 出键，主库用 `UNLINK` 分批删，每批几百个，批间 sleep，别一把梭。

## Q13. 海量去重、计数、签到怎么用 Redis 做？

| 需求 | 结构 | 数字 |
|---|---|---|
| 精确去重，规模小 | Set | 每个元素几十字节，百万级就是上百 MB |
| 用户 ID 连续的签到、活跃 | Bitmap（`SETBIT` / `BITCOUNT`） | 一亿用户一天只要 12.5MB |
| 近似去重计数（UV） | HyperLogLog（`PFADD` / `PFCOUNT`） | 固定约 12KB，标准误差 0.81% |
| 判断「可能存在」 | Bloom filter（RedisBloom 模块，或位图自己实现） | 1% 误判率约每元素 9.6 位 |
| 附近的人 | GEO（底层是 ZSet，score 是 geohash） | `GEOSEARCH` |

- **计算**：1 亿位 ÷ 8 = 1250 万字节 ≈ 12.5MB。
- **追问 · HyperLogLog 为什么能这么省？** 对每个元素取哈希，统计哈希值前导零的最大个数，分到 16384 个桶里取调和平均；只记最大值，所以不能列出元素、不能删除，只能估数。
- **追问 · 实时 UV 要合并多天？** `PFMERGE` 把多个 HyperLogLog 合并，不会重复计数。
- **追问 · 消息队列能用 Redis 吗？** List（`BRPOPLPUSH`）简单但没有消费确认；Pub/Sub 不持久化，订阅者离线就丢；Stream（5.0+）有消费组（consumer group）、`XACK` 和待确认列表（PEL），可以做轻量队列，规模大了还是用 Kafka，见 [[tiktok-message-queues]]。

## 延伸阅读

- Redis 官方文档：分布式锁 <https://redis.io/docs/latest/develop/use/patterns/distributed-locks/>
- Martin Kleppmann：How to do distributed locking <https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>
- 相关：[[tiktok-cache-problems]] · [[tiktok-idempotency-transactions]] · [[tiktok-fundamentals]]
