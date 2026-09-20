---
id: problems-leaderboard-server-authoritative-score-submission
node: problems.realtime.leaderboard
type: qa
step: 8
tags: [grown]
---
## Q
Why is having the game client submit its own final score directly to a leaderboard API a weak anti-cheat design, and what structural change closes off the cheapest class of cheating, even though it doesn't eliminate cheating entirely?

## A
A client-submitted final score trusts an input source that is fully under the attacker's control — the score can be forged by modifying the client, replaying a captured request, or calling the API directly, with no game logic ever actually enforced. The structural fix is to never accept a final score directly from the client at all: scores can only be written by a trusted backend match-settlement service that computes the result from the authoritative game state it observed, not from a number the client asserts. This doesn't eliminate cheating — a flaw in the settlement service's own logic could still be exploited — but it closes off the cheapest and most common attack, forging a single request, which no amount of after-the-fact anomaly detection can substitute for as a first line of defense.

## Q zh
为什么让游戏客户端直接把自己算出的最终分数提交给排行榜 API 是一种薄弱的反作弊设计？什么样的结构性改变能堵住成本最低的一类作弊，即便它不能彻底消灭作弊？

## A zh
客户端提交的最终分数信任了一个完全被攻击者控制的输入源——分数可以通过修改客户端、重放抓到的请求、或者直接调用 API 来伪造，游戏逻辑本身从未被真正执行过。结构性的修复是彻底不再直接接受来自客户端的最终分数：分数只能由一个受信任的后端比赛结算服务写入，这个服务根据它自己观测到的权威比赛状态计算结果，而不是客户端自己断言的一个数字。这不能消灭作弊——结算服务自身的逻辑漏洞仍可能被利用——但它堵死了成本最低、也最常见的一类攻击，即伪造一次请求，而任何事后的异常检测都无法替代这第一道防线。
