---
slug: hotel-booking-system
kind: system-design
---

## Q
**酒店预订系统（Expedia 型聚合与自营）**｜系统设计

设计一个酒店预订系统：用户按城市、日期、人数搜索酒店，查看各房型每晚价格，下单预订，管理和取消订单。面试官通常把重点压在数据建模和 SQL 上：房态（availability）、按日定价、预订三张表怎么设计，怎样一条查询找出某日期范围内有房的酒店，怎样避免超卖。典型规模：1 亿日活用户，10 万家酒店，每家约 1000 间房，每天约 100 万笔预订。常见变体：房源和支付是外部服务，预订与支付可能不可用，要允许异步重试；酒店房态由外部系统每 30 分钟导出一次数据转储，或通过 webhook 与 API 推送，数据变更要在 15 分钟内反映，所以搜索可能看到过期房源；酒店需要审批预订并通过回调通知；预订保留（TTL）；高峰突发；预订过程中某个组件宕机怎么恢复；会议室预订的缩小版。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这是一个"读极多、写极少、但写必须绝对不超卖"的系统：搜索走可以略微过期的预聚合索引，下单才对"房型 × 每个晚上"的库存行做原子扣减；而房态必须按房型和日期聚合存储，而不是一个房间一行，否则 1000 间房 × 365 天 × 10 万家酒店会产生 365 亿行。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–5 分 | 要求和数字：读多写少，不能超卖 |
| 5–10 分 | 实体（房型 × 日期的库存行）和接口 |
| 10–25 分 | 整体设计：搜索路径、下单路径、核心下单事务 |
| 25–50 分 | 深入：库存建模、防超卖、保留与支付 |
| 50–60 分 | 追问：热点、状态机与发件箱、外部同步、审批 |

**需求。**
- 功能：
  1. 搜索：城市或地图范围、入住与退房日期、人数，返回有房的酒店及最低价，支持筛选与排序。
  2. 查看酒店详情与各房型每晚价格。
  3. 预订：选房型下单，支付，得到确认；可取消并按政策退款。
  4. 酒店侧（或外部供应商）同步房态与价格；可选的酒店审批。
- 非功能：
  - 读写比：1 亿日活，每人约 5 次搜索，平均约 5800 次每秒，峰值按 5 倍约 3 万次每秒；预订 100 万笔每天，平均约 12 笔每秒，峰值百级。写入量很低，难点在于不超卖和读扩展。
  - 数据新鲜度：外部变更 15 分钟内反映到搜索；下单时必须用实时库存核验。
  - 一致性：库存扣减强一致；搜索结果最终一致。
  - 容量：房型级库存约 10 万家 × 20 个房型 × 365 天 = 7.3 亿行，每行约 50 字节，共约 36 GB，单库难以承载写入高峰但可以轻松分片；若按单间房存则 365 亿行，不可行。
  - 可用性：下单链路在支付或供应商不可用时不丢单、不超卖、不重复扣款。

**核心实体与接口。**
- 实体：
  - 酒店（Hotel）：位置、设施、评分、时区。房型（RoomType）：酒店下的类型、容量、总间数。
  - 库存（Inventory）：主键 `(hotel_id, room_type_id, date)`，字段 `total`、`reserved`（含未过期的保留），`price`、`version`。这是预订的核心表。
  - 预订（Reservation）：reservation_id、user_id、hotel_id、room_type_id、入住与退房日期、状态（HELD、PENDING_SUPPLIER、CONFIRMED、CANCELLED、EXPIRED）、保留到期时间、支付引用、幂等键、总价快照。
  - 酒店的"每个房间一行"的 Room 表只在需要分配具体房号（会议室、分房）时使用。
- 接口：
  - `GET /search?city=&checkin=&checkout=&guests=&cursor=` 返回酒店摘要及最低价。
  - `GET /hotels/{id}/availability?checkin=&checkout=` 返回各房型可订数与总价。
  - `POST /reservations`（带幂等键）创建保留，返回 reservation_id 与到期时间。
  - `POST /reservations/{id}/confirm`（携带支付凭证）、`DELETE /reservations/{id}` 取消。
  - 供应商回调：`POST /webhooks/inventory`、`POST /webhooks/reservations`。

