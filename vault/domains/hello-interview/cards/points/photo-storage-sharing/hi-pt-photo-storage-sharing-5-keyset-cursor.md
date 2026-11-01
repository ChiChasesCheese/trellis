---
id: hi-pt-photo-storage-sharing-5-keyset-cursor
node: qb.sd.photo-storage-sharing.points
type: qa
step: 5
---
## Q
**照片存储与分享系统 · 键集游标分页**｜出自：照片存储与分享系统 › 深入 1

照片无限滚动为什么不用 OFFSET 分页？键集游标怎么写，游标是什么？大图滑动怎么取邻居？

## A
**问题。** `OFFSET 6000 LIMIT 60` 越翻越慢，新上传还会使页面错位。
**键集。** 索引 `(owner_id, taken_at DESC, photo_id DESC)`，`WHERE owner_id=? AND (taken_at, photo_id) < (?, ?) ... LIMIT 60`；游标是上一页最后一条的 `(taken_at, photo_id)`，复杂度与页数无关。排序键含 photo_id 打破并列。
**大图。** 客户端已有列表直接取邻居，深链进入用 `neighbors` 接口；预取前后 2 张中等尺寸图。
