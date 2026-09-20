---
nodes: [problems.commerce.hotel-reservation]
tags: [solution]
---
# 设计题解：酒店与民宿预订系统（Hotel & Marketplace Reservation，Airbnb / 连锁酒店）

## 题目与范围

面试官通常这样开场："设计一个像 Airbnb 或连锁酒店官网一样的预订系统：用户搜索某个目的地、
某段日期、若干房客，看到可订的房源和价格；选定一个房型后提交一段连续日期的预订，系统要保
证同一间房不会被卖给两个人。" 这句话表面上和「Ticket Booking」很像，但驱动这道题的核心难
点完全不同：库存的最小单位不是"一个座位"，而是**一个房型在某一晚的可售数量**，一次预订不
是买一个位置，而是**同时锁定一段连续的多个夜晚**——这段区间必须作为一个整体成功或整体失
败，任何一晚不可用都会让整笔预订失败。相邻的题目「Ticket Booking」已经把"单点资源的原子占
用"讲透（座位状态机、条件更新、虚拟队列），本题不重复那部分，而是聚焦"区间"这个维度本身带
来的新问题（详见 [[solution-ticket-booking]]）。

值得当场问清楚的澄清问题，以及它们各自改变的设计决策：

- **即时预订（instant book）还是房东确认制（request-to-book）？** 即时预订要求预订路径在
  提交的那一刻就完成强一致的库存扣减；确认制允许先"占位"几小时等房东回复，占位期间库存处
  于一个中间状态。本题按即时预订设计，因为这是 Airbnb 和几乎所有连锁酒店直销渠道的主流形
  态，也是这道题真正的并发难点所在；确认制只是把「深入探讨」第 5 节的"保留有效期"从几分钟
  换成几小时，机制不变。
- **是否允许超售（overbooking）？** 决定「深入探讨」第 3 节要不要做，以及库存表的"总量"字
  段是物理房间数还是一个可配置的商业参数。本题假设平台允许房源方开启超售，因为这是酒店业
  几十年的真实定价策略（对比强行"零超售"的电影院/演唱会座位）。
- **房源是自营连锁酒店的标准化房型，还是像 Airbnb 一样每个房源独一无二？** 决定搜索索引里
  "同类可替代房型聚合"这一层要不要做。本题两者都覆盖：连锁酒店的"每晚 N 间大床房"和民宿房
  东的"这一套房子"在数据模型上是同一种东西——都是"某个可售单元在某一晚的库存数量"，差别只
  在 N 是几十还是 1。
- **要不要处理和外部第三方 OTA 渠道的库存同步？** 决定「深入探讨」第 6 节要不要做，以及"谁
  是库存的唯一真相来源"这个问题怎么回答。本题假设房源方常年在本平台之外的至少一个外部渠道
  （自建官网、其他 OTA）同时售卖同一批房间，必须处理跨渠道的库存同步，这是本题和大多数单一
  平台内部售卖的题目（比如电影票）最本质的区别之一。
- **取消、退款、修改预订在不在范围内？** 不在——本题只设计"预订创建"这条主链路，取消/改期
  只在容量估算里作为"归还库存"的一个事件类型提及，不展开状态机。

**范围内**：房源与房型浏览、按日期区间的搜索与可用性/价格查询、多晚预订的原子提交与支付、
超售策略、库存与外部渠道的双向同步。**范围外**：动态定价算法本身（只把价格当作库存表里的
一个字段，不设计定价模型）、支付网关内部实现（复用一次性扣款、幂等键这类通用结论，见
[[solution-ticket-booking]]，不重新设计 PSP）、取消/改期/退款状态机、房源审核与信任安全、
消息/评价系统、真正的座位级/房间级资产管理（保洁排班、维修阻断，这属于房源方后台系统）。

## 需求

**功能需求（驱动设计的 3–5 条）**

1. 用户按地点、日期区间（入住/离店）、房客数搜索，看到候选房源/房型列表及各自的价格和"是
   否可订"状态。
2. 用户对一个房型提交一段连续日期（如 3 晚）的预订请求，系统必须保证这段区间内**每一晚**
   都有可用库存，整段要么全部预订成功，要么整体失败——不存在"订到一半"的状态。
3. 同一个房型同一晚的已售数量任何时刻都不超过（总量 ×（1 + 超售系数）），超售系数由房源方
   按自己的历史 no-show/取消率配置，默认 0。
4. 预订确认后系统与支付完成一次幂等编排，重复提交或支付回调重复到达都不会产生重复订单或
   重复扣款。
5. 房源方对同一批物理房间在外部渠道（自建官网、其他 OTA）也在售卖时，任何一个渠道确认一
   笔预订，其余渠道（包括本平台）必须在有限延迟内感知库存变化，防止跨渠道超售。

**非功能需求（数字化）**

- **搜索延迟**：`GET /search` P99 < 300ms——这是用户翻页浏览、调整日期反复触发的交互，容
  忍轻微过时换取速度。
- **预订延迟**：`POST /bookings` P99 < 500ms（比搜索宽松，因为这条路径要做真实库存的强一
  致校验和支付发起，用户对"提交订单"的等待容忍度也更高）。
- **一致性分层**：搜索路径最终一致，新鲜度目标 P99 < 1 分钟（库存变化到搜索结果反映之间的
  延迟）；预订路径对库存表的读写必须强一致，绝不允许两笔并发预订让同一晚超过策略允许的上
  限。
- **可用性分层**：搜索路径 99.95% 可用；预订路径宁可短暂返回"该日期已满"（409）也不能牺牲
  正确性。
