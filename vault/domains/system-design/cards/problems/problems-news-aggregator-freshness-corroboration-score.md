---
id: problems-news-aggregator-freshness-corroboration-score
node: problems.search.news-aggregator
type: qa
step: 6
tags: [grown]
---
## Q
In a news aggregator's ranking design, why does combining exponential time decay with a log-dampened corroboration count (rather than either signal alone) let a well-corroborated older story compete with a fresher, thinly-sourced one, and what does a worked example show?

## A
Pure chronological ranking gives an unverified single-source article the same prominence as a widely-corroborated major story; pure corroboration ranking lets a story that accumulated many sources earlier in the day keep outranking a genuinely new story until the new one accumulates comparable corroboration, by which point it is no longer news. Multiplying an exponential time-decay factor by log(1 + corroboration_count) balances both: the log keeps a story's marginal 50th source from moving its score much once it's already well-corroborated, while decay keeps pulling older stories down. With a 6-hour half-life, a story 2 hours old with 1 source (authority weight 0.9) scores about 0.495, while a story 10 hours old with 12 corroborating sources (average authority weight 0.6) scores about 0.485 — nearly tied, showing the design deliberately lets the two signals compete rather than letting either dominate outright.

## Q zh
在一个新闻聚合器的排序设计中，为什么把指数时间衰减和对数压缩的佐证来源数结合起来（而不是只用其中一个信号）能让一条被广泛佐证的旧故事和一条更新但佐证尚少的故事相互竞争？一个具体算例展示了什么？

## A zh
纯时间倒序会让一篇未经证实的单一来源文章获得和被广泛佐证的重大报道相同的展示权重；纯佐证数量排序会让一条当天早些时候就积累了大量来源的故事持续压制一条真正新出现的故事，直到后者也积累出可比的佐证数——那时它往往已经不再是「新」闻了。把指数时间衰减因子乘以 `log(1+佐证来源数)` 平衡了两者：对数项让一个故事已经被广泛佐证后，边际的第 50 个来源不会再明显推高分数，而衰减持续把旧故事往下拉。取 6 小时半衰期：一条 2 小时前发布、1 个来源（权威度 0.9）的故事得分约 0.495，一条 10 小时前发布、12 个佐证来源（平均权威度 0.6）的故事得分约 0.485——两者几乎打平，说明这个设计刻意让两个信号相互竞争，而不是让任何一个单方面压制另一个。
