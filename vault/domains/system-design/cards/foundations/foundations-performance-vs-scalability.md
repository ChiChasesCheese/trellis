---
id: foundations-performance-vs-scalability
node: foundations.tradeoffs
type: qa
---
## Q
"The service is slow" — how do you tell a performance problem from a scalability problem, and why does the distinction matter?

## A
- **Performance problem**: slow for a *single* user even at low load — fix the code path (algorithms, queries, I/O).
- **Scalability problem**: fast when idle, degrades as *load grows* — fix the architecture (add nodes, remove shared bottlenecks, partition).

Matters because the fixes are disjoint: optimizing code won't save a system whose bottleneck is one shared database, and adding servers won't fix an O(n²) endpoint.


## Q zh
"这个服务很慢" — 你怎么区分性能问题和可扩展性问题，为什么这个区分很重要？

## A zh
- **性能问题**：即使在低负载下，单个用户也觉得慢 — 修代码路径（算法、查询、I/O）。
- **可扩展性问题**：空闲时很快，随着**负载增长**而恶化 — 修架构（加节点、去掉共享瓶颈、做分区）。

之所以重要，是因为两者的修法互不相干：优化代码救不了瓶颈是一个共享数据库的系统，加服务器也修不好一个 O(n²) 的端点。