**整体设计。**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="88" y1="36" x2="88" y2="53"/>
<line x1="252" y1="36" x2="252" y2="53"/>
<line x1="170" y1="86" x2="170" y2="103"/>
<line x1="170" y1="136" x2="170" y2="153"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="8" width="153" height="28" rx="3"/>
<rect x="175" y="8" width="153" height="28" rx="3"/>
<rect x="12" y="58" width="153" height="28" rx="3"/>
<rect x="175" y="58" width="153" height="28" rx="3"/>
<rect x="12" y="108" width="316" height="28" rx="3"/>
<rect x="12" y="158" width="316" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="88,58 86,52 92,52"/>
<polygon points="252,58 248,52 254,52"/>
<polygon points="170,108 167,102 173,102"/>
<polygon points="170,158 167,152 173,152"/>
</g>
<g fill="currentColor">
<text x="88" y="26" font-size="12">搜索 API</text>
<text x="252" y="26" font-size="12">预订 API</text>
<text x="88" y="76" font-size="12">ES 候选 + 摘要缓存</text>
<text x="252" y="76" font-size="12">库存分片库(强一致)</text>
<text x="170" y="126" font-size="12">供应商 webhook / API / 转储</text>
<text x="170" y="176" font-size="12">Kafka 规范化 -> 库存与价格</text>
</g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="202" font-size="11">搜索读预聚合, 下单扣减库存行</text></g>
<g style="fill:var(--dim,#6b7280)"><text x="170" y="218" font-size="11">库存变更事件异步刷新搜索摘要</text></g>
</g></svg>
```
1. 搜索路径（读）：地理与静态条件（城市、设施、评分）走搜索引擎（Elasticsearch）得到几百个候选酒店；再对这些候选酒店批量查询"日期范围内的可订性与最低价"，来源是一张预聚合的 `availability_summary(hotel_id, date, min_price, rooms_left)` 表，放 Redis 或只读副本；过滤、排序后返回。静态索引变化慢，动态摘要由库存变更事件异步刷新，所以搜索允许最多几十秒到分钟的过期。
2. 下单路径（写）：对房型库存行做原子扣减，创建 HELD 状态的预订并设置保留到期时间（例如 10 分钟）；用户支付成功后转为 CONFIRMED；支付失败或超时，由清理任务把库存释放。
3. 外部同步：供应商的 webhook 与 API 推送先写入 Kafka，规范化服务解析后用"来源时间戳更晚才覆盖"的规则更新库存与价格（旧事件被丢弃，防止乱序），再产生事件刷新搜索摘要。30 分钟一次的数据转储用差异导入：与上次对比，只更新变化的行。
4. 数据库按 hotel_id 分片：同一酒店的所有库存与预订在同一分片，下单事务不跨分片。

核心下单事务如下，两种写法都要能讲清楚：

```sql
-- 悲观写法：按日期升序加锁，避免两个事务按不同顺序加锁造成死锁
BEGIN;
SELECT date, total - reserved AS remaining
FROM inventory
WHERE hotel_id = :h AND room_type_id = :t AND date >= :checkin AND date < :checkout
ORDER BY date
FOR UPDATE;
-- 应用层检查每一行 remaining >= 1，否则 ROLLBACK 返回"已售罄"
UPDATE inventory SET reserved = reserved + 1
WHERE hotel_id = :h AND room_type_id = :t AND date >= :checkin AND date < :checkout;
INSERT INTO reservation (...) VALUES (...);
COMMIT;

-- 乐观写法：带条件的单条更新，影响行数必须等于晚数
UPDATE inventory SET reserved = reserved + 1, version = version + 1
WHERE hotel_id = :h AND room_type_id = :t
  AND date >= :checkin AND date < :checkout AND reserved < total;
