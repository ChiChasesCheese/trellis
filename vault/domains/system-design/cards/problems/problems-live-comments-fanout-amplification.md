---
id: problems-live-comments-fanout-amplification
node: problems.social.live-comments
type: qa
step: 1
tags: [grown]
---
## Q
In a live-comments broadcast system, a video has 10 million concurrent viewers and comments arrive at about 167/second. If every comment were pushed to every viewer, roughly how many delivery events per second does that require, and why does this number alone rule out a naive "broadcast every comment to every connection" design?

## A
167 comments/sec × 10,000,000 viewers ≈ 1.67 billion delivery events/second. No realistic fleet can perform anywhere near that many push operations per second — the amplification is per-viewer, so adding more servers to hold connections doesn't reduce this total; it only redistributes it. This single number is what forces a design to sample or rate-limit the broadcast itself (deciding not to forward every comment to every viewer) rather than just adding more gateway capacity.

## Q zh
在一个直播评论广播系统中，一场直播有 1000 万并发观众，评论以约 167 条/秒的速度到达。如果每条评论都推送给每个观众，大约需要多少次/秒的投递事件？为什么这一个数字本身就排除了"每条评论广播给每个连接"的朴素设计？

## A zh
167 条/秒 × 1000 万观众 ≈ 16.7 亿次投递事件/秒。没有任何现实系统能以这个速率执行推送操作——这个放大是按每个观众发生的，所以加更多服务器持有连接并不能降低这个总量，只是把它重新分摊。正是这一个数字迫使设计必须对广播本身做采样或限速（决定不把每条评论都转发给每个观众），而不是单纯增加网关容量。
