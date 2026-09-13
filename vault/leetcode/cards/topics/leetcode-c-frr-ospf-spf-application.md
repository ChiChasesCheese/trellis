---
id: leetcode-c-frr-ospf-spf-application
node: topics.uncategorised
type: qa
anki: 1787361363173
tags: [algorithm::dijkstra, algorithm::priority-queue, algorithm::shortest-path-tree, application, case, case::frr-ospf-spf, category::distributed-streaming, chapter::06, chapter::08, leetcode, system::frrouting, system::ospf]
---
## Q
OSPF 中 flooding 与 Dijkstra 分别负责什么？为什么每台路由器都要自己算一次？

## A
flooding 传播链路状态数据库；Dijkstra 在本地快照上以当前路由器为根计算 shortest-path tree。根不同，next hop 也不同，所以每台路由器独立计算。

**Evidence**

RFC 2328 描述 SPF tree 计算；FRRouting 官方文档说明 OSPF daemon、LSDB 与 SPF 行为。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FFRRouting%20OSPF%EF%BC%9ADijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF%E5%BE%84%E6%A0%91)
