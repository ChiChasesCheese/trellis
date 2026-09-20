---
nodes: [problems.social.reddit]
url: https://news.ycombinator.com/item?id=1781013
---
# Hacker News 排序公式讨论帖

值得读：对 Hacker News 自己公开过的 Arc 源码（`news.arc`）里排序逻辑的讨论，给出公式
`(points - 1) / (age_hours + 2)^gravity`（`gravity = 1.8`）——一种"分母随时间连续变大"
的持续衰减方案，和 Reddit "分数是创建时刻的纯函数、只在新投票时才重算"的方案形成一组真实
存在的架构分歧。本题解选择了 Reddit 的做法并在正文里说明了原因：连续衰减意味着即使没有
新投票，所有帖子的相对排名理论上也在每一秒变化。