-- affected_rows < 晚数 则 ROLLBACK
```

**深入。**
1. 【必讲】房态怎么建模：为什么是"房型 × 日期"的计数。
   - 每个房间每天一行：365 亿行，且"某房型是否有房"要对大量行聚合。
   - 只存预订表，查询时用日期区间重叠计算占用：每次搜索都要扫预订表，正是"预订表被查爆"的场景。
   - 房型 × 日期计数行（选用）：下单是对 N 行（N 为晚数）加一，查询是对 N 行比较，行数 7.3 亿级可分片。代价是无法记录具体房号，需要房号时在入住前再分配，或另设 Room 表对少量场景使用区间排他约束（PostgreSQL 的 `EXCLUDE USING gist (room_id WITH =, daterange WITH &&)`）。
2. 【必讲】防止超卖：正确性靠数据库的行级条件更新或行锁（整体设计里的两种写法），不要靠先查后写的应用逻辑。
3. 【必讲】保留（TTL）与支付的两阶段。
   - 先保留库存、后支付，保留有 10 分钟期限，到期未支付就释放，防止库存被占而不成交。
   - 清理：定时任务每 30 秒扫描 `HELD` 且 `hold_expires_at < now()` 的预订，状态改 EXPIRED 并把对应库存减一，整个动作在一个事务内；支付回调迟到时，如果预订已过期，则重新尝试扣减，成功则确认，失败则退款。
   - 支付采用预授权加扣款：下单时预授权，确认成功后再扣款，失败则撤销授权，避免"钱扣了房没订上"。
4. 【追问再讲】热点：一个热门酒店在活动日被大量抢订，所有请求集中到少数几行。可用的缓解：事务尽量短（支付放在事务之外）；单行更新每秒数百次是上限，更高就在入口排队（虚拟等候室）而不是让数据库锁等待堆积；也可把热门房型的库存拆成多个计数器子行，扣减时随机挑一个有余量的，读时求和。
5. **【追问再讲】外部依赖恢复用状态机：** 外部依赖不可用时的恢复（分布式事务用状态机，不用两阶段提交）。
   - 状态机：HELD → PAID → PENDING_SUPPLIER → CONFIRMED。每一步在本地事务内改状态，并写一条待发送消息到发件箱表（outbox），由中继进程投递，保证"状态变更与调用外部服务"不会只成功一半。
   - 调用供应商用预订 ID 作幂等键；超时不要立即判失败，进入重试队列，用户看到"确认中"，几秒到几分钟后收到结果。
   - 补偿：供应商最终拒绝时，释放库存并退款；对账任务定期比对本地状态与供应商状态，修复不一致。
6. 【追问再讲】数据过期与最终核验。
   - 搜索结果带 `as_of` 时间；用户点进酒店详情和下单时，再向实时库存（或供应商）核验一次价格和可订性，价格变化要明确提示用户。
   - 15 分钟新鲜度承诺：对大型供应商以推送为主，拉取为兜底，按供应商优先级决定轮询频率；监控每个供应商的数据延迟。
7. 【加分】酒店审批型预订：预订进入 PENDING_SUPPLIER，保留库存并设置较长期限；酒店通过 webhook 确认或拒绝，超时自动取消；取消的 webhook 事件带事件 ID，幂等处理后把库存加回。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 为什么搜索不直接查库存表：每次搜索要跨几百家酒店、每家几十个房型、多个晚上，写库承受不了 3 万次每秒；预聚合牺牲几十秒新鲜度，换读的两个数量级降幅。
- 同一用户重复点击下单：幂等键，唯一约束 `(user_id, 幂等键)`。
- 取消与退款政策：预订上存价格与政策快照，取消按政策算退款，释放库存。
- 超额预订（overbooking）：酒店业有主动超订的做法，可在库存里加一个超订比例，`reserved < total * (1 + ratio)`，作为产品配置而不是事务逻辑的改变。
- 多币种、含税价格：价格表存基础价，税费和币种在展示层计算，预订保存当时的总价快照。
- 会议室预订的缩小版：房间数少，直接对 Room 表使用区间排他约束，开始结束时间重叠即冲突，省去计数行。

**级别期望。**
- 中级：酒店、房型、预订三类实体，查询空房的 SQL，用事务防止同一房间被订两次。
- 高级：房型 × 日期的库存建模、预聚合搜索、乐观或悲观扣减、保留与支付的两阶段、分片键为酒店 ID。
- 资深（staff）：外部供应商同步与过期数据处理、状态机加发件箱的恢复策略、热点酒店的排队、对账、监控供应商数据延迟，并能解释每个一致性取舍。

**先修概念。** [[hi-system-design-core-concepts-data-modeling|数据建模]]、[[hi-system-design-core-concepts-sharding|分片（Sharding）]]、[[hi-system-design-core-concepts-caching|缓存]]、[[hi-system-design-deep-dives-elasticsearch|Elasticsearch]]、[[hi-system-design-patterns-dealing-with-contention|处理争用（Contention）]]、[[hi-system-design-deep-dives-postgres|PostgreSQL]]

**同类题。** [[solution-hotel-reservation]]（本库完整题解）、[[solution-ticket-booking]]、[[hi-system-design-problem-breakdowns-ticketmaster|票务预订（Ticketmaster）]]、[[solution-hotel-booking]]（低层设计版）
