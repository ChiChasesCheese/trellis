---
id: problems-multiplayer-game-disconnect-grace-pool
node: problems.realtime.multiplayer-game
type: qa
step: 6
tags: [grown]
---
## Q
In an online chess design, why should a disconnected player's offline time be deducted from a separate per-game 'disconnection grace pool' instead of directly from their own game clock, and why should the grace pool's initial size scale with the time control?

## A
Deducting offline time directly from the player's game clock conflates a network problem with the game's own thinking-time budget — a brief Wi-Fi drop would cost the same clock time as if the player had spent it thinking, which is unrelated to the game itself. A separate grace pool isolates connectivity issues from clock fairness: once the pool is exhausted, the choice of whether to keep waiting, offer a draw, or claim the win passes to the opponent rather than being decided automatically by the system. The pool's initial size should scale with the time control because a disconnect that's a minor inconvenience in a 30-minute game can single-handedly decide a 30-second bullet game if the grace period is the same fixed length in both.

## Q zh
在一个在线国际象棋设计中，为什么掉线玩家的离线时长应该从一个独立于该局本身时钟之外的'断线宽限池'里扣除，而不是直接从他自己的对局用时里扣？为什么这个宽限池的初始额度应该随用时制式的长短而变化？

## A zh
直接从玩家自己的对局时钟里扣离线时长，会把网络问题和棋局本身的思考用时预算混为一谈——一次短暂的 Wi-Fi 断连会消耗和真正思考同样多的时钟时间，而这和棋局本身毫无关系。用独立的宽限池把连接问题和时钟公平性隔离开：宽限池耗尽后，是继续等待、提和还是判对手获胜的选择权交给对手，而不是由系统自动决定。宽限池的初始额度应该随用时制式变化，因为如果两种制式用同样固定长度的宽限期，一次掉线在 30 分钟的慢棋里只是小麻烦，在 30 秒的超快棋里却足以单方面决定整局胜负。
