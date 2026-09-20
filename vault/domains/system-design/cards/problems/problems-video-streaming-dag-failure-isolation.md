---
id: problems-video-streaming-dag-failure-isolation
node: problems.media.video-streaming
type: qa
step: 4
tags: [grown]
---
## Q
In a video transcoding pipeline, why does splitting the work into a DAG of independent per-rendition jobs (one node per codec/resolution combination) give better failure isolation than a single sequential script that generates the full bitrate ladder for one video end to end?

## A
Because the rendition jobs have no dependency on each other, a failure in one job (for example, a corrupted-frame error during 4K encoding) can be retried in isolation without discarding or re-running the renditions that already succeeded, and the jobs can run concurrently across a worker pool instead of one after another. A single sequential script, by contrast, treats the whole ladder as one unit of work, so any single rendition's failure forces a full retry of everything, and there is no way to run renditions in parallel across machines.

## Q zh
在视频转码流水线中，为什么把工作拆成一个由多个独立的按渲染版本划分的任务组成的 DAG（每个 编码格式/分辨率 组合一个节点），比一个从头到尾顺序生成全套码率阶梯的单一脚本有更好的故障隔离？

## A zh
因为各渲染版本任务之间互不依赖，某一个任务的失败（例如 4K 编码遇到损坏帧错误）可以被单独重试，而不需要丢弃或重跑已经成功的其他渲染版本，而且这些任务可以在一个 worker 池里并发执行，而不是逐个顺序执行。相比之下，单一顺序脚本把整个阶梯当成一个工作单元，任何一个渲染版本失败都要整体重来，也无法把不同渲染版本分摊到多台机器并行处理。
