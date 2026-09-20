---
id: problems-url-shortener-10x-100x-evolution
node: problems.foundations.url-shortener
type: qa
step: 8
tags: [grown]
---
## Q
In a URL shortener design, what changes structurally when redirect traffic grows from a baseline peak of about 5,800 QPS to 10x (~58,000 QPS) and then 100x (~580,000 QPS)?

## A
At 10x, the system moves to multi-region deployment: each region gets a disjoint counter range for short-code creation (e.g., region A gets 0–1B, region B gets 1B–2B) so creation needs no cross-region coordination, and redirect logic is pushed to edge compute (e.g., Cloudflare Workers or Lambda@Edge) so most redirects never reach the origin. At 100x, the short_code → long_url mapping itself is replicated into an edge key-value store (e.g., DynamoDB Global Tables or a CDN's edge KV), so the origin database becomes mainly a write target and source of truth rather than something most reads touch, and analytics shifts from per-click aggregation to sampled counting because exact click counts stop being worth their write throughput at that volume.

## Q zh
在一个短链接设计中，当重定向流量从基准峰值约 5,800 QPS 增长到 10 倍（约 58,000 QPS）、再到 100 倍（约 58 万 QPS）时，系统结构上会发生什么变化？

## A zh
在 10 倍规模，系统转向多区域部署：每个区域拿到不相交的计数器区间用于短码创建（例如区域 A 为 0–10 亿，区域 B 为 10 亿–20 亿），创建路径不再需要跨区域协调，重定向逻辑下沉到边缘计算（例如 Cloudflare Workers 或 Lambda@Edge），使得大多数重定向永远不会到达源站。在 100 倍规模，short_code → long_url 映射本身被复制到边缘键值存储（例如 DynamoDB Global Tables 或 CDN 的边缘 KV）中，源站数据库主要变成写入目标和最终真源，而不是大多数读请求会触达的地方；分析也从逐次点击聚合转为采样统计，因为在这个量级下精确点击计数的价值已经比不上它占用的写吞吐。
