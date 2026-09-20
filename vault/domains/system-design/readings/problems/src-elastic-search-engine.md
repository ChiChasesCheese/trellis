---
nodes: [problems.search.search-engine]
url: https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html
---
# Near real-time search

值得读：Elasticsearch 官方文档说明了默认每 1 秒做一次 refresh、缓冲文档写入新内存段后
才对查询可见的近实时机制，是"近实时索引"这个概念最权威的一手说明。本题解「需求」一节把
站内搜索的新鲜度目标定在 P99 < 10 秒，比这里的默认 1 秒刷新间隔更宽松，因为本题解的
预算还要覆盖变更事件从源系统传到索引摄取worker的排队延迟，而不只是刷新间隔本身；分段
和合并的更底层机制（segment 不可变、删除只是标记、合并压实）本题解不重复展开，见
[[storage.search|Search Indexes]] 域内相关卡片。
