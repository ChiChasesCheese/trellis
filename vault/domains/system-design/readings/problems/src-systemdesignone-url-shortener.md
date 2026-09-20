---
nodes: [problems.foundations.url-shortener]
url: https://systemdesign.one/url-shortening-system-design/
tags: [no-archive]
---
# URL Shortening System Design

值得读：提出用布隆过滤器（Bloom filter）挡住对不存在短码的重复查询，以及用倒排索引避免同一长 URL 被重复缩短——两点都被本题解采纳。它给出的 5 年 1.6PB 存储估算比本题解大约 1750 倍，本题解在容量估算一节指出差距主要来自 DAU 假设和单行字节数假设，而非方法本身有误。
