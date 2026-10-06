# sd01 · 参考答案

> 数字由 `python3 -c` 计算（见 REPORT 行）；口播用量级。

## 1. 先算（2 min）

| 量 | 今天（2k ev/s） | 目标（50k ev/s） |
|---|---|---|
| 入口带宽（1 KB/事件） | 2 MB/s | **50 MB/s** |
| 事件/天 | 1.73 亿 | **43.2 亿** |
| 原始数据/天 | 0.17 TB | **4.32 TB** |
| Kafka 7 天保留（×3 副本） | — | 30 TB（×3 = 91 TB） |
| history 查询（每事件 1 次） | 2k QPS | **5 万 QPS** |
| 告警（假设 0.1% 事件命中） | 2/s | 50/s ≈ 432 万/天（去重 10× 后 ≈ 43 万/天） |
| 最大租户（40%） | — | **2 万 ev/s 进同一个 partition**（按 tenant_id 分区） |

> "At 50k events a second the raw event stream is 4.3 terabytes a day. Postgres is doing three jobs it can't do at that rate: storing raw events, answering a history lookup per event, and counting windows for brute force."

## 2. 现状哪里先坏（按顺序）

1. **Postgres 主库**：每事件 1 次 INSERT 事件 + 1 次 history SELECT + brute_force 的窗口 `count(*)` → 写 5 万/s + 读 5 万/s 以上（history 每事件一次，再加登录事件的窗口 count），单主库撑不住；告警 API 和管线抢同一个主库，所以 API p99 已经 2 s。
2. **热分区**：key = tenant_id，大租户 2 万 ev/s 全部进一个 partition → 一个 consumer 处理，无论加多少 pod 都没用（consumer 数 ≤ partition 数，且热分区只能一个 consumer）。
3. **每事件两次同步 HTTP**（geoip-svc、intel-svc）：延迟叠加 + 下游限流（→ 与 `ic01` 是同一类事故）。
4. **API**：`OFFSET n` 分页越翻越慢；`ORDER BY score` 若无匹配索引是 filesort。

## 3. 写路径

- 原始事件**离开 OLTP**：Kafka → (a) 对象存储（Parquet，按 `tenant/date/hour` 分区，批量 128 MB 文件，冷数据一年）(b) OpenSearch（30 天热，ILM 滚动，按租户路由）。Postgres 只存**告警、抑制规则、配置**等有界数据。
- **告警幂等写**：告警 id = hash(tenant, rule set, 去重键, 时间桶)，`INSERT … ON CONFLICT DO UPDATE SET event_count = event_count + 1, last_seen = …`。at-least-once 消费 + 幂等写 = 效果上 exactly-once。
- Kafka 分区：按 `hash(tenant_id, user)`；分区数按"峰值 / 单 consumer 吞吐 × 2–3 倍余量"：若单 consumer 2k ev/s，50k 需要 25 个，开 64 个分区留余量（分区数难以下调，宁多勿少）。

## 4. 状态与 enrichment（真正的大头）

- **键控状态**：同一 (tenant, user) 的事件进同一 partition → 同一 consumer，有序。brute_force 的 10 分钟窗口、history（见过的国家/IP/设备）放在 consumer 本地状态（内存 + 定期快照到 S3/RocksDB，或按 key 分片的 Redis），**不再每事件查库**。重启时从快照 + Kafka offset 回放恢复。
- geo-ip：进程内 mmdb 文件（每周更新），纳秒级、零网络。威胁情报：进程内集合 / bloom filter，每分钟从 intel-svc 拉增量。
- 结果：管线对外部系统的每事件调用从 3 次（2 HTTP + 1 DB）降到 0，只剩 Kafka 读与批量写出。

## 5. 读路径（分析师 API）

- 告警表索引 `(tenant_id, status, score DESC, id)`；score 写时计算（ranking 的时间衰减可以用"写时基础分 + 读时按 created_at 的简单衰减"，或者定时重算 OPEN 告警）。
- keyset 分页：`WHERE (score, id) < (?, ?) ORDER BY score DESC, id DESC LIMIT 50`。
- API 走只读副本（允许秒级延迟），写走主库；告警详情里的原始事件从 OpenSearch 取。
- 列表计数（"312 open"）缓存 30 s。

## 6. 极限与下一个瓶颈（"beyond add more workers"）

- 热 key：大租户里一个服务账号可能单 key 就上千 ev/s → 对该 key 先预聚合（每秒合并同类失败登录）再进规则；或对高频 key 拆子分区并在规则侧合并。
- OpenSearch 写入速率与分片数；S3 小文件 → 批量与 compaction。
- noisy neighbor：按租户的入口配额与独立 consumer group（大租户单独 topic）。
- 告警风暴：去重 + 每租户告警速率上限，超出转成聚合告警。

## 7. 失败场景

consumer 崩溃（回放，幂等写兜底）· 状态快照损坏（从更早快照 + 更长回放重建）· 下游 OpenSearch 慢（与告警路径解耦：告警路径不依赖搜索写入）· 毒消息（DLQ + 计数告警）· 重新分区（新 topic 双写，消费者切换，状态迁移按 key 重建）。观测：每 partition lag、最老消息年龄、端到端延迟（事件时间 → 告警时间）p99 SLO。

## 8. 迁移顺序（怎么不停机地走过去）

1. 先止痛：API 索引 + keyset 分页 + 只读副本（几天）。2. geo-ip/intel 进程内化。3. 新 topic `events.v2` 按 (tenant,user) 分区，双写；新管线影子运行，对比告警差异。4. 原始事件写对象存储 + OpenSearch，停止写 Postgres events 表。5. 大租户切流。
