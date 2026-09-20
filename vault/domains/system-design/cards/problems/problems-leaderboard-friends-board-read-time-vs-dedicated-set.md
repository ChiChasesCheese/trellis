---
id: problems-leaderboard-friends-board-read-time-vs-dedicated-set
node: problems.realtime.leaderboard
type: qa
step: 6
tags: [grown]
---
## Q
For a friends-only leaderboard, why is maintaining a dedicated sorted set per user (containing only their friends) the wrong default, and what read-time alternative avoids the problem — and what other well-known fan-out problem is this the same trade-off as?

## A
A dedicated sorted set per user scales the number of maintained data structures with the total user count, and every friend-list change (adding or removing a friend) requires updating that structure — write cost and storage grow with the product of users and their average friend count, largely independent of how often anyone actually looks at their friends leaderboard. The read-time alternative looks up a user's (bounded, typically at most a few hundred) friend ids, batch-fetches their scores from the single global per-period sorted set, and sorts that small result set in the application layer on each request — avoiding any dedicated per-user structure and any need to keep one in sync with friend-graph changes, at the cost of a small amount of read-time compute. This is the same write-fan-out-vs-read-fan-out trade-off a social news feed faces deciding whether to push a new post into every follower's inbox versus assembling a feed by reading follows at request time; here, the read-time option wins because a friends leaderboard query is cheap and infrequent relative to the write amplification of the alternative.

## Q zh
对于一个好友专属排行榜，为什么给每个用户维护一份专属有序集合（只含其好友）是错误的默认做法？读时现算的替代方案如何避免这个问题？这和哪个知名的扇出问题是同一种权衡？

## A zh
为每个用户维护一份专属有序集合，意味着需要维护的数据结构数量随总用户数增长，而且每一次好友关系变化（加好友/删好友）都要更新这份结构——写入成本和存储量随「用户数 × 平均好友数」增长，且这个成本和实际有多少人真的会去查看好友榜基本无关。读时现算的替代方案是：查询该用户（数量有限，通常不超过几百）的好友 id 列表，从唯一的全局周期榜单里批量查询这些好友的分数，在应用层对这个小结果集排序后返回——不需要任何专属数据结构，也不需要让任何东西和好友关系的变化保持同步，代价只是每次请求时一点点排序计算。这和信息流场景里「发帖时把内容推给每个粉丝的收件箱」还是「读时现拉取关注列表拼装」是同一种写扇出 vs 读扇出的权衡；这里读时现算胜出，是因为一次好友榜查询相对于另一种方案的写放大而言足够便宜、足够不频繁。
