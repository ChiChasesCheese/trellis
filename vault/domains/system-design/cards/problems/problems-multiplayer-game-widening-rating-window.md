---
id: problems-multiplayer-game-widening-rating-window
node: problems.realtime.multiplayer-game
type: qa
step: 1
tags: [grown]
---
## Q
In an online chess matchmaking design, why does the rating window used to pair opponents start narrow (e.g. plus or minus 100) and widen the longer a player waits (e.g. plus or minus 50 every 2 seconds), rather than using one fixed window width for everyone?

## A
A fixed narrow window keeps match quality high but can leave players waiting indefinitely when few compatible opponents are online; a fixed wide window guarantees fast matches but frequently pairs mismatched opponents, hurting both the game experience and the accuracy of rating updates (which assume comparable opponents). Widening the window only as wait time grows gets the best of both: short waits still get tight, high-quality matches, and the window only loosens once it's clear a tight match isn't available soon — trading match quality for wait time only when necessary rather than upfront for everyone.

## Q zh
在一个在线国际象棋匹配设计中，为什么用来配对对手的评分窗口从一个较窄的值开始（例如 ±100），随着等待时间增长而扩大（例如每等待 2 秒扩大 ±50），而不是给所有人用一个固定宽度的窗口？

## A zh
固定的窄窗口能保持高匹配质量，但在符合条件的在线对手不多时，可能让玩家无限期等待；固定的宽窗口能保证快速匹配，但经常配对到实力悬殊的对手，既损害游戏体验，也影响评分更新的准确性（评分更新假设对局双方实力接近）。只在等待时间变长时才扩大窗口，能同时兼顾两者：短等待依然能获得严格、高质量的匹配，只有在确实短期内找不到合适对手时窗口才放宽——用等待时间换匹配质量，而不是一开始就对所有人做这个取舍。