- **跨渠道同步延迟**：外部渠道确认一笔预订到本平台库存扣减生效，目标 P99 < 2 分钟——这个数
  字直接来自"两个渠道各自独立向外发起预订请求"这个业务现实，不可能做到毫秒级强一致（后文
  「深入探讨」第 6 节展开）。
- **超售风险预算**：房源方可接受的"实际到店人数超过物理容量"的概率上限，默认 ≤1%（不是
  0%——这是本设计与「Ticket Booking」在正确性目标上最根本的不同：那道题"绝不超卖"是不可
  妥协的硬约束，这道题的"不超卖"是一个可配置的风险预算，见「深入探讨」第 3 节）。

## 容量估算

估算的核心是两层放大：**房型数如何从房源数放大**，以及**一年的可订窗口如何把"库存表的行
数"再放大一个数量级**——这两层放大直接决定了库存表该用哪种数据模型（见「深入探讨」第 1
节）。

**场景假设**：平台上有 600 万个活跃房源（`listings = 6,000,000`），连锁酒店房源平均每个
房源卖多种房型（大床房/双床房/套房等），民宿房源通常只有一种"房型"（房子本身），两者混合
后平均每个房源 1.5 个可售房型（`avg_room_types_per_listing = 1.5`）。

- **房型数**：`6,000,000 × 1.5 = 9,000,000` 个房型。
- **可订窗口**：房源方通常把未来 365 天的日历打开供预订（`booking_window_days = 365`）。
- **库存行数（按房型-夜计数模型）**：`9,000,000 × 365 = 3,285,000,000` 行——这是这道题里
  真正的大数字，也是「深入探讨」第 1 节要讨论"这个模型是否还合理"的直接原因。
- **存储量**：每行约 40 字节（`room_type_id` 8B + `date` 4B + `total_units` 2B +
  `booked_units` 2B + `overbook_pct` 2B + `price_cents` 4B + 索引与对齐开销约 18B），
  `3,285,000,000 × 40 ≈ 131.4GB`。这个体量对一个分片良好的关系型集群完全在可承受范围内
  ——**存储不是这道题的瓶颈，正确性和一致性才是**，这个对比值得在面试里主动说出来（呼应
  「Ticket Booking」的同一个论点）。
- **预订写 QPS**：假设平台日均 100 万笔预订（`bookings_per_day = 1,000,000`），
  平均 QPS = `1,000,000 / 86,400 ≈ 11.57`。相比「Ticket Booking」的场景，酒店预订的峰值
  远没有那么陡峭——需求分散在全球几百万个房型上，不存在"同一秒钟一百万人抢同一批座位"的
  单点热点，假设峰谷比 5×（全球时区错峰后仍有晚间预订高峰），**峰值 QPS ≈
  `11.57 × 5 ≈ 57.87`**。这个量级一台托管关系型数据库实例轻松承受，说明这道题的难点根本
  不在"扛峰值"，而在"跨多行的原子性"（见「深入探讨」第 2 节）。
- **搜索读 QPS**：假设搜索会话到最终成交的转化率 2%（`conversion_rate = 0.02`，行业典型
  的"多次比价、少数下单"漏斗），则日搜索会话数 = `1,000,000 / 0.02 = 50,000,000`，平均搜
  索 QPS = `50,000,000 / 86,400 ≈ 578.70`；搜索峰谷比通常比预订更平——旅行调研全天都在发
  生，假设峰谷比 3×，**峰值搜索 QPS ≈ `578.70 × 3 ≈ 1,736.11`**。
- **读写比**：`578.70 / 11.57 ≈ 50:1`——不像「Ticket Booking」开票瞬间能冲到 700:1，但
  50:1 已经足够说明搜索必须走独立于预订库存表的只读路径，任何方案如果让搜索直接查询预订
  写库都会在峰值把预订路径拖垮（见「深入探讨」第 4 节）。
- **年预订量与订单存储**：`1,000,000 × 365 = 365,000,000` 笔/年，每条订单记录（含房客信
  息引用、入离日期、金额、支付引用、幂等键）约 300 字节，`365,000,000 × 300 ≈ 109.5GB`/
  年——同样不是瓶颈。
- **哪个估算改变哪个设计决策**：库存行数（32.85 亿）决定了库存表必须按房型或地理分片，且
  不能给每一晚建一个独立索引结构；读写比（50:1）决定了搜索必须走反规范化索引和缓存，绝不
  能共享预订写库的连接池；峰谷比的量级差异（预订 5× vs 「Ticket Booking」的数百倍）决定了
  这道题**不需要**虚拟排队厅这类削峰机制，这是两道题在架构选择上最直接的分野。

## 核心实体与 API

**实体**

- **Property**：`id, name, geo, ownerType(hotelChain/individualHost)`。
- **RoomType**：`id, propertyId, name, maxGuests, basePrice`——面向连锁酒店是标准化房型，
  面向民宿房东退化成"这套房子本身"，数据模型不区分。
- **NightlyInventory**：`roomTypeId, date, totalUnits, bookedUnits, overbookPct,
  priceCents`——**一行代表一个房型在一个具体夜晚的库存**，是本设计最核心的建模决定（对比
  见深入探讨第 1 节）。`totalUnits` 为 1 时就退化成「Ticket Booking」的单座位模型。
- **Booking**：`id, guestId, roomTypeId, checkIn, checkOut, guests, amount, status
  (pending/confirmed/cancelled), paymentIntentId, idempotencyKey, channel`。
