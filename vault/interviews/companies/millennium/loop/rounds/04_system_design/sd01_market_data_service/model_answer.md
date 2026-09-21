# 模型答案：设计 Market / Price Data Service

> 取材：LeetCode Discuss 7423863 R5 "price data design problem"（题名，一手）；TechPrep "research data pipelines / real-time risk monitors"；QuantVault "multi-currency PnL"；mlp.com 官方技术页"900K+ 数据文件/天"。接口签名、数据模型、failure mode 展开为 **(reconstructed)**。按 `rubric.md` 五维组织。

## 0. 两句话复述 + 不变量

**复述**：这是一个服务几百个 trading pod 和一个中央 risk 系统的多供应商行情数据服务，对外是"最新价"和"as-of 历史价"两类查询、外加 OHLC/VWAP 聚合和多币种换算，内部要在多个供应商各自迟到、互相冲突的前提下，保证历史查询结果永远不受"未来才发生的修正"影响。

**核心不变量**：

1. **No-lookahead**：一次 `as_of(ts)` 查询的结果，只取决于"系统在 `ts` 这个时刻已经知道什么"，不取决于"之后又知道了什么"——risk 系统拿这个做历史归因，如果结果会因为未来的修正而变化，归因就是不可复现、不可信的。
2. **修正是追加，不是覆盖**：供应商迟到的修正值必须作为一条新记录写入，原始值和修正值都要能被查到；系统需要记住"这条修正是什么时候被系统真正得知的"，这个时间戳（而不是价格本身生效的时间戳）才是 no-lookahead 判断的依据。
3. **latest 读和 as-of 读是两种不同的访问模式**：latest 是几百个 pod 高频轮询/推送的热路径，要快；as-of 是 risk 系统偶发的历史回溯，要准且可复现——两者不该抢同一份索引资源。
4. **多币种换算要按时间点对齐**：换算用的汇率必须是跟价格同一时间点的汇率，不能用"当前"汇率去换算"历史"价格，否则多币种 PnL 会算错。

明确"不做什么"：不追求把每一笔 tick 都无限期保留在热存储里（有冷热分层）；不在这个服务里做仓位/PnL 计算本身（那是 risk 系统的事，这个服务只保证喂给它的价格是 point-in-time 正确的）。

## 1. 开场 60 秒（English）

> This is a price data service for a multi-manager hedge fund: dozens of independent trading pods and one central risk system all depend on the same market data, sourced from several vendors — end-of-day prices as files, intraday prices as a stream. The hard part isn't "store a price and look it up" — it's that **as-of queries must never see the future**, because risk uses them for historical attribution, and vendors routinely send **late corrections** that must not silently overwrite history. So the core invariant I'll design around is bitemporal: every price record has both a **valid time** — when it was true in the market — and a **knowledge time** — when this service actually learned about it. `as_of(ts)` always resolves against knowledge time, so a query made before a correction arrived reproduces exactly what the system knew then, forever, no matter how many corrections show up later. On top of that store I'll add OHLC/VWAP derivation, currency conversion that's aligned to the same point in time as the price it's converting, and a push path to subscribers that's decoupled from ingestion so a slow pod never backs up the write path. Let me start with the API and data model, then walk through ingestion, failure modes, and how I'd split this into components.

## 2. API 契约

```
PUT_PRICE(symbol, vendor, price, currency, valid_time)
                              -> {version, knowledge_time}
CORRECT_PRICE(symbol, vendor, original_valid_time, corrected_price, reason)
                              -> {version, knowledge_time}     # 显式修正，不是覆盖
GET_LATEST(symbol, [ccy=base])
                              -> {price, valid_time, version, ccy}
GET_AS_OF(symbol, as_of: knowledge_time, [ccy=base])
                              -> {price, valid_time, knowledge_time, version} | NotFound
GET_BAR(symbol, interval, start, end, [as_of], [ccy=base])
                              -> {items: [(ts, open, high, low, close, vwap, volume)]}
SUBSCRIBE(symbols | pattern) -> stream of {symbol, price, valid_time, knowledge_time, ccy}
```

