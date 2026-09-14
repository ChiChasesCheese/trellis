---
id: leetcode-c-postgresql-pg-trgm-application
node: topics.uncategorised
type: qa
anki: 1787361365625
tags: [algorithm::inverted-index, algorithm::n-gram, algorithm::set-similarity, application, case, case::postgresql-pg-trgm, category::storage-databases, chapter::08, chapter::12, leetcode, system::postgresql-pg_trgm]
---
## Q
pg_trgm 为什么能加速前缀不固定的 LIKE/相似搜索？为什么仍要 recheck？

## A
它索引字符串 trigrams，用查询 trigrams 从倒排结构取共享 token 的候选 rows。token overlap 只是一种过滤或相似度估计，候选仍需执行原始谓词确认。

**Evidence**

PostgreSQL 官方 pg_trgm 文档定义 trigram extraction、similarity operators 及 GiST/GIN index support。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20pg_trgm%EF%BC%9A%E4%B8%89%E5%85%83%E7%BB%84%E5%80%92%E6%8E%92%E4%B8%8E%E7%9B%B8%E4%BC%BC%E6%90%9C%E7%B4%A2)