- **ChannelSyncEvent**：`propertyId, channel, eventType(bookingCreated/inventoryUpdated),
  externalRef, receivedAt, appliedAt`——外部渠道的库存变更事件，供「深入探讨」第 6 节的对
  账逻辑使用。

**API**

```
GET  /search?geo=..&checkIn=..&checkOut=..&guests=..     反规范化索引，弱一致，缓存友好
GET  /room-types/{id}/availability?checkIn=..&checkOut=.. 权威查询，读 NightlyInventory 本身
POST /bookings                                            {roomTypeId, checkIn, checkOut,
                                                            guests, paymentMethodToken,
                                                            clientRequestId}
                                                           按 clientRequestId 幂等
                                                           → {bookingId, status} 或 409
GET  /bookings/{id}                                       轮询订单状态
PUT  /room-types/{id}/inventory                           房源方设置某段日期的 totalUnits/
                                                            price/overbookPct，触发 CDC
POST /channels/{channel}/webhook                          外部渠道推送"它那边刚确认了一笔预
                                                            订"，触发库存扣减与对账
POST /webhooks/payment                                    PSP 异步回调，按事件 id 去重
```

**幂等性**：`POST /bookings` 用 `clientRequestId` 做幂等键，语义和 [[solution-ticket-booking]]
中 `POST /orders` 完全一致——重复提交只返回同一笔订单，不产生二次扣款；这部分结
论直接复用，不在本题重新论证。本题新增的是 `POST /channels/{channel}/webhook` 的幂等性：
外部渠道可能因为自己的重试机制重复推送同一个 `externalRef`，`ChannelSyncEvent` 表按
`(channel, externalRef)` 加唯一约束防止同一笔外部预订被应用两次。

**故意不做的**：一次 `POST /bookings` 只能预订一个房型的一段连续日期，不支持"跨房型拼单"
或"跨房源购物车"原子提交（需要客户端发起多次独立请求，各自承担各自的失败/重试，不做分布
式事务，因为收益配不上代价）；不提供"部分入住"（比如 5 晚订单里只确认其中 3 晚）；库存的
"总量"字段只能由房源方或渠道同步写入，预订路径永远只减不加（减法只在预订创建时发生，加法
——归还库存——只在取消流程里发生，取消状态机不在本题范围）。

## 高层设计

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Search Service (Index + Cache)
    participant B as Booking Service
    participant IDB as Inventory DB (relational, sharded by room_type)
    participant P as Payment (PSP)
    participant CDC as CDC Pipeline
    participant CH as Channel Sync Service
    C->>S: GET /search?geo&checkIn&checkOut
    S-->>C: 候选房型 + 价格（来自反规范化索引，弱一致）
    C->>B: POST /bookings {roomTypeId, checkIn, checkOut}
    B->>IDB: 事务: UPDATE nightly_inventory SET booked_units=booked_units+1
             WHERE room_type_id=.. AND date IN (checkIn..checkOut-1)
             AND booked_units < total_units*(1+overbook_pct)
    IDB-->>B: 影响行数 = 晚数 (全部成功) 或 < 晚数 (部分失败 → 应用层 ROLLBACK)
    B->>P: 创建 PaymentIntent 并扣款
    P-->>B: webhook 异步确认
    B->>IDB: 事务: booking pending→confirmed（以 clientRequestId 幂等）
    B-->>C: 订单确认
    IDB->>CDC: 变更日志（binlog/WAL）
    CDC->>S: 异步更新反规范化索引
    CH->>IDB: 外部渠道 webhook 到达 → 按同样的多行条件更新扣减库存
    IDB->>CH: 冲突时返回 409，进入对账队列（见深入探讨第 6 节）
