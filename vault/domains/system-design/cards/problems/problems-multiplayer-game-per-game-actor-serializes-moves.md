---
id: problems-multiplayer-game-per-game-actor-serializes-moves
node: problems.realtime.multiplayer-game
type: qa
step: 4
tags: [grown]
---
## Q
In an online chess design, why does giving each in-progress game its own single-threaded actor (holding that game's mutable state and processing its move requests one at a time) avoid the need for a distributed lock when two moves for the same game arrive nearly simultaneously?

## A
Because exactly one actor instance owns a given game's state and that actor processes incoming move requests for the game strictly one at a time, two near-simultaneous requests for the same game are naturally serialized by the actor's own message queue rather than by any external locking mechanism — the second request is simply evaluated against the state left by the first. This only works because state and concurrency control are both scoped to a single game: different games run on independent actors with no shared mutable state, so there is nothing to lock across games in the first place.

## Q zh
在一个在线国际象棋设计中，为什么给每一局进行中的对局分配一个独立的单线程 actor（持有该局的可变状态、逐个处理走子请求），能在同一局的两步走子几乎同时到达时，不需要引入分布式锁？

## A zh
因为某一局对局的状态恰好只由一个 actor 实例持有，且这个 actor 严格按顺序、一次处理一个走子请求，同一局的两个几乎同时到达的请求会被 actor 自己的消息队列自然串行化，而不依赖任何外部加锁机制——后到达的请求只是基于前一个请求处理完之后的状态被评估。这之所以成立，是因为状态和并发控制都被限定在单局范围内：不同对局运行在互相独立的 actor 上、没有共享的可变状态，所以对局之间本来就不存在需要加锁的东西。
