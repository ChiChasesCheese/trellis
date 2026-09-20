---
id: problems-live-comments-10x-sampling-tightens
node: problems.social.live-comments
type: qa
step: 8
tags: [grown]
---
## Q
At 10x scale (peak concurrent viewers on the largest live video growing from 10 million to 100 million, and the posted comment rate growing proportionally with it), what happens to the gateway's per-connection push load and to the broadcast sampling ratio, and why do they change for different reasons?

## A
The gateway's push load is unaffected by this growth: since comments are batched into one frame per connection per fixed interval, a gateway's frame-send rate stays at connections/interval (e.g. still 50,000 frames/sec at 50,000 connections and a 1-second interval) regardless of how many comments were posted — scaling the fleet from 200 to 2,000 gateways handles the extra connections without any per-gateway throughput change. The sampling ratio, however, does tighten — from about 1/42 to about 1/417 — because it's driven by the posted comment rate relative to a fixed per-viewer reading-speed target (unchanged at ~4/sec): if 10x more people are watching and commenting proportionally, roughly 10x more comments compete for the same fixed reading-speed budget, so a proportionally smaller fraction can be shown live. The product consequence is that what viewers see live becomes an even sparser sample of all comments, which should be surfaced explicitly in the UI rather than left implicit.

## Q zh
在 10 倍规模下（最大直播的峰值并发观众从 1000 万增长到 1 亿，且评论发出速率随之成比例增长），网关每连接的推送负载和广播采样比例分别会怎样变化？为什么它们变化的原因不同？

## A zh
网关的推送负载不受这次增长影响：因为评论被按固定间隔打包成每连接一帧，网关的帧发送速率始终是连接数/间隔（例如 5 万连接、1 秒间隔下仍是每秒 5 万帧），和评论发出了多少条无关——把网关数从 200 台扩到 2,000 台就能应付新增的连接数，单台网关的吞吐不用变。但采样比例确实会收紧——从约 1/42 收紧到约 1/417——因为它由"评论发出速率相对固定的单观众阅读速度目标（仍是约 4 条/秒）"决定：如果观看和评论的人数都涨了 10 倍，大约就有 10 倍多的评论在争夺同一份不变的阅读速度预算，能被实时展示的比例就要相应缩小。产品后果是观众实时看到的会变成全部评论中更稀疏的一个样本，这应该在 UI 上明确提示，而不是留给观众自己猜。

