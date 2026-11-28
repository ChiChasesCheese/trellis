---
id: hi-pt-nearby-restaurants-app-7-cursor-paging
node: qb.sd.nearby-restaurants-app.points
type: qa
step: 7
---
## Q
**附近餐厅发现 · 游标分页**｜必会 · 出自：附近餐厅发现 › 深入 3

附近餐厅列表的分页为什么不用偏移量？游标怎么设计才能让翻页时顺序不抖动？

## A
**问题。** 翻页时数据会变，深翻页也贵，偏移量会重复或漏项。

**做法。** 游标是上一条的（排序分，restaurantId）；首次请求固定前 200 家，翻页读同一份，列表不会抖动。
