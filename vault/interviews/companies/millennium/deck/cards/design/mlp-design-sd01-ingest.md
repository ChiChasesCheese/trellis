---
id: mlp-design-sd01-ingest
node: design.sd01
step: 5
type: qa
---
## Q
**深挖：摄入、幂等与修正**｜设计轮

"供应商可能重复投递同一个文件，流连接断了会重连，还会迟到地发修正。摄入这一层怎么保证数据不重、不丢、历史不被改？"

## A
**两条独立路径。**
- **文件（EOD）：** 供应商每天收盘后落一批文件，loader 按供应商的配置解析，归一化成内部记录；文件会被重投，所以用幂等键 `(symbol, 供应商, valid_time, 源文件 id)` 写入。
- **流（盘中）：** 每个供应商一个独立的 normalizer，断线重连后从连接自己记录的 offset（读到哪里的位置）续传，不依赖摄入层记住重连前处理到哪；用供应商自带的序列号或消息 id 去重。

**幂等写入。** 用"不存在才写入"的原子操作（类似 `MERGE ... WHEN NOT MATCHED`），不要先查后写，否则两个并发重投都会查到"不存在"。去重在摄入层一次性做完，不让每个订阅方自己判断见没见过。

**修正是追加。** `CORRECT_PRICE` 不改任何旧记录，只追加一条新版本，`correction_of` 指向被修正的版本，`knowledge_time` 是修正到达的时刻。随后最新价缓存更新，`GET_LATEST` 立刻拿到新值；早于这个时刻的 `as_of` 查询不受影响。覆盖会让同一个历史查询今天和明天答案不同，风控归因就无法复现。

**回补（backfill）。** 新接一个供应商要灌入过去一年的数据时，走独立路径直写历史层，不经最新价缓存，`knowledge_time` 如实记为回补实际执行的时刻，不伪造成历史日期；否则等于声称系统当时就知道，制造出历史上不存在的"看到未来"。

**英文答法。**
- "Corrections are **appended** as new versions; we never update a record in place."
- "Dedup happens at ingestion with an **idempotency key** and an atomic insert-if-absent."
- "Backfill stamps the **real load time** as knowledge time, so old as-of queries stay unchanged."
