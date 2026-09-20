---
id: problems-multiplayer-game-clock-lag-compensation
node: problems.realtime.multiplayer-game
type: qa
step: 5
tags: [grown]
---
## Q
In an online chess design, why does timing a move purely by 'when the server received the move request' unfairly penalize a player, and why is 'trust the client's self-reported thinking time' not an acceptable fix?

## A
If the server deducts time strictly from receipt timestamp, ordinary network latency between the client and server gets charged against the player's own thinking time — a player whose request takes an extra 300ms to arrive effectively loses 300ms of clock for a delay that wasn't their decision-making at all, which feels especially unfair under fast time controls. Trusting the client's self-reported elapsed time would fix the fairness problem but breaks the authoritative-server principle: a malicious client could simply under-report its thinking time to gain unlimited effective clock. The fix that preserves authority is having the server still time from its own receipt timestamp, but subtract a small fixed lag-compensation allowance before any time is actually deducted, absorbing ordinary jitter without trusting anything the client claims.

## Q zh
在一个在线国际象棋设计中，为什么单纯按'服务器收到走子请求的那一刻'来计时，会不公平地惩罚玩家？为什么'完全信任客户端自己上报的思考用时'不是一个可接受的修复方案？

## A zh
如果服务器严格按收到请求的时间戳扣时间，客户端和服务器之间正常的网络延迟就会被算进玩家自己的思考用时里——一次请求多花 300 毫秒才到达，玩家实际上就白白损失了这 300 毫秒的时钟，而这根本不是他的决策时间，在用时紧张的快棋制式下尤其不公平。信任客户端自己上报的用时能解决公平性问题，但破坏了权威服务器的原则：恶意客户端完全可以谎报更短的思考用时来变相获得无限的有效时间。既保持权威性又解决公平性的做法是：服务器依然按自己收到请求的时间戳计时，但在真正扣减时间之前先减去一个小的固定滞后补偿值，用来吸收正常的网络抖动，同时不信任客户端上报的任何数值。
