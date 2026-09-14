---
id: content-static-generation-manifest-atomicity
node: content.static-generation
type: qa
---
## Q
A deploy uploads page files one by one, then overwrites the live manifest in place. Users intermittently get missing assets. What publication model fixes this?

## A
Upload all immutable artifacts under a new deployment ID, verify completeness and checksums, then atomically switch one small routing/manifest pointer to that ID. Never expose a partially uploaded release. Readers resolve one immutable snapshot for the whole request; rollback repoints to the prior snapshot. Garbage-collect old artifacts only after no live manifest or rollback window references them.

## Q zh
deploy 逐个上传 page file，再原地覆盖 live manifest，用户偶发 missing asset。什么 publication model 能修复？

## A zh
把所有 immutable artifact 上传到新的 deployment ID 下，验证 completeness 和 checksum 后，再原子切换一个小型 routing/manifest pointer。绝不暴露 partially uploaded release。一次请求应解析到同一个 immutable snapshot；rollback 只需指回旧 snapshot。只有在没有 live manifest 或 rollback window 引用后，才 garbage-collect 旧 artifact。
