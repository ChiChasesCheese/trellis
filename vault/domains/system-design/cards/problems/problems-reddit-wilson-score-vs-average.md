---
id: problems-reddit-wilson-score-vs-average
node: problems.social.reddit
type: qa
step: 3
tags: [grown]
---
## Q
When sorting comments by 'best', why does a design that ranks comments by the raw ratio 'upvotes / (upvotes + downvotes)' produce a worse ordering than one using the Wilson score confidence interval lower bound, given a comment with 2 upvotes and 0 downvotes versus a comment with 6 upvotes and 1 downvote?

## A
The raw ratio gives 2/0 a perfect score of 1.0 versus 6/1's 0.857, so the raw-ratio design ranks the 2-vote comment first — but a 100% approval rate on only 2 votes carries far less statistical confidence than an 85.7% approval rate on 7 votes. The Wilson score lower bound (computed at 80% confidence) accounts for sample size directly, giving roughly 0.549 to the 2-upvote comment and about 0.622 to the 6-upvote-1-downvote comment — correctly flipping the order to favor the larger, more-certain sample instead of rewarding a small sample's lucky perfect ratio.

## Q zh
在按'最佳'（best）给评论排序时，为什么用赞成票 / (赞成票+反对票) 这个原始比例排序，会比用 Wilson 得分区间下界排序得出更差的顺序——以一条 2 赞成 0 反对的评论对比一条 6 赞成 1 反对的评论为例？

## A zh
原始比例给 2 赞 0 反的评论打出满分 1.0，6 赞 1 反只有 0.857，所以原始比例排序会把 2 票的评论排在前面——但只有 2 票的 100% 好评率，统计置信度远低于 7 票里 85.7% 的好评率。Wilson 得分区间下界（按 80% 置信度计算）直接把样本量纳入考虑，给 2 赞的评论打出约 0.549，给 6 赞 1 反的评论打出约 0.622——正确地把顺序反了过来，让更大、更确定的样本胜出，而不是奖励小样本侥幸凑出的完美比例。
