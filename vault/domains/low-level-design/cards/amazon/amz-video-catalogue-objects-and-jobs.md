---
id: amz-video-catalogue-objects-and-jobs
node: amazon.amz-video-catalogue
type: qa
step: 2
tags: [grown]
---
## Q
在视频目录设计里应该有哪几个对象？各自只负责一件什么事？

## A
`Title`（片名、类型列表、电影还是剧集）、`Episode`（所属片、季、集、时长）、`Profile`（档案，属于账号）、`Catalogue`（添加和按类型浏览）、`PositionStore`（`(档案, 视频) → 秒数、更新时间`）。切分依据：目录所有人共享、几乎只读；观看位置每个档案私有、频繁写——读写比和一致性要求不同，所以分成两个对象。