- `knowledge_time` 是系统真正把这条记录持久化的时刻（摄入时打的时间戳，不是供应商声称的时间），`valid_time` 是供应商报告的"这个价格在市场上生效的时刻"，两者都以 UTC 存储。
- `as_of` 语义：返回"`knowledge_time <= as_of` 中，同一 symbol 里 `valid_time` 最新的那条记录"——即"在 `as_of` 这个时刻，系统所知道的、关于这个 symbol 最新的价格"。
- `CORRECT_PRICE` 不修改任何已有记录，只追加一条新版本，`knowledge_time` 是修正真正到达系统的时刻；任何 `as_of` 早于这个 `knowledge_time` 的查询继续返回原始值。
- `GET_BAR` 同样支持 `as_of`——risk 系统要能问"在某个历史时刻，我们当时算出来的 5 分钟 VWAP bar 是什么样"，这个 bar 必须只用当时已知道的 tick 算，不能用之后修正过的 tick 重算。

## 3. 数据模型

```
摄入层归一化后的内部记录（EOD 文件和 intraday 流最终都落成这个形状）:
  (symbol, vendor, price, currency, valid_time_utc, knowledge_time_utc,
   version, correction_of: version | null)

存储分两层:
  当前值索引: (symbol, ccy) -> latest_version 指针     # GET_LATEST 的快路径，内存/缓存为主
  价格历史（bitemporal, 按 (symbol, knowledge_time) 天然有序的日志/列存）:
    每条记录不可变；GET_AS_OF/GET_BAR 在这一层做归并查找

汇率跟价格走同一条摄入/存储路径:
  把 (base_ccy, quote_ccy) 当成一个"symbol"，一样有 valid_time/knowledge_time/version
  换算时找跟被换算价格同一时间点对齐的汇率记录，不用"当前"汇率
```

**为什么是 bitemporal 而不是单一时间戳加版本号**：单一时间戳只能回答"这个价格是什么时候生效的"，回答不了"我在某个历史时刻问这个价格时，系统当时到底知不知道后来的修正"——而这正是 no-lookahead 这条不变量要求的语义。这跟我在 DuckDB/Parquet 上做的 point-in-time 数据面是同一个模式：**as-of join 的正确性不取决于数据本身的时间戳，取决于"这份数据在查询发起的那一刻是否已经存在"**，用回测里的行话说就是防止 look-ahead bias；这里换成生产系统，防的是"risk 归因用到了事后才有的信息"。

## 4. 核心流程

**EOD 文件摄入**：供应商每天收盘后落一批文件（mlp.com 口径全公司量级 900K+ 份/天）→ 文件 loader 按供应商解析（每个供应商的字段格式独立、配置驱动，不是每接一个新供应商就写一段新代码）→ 归一化成内部记录 → 用 `(symbol, vendor, valid_time, source_file_id)` 做幂等键写入 append-only 日志——文件会被重投，幂等键保证重复摄入不产生重复记录。

**Intraday 流式摄入**：每个供应商的流式连接由一个独立的 normalizer 消费，断线重连后从连接自己记录的 offset 续传（不依赖摄入路径记忆"重连前处理到哪了"），同样归一化成内部记录写入同一条日志。

**写路径**：无论来自文件还是流，最终都是"归一化 → 写日志（source of truth）→ 更新当前值索引缓存"；EOD 和 intraday 两条摄入路径完全独立，互不阻塞，这跟 Amex 结算管线里"六条 append-only Stream 各自独立 offset、互不阻塞"是同一个设计动机——不同的失败模式（文件重投 vs 连接断线）不应该共用一条容错逻辑。

**读路径**：
- `GET_LATEST`：查当前值索引缓存，命中直接返回；未命中回源到日志层取最新一条。
- `GET_AS_OF`：跳过当前值索引，直接在价格历史层做"`knowledge_time <= as_of` 中最新一条"的查找。
- `GET_BAR`：从价格历史层拉出区间内的原始记录，按 `as_of`（如果指定）过滤掉查询时刻之后才被知道的记录，再做 OHLC/VWAP 聚合——聚合本身是无状态的读时计算，不回写。

**修正流程**：供应商发来修正 → `CORRECT_PRICE` 写一条新记录，`correction_of` 指向被修正的原始版本，`knowledge_time` 是这次修正真正到达的时刻 → 当前值索引更新为修正后的值（`GET_LATEST` 立刻拿到新值）→ 但历史上任何 `as_of` 早于这次修正 `knowledge_time` 的查询结果不变，risk 系统重放某个历史时点的计算天然可复现。

