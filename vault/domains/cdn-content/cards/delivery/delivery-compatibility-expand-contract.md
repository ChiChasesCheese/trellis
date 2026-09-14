---
id: delivery-compatibility-expand-contract
node: delivery.compatibility
type: qa
---
## Q
How should a fleet migrate from cache metadata v1 to v2 while old and new workers run together?

## A
Expand first: deploy readers that accept v1 and v2 while writers continue v1. Then enable v2 writes gradually, observe mixed-fleet behavior, and backfill only if required. After all readers are v2-capable and rollback windows close, contract by removing v1 writes and later v1 reads. Version the metadata explicitly; do not infer format from deployment time.

## Q zh
当 old 和 new worker 同时运行时，fleet 应如何从 cache metadata v1 迁移到 v2？

## A zh
先 expand：部署能读取 v1 和 v2 的 reader，同时 writer 继续写 v1。然后逐步启用 v2 write，观察 mixed-fleet behavior，并只在必要时 backfill。所有 reader 都具备 v2 能力且 rollback window 关闭后，再 contract：先删除 v1 write，之后删除 v1 read。明确 version metadata；不要根据 deployment time 猜 format。
