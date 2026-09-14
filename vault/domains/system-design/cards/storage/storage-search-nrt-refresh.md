---
id: storage-search-nrt-refresh
node: storage.search
type: qa
---
## Q
In Elasticsearch, a document is indexed successfully but a search doesn't find it for another second. Explain the mechanism — and why durability is a *separate* knob.

## A
Searchability requires a **refresh**: buffered docs are written into a new in-memory **segment** and only then become visible to queries. Refresh runs every 1s by default ("near-real-time") because opening segments per-document would be ruinously expensive.

Durability is independent: every operation is also appended to the **translog** (fsynced by default before acking), so an un-refreshed doc survives a crash — it's durable but not yet searchable.

Levers: lengthen `refresh_interval` (or `-1`) during bulk loads for big ingest speedups; use `?refresh=wait_for` when a workflow must read-its-write; GET-by-ID bypasses refresh entirely.

## Q zh
在 Elasticsearch 中，文档被成功索引但搜索再过一秒才找到它。解释机制——为什么持久性是**独立**的旋钮。

## A zh
可搜索性需要**刷新**：缓冲文档被写进一个新的内存**分段**，只有那时才对查询变可见。刷新默认每 1 秒运行（"近实时"），因为每文档打开分段会非常昂贵。

持久性是独立的：每个操作也被 append 到**translog**（默认在 acking 前 fsynced），所以未刷新的文档在崩溃时存活——它持久但还不可搜索。

杠杆：在 bulk 加载期间延长 `refresh_interval`（或 `-1`）以获得大摄入加速；当工作流必须读-其-写时使用 `?refresh=wait_for`；GET-by-ID 完全绕过刷新。
