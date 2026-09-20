---
id: problems-news-feed-multipass-ranking-funnel
node: problems.social.news-feed
type: qa
step: 4
tags: [grown]
---
## Q
In a ranked news feed serving 200M daily active users where each user has over 1,000 ranking candidates per day on average, why is a single-stage 'run the heavy model on every candidate' ranking design computationally infeasible, and what architecture does Meta's real News Feed ranking system use instead?

## A
Running a heavy model on every candidate for every user works out to roughly 2x10^8 users x 1,000 candidates = 2x10^11 model inferences per day, which is not affordable at read-latency budgets. Meta's real architecture instead uses a multi-pass funnel: Pass 0 runs a lightweight model to narrow over 1,000 candidates down to about 500; Pass 1 runs a heavier multitask neural network to score only those ~500 candidates individually; Pass 2 applies contextual rules (like content-type diversity) to re-rank the final list. The expensive model only ever runs on the small candidate set that survives Pass 0.

## Q zh
在一个服务 2 亿日活用户的排序信息流（ranked feed）中，假设每个用户每天平均有超过 1,000 个排序候选，为什么'对每个候选都跑重模型'的单阶段排序方案在计算量上不可行？Meta 真实的信息流排序系统采用了什么架构来代替它？

## A zh
对每个用户的每个候选都跑重模型，计算量约为 2×10^8 用户 × 1,000 候选 = 2×10^11 次模型推理/天，在读延迟预算下完全无法承受。Meta 真实架构采用的是多阶段（multi-pass）漏斗：Pass 0 用轻量模型把超过 1,000 条候选筛到约 500 条；Pass 1 用较重的多任务神经网络只对这约 500 条逐条打分；Pass 2 应用上下文规则（如内容类型多样性）对最终列表重排。昂贵的模型自始至终只运行在 Pass 0 筛选后剩下的小候选集上。
