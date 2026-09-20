---
id: problems-multiplayer-game-statistical-anticheat-review-queue
node: problems.realtime.multiplayer-game
type: qa
step: 8
tags: [grown]
---
## Q
In an online chess design, why should engine-assist cheat detection be built as a statistical model that flags suspicious players for human review, rather than a rule that automatically bans players whose moves match a chess engine's top choice too often?

## A
Move quality naturally varies with a player's skill, and even strong human players sometimes match an engine's top move by legitimate skill or by the position simply having one clearly best move — a fixed match-rate threshold would produce false positives against strong, honest players. A statistically grounded approach instead compares a player's observed move-quality distribution against what their official rating would predict, converting the deviation into a significance measure (a z-score-style statistic, as in academic chess cheat-detection research) so suspicion scales with how implausible the deviation is. That score should route to human review, not an automatic verdict, since a wrongly banned honest player is a much worse outcome than a delayed detection of an actual cheater.

## Q zh
在一个在线国际象棋设计中，为什么检测借助引擎辅助作弊应该建成一个把可疑玩家标记出来交给人工复核的统计模型，而不是一条'走子和引擎首选一致率过高就自动封号'的规则？

## A zh
走子质量本身会随玩家实力自然变化，即使是很强的人类玩家，也可能因为真实水平高、或者某个局面本来就只有一步明显最优解，而经常和引擎的首选走法一致——固定的一致率阈值会对实力强但诚实的玩家产生大量误判。统计化的方法则是把玩家实际观察到的走子质量分布，和其官方评分'应有'的质量分布相比较，把偏差转换成一个统计显著性指标（类似学术界棋类反作弊研究里用的 z-score），可疑程度随偏差有多不可能而变化。这个分数应该导向人工复核，而不是自动判决，因为错误封禁一个诚实玩家的代价，远高于延迟发现一个真正作弊者的代价。
