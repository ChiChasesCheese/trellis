---
id: problems-multiplayer-game-turnbased-vs-realtime-tick-rate
node: problems.realtime.multiplayer-game
type: qa
step: 3
tags: [grown]
---
## Q
In a design where the average move in an active chess game arrives roughly every 6.86 seconds (from ~70 plies over an average 480-second game), versus a fast-paced real-time game simulating the world at a fixed 128 ticks per second, roughly how many times more frequently does the real-time game's authoritative server do active work per unit time for one concurrent game, and why does chess's authoritative server not need a fixed simulation loop at all?

## A
128 ticks/second versus about 1/6.86 ≈ 0.146 move-events/second works out to roughly 878x more frequent server work for the real-time game. Chess's server only needs to act when a move request actually arrives — the rest of the time the game's state machine is idle waiting for input — because there's no continuously changing world state between discrete moves. A real-time game has no such gaps: the world keeps evolving (physics, positions, hit detection) whether or not a player just acted, so its authoritative server must run a fixed-frequency loop regardless of input timing.

## Q zh
在一个设计里，一局进行中的国际象棋对局平均每 6.86 秒才有一步走子（来自平均 480 秒的对局中约 70 步半回合），而一款快节奏实时游戏以固定的 128 tick/秒持续模拟世界，对于一局并发对局而言，实时游戏的权威服务器每单位时间要做的活跃工作量大约是回合制的多少倍？为什么国际象棋的权威服务器完全不需要一个固定频率的模拟循环？

## A zh
128 tick/秒 对比约 1/6.86 ≈ 0.146 次走子事件/秒，算出实时游戏的服务器工作频率约是回合制的 878 倍。国际象棋的服务器只需要在真正收到走子请求时才行动——其余时间这局对局的状态机都在空闲等待输入——因为两步离散走子之间不存在持续变化的世界状态。实时游戏没有这种空档：不管玩家刚才是否有操作，物理、位置、命中判定这些世界状态都在持续演化，所以它的权威服务器必须不论输入时机如何都运行一个固定频率的循环。
