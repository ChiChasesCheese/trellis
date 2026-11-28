---
id: mlp-design-sd01-asof
node: design.sd01
step: 4
type: qa
---
## Q
**深挖：as-of 查询与双时间模型**｜设计轮

"风控要查某个历史时刻的价格，而且这个查询绝对不能看到事后才收到的修正。你的存储怎么设计，`GET_AS_OF` 怎么实现？"

## A
**核心不变量。** 一次 `as_of(ts)` 查询的结果只取决于"系统在 `ts` 那一刻已经知道什么"，不取决于之后又知道了什么。单一时间戳回答不了这件事：它只能说价格什么时候生效，说不清系统当时是否已经知道后来的修正。

**双时间（bitemporal）。** 每条记录带两个时间，都用 UTC：
- **`valid_time`：** 供应商报告的这个价格在市场上生效的时刻。
- **`knowledge_time`：** 系统真正持久化这条记录的时刻，摄入时由系统自己打，不信供应商声称的时间。

**查询语义。** `GET_AS_OF(symbol, as_of)` 返回"`knowledge_time <= as_of` 的记录里，该 symbol `valid_time` 最新的一条"。修正是一条新记录，它的 `knowledge_time` 是修正到达的时刻，所以 `as_of` 早于这个时刻的查询继续返回原始值。历史层按 (symbol, `knowledge_time`) 有序，查询是在有序数据上的二分查找，和编程题里价格存储的 as-of 是同一个技巧。

**两条路径分开。** `GET_LATEST` 走当前值缓存，是 pod 高频读的热路径；`GET_AS_OF` 直接查历史层，不经缓存。缓存天然只为最新值优化，拿它做历史快照要么一致性不对，要么性能不行。

**衍生数据同理。** `GET_BAR` 也带 `as_of`：风控问"当时算出来的 5 分钟 VWAP 是多少"，只能用当时已知的 tick 重新聚合，不能用事后修正过的。

**英文答法。**
- "Every record has a **valid time**, when it was true in the market, and a **knowledge time**, when we learned it."
- "`as_of` resolves against **knowledge time**, so a past query reproduces exactly what we knew then."
- "Latest reads hit a **cache**; as-of reads go to the history store, so they never compete."
