---
id: hi-pt-food-item-reviews-3-one-vote
node: qb.sd.food-item-reviews.points
type: qa
step: 3
---
## Q
**带打赏的菜品评价系统 · 一人一票与订单项资格**｜出自：带打赏的菜品评价系统 › 核心实体与接口

菜品评价系统怎样保证只有收到过这道菜的人才能评价，且每人对每条评论只有一票、可改票撤票？

## A
**评论资格。** 校验订单项属于该用户且已送达，orderItemId 上加唯一约束，每个订单项最多一条评论。
**投票。** Vote 以 (reviewId, voterId) 为主键，接口 PUT /reviews/{id}/vote {1 | -1 | 0}，0 表示撤票，PUT 天然幂等。
**差值。** upsert 时读出旧值算差值（踩改赞则赞 +1、踩 −1），差值非零才继续。
