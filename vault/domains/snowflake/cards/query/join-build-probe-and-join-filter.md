---
id: join-build-probe-and-join-filter
node: query.join-strategies-broadcast-shuffle
type: qa
tags: [grown]
---
## Q
哈希连接中的 build 端与 probe 端各是什么？Snowflake 查询画像中出现的 JoinFilter 算子起什么作用？

## A
build 端是用来构建哈希表的输入，通常选较小的一侧；probe 端是逐行（按批）去哈希表中查找匹配的另一侧。JoinFilter 利用 build 端已知的连接键集合生成一个紧凑的过滤器，推到 probe 端的表扫描附近，在数据参与连接之前就丢弃不可能匹配的行，从而减少需要传输、重分布和探测的数据量。
