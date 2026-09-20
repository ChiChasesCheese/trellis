---
id: problems-web-crawler-mercator-front-back-queues
node: problems.search.web-crawler
type: qa
step: 2
tags: [grown]
---
## Q
In the Mercator-style URL frontier design for a web crawler, why does the number of back queues need only scale with worker concurrency (thousands) rather than with the total number of distinct hosts ever discovered (which can be hundreds of millions), while still guaranteeing at most one in-flight request per host?

## A
Front queues hold URLs bucketed by priority and feed a much smaller set of back queues; a routing table binds each back queue to exactly one host at a time, and a worker only pulls from the back queue whose bound host is next allowed to be fetched (tracked via a min-heap of per-host next-allowed-fetch times). Because at any given moment only as many hosts are actively being crawled as there are workers, the back queues only need to represent that active subset, not every host ever seen — most discovered hosts have no URL in flight at all at a given instant, so they don't need a dedicated permanent queue.

## Q zh
在 Mercator 风格的爬虫 URL frontier 设计中，为什么后端队列（back queue）的数量只需要跟 worker 并发度（几千级）同量级，而不需要跟历史上曾发现过的宿主总数（可能是几亿）同量级，却仍能保证任意时刻对一个宿主最多只有一个在途请求？

## A zh
前端队列按优先级把 URL 分桶，喂给数量小得多的后端队列；一张路由表把每个后端队列在任意时刻绑定到恰好一个宿主，worker 只从「其绑定宿主当前允许被抓取」的后端队列取 URL（通过一个按各宿主下次允许抓取时间排序的最小堆来判断）。因为在任意时刻真正处于活跃抓取状态的宿主数量最多等于 worker 数量，后端队列只需要代表这个活跃子集，而不是历史上见过的每一个宿主——绝大多数已发现的宿主在某一时刻根本没有在途 URL，不需要为它们常驻一个专属队列。
