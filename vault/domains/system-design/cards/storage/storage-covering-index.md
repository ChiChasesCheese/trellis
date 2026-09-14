---
id: storage-covering-index
node: storage.relational.indexing
type: qa
---
## Q
What makes an index "covering" for a query, why is it dramatically faster, and what's the cost of covering everything?

## A
The index contains **every column the query needs** (key columns + `INCLUDE`d payload), so the engine answers from the index alone — an **index-only scan** — skipping the per-row hop to the heap/table (a random I/O per row in Postgres, unless the visibility map lets it skip the check).

For a 1000-row range that hop is often 90%+ of the cost; covering turns it into one contiguous index range read.

Cost: every extra indexed/included column makes **every write** update more index bytes, bloats index size, and slows vacuum — indexes are derived data you pay for on each mutation. Cover your hottest queries, not all of them.

## Q zh
什么让一个索引对查询"覆盖"，为什么这快得多，覆盖所有东西的代价是什么？

## A zh
索引包含**查询需要的每一列**（key 列 + `INCLUDE`d payload），所以引擎从索引单独回答——一个**索引只查**——跳过每行到 heap/table 的跳转（Postgres 中每行一个随机 I/O，除非 visibility map 让它跳过检查）。

对于 1000 行范围，那个跳转经常是 90%+ 的成本；覆盖把它变成一个连续的索引范围读。

代价：每个额外被索引/包含的列让**每次写**更新更多索引字节，膨胀索引大小，减慢 vacuum——索引是衍生数据，你在每次变异时付出代价。覆盖你最热的查询，不是所有的。
