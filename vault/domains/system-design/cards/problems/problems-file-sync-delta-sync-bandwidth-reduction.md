---
id: problems-file-sync-delta-sync-bandwidth-reduction
node: problems.media.file-sync
type: qa
step: 1
tags: [grown]
---
## Q
In a file sync system that splits files into fixed 4MB blocks, why does a localized edit to a 200MB file (touching only 2 of its 50 blocks) upload roughly 25x less data than re-uploading the whole file, and what design choice does this justify?

## A
A 200MB file split into 4MB blocks has 50 blocks; if an edit only changes 2 of them, block-level delta sync uploads just 2 x 4MB = 8MB instead of the full 200MB, a 200/8 = 25x reduction. This gap justifies making block-level chunking and delta sync a core part of the write path rather than an optional optimization, because without it the platform's raw daily change-data volume would need to be multiplied by dozens of times in workloads where large files are common, which no realistic bandwidth or storage budget could absorb.

## Q zh
在一个把文件切成固定 4MB 块的文件同步系统中，为什么对一个 200MB 文件的一次局部编辑（只改动其 50 个块中的 2 个）上传的数据量比重传整个文件少约 25 倍？这个数字支撑了什么设计决策？

## A zh
一个 200MB 的文件按 4MB 分块共有 50 个块；如果一次编辑只改动其中 2 个，块级增量同步只需要上传 2 × 4MB = 8MB，而不是整份 200MB，即 200÷8 = 25 倍的减少。这个差距证明块级分块和增量同步必须是写路径的核心部分，而不是可选优化——如果不做，在大文件常见的场景下，平台每日原始变更数据量要再乘以几十倍，任何现实的带宽或存储预算都扛不住。
