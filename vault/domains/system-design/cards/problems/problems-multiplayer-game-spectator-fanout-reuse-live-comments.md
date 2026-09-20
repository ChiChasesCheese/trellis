---
id: problems-multiplayer-game-spectator-fanout-reuse-live-comments
node: problems.realtime.multiplayer-game
type: qa
step: 7
tags: [grown]
---
## Q
In an online chess design, why is broadcasting moves to hundreds of thousands of spectators of one viral game structurally the same fan-out problem as a live-comment broadcast, and why does it not need that system's sampling/rate-limiting degradation strategy?

## A
Both are the same shape of problem: one event source (a move, or a comment) needs to reach every subscriber of one shared channel (a gameId, or a video id), and the subscriber count can scale from single digits to hundreds of thousands — the fix is the same broadcast-bus-plus-gateway-fanout architecture in both cases, not something a game service should reinvent. They differ in event rate: a game's move events arrive roughly every several seconds even under heavy spectator load, far below a busy live stream's comment rate, so the load spectators add is concentrated in connection count and fan-out width rather than event-production rate — the sampling/rate-limiting degradation a live-comment system needs to survive its own event volume isn't necessary here.

## Q zh
在一个在线国际象棋设计中，为什么把一场爆红对局的走子广播给几十万观众，在结构上和直播评论的广播是同一个扇出问题？为什么它不需要直播评论方案里的采样/限速降级策略？

## A zh
两者是同一种问题形状：一个事件源（一步走子，或一条评论）需要触达同一个共享频道（一个 gameId，或一个视频 id）的全部订阅者，订阅者数量可以从个位数扩展到几十万——两种场景下的修复方案都是同一套广播总线加网关扇出的架构，而不该由对局服务自己重新发明一套。两者的区别在事件产生速率上：即使在观众压力很大的情况下，一局对局的走子事件依然大约每几秒才产生一次，远低于一场热门直播的评论产生速率，所以观众带来的压力集中在连接数和扇出宽度上，而不是事件产生速率上——直播评论系统为了扛住自身事件量而需要的采样/限速降级，在这里并不需要。
