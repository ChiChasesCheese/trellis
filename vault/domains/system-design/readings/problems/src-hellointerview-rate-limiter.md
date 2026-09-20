---
nodes: [problems.foundations.rate-limiter]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter
tags: [no-archive]
---
# Distributed Rate Limiter

值得读：给出了一套完整的面试标准答案框架——API 网关放置、按一致性哈希扩展的 Redis
分片、以及"限流故障常与真实流量高峰同时发生，所以应该 fail-closed"的论证角度。本题解
在失败策略上和它分歧较大：本题解采用分层不对称的 fail-open（公平性层）+ 保守退化
（自保层）组合，对齐 Stripe 公开的真实做法，而不是它建议的整体 fail-closed；容量估算上
本题解也用具体算出的检查量（900,000 次/s）和所需分片数（14）替代了它更抽象的场景设定。
