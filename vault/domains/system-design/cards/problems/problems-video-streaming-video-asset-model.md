---
id: problems-video-streaming-video-asset-model
node: problems.media.video-streaming
type: qa
step: 3
tags: [grown]
---
## Q
In a video streaming platform's data model, why is a single Video entity modeled as owning multiple independent VideoAsset (rendition) records — one per (codec, resolution) pair — rather than storing all renditions as fields on the Video record itself?

## A
Each rendition is produced by an independent transcode job that can succeed or fail on its own schedule (a 1080p job can finish while a 4K job is still queued or retrying), so each VideoAsset needs its own status field and its own lifecycle independent of the Video's overall record. Modeling renditions as a one-to-many child collection lets the manifest generator publish a video as soon as a subset of renditions (e.g. the lower rungs) are ready, while higher renditions are added later — a single Video record with fixed rendition fields couldn't represent 'partially ready' without becoming a wide table of nullable columns that grows every time a new codec is added.

## Q zh
在视频流媒体平台的数据模型中，为什么一个 Video 实体要对应多个独立的 VideoAsset（渲染版本）记录——每个 (编码格式, 分辨率) 组合一条——而不是把所有渲染版本都存成 Video 记录本身的字段？

## A zh
每个渲染版本都由一个独立的转码任务生成，各自可能按自己的节奏成功或失败（1080p 任务可能已完成，而 4K 任务还在排队或重试），所以每个 VideoAsset 需要有自己的状态字段和独立于 Video 整体记录的生命周期。把渲染版本建模成一对多的子集合，能让 manifest 生成器在部分渲染版本（如较低档位）就绪后立即发布视频，高档位之后再补上——如果用固定字段把所有渲染版本塞进一条 Video 记录，就无法表达「部分就绪」这种状态，而且每新增一种编码格式都要给表加一列可空字段，越来越臃肿。
