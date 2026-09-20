---
id: problems-search-engine-derived-index-not-writable-directly
node: problems.search.search-engine
type: qa
step: 3
tags: [grown]
---
## Q
In a post-search design, why does the search API deliberately not expose any endpoint for a client to write directly into the search index, and how does new content reach the index instead?

## A
If clients (or the application's own post-creation path) could write directly to the search index, there would be no single point enforcing consistency between the index and the system of record (the post-creation database), and a partial or reordered write could silently desynchronize them. Instead, the search index is only ever updated through an asynchronous change-event pipeline: the post service (the system of record) emits domain events like `PostCreated` or `LikeMilestone`, which flow through a queue to index ingestion workers that write into the owning shard. This keeps the index a rebuildable, eventually-consistent derived view rather than a second, independently writable source of truth.

## Q zh
在一个站内帖子搜索设计中，为什么搜索 API 故意不暴露任何让客户端直接写入搜索索引的接口？新内容是通过什么路径进入索引的？

## A zh
如果客户端（或应用自身的发帖路径）可以直接写入搜索索引，就没有任何单点能强制索引和权威数据源（发帖数据库）保持一致，一次不完整或乱序的写入就可能让两者悄悄产生分歧。正确做法是索引只能通过一条异步的变更事件管道更新：帖子服务（权威数据源）发出 `PostCreated`、`LikeMilestone` 这类领域事件，事件经过队列流向索引摄取 worker，由 worker 写入对应的分片。这样索引始终是一个可重建的、最终一致的衍生视图，而不是一个可以被独立写入的第二数据源。
