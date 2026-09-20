---
id: problems-llm-chat-service-10x-model-routing-lever
node: problems.realtime.llm-chat-service
type: qa
step: 8
tags: [grown]
---
## Q
As an LLM chat service scales DAU by roughly 10x, why does simply adding a proportional number of GPUs stop being the primary scaling lever, and what design change takes over as the main way to keep serving demand?

## A
GPU fleet size for the decode tier scales close to linearly with peak concurrent sessions, which scales with request volume — so a 10x growth in DAU pushes toward roughly a 10x growth in GPU count, quickly reaching a scale where a single region or cluster is no longer practical, and where GPU supply itself (not budget) becomes hard to source on short notice. The lever that changes the scaling curve is routing requests to differently-sized models rather than running every request through the same large model: cheap, fast requests get served by a small or distilled model, and only requests that need the large model's capability are escalated to it. This turns "serve more requests" from "acquire proportionally more GPUs of the largest model" into "serve more requests per GPU" by shrinking the fraction of traffic that needs the most expensive model at all.

## Q zh
当一个 LLM 聊天服务的 DAU 增长约 10 倍时，为什么单纯按比例增加 GPU 数量不再是主要的扩展杠杆？取而代之成为维持服务能力的主要设计变化是什么？

## A zh
解码层的 GPU 集群规模大致随峰值并发会话数线性增长，而并发会话数又随请求量增长——所以 DAU 增长 10 倍会把 GPU 数量也推高约 10 倍，很快到达单一区域或单一集群不再现实的规模，GPU 供给本身（而不是预算）也会变得难以在短时间内采购到。真正改变这条增长曲线的杠杆是把请求路由到大小不同的模型，而不是让每个请求都跑同一个大模型：便宜、简单的请求交给一个小型或蒸馏模型处理，只有真正需要大模型能力的请求才升级过去。这把「服务更多请求」从「按比例采购更多跑最大模型的 GPU」，变成了「每张 GPU 服务更多请求」，因为需要最贵模型的流量占比被主动压缩了。
