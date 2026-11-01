---
id: hi-pt-food-item-reviews-10-rating-aggregate
node: qb.sd.food-item-reviews.points
type: qa
step: 10
---
## Q
**带打赏的菜品评价系统 · 平均星级与需求澄清**｜出自：带打赏的菜品评价系统 › 取舍与追问

菜品评价要展示菜品平均星级，怎么算才不用每次扫描所有评论？需求很宽时开场该问什么？

## A
**聚合。** ItemRating 存 sum 与 count，新评论增量加；改评分要减旧值再加新值，用评论行版本号避免重复计算。
**澄清三问。** 是否需要平均星级、付款规则是比例还是每 N 个赞、是否要防刷，并给出默认选择。
**删评论。** 状态置 REMOVED，不再接受投票，未付款里程碑作废。
