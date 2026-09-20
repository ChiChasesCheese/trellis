---
id: problems-leaderboard-time-windowed-keys-not-in-place-reset
node: problems.realtime.leaderboard
type: qa
step: 5
tags: [grown]
---
## Q
For daily and weekly leaderboards that need to "reset" at the start of each period, why is clearing and reusing the same sorted set in place the wrong approach, and what key design avoids the problem while still supporting a reset?

## A
Clearing a single reused sorted set at the start of each period permanently destroys the previous period's final standings the moment the reset happens, with no way to look back at yesterday's or last week's results for history, disputes, or reward settlement after the fact. The alternative is to give each period its own independently-keyed sorted set (e.g. one key per calendar day, one per week), written to by fanning out each incoming score event to every period key it belongs to (daily, weekly, and an all-time key) rather than reading and aggregating on demand. "Resetting" then just means the next period's key starts empty by construction — nothing is destroyed — and an old period's key can be archived to durable storage and given an expiration with a grace window (e.g. a day or two) so it remains queryable for a while after the period ends before it's finally cleaned up.

## Q zh
对于需要在每个周期开始时「重置」的日榜和周榜，为什么原地清空并复用同一个有序集合是错误的做法？什么样的键设计能既避免这个问题、又支持重置？

## A zh
在每个周期开始时清空一个被反复复用的有序集合，会在重置发生的那一刻永久销毁上一个周期的最终排名，之后完全无法回看昨天或上周的结果用于历史查询、争议核实或事后的奖励结算。替代方案是给每个周期一个各自独立的键（例如每个自然日一个键、每周一个键），每条新到的分数事件被同时扇出写入它所属的每一个周期键（日榜键、周榜键、以及一个永久累积键），而不是按需读取时再聚合。这样「重置」只是意味着下一个周期的键从构造上就是空的——什么都没被销毁——而一个已结束周期的键可以被归档到持久存储，并设置一个带宽限期的过期时间（比如一到两天），让它在周期结束后仍可查询一段时间，最终再被清理。
