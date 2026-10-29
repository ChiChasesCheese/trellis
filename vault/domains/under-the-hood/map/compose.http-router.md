%% trellis:begin %%
# HTTP 路由表：每个方法一棵基数树
*数据结构组合：开源框架里的类设计*

按 URL 找处理函数：逐条正则匹配太慢；httprouter / Gin 给每个 HTTP 方法建一棵基数树，路径参数（/user/:id）是特殊节点，查找基本只和路径长度有关，不随路由条数增长。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-http-router-1-spec]]
2. [[uth-compose-http-router-2-radix-tree]]
3. [[uth-compose-http-router-3-core-code]]
4. [[uth-compose-http-router-4-real-router]]
5. [[uth-compose-http-router-5-interview]]
%% trellis:end %%

## Notes
