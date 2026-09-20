---
id: problems-ad-click-aggregation-deterministic-upsert-key
node: problems.search.ad-click-aggregation
type: qa
step: 6
tags: [grown]
---
## Q
In an ad click aggregation pipeline writing windowed aggregates into an OLAP store, why must the upsert key used to make the sink idempotent be built entirely from deterministic fields of the aggregation (like `ad_id` and `window_start`), and what breaks if it isn't?

## A
After a stream processor restarts from a checkpoint, it replays and re-emits output for everything since the last checkpoint — end-to-end exactly-once depends on that replayed output landing as a harmless overwrite rather than a duplicate. An upsert keyed by fully deterministic fields (`ad_id`, `campaign_id`, `window_start`, `window_granularity`) produces the identical key on replay, so the second write just overwrites the first with the same (correctly recomputed) value. If the key instead includes something non-deterministic — a freshly generated `uuid4()`, or a wall-clock `received_time` — replay produces a *different* key each time, so the replayed aggregate lands as a brand-new row instead of overwriting the old one, silently double-counting the affected clicks.

## Q zh
在一个把窗口聚合结果写入 OLAP 存储的广告点击聚合流水线中，为什么用来让 sink 幂等的 upsert key 必须完全由聚合本身的确定性字段（比如 `ad_id` 和 `window_start`）构成？如果不是会出什么问题？

## A zh
流处理器从 checkpoint 重启后，会重放并重新发出上一次 checkpoint 之后的所有输出——端到端精确一次依赖于这次重放的输出落地时是一次无害的覆盖写，而不是一条重复记录。用完全确定性的字段（`ad_id`、`campaign_id`、`window_start`、`window_granularity`）构成的 upsert key，在重放时会得到完全相同的 key，所以第二次写入只是用同一个（重新算出的、正确的）值覆盖第一次。如果 key 里混入了非确定性的部分——比如每次新生成的 `uuid4()`，或者一个挂钟时间的 `received_time`——重放每次都会得到不同的 key，于是重放的聚合结果会落地成一条全新的记录而不是覆盖旧记录，悄悄把受影响的点击重复计费。
