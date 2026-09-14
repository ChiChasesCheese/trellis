---
id: architecture-serverless-economics
node: architecture.serverless
type: qa
---
## Q
When does per-request (FaaS) pricing beat owning servers, and when does it flip?

## A
FaaS wins when utilization is **low or spiky**: you pay only for execution time, and idle costs zero — cron jobs, webhooks, rare admin endpoints, unpredictable bursts, and scale-to-zero for anything with dead hours. You're also buying off the ops bill (patching, capacity planning, autoscaling config).

It flips at **steady, high utilization**: per-invocation pricing carries a large premium over the same compute as reserved instances/containers — a server busy most of the day is several-fold cheaper than the equivalent Lambda-hours. High-throughput constant traffic on FaaS is the classic cost horror story.

Interview answer shape: "spiky or idle → serverless; flat and busy → provisioned; measure the crossover in $/vCPU-hour at your duty cycle."

## Q zh
什么时候 per-request（FaaS）定价打败拥有服务器，何时翻转？

## A zh
FaaS 赢得当使用率**低或峰值**：你仅支付执行时间，空闲成本零——cron 工作、webhook、罕见管理端点、不可预测的突发、scale-to-zero 对任何有死小时。你也正在买断 ops 账单（补丁、容量计划、自动缩放配置）。

它在**稳定、高使用率**翻转：每调用定价对相同的计算作为预留实例/容器带有大高级——一个服务器大部分时间忙是几倍更便宜比等价的 Lambda 小时。高吞吐恒定流量在 FaaS 是经典成本恐怖故事。

面试答案形状："峰值或空闲 → serverless；平面和忙 → 已配置；测量在 $/vCPU-小时的交叉点在你的职责周期。"
