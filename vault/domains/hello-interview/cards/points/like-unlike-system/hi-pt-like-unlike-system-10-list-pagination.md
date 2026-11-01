---
id: hi-pt-like-unlike-system-10-list-pagination
node: qb.sd.like-unlike-system.points
type: qa
step: 10
---
## Q
**点赞与取消点赞系统 · 用户列表分页**｜出自：点赞与取消点赞系统 › 深入 4

点赞系统的"我点赞过的内容"列表为什么不用 offset 分页？怎么做？

## A
**要点。** 按 (userId, createdAt desc, itemId) 排序，游标分页（游标是时间加内容 ID）。
**为什么。** 用户可能中途点赞，offset 会漏项或重复。
**细节。** 取消点赞要同时删排序索引条目（本地二级索引自动维护）；只存 ID，详情读取时批量取。
