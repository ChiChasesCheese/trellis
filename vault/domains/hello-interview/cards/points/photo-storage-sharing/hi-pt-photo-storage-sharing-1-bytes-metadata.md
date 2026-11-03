---
id: hi-pt-photo-storage-sharing-1-bytes-metadata
node: qb.sd.photo-storage-sharing.points
type: qa
step: 1
---
## Q
**照片存储与分享系统 · 字节与元数据两个量级**｜必会 · 出自：照片存储与分享系统 › 需求

设计 Google Photos 式照片存储与分享服务，照片字节和照片元数据分别怎么处理？真正要想清楚的是什么？

## A
**要点。** 字节走对象存储加 CDN，直传、不经应用服务器；元数据是按用户分片的小记录。
**重点。** 时间线的游标分页、集合的层级与多对多关系，以及不让分析查询拖累线上库。
