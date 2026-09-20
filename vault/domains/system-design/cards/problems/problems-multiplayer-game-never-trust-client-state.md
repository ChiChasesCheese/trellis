---
id: problems-multiplayer-game-never-trust-client-state
node: problems.realtime.multiplayer-game
type: qa
step: 2
tags: [grown]
---
## Q
In an online chess design, why must the server never accept a client's own report of the board state, clock values, or game outcome as authoritative, even though the client already validates moves locally for UI responsiveness?

## A
Local client validation only prevents accidental UI mistakes; it does nothing to stop a modified or malicious client from submitting a fabricated request, such as an illegal move or a false 'checkmate' outcome. The server holds the only authoritative current state (current board position and both clocks) and derives every update solely from move requests it has itself validated against that state — this is the same principle Riot states for real-time games ('a server must never trust a client's view of the world'), applied to a turn-based game's state machine instead of a continuously simulated world.

## Q zh
在一个在线国际象棋设计中，即使客户端已经在本地做走子合法性校验以提升响应体验，为什么服务器绝不能把客户端自己上报的棋盘状态、时钟数值或对局结果当作权威事实？

## A zh
客户端本地校验只能防止 UI 层面的误操作，无法阻止一个被修改过的恶意客户端直接提交伪造的请求，比如一步非法走子，或一个虚假的'已将死'结果。服务器持有唯一权威的当前状态（当前局面和双方时钟），每一次更新都只能由服务器自己针对这份状态校验通过的走子请求推导出来——这和 Riot 在实时游戏里强调的'服务器绝不能信任客户端对世界状态的上报'是同一个原则，只是应用在回合制的状态机上，而不是持续模拟的世界上。