## 5. 失败模式与规模

**迟到数据与修正**：见上一节修正流程；关键是"覆盖 vs 追加"这个选择本身就是这题的核心考点——覆盖会让历史不可复现，追加才能同时满足"最新值要新"和"历史可复现"两个看似矛盾的要求。

**供应商互相冲突**：同一 symbol 多个供应商同时报价、数值不一致时，配置每个 symbol 的 primary/fallback 供应商顺序；一个后台校验任务持续比较各供应商对同一 symbol 的报价，超过阈值（如若干 bps）的分歧标记出来并告警，而不是静默选一个了事——这跟 Amex 管线里"两个 UDTF 用 `FULL OUTER JOIN` 校验 pending 和文件记录、不匹配的记录进 `ERROR_LOGS` 永不丢"是同一个思路：校验的输出是"标记 + 保留"，不是"静默丢弃或静默选择"。

**时区/交易所日历**：不同交易所的本地收盘时间、DST 规则都不同；摄入时立刻把供应商给的本地时间归一化成 UTC 存储，`valid_time` 永远只用 UTC 表达，日历相关的展示逻辑（"这是 A 股收盘价还是美股收盘价"）放在查询层用交易所元数据做，不掺进存储层的排序依据——这是从 Amex 管线"文件落进'昨天'目录导致按日期过滤漏数据"这个真实事故里学到的教训：任何跟"日期/时间"相关的判断，一旦掺进本地时区的隐含假设，就会在边界情况上出错。

**Backfill**：历史批量补录（比如新接入一个供应商，需要把它过去一年的数据也灌进来）不能走实时摄入路径，否则会污染当前值索引；backfill 走独立路径直写价格历史层，`knowledge_time` 如实标记成"backfill 任务实际执行的时刻"（而不是伪造成价格本来生效的历史时刻），这样任何早于 backfill 执行时刻的 `as_of` 查询依然不会看到这批数据——backfill 本身也不能破坏 no-lookahead。

**热门 symbol**：少数被绝大多数 pod 订阅的 symbol（大盘指数、mega-cap）会有远超均值的读和订阅负载；按 symbol 哈希分片，热门 symbol 的 `GET_LATEST` 走内存缓存 + 多副本读，历史 `as_of`/`GET_BAR` 查询走单独的列存后端，两条路径物理上不共享资源，热路径的压力不会拖慢冷路径的吞吐，反之亦然。

**规模估算**：以 mlp.com "900K+ 数据文件/天"做量级锚点，假设其中一部分是行情文件，EOD 摄入是批量、可并行的吞吐问题；intraday 流按 symbol 分片后单分片吞吐可控；真正的扇出压力在推送——几百个 pod、每个 pod 可能订阅几十到上百个 symbol，扇出规模是"pod 数 × 平均订阅数"，这也是为什么推送必须走独立于摄入的日志尾随服务，而不是让每个订阅直接打摄入路径。

## 6. 分层与组件

- **摄入层**：EOD 文件 loader（按供应商配置驱动解析）+ intraday 流 normalizer（每个供应商独立连接、独立 offset），两条路径各自处理自己的失败模式，归一化成同一种内部写入格式后交给存储层。
- **存储层**（bitemporal 价格历史，唯一的 source of truth）：只负责持久化和按 `(symbol, knowledge_time)` 排序读取，不关心数据是从文件还是流进来的。
- **衍生层**（OHLC/VWAP、FX 换算）：对存储层的无状态读时变换，独立演进——换 bar 的聚合算法或加新的衍生指标，都不动存储层和摄入层。
- **分发层**（pub/sub fan-out）：尾随存储层的写日志，把变更推给订阅的 pod/risk 系统；跟摄入层之间只有"读日志"这一个耦合点，慢订阅者或推送故障不会反压摄入。
- **查询服务层**：对外暴露 `GET_LATEST`/`GET_AS_OF`/`GET_BAR`，背后接当前值缓存 + 存储层，不感知供应商细节，新增供应商不需要改这一层。

## 7. rollout/测试/监控