```

**搜索路径**：`GET /search` 只读反规范化索引（如 Elasticsearch/OpenSearch 或等价的搜索
引擎），索引文档按房型聚合了地理位置、未来一段时间的价格区间和一个粗粒度的"大致可订"标
记，由 CDC 管道异步从 Inventory DB 同步（延迟目标 P99 < 1 分钟）。存储技术类是**倒排索引
+ 只读缓存**，选它是因为读写比高达 50:1，任何让搜索直接命中 Inventory DB 的方案都会在预
订路径最需要低延迟的时刻被搜索流量拖慢。

**权威可用性查询**：用户点开一个具体房型详情页时，`GET /room-types/{id}/availability` 绕
过索引，直接读 `NightlyInventory`（同一批数据，但走 Inventory DB 的只读副本），拿到当前
真正准确的价格和逐晚可订状态——这是「深入探讨」第 4 节里"候选生成"和"精确定价"两阶段分离
的第二阶段。

**预订路径**：Booking Service 对 Inventory DB 发起一次多行条件更新事务，Inventory DB 是
**单主关系型数据库，按 `room_type_id` 分片**（分片键选房型而不是房源，因为查询和更新的
粒度天然是"这一个房型的这几晚"，不需要跨房型的多分片事务）。选关系型数据库是因为这条路径
需要"同一段日期区间内每一行都满足容量约束才整体生效"的原子性保证，这正是关系型数据库单个
事务天然提供的能力（参见 [[distributed.transactions.isolation|Isolation Levels &
Anomalies]]，具体机制见「深入探讨」第 2 节）。

**渠道同步路径**：Channel Sync Service 是一个独立的适配层，把外部渠道的 webhook/轮询结
果翻译成对同一个 Inventory DB 的写入（和本平台内部预订走同一条"多行条件更新"逻辑，Inventory DB 不知道、也不需要知道这次扣减来自哪个渠道），失败（比如渠道已经把库存卖给了另一个人，
本地条件更新失败）进入对账队列，见「深入探讨」第 6 节。

## 深入探讨

### 库存数据模型：按房型-夜计数行，还是区间行

**问题**：容量估算给出了 32.85 亿这个数字——按房型-夜存一行，一年的库存表就有几十亿行。
这个模型是不是从一开始就选错了？有没有更紧凑的替代方案？

**方案一：区间行 + 排他约束（exclusion constraint）**，即 [[solution-ticket-booking]] 座
位模型的直接推广：每个物理房间实例一行，字段包含 `during`（一个 `daterange`），用
PostgreSQL 的 `EXCLUDE USING GIST (room_instance_id WITH =, during WITH &&)` 保证同一个
房间实例不会有两段重叠的预订区间（这正是 PostgreSQL 官方文档 `rangetypes` 一章给出的教
科书级预订表例子，见「来源与延伸」）。这个方案的行数只随"实际发生的预订"增长，而不是随
"日历天数 × 房型数"增长，长期看远比按夜计数紧凑；对精品酒店或需要把具体房间号分给具体客
人（对接保洁排班、房型升级）的场景非常合适。但它的前提是**每个可售单元必须有一个持久的物
理/虚拟身份**——一旦一个房型下有 50 个完全可互换的单元（"随便哪间大床房都行"），排他约束
只能保证"单个房间实例不重叠"，不能表达"50 个房间里最多同时卖 50 份"这种池化容量语义，除
非退化成建 50 个排他约束实例分别维护，牺牲了池化带来的装箱效率（见后文数字）。

**方案二（本设计采用）：按房型-夜计数行**。每行是 `(room_type_id, date)` 加一个计数器
`total_units/booked_units`，不关心具体是哪个物理单元被订走，退房后再入住的客人也不需要
和上一位客人对应同一个"房间实例"。代价正是容量估算算出的行数——但把这行数换算成存储只有
131.4GB，对一个分片良好的关系型集群完全不是问题；真正的收益是**装箱效率**：50 个可互换单
元可以被任意组合的客人订满，不会出现"房间 A 空着但客人只能订到房间 B（已满）"这种因为过早
绑定物理身份而产生的虚假满房。这正是大多数 OTA 和连锁酒店直销系统实际选择的模型——多数客
人根本不关心自己入住哪个具体房间号，酒店前台在客人抵达时才做物理分配。

**结论**：默认用方案二（池化计数），只有当房源方明确需要"预订时就锁定具体房间号"（常见于
精品酒店、按房型升级收费、或维修/清洁阻断需要精确到某一间房）时，才在该房源上叠加方案一
的排他约束表——两个模型可以在同一个系统里按房源类型共存，`NightlyInventory` 的
`total_units` 本身也可以理解成"这个房型当前有多少个房间实例还没被方案一的排他约束表占
用"，两层可以对账但不需要合并成一张表。

### 多晚预订的原子性：为什么"先查后插"在读已提交下会双订

**问题**：一次预订要锁定 N 个夜晚（`NightlyInventory` 的 N 行），这 N 行的扣减必须整体成
功或整体失败。最直觉的实现是"先 `SELECT` 这 N 晚的剩余库存，应用层判断都 ≥1，再逐行
`UPDATE` 扣减"——这个写法哪里错了？

**方案一（错误但常见）：先查后写（check-then-write）**。伪代码：
```sql
SELECT date, total_units - booked_units AS remaining
FROM nightly_inventory
WHERE room_type_id = :rt AND date BETWEEN :checkin AND :checkout - 1;
-- 应用层判断每晚 remaining >= 1
UPDATE nightly_inventory SET booked_units = booked_units + 1
WHERE room_type_id = :rt AND date IN (:dates);
```
在读已提交（read committed）隔离级别下，`SELECT` 和后续 `UPDATE` 之间没有任何锁把这段"决
策窗口"保护起来：两个并发事务可以都读到某一晚 `remaining = 1`，都在应用层判断"可以订"，
然后都执行 `UPDATE`——这正是「Isolation Levels & Anomalies」（参见
[[distributed.transactions.isolation|Isolation Levels & Anomalies]]）里的经典写偏斜
（write skew）异常：两个事务基于同一份快照独立做出决策，各自的写不冲突（都是"把这一行的
`booked_units` 加一"），但合并后共同违反了"不超过容量"这个不变量。这不是"该用可串行化"的
借口——即便升到可串行化，`SELECT` 之后要等两阶段判断，代价也远高于方案二。

**方案二（本设计采用）：单条多行条件更新**。把"检查剩余库存"直接写进 `UPDATE` 的
`WHERE` 子句，让数据库在同一条语句里原子地完成判断和写入：
```sql
UPDATE nightly_inventory
SET booked_units = booked_units + 1
WHERE room_type_id = :rt
  AND date = ANY(:dates)                                    -- N 个日期
  AND booked_units < total_units * (1 + overbook_pct);
