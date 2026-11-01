---
id: hi-pt-photo-storage-sharing-3-entities
node: qb.sd.photo-storage-sharing.points
type: qa
step: 3
---
## Q
**照片存储与分享系统 · 照片、集合与成员的实体**｜出自：照片存储与分享系统 › 核心实体与接口

照片、集合和集合成员三个实体各存什么？为什么照片在不同集合里不复制？

## A
**照片。** photo_id、owner_id、拍摄时间 taken_at（来自 EXIF，缺失用上传时间）、字节数、内容哈希、对象存储键、状态（UPLOADING、READY、DELETED）。
**集合。** collection_id、名称、parent_id（可空）、照片数、总字节数。
**成员。** CollectionItem 多对多，照片在不同集合里只是引用，不复制。