- **测试**：拿供应商自己发的汇总/校验记录做行数与总量对账（复用会上生产的查询路径本身去验证，而不是另写一套抽样脚本）；专门做"修正重放"测试——先发一条价格、发起并记录一次历史 `as_of` 查询结果，再发一条修正，断言那次历史查询的结果如果重新发起仍然不变。
- **监控**：每个供应商的摄入新鲜度（超过预期 SLA 未收到新数据即告警，这是发现"供应商这边掉线了"的第一道信号，而不是等 pod 自己发现价格不对）；供应商间价格分歧率；fan-out 推送延迟与订阅方积压；bar 聚合结果与供应商官方 OHLC 的对账偏差。
- **rollout**：新供应商接入是配置变更（一份解析配置 + 一条摄入连接），不是新代码路径；先影子摄入（数据进系统但不作为任何 symbol 的 primary 来源）观察一段时间的数据质量和分歧率，达标后再切成 primary。
- **on-call**：摄入新鲜度和供应商分歧率超阈值直接告警分派 on-call，而不是被动等下游报告价格不对——这是从"迟到发现的问题成本远高于主动发现"这条经验里学到的默认做法。

## 8. 用 Chi 自己的经验作参照

这道题的两个核心难点——"多供应商、各自独立失败模式的摄入路径"和"点查询绝对不能看到未来"——分别正好对应我做过的两件事。

**摄入侧**：我在 Braintree 做过一条 Snowflake-native 的 Amex 结算管线——`COPY INTO` 把供应商（Amex）落的定宽文件摄入 staging，六条**各自独立 offset 的 append-only Stream** 把混在一起的六种记录类型分流，六个解析 procedure 用复合键 `MERGE` 幂等写入类型化表，两个校验 UDTF 用 `FULL OUTER JOIN` 比对、不匹配的记录进错误日志**永不丢**。这套模式直接搬到这题上：每个供应商就是一种"记录类型"，独立摄入路径、独立失败域；`MERGE` 的幂等键防止文件重投产生重复记录；校验层的"标记 + 保留"而不是"静默丢弃"，对应这题里"供应商冲突要标记告警而不是静默选一个"。我在那条管线上还踩过一个真实的坑——文件落进"昨天"的日期目录导致按日期过滤漏数据，改成正则扫全部日期目录才修复——这正是这题"时区/交易所日历"这一节我特别强调"不能把本地时区的隐含假设掺进存储层排序依据"的直接教训来源。

**存储侧**：我在自己的 Quant-Stroller 项目里搭过一个 DuckDB/Parquet 上的 point-in-time 数据面（raw → bars → panel，跨 9 个供应商的 2,300+ 因子目录），核心就是 as-of join——保证任意一次历史查询只用"当时已经存在"的数据，不掺入未来才出现的修正或未来才计算出的因子值,这是防止量化研究里 look-ahead bias 的标准做法。这题的 bitemporal 数据模型是这个思路在生产系统里的对应版本：`valid_time`/`knowledge_time` 分离，本质上就是把"这份数据什么时候在业务上生效"和"这份数据什么时候被系统实际看到"这两个维度显式拆开，跟 as-of join 要保证的语义是同一件事，只是这里多了一个"修正会迟到"的生产系统现实。

## 9. 45 分钟口述时间表

- **0–5 min**：复述题目 + 说不变量（no-lookahead、修正追加不覆盖、latest/as-of 两条路径分离、FX 换算时间点对齐），确认规模（供应商数、pod 数、symbol 数、EOD 文件量级）。
- **5–12 min**：API 契约（`PUT_PRICE`/`CORRECT_PRICE`/`GET_LATEST`/`GET_AS_OF`/`GET_BAR`/`SUBSCRIBE`），数据模型（bitemporal 价格历史 + 当前值索引 + 汇率同路径摄入）。
- **12–22 min**：核心流程——EOD 文件摄入与 intraday 流摄入两条独立路径、写路径怎么落地、`as_of` 怎么在 bitemporal 存储上实现、修正流程怎么保证历史可复现。
- **22–35 min**：失败模式——迟到修正、供应商冲突、时区归一化、backfill、热门 symbol 扩容（这一段通常是面试官追问最密集的地方，主动往这个方向讲，尤其是"覆盖 vs 追加"这个选择的取舍）。
- **35–42 min**：分层图 + rollout（新供应商配置化接入、影子摄入）+ 监控指标。
- **42–45 min**：一句话总结不变量与最大的 trade-off（正确性优先于存储成本——保留完整的修正历史比省存储更重要，因为 risk 归因不可复现的代价远高于多存几份历史记录），反问面试官。
