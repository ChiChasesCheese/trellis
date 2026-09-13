---
id: leetcode-c-postgresql-wal-application
node: topics.uncategorised
type: qa
anki: 1787359913393
tags: [algorithm::append-only-log, algorithm::checkpointing, algorithm::monotonic-sequence, algorithm::write-ahead-log, application, case, case::postgresql-wal, category::storage-databases, leetcode, system::postgresql]
---
## Q
PostgreSQL 为什么能在事务提交时不立刻刷完所有脏数据页？WAL 的核心不变量是什么？

## A
描述修改的 WAL record 必须先于对应数据页持久化。提交先确保必要 WAL durable；脏页可以稍后批量写回。崩溃后从 checkpoint 附近开始按 LSN 重放 WAL，把尚未写入数据文件的修改 REDO。

**Evidence**

PostgreSQL 官方 WAL 文档明确规定 data file changes 只能在对应 WAL records flushed 后写入，并说明 LSN 是单调递增的 WAL byte offset。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20WAL%EF%BC%9A%E5%85%88%E5%86%99%E6%97%A5%E5%BF%97%E5%86%8D%E5%86%99%E6%95%B0%E6%8D%AE%E9%A1%B5)
