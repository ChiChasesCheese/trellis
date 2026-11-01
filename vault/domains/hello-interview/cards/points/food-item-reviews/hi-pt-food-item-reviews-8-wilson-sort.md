---
id: hi-pt-food-item-reviews-8-wilson-sort
node: qb.sd.food-item-reviews.points
type: qa
step: 8
---
## Q
**带打赏的菜品评价系统 · 有帮助排序**｜出自：带打赏的菜品评价系统 › 深入 3

菜品评价按"最有帮助"排序，用赞数除以总数会有什么问题？应该怎么排？

## A
**问题。** 1 赞 0 踩 = 100%，小样本评论会排到最前面。
**做法。** 用 Wilson 置信区间下界之类的分数，样本少时自动保守。
**工程。** 异步重算，不在读时现算。
