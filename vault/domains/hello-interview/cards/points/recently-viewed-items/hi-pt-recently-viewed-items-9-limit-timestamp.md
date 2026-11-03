---
id: hi-pt-recently-viewed-items-9-limit-timestamp
node: qb.lld.recently-viewed-items.points
type: qa
step: 8
---
## Q
**"最近浏览"记录 · limit 调整与时间语义**｜追问 · 出自："最近浏览"记录 › 取舍与追问

"最近浏览"被追问：limit 要能运行时调整、要支持"最近 7 天"，怎么改？

## A
**调小 limit。** 要裁剪所有客户的列表，可惰性：下次访问该客户时裁剪。
**最近 7 天。** 字典的值存时间戳，读取时过滤过期的。
**要计频次。** 值改为（次数，最后时间），顺序仍按最后时间，但这会演变成带频次的缓存。
