---
id: hi-pt-recently-viewed-items-7-redis-real
node: qb.lld.recently-viewed-items.points
type: qa
step: 10
---
## Q
**"最近浏览"记录 · 真实系统用 Redis**｜加分 · 出自："最近浏览"记录 › 深入 6

"最近浏览"在真实系统里一般怎么放？每次浏览同步写有什么问题？

## A
**Redis 有序集合。** 键 recent:{customer}，成员是商品，分数是浏览时间戳；浏览时 ZADD（已存在则更新分数，等于提前），ZREMRANGEBYRANK 裁掉多余，读用 ZREVRANGE，键设过期（如 30 天）。
**事件量大。** 先合并同一商品重复上报，再批量写。
**登录。** 匿名设备记录在登录时按时间与账号记录合并再裁剪。