```
根据 PostgreSQL 官方文档对读已提交隔离级别的定义："`UPDATE` 命令在寻找目标行时的行为和
`SELECT` 相同，只会找到命令开始时已提交的行；但如果这一行同时正被另一个并发事务更新（尚未
提交），后到的 `UPDATE` 会等待第一个事务提交或回滚——如果第一个事务提交了，第二个更新者会
针对这一行更新后的版本，重新求值自己的 `WHERE` 子句"（原文见「来源与延伸」）。这意味着两
笔并发预订如果争抢同一晚的最后一个名额，后到达的那笔事务会**排队等待先到的事务提交，然后
针对刚提交的新值重新判断**，不存在"两边都读到旧值、都以为自己抢到了"的窗口——这正是方案一
缺失、方案二天然具备的保护。

但方案二本身还差最后一步：`UPDATE ... WHERE date = ANY(:dates)` 如果 N 晚里有一晚不满足
容量条件，PostgreSQL **不会**让整条语句失败，而是**只更新满足条件的那些行**，返回的受影
响行数会小于 N——这正是"区间必须整体成功或整体失败"这个业务要求和"UPDATE 只更新匹配行"这
个 SQL 语义之间的落差。解决办法是应用层在同一个数据库事务内检查受影响行数：`rowcount ==
len(dates)` 才 `COMMIT`，否则显式 `ROLLBACK`——由于这条 `UPDATE` 本身就在一个事务里，
`ROLLBACK` 会撤销这条语句已经生效的那部分行（哪怕它们各自单独看是"合法"的），从而保证了
"全有或全无"。这一步应用层检查，是本设计相对「Ticket Booking」单行条件更新真正多出来的复
杂度——单座位模型天生就是"1 行要么成功要么失败"，不需要这层显式的整体性检查。

### 超售（overbooking）作为业务策略：不是开关，是一个风险预算

**问题**：「Ticket Booking」的"绝不超卖"是硬约束；酒店行业几十年来恰恰相反——大量连锁酒店
和精品酒店**主动**允许某一晚的预订数超过物理房间数，赌的是历史 no-show（未到店）和最后一
刻取消率。这道题该怎么把"允许超售"设计成一个可控的数字，而不是一个模糊的开关？

**方案一：固定超售百分比（如统一 +5%）**。实现简单——`total_units * 1.05` 直接作为
`UPDATE` 里的容量上限。但一个固定百分比对不同规模的库存池风险完全不同，下面用二项分布精
确算一遍就看得出来：假设某晚的历史 no-show/取消率是 6%，如果只有 50 间房的库存池，允许多
订到 51 间（超售 1 间，+2%），实际到店人数超过 50 间的概率就已经是 **4.26%**（`51` 间预
订中 no-show 数服从 `Binomial(51, 0.06)`，到店数 `= 51 - no-show 数 > 50` 当且仅当
no-show 数 `< 1`，精确计算得 `P ≈ 4.26%`）——这已经超过多数房源方能接受的 1% 风险预算，
说明**小库存池几乎没有安全的超售空间**。同样的 6% no-show 率放到 200 间房的池子上，超售
到 205 间（+2.5%）时超容风险仍能压在 **1%** 以内；放到 500 间的池子上，超售到 519 间
（+3.8%）时风险预算依然是 1%——池子越大，二项分布的相对方差越小（大数定律），能承受的超
售比例反而越高。这组数字（1.05× 固定百分比在小池子上完全不安全，在大池子上又留了太多钱在
桌上没赚）就是固定百分比这个方案的问题所在。

**方案二（本设计采用）：按历史 no-show 率和风险预算动态计算超售上限**。房源方配置一个可
接受的超容概率 `target_risk`（默认 1%），系统按该房型/该渠道/该季节的历史 no-show 率
`p`，用二项分布（或大样本下的正态近似）反解出容量 `capacity` 下允许预订到的上限
`B`，使得 `P(Binomial(B, p) < B - capacity) ≤ target_risk`，把结果写回
`NightlyInventory.overbook_pct` 这个字段，按需要每晚甚至按渠道单独计算和更新（周末和平日
的 no-show 率通常不同）。这把"超售系数"从一个静态配置变成一个由历史数据驱动、按库存池规模
自适应的计算结果——**代价**是需要维护可靠的历史 no-show/取消统计（按房型、星期几、提前预
订天数分桶），这是一次性的数据基建投入，换来的是超售策略本身不再是"赌"，而是一个有精确风
险边界的决策。

**超售触发后的补偿**：这道题不展开"walk"（把客人转移到附近同档次酒店并补偿差价）这类运营
流程的设计，只在数据模型上要求：超售发生时（到店人数确实超过物理容量的小概率事件），系统
必须能立刻查出"哪些预订是最后确认的"（按 `Booking.createdAt` 排序）以确定转移候选人，这是
`Booking` 表需要保留精确创建时间戳、而不能只存日期的原因之一。

### 搜索路径与预订路径的彻底分离

**问题**：容量估算给出 50:1 的读写比——真正的难点不是"读比写多"，而是每一次搜索查询理论上
需要对候选集合里的**每一个房型**都做一次"这段日期是否可订+多少钱"的查询，而这个查询本身
（读 N 晚的 `NightlyInventory` 并算总价）并不便宜。Expedia 工程团队在自己的房源排序博客
里把这一步明确点出来："给定一个搜索查询，对每个房源识别按房型的可用性并取回对应价格"这一
步"代价特别高"，本身就会随日期跨度和候选房源数产生"组合爆炸"（原文见「来源与延伸」）——一
个中等城市（如纽约、洛杉矶、奥兰多）单一目的地就有"一万多个房源"（同上），如果每次搜索都
对这一万多个候选房源逐一做精确可用性+定价查询，这一步会先于任何其他组件成为瓶颈。

**方案一：每次搜索都直接查 Inventory DB**。省去维护一份额外索引的复杂度，永远返回最新数
据。但读写比 50:1 意味着搜索峰值（1,736 QPS）会和预订峰值（57.87 QPS）共享同一批数据库
连接和缓冲池，搜索流量会在预订最需要低延迟的时刻挤占资源——这正是本设计明确要避免的耦合。

**方案二（本设计采用）：两阶段——候选生成（弱一致索引）+ 精确定价（权威查询）**。第一阶
段，`GET /search` 只查一份反规范化的搜索索引：按地理网格聚合房型，存储一个粗粒度的价格区
间和"大致可订"标记，由 CDC 从 Inventory DB 异步刷新（目标 P99 < 1 分钟新鲜度），把候选集
从"一万多个房源"收窄到用户实际会翻看的头部几十到几百个。第二阶段，只对用户点开的房型触发
`GET /room-types/{id}/availability`，绕过索引读 Inventory DB 的只读副本拿到精确的逐晚价
格和库存——真正昂贵的"逐晚定价"计算被限制在极少数用户真正点开的房型上，而不是每次搜索都
对全部候选做一遍。这正是 Expedia 博文里描述的同一个两阶段模式："优先对一个搜索区域内较少
数量的房源定价，再对这个较小的候选集做计算上更昂贵的排序"（见「来源与延伸」）——本设计把
它落到"索引 vs 权威查询"这两张物理上分开的存储上，而不只是同一个数据库里的两次查询。

**索引更新频率与索引结构的取舍**：Airbnb 自己的搜索检索工程博文提到，房源的"价格与可用性
数据频繁更新"这一约束，直接影响了他们在检索层选择索引结构的取舍（提到为了控制频繁更新下
的内存占用，权衡过 HNSW 和 IVF 两类近似检索索引，见「来源与延伸」）——本设计不需要做到
Airbnb 那种向量检索的精细程度，但同一个约束成立：反规范化索引里存的必须是**粗粒度**信号
（价格区间、可订/不可订布尔标记），而不是精确库存数字，否则每一次 `NightlyInventory` 的
微小变动都要触发一次索引重建，索引更新的吞吐会反过来成为瓶颈。

### 幂等预订与支付编排

**问题**：预订确认要和支付完成一次编排，网络重试、超时、webhook 重复投递都可能发生。这条
链路的幂等性设计和 [[solution-ticket-booking]] 里"占座 → 扣款 → 确认"的 saga 编排几乎是
同一个机制，本节不重复推导，只说本题因为"区间"这个维度而多出来的差异。

**和 Ticket Booking 的关键差异**：座位预订的"占座"要跨越用户填写支付表单的几分钟到十分
钟，因此需要一个显式的 hold 状态和 TTL；本设计的即时预订（instant book）场景里，从提交预
订到支付结果通常在几秒到十几秒内完成（多数平台已经在客户端预先收集好支付方式，不需要用户
现场填表单），所以`NightlyInventory` 的扣减和支付发起被设计成**同一个短生命周期的编排**
而不是"先长期占位、再等用户付款"：`POST /bookings` 里的多行条件更新一旦成功，立刻在同一
个请求内发起扣款；只有当扣款在一个很短的超时窗口（如 30 秒）内没有结果时，才把预订状态标
记为 `pending` 并允许一次异步的最终确认或回滚，而不是像座位场景那样预留一个数分钟到十分
钟的用户填表窗口。请求到 PSP 侧仍然复用 [[solution-ticket-booking]] 里同样的
`clientRequestId`/`idempotencyKey` 双层幂等模型（网络重试用请求级随机键，扣款确认用订单
级确定性键），机制不需要重新设计。

### 渠道同步：谁是库存的唯一真相来源

**问题**：房源方常年在多个渠道（自己的官网、多个 OTA）同时售卖同一批房间。任意一个渠道确
认一笔预订，其余所有渠道都必须尽快感知，否则会出现"这一晚在两个渠道上都显示可订，两边各
成交一笔"的跨渠道超售——这是数据库层面的原子性完全无法单独解决的问题，因为写入根本不是发
生在同一个数据库事务里，甚至不是发生在同一家公司的系统里。

**方案一：本平台单向推送库存变化给外部渠道，不接收外部渠道的确认事件**。实现最简单，但只
能保护"本平台卖出后不让外部渠道超卖"这一个方向，反方向（外部渠道先卖出）完全没有防护，等
于放弃了"双向同步"这个需求。

**方案二（本设计采用）：把外部渠道当成另一个"预订发起方"，复用同一条多行条件更新逻辑**。
外部渠道的 webhook（"我们这边刚确认了一笔预订，日期 X-Y"）被 `ChannelSyncEvent` 接收后，
直接对 `NightlyInventory` 发起和本平台内部预订完全相同的多行条件更新——库存表不区分这次
扣减来自哪个来源，一视同仁地检查容量约束。**关键结论**：两个渠道谁先到达 Inventory DB 的
那条 `UPDATE`，谁就成功；后到达的一方，如果此时容量已经不允许，条件更新在数据库层面必然
失败（依据的还是深入探讨第 2 节同一个读已提交下的行为），这时进入对账队列——如果失败的一
方恰好是本平台自己确认过的预订（钱可能已经收了），触发自动退款和向用户道歉的流程；如果失
败的一方是外部渠道推来的事件，本平台向该渠道回报"库存冲突，无法确认"，由渠道自己的规则处
理（多数 OTA 渠道管理协议本身就定义了这种"冲突拒绝"响应码）。**代价是跨渠道同步天然是最
终一致的**——`ChannelSyncEvent` 从外部系统产生到打到本平台的 webhook 端点，本身就有网络
延迟和外部系统自己的批处理延迟，需求里 P99 < 2 分钟的同步延迟目标就是承认了这一点，而不是
假装可以做到强一致。

## 瓶颈、故障与演进

**热点与倾斜**：不同于「Ticket Booking」单场演出座位那种极端热点，本设计的负载天然分散在
数百万个房型上；真正的倾斜来源是**热门目的地在热门日期的搜索聚集**——比如跨年夜的纽约、
情人节的巴黎，这类事件会让某个地理网格分片的搜索 QPS 短时冲高一个数量级。缓解手段是索引
按地理网格分片、对已知的年度性热点日期（新年、重大节假日）提前扩容对应分片的缓存容量，而
不是依赖自动弹性伸缩来追赶一个提前已知的日期。

**故障域**：
- **搜索索引/缓存不可用**：降级为直接查询 Inventory DB 的只读副本，牺牲延迟但不牺牲正确
  性——因为搜索路径本来就是弱一致的补充路径，不是唯一真相来源。
- **Inventory DB 主库不可用**：预订这条唯一强一致写路径完全停摆，需要秒级自动故障转移；
  搜索路径继续用缓存的陈旧索引撑几分钟，用户能看但不能订。
- **渠道 webhook 端点抖动**：外部渠道的推送重试机制通常自带退避重试，短暂的接收方故障不
  会丢事件，只会推迟同步延迟；但如果故障持续超过渠道自己的重试窗口，需要一个主动对账任
  务定期拉取渠道侧的"最近确认列表"做补偿同步，不能完全依赖被动 webhook。
- **PSP 抖动**：复用 [[solution-ticket-booking]] 里同样的"卡在 charging 状态靠超时对账任
  务兜底"的结论。

**10 倍演进**：从 600 万房源到 6,000 万房源。库存行数从 32.85 亿涨到约 328.5 亿，单一关
系型集群即便分片也开始吃力，需要把 `NightlyInventory` 按地理区域做更粗的物理隔离（类似数
据库层面的多租户分片），并把可订窗口从 365 天缩短或分层存储（近 90 天热数据用高性能存储，
更远的窗口用更廉价的存储，因为绝大多数预订发生在未来 90 天内）。

**100 倍演进**：平台级别，多个业务线（民宿、连锁酒店直销、企业差旅）共享同一套基础设施。
这时候搜索索引层本身要做成独立于任何单一业务线的通用检索服务，而 Inventory DB 这层"同一
段日期区间要么全订成功要么全失败"的事务边界不能被拆分——这是全书里反复出现的模式：无状态
的读/缓存层可以随意水平扩展，唯一有状态、承载正确性的那一层永远是扩展中最谨慎的一环。

## 面试官会追问什么

**中级（mid）**

- "如果一次预订只锁一晚而不是一段区间，这道题会简单多少？" 会退化成「Ticket Booking」的
  单行条件更新模型（`total_units` 就是"座位数"），不再需要应用层显式检查受影响行数是否等
  于晚数这一步——这个问题在考察你是否真正理解"区间"这个维度带来的额外复杂度具体在哪一行代
  码上。
- "取消一笔预订之后库存怎么归还？" 归还是"加法"，和预订的"减法"走不同的路径，同样需要在一
  个事务里对区间内每一晚做 `booked_units = booked_units - 1`，且要考虑"取消发生时这一晚
  是否已经被超售占满"这类边界，不能假设归还总是安全的。

**高级（senior）**

- "为什么搜索索引不直接存精确库存数字，而只存一个粗粒度的可订标记？" 精确数字意味着
  `NightlyInventory` 的每一次微小变动都要触发索引重建，索引更新的吞吐会反过来成为新瓶
  颈；粗粒度标记允许索引以分钟级批量刷新，把"精确"这件事留给用户真正点开房型时才做的权威
  查询。
- "两个渠道同时把最后一间房卖给不同的人，谁赢？" 数据库层面永远是先到达 `UPDATE` 语句的一
  方赢，这不是业务规则决定的，是读已提交隔离级别下行锁的天然结果；业务规则决定的只是"输的
  一方怎么善后"（自动退款、道歉、备选房源）。

**参谋级（staff）**

- "如果房源方想要'先到先得'之外的分配策略（比如给平台会员优先权），架构要怎么改？" 多行
  条件更新本身只能表达"容量是否还够"，不能表达优先级；需要在条件更新之前叠加一层准入判
  断（类似「Ticket Booking」的虚拟队列，但这里更接近一个按会员等级排序的短暂准入窗口），
  且要接受"给高优先级用户预留库存"本身会降低整体装箱效率这个权衡。
- "整个系统要不要支持跨房源的'打包预订'（酒店+租车）原子提交？" 这会把事务边界从单一
  Inventory DB 扩展到多个完全独立的库存系统，传统两阶段提交的可用性代价在这个规模下不可
  接受，更现实的做法是 saga：先各自独立预留，任何一步失败就对已成功的步骤发起补偿（退订/
  退款），代价是短暂的"用户看到部分确认"的中间状态，这是本设计明确排除在范围外、但值得在
  面试里主动指出权衡的方向。
- "超售的风险预算模型假设了 no-show 率是稳定可预测的，如果遇到突发事件（航班大面积取消、
  自然灾害）导致 no-show 率骤变怎么办？" 静态计算的 `overbook_pct` 在突发事件下会失效，
  需要一个能实时收窄超售系数的熔断机制（比如检测到某地区取消率异常升高时，自动把该地区未
  来几天的 `overbook_pct` 临时下调至 0），这本质上是把"超售"这个风险模型本身也纳入可观测
  性和自动降级的范围，而不是当成一次性配置。

## 常见错误

- 把这题当成「Ticket Booking」的单行条件更新直接照抄，完全忽略"区间"要求应用层显式检查受
  影响行数是否等于晚数，导致"半段区间被扣减、半段没扣"的隐藏 bug。
- 用"先 `SELECT` 判断，再 `UPDATE`"的两步写法，被追问"两个用户同时抢最后一晚"时答不上来，
  或者含糊地说"加个锁"却说不清锁的粒度和持有时长。
- 把超售设计成一个全局固定的百分比常量，被追问"为什么这个数字对所有房型都适用"时说不出道
  理——没有意识到超售的安全空间随库存池大小系统性变化。
- 搜索路径直接查预订库，只在被明确问"如果搜索流量很大怎么办"时才现场加一层缓存，而不是从
  一开始就把两条路径设计成物理上独立的存储。
- 完全忽略跨渠道库存同步，或者把它简化成"我们直接强一致地同步"，没有意识到跨公司边界的同
  步天然是最终一致的，需要设计冲突后的补偿流程而不是假装冲突不会发生。
- 通篇"加缓存""加索引"却给不出具体的行数、QPS、风险概率这些数字，论证停留在堆砌名词，没
  有到达"为什么是这个数字"的层次。

## 五分钟讲法

This is a date-range inventory problem, not a single-resource problem: every booking locks a
contiguous span of nights across a room type, and that span must succeed or fail as one unit,
which is the core difference from a seat-booking system. I model inventory as one row per
room-type per night with a total and a booked count, because most guests don't care which
physical unit they get — pooling capacity this way beats binding a specific room too early. A
multi-night booking is a single multi-row conditional UPDATE across every night in the range,
guarded by the same read-committed re-evaluation semantics that make single-row conditional
updates safe elsewhere, but I add an explicit application-level check that the affected row
count equals the number of nights, rolling back the whole transaction otherwise, because SQL
UPDATE quietly skips rows that fail their WHERE clause instead of failing the whole statement.
Overbooking here isn't a binary switch, it's a risk budget: I compute the safe overbooking
percentage from a binomial model of historical no-show rates, and that safe percentage grows
with pool size, so a fixed flat overbooking rate is wrong for small properties and too
conservative for large ones. Search and booking are two completely separate paths: search hits
a denormalized, minutes-stale index that narrows millions of listings down to a handful of
candidates, and only the listings a user actually opens get a precise, authoritative
availability query against the real inventory table — this two-stage funnel is what keeps the
expensive per-night pricing computation off the critical path for every search. Cross-channel
sync with external OTAs is inherently eventually consistent, since two independent companies
can't share one database transaction, so I treat every external channel's booking confirmation
as just another writer racing for the same conditional update, and I build an explicit
reconciliation path for the loser instead of pretending the conflict can't happen. At 10x scale
the inventory table needs geographic sharding and time-window tiering; the read-heavy search
layer scales horizontally without any of this care, because it was never the source of truth.

## 来源与延伸

- [PostgreSQL — Range Types (Exclusion Constraints)](https://www.postgresql.org/docs/current/rangetypes.html)：
  官方文档给出的 `reservation` 表教科书例子（`EXCLUDE USING GIST (during WITH &&)`），本
  文在「深入探讨」第 1 节把它作为"区间行"方案的直接依据，并论证了它在多单元池化库存场景下
  为什么不是默认选择——这是本文和一个只会说"用排他约束"的简化题解最大的分歧点。
- [PostgreSQL — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)：
  官方文档对读已提交隔离级别下 `UPDATE` 遇到并发已提交更新时"等待并针对新值重新求值 WHERE
  子句"的精确描述，是本文「深入探讨」第 2 节"为什么单条多行条件更新是安全的"这一论证的直
  接依据，而不是凭经验断言。
- [Expedia Group Technology — Choosing the Right Candidates for Lodging Ranking](https://medium.com/expedia-group-tech/choosing-the-right-candidates-for-lodging-ranking-d0841bf40c0e)：
  给出了"可用性与定价查询计算上特别昂贵、会产生组合爆炸"以及"纽约/洛杉矶/奥兰多等中等目的
  地单地有一万多个房源"这两个一手数字，是本文「深入探讨」第 4 节两阶段搜索设计的直接依
  据。本文与它的差异在于：本文把两阶段落到两个物理上分开的存储（索引 vs 权威库），而不是
  同一数据库内的两次查询。
- [Airbnb Engineering — Embedding-Based Retrieval for Airbnb Search](https://medium.com/airbnb-engineering/embedding-based-retrieval-for-airbnb-search-aabebfc85839)：
  提到房源"价格与可用性数据频繁更新"这一约束如何影响了检索索引结构的选型（在 HNSW 和 IVF
  之间因为更新频率和内存占用而选择后者）。本文没有采用 Airbnb 同等复杂度的向量检索方案，
  但复用了同一个结论：搜索索引必须存粗粒度信号，否则更新吞吐会成为新瓶颈（见深入探讨第 4
  节）。
- [Airbnb Engineering — Avoiding Double Payments in a Distributed Payments System](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)：
  Airbnb 自己关于幂等键（请求级 vs 实体级）和"五个九一致性"支付框架 Orpheus 的工程博文，
  是「深入探讨」第 5 节幂等编排结论的来源之一，也是 [[solution-ticket-booking]] 同一结论
  的共同依据，本文不重复展开，只指出本题因为即时预订通常没有分钟级填表窗口而做的编排简
  化。
