---
id: problems-llm-chat-service-per-tier-reserved-capacity
node: problems.realtime.llm-chat-service
type: qa
step: 6
tags: [grown]
---
## Q
In an LLM chat service where free and paying users share the same GPU fleet, why does a single global request queue with only per-user rate limiting fail to protect paying users during a surge of free-tier traffic, and what's the alternative admission-control design?

## A
Per-user rate limiting caps how fast any one user can send requests, but it does nothing about the aggregate effect of many free users being active at once — a surge across thousands of individual free users, each staying within their own rate limit, can still collectively saturate the shared GPU capacity that paying users' requests are waiting on, since the queue and the capacity pool are undifferentiated. The alternative is to reserve a fixed share of the GPU replica fleet per subscription tier (e.g. free, plus, enterprise each get their own slice) so tiers compete for capacity only within their own reservation; when a tier's own reserved capacity is exhausted, the admission controller rejects further requests from that tier (429 with a retry hint) rather than borrowing from another tier's reservation, even if the other tier's capacity is currently idle. This guarantees paying users' latency can't degrade because of free-tier volume, at the cost of not being globally utilization-optimal.

## Q zh
在一个免费用户和付费用户共享同一个 GPU 集群的 LLM 聊天服务中，为什么仅靠按用户做速率限制、所有人共用一个全局请求队列，无法在免费用户流量暴涨时保护付费用户？替代的准入控制设计是什么？

## A zh
按用户做速率限制只能约束单个用户发请求的速度，管不住「大量免费用户同时活跃」这种群体性效应——成千上万个各自都没超出自己速率限制的免费用户，叠加起来仍然可能把付费用户的请求正在等待的共享 GPU 容量打满，因为队列和容量池本身没有做区分。替代方案是按订阅档位为 GPU 副本集群预留固定比例的容量（例如免费、付费、企业各自拥有自己的份额），各档位只在自己的预留额度内竞争；当某个档位自己的预留容量耗尽时，准入控制器会拒绝该档位的后续请求（返回 429 和重试提示），而不会借用其他档位的预留容量，即使那部分容量当前是空闲的。这保证了付费用户的延迟不会因为免费用户的流量而变差，代价是集群整体利用率不是全局最优。
