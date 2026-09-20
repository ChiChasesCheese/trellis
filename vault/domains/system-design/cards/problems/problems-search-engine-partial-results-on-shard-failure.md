---
id: problems-search-engine-partial-results-on-shard-failure
node: problems.search.search-engine
type: qa
step: 7
tags: [grown]
---
## Q
In a document-partitioned search system, what should the search aggregator do when one of the shards it fans out to doesn't respond within the query's latency budget, and why is this better than failing the whole query?

## A
The aggregator should return the results collected from the shards that did respond in time, along with an explicit `partial: true` flag in the response, rather than waiting indefinitely or failing the entire query because one shard is unavailable. Since the index is document-partitioned, every shard holds a distinct slice of the corpus, so a missing shard means some matching documents are absent from the results (reduced recall) — but the results that are present are still valid. Returning a mostly-correct, explicitly-marked-partial result set is a better trade than making the whole search feature unavailable because of one slow or down shard out of many.

## Q zh
在一个按文档分片的搜索系统中，当扇出对象里的某个分片没有在查询的延迟预算内响应时，聚合器应该怎么做？为什么这比让整个查询失败更好？

## A zh
聚合器应该返回已经按时响应的那些分片收集到的结果，并在响应里显式标注 `partial: true`，而不是无限等待或者因为一个分片不可用就让整个查询失败。由于索引是按文档分片的，每个分片持有语料的一个独立切片，缺失一个分片意味着一部分匹配的文档不在结果里（召回率下降）——但已经返回的那些结果仍然是有效的。相比因为众多分片中的一个变慢或宕机就让整个搜索功能不可用，返回一份大部分正确、明确标注为不完整的结果集是更好的取舍。
