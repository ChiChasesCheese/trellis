---
id: problems-live-comments-sampling-ratio
node: problems.social.live-comments
type: qa
step: 4
tags: [grown]
---
## Q
In a live-comments system, why is the target push rate for the real-time broadcast set by how fast a person can read comments rather than by what a gateway can push, and what sampling ratio results when comments are posted at about 167/second and the system batches sampled comments into one frame per connection every second?

## A
A gateway holding tens of thousands of connections and batching comments into one frame per connection per interval has a push rate that depends only on connection count and the batching interval — e.g. 50,000 connections / 1-second interval = 50,000 frame-sends/second — not on how many comments were posted, so gateway throughput isn't actually the binding constraint once batching is in place. The real limit is that a person can follow only about 3-5 comments a second, so the system targets a fixed per-viewer delivery rate (this design uses 4/second) and derives the sampling ratio as that target divided by the posted comment rate: 4 / 166.7 ≈ 1/42 — roughly 1 comment in 42 is selected for the live broadcast at this comment rate, not 1 in thousands. Comments that aren't sampled are still persisted and remain visible in non-realtime views (e.g. browsing full comment history); only the live broadcast stream excludes them.

## Q zh
在一个直播评论系统中，为什么实时广播的目标推送速率应该由人的阅读速度决定，而不是由网关能推多快决定？当评论以约 167 条/秒的速度发出、系统把采样后的评论按每个连接每秒一帧打包推送时，得到的采样比例是多少？

## A zh
一台持有数万个连接、并把评论按每个连接每个间隔打包成一帧推送的网关，其推送速率只取决于连接数和打包间隔——例如 5 万个连接 / 1 秒间隔 = 每秒 5 万次帧发送——和评论发出了多少条无关，所以一旦引入批量打包，网关吞吐其实并不是真正的约束。真正的上限是一个人同一时间只能跟上大约每秒 3-5 条评论，所以系统把单观众的目标送达速率定为一个固定值（本设计取每秒 4 条），并把采样比例算成这个目标除以评论发出速率：4 / 166.7 ≈ 1/42——在这个评论速率下大约每 42 条评论挑 1 条进入实时广播，而不是千分之一。没被采样命中的评论仍然被持久化，仍然可以通过非实时视图（比如浏览完整评论历史）看到，只有实时广播流会排除它们。

