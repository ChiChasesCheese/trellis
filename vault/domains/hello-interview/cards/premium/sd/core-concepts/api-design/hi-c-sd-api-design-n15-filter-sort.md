---
id: hi-c-sd-api-design-n15-filter-sort
node: sd.core-concepts.api-design.notes
type: qa
step: 15
---
## Q
**API 设计 · 过滤与排序**｜摘要 · 追问
过滤和排序在 REST 里用什么约定？设计上真正要注意什么？

## A
- **约定：** 都用查询参数。过滤 `?city=NYC&status=upcoming`；排序 `?sort=date`，前面加减号表示降序，`?sort=-date` 是最新的在前。
- **难点不在发明参数，而在一致：** 活动按 `status` 过滤，订单也应该叫 `status`，别叫 `state`。调用方学会一个端点后就会默认其他端点也这样，名字对不上是 API 评审里最常见的一致性问题。
- **面试里：** 展示一个带过滤的端点，说明其余端点沿用同一约定即可，不必列举所有过滤条件。
