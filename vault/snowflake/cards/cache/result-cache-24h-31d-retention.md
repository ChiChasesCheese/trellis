---
id: result-cache-24h-31d-retention
node: cache.result-cache
type: cloze
source: snowflake-docs
---
一条持久化查询结果在缓存中默认保留 {{c1::24}} 小时；此后每被重用一次，这个保留期就会重置一次，但最多只能从首次执行起累计延长到 {{c2::31}} 天，超过这个上限后结果被清除，下次提交相同查询会触发重新计算。
