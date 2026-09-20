---
id: problems-instagram-transcode-worker-failure-isolation
node: problems.social.instagram
type: qa
step: 7
tags: [grown]
---
## Q
In a photo/video sharing system, if the transcoding/resizing worker pool becomes completely unavailable, why does this degrade only the write (upload-to-publish) path and not the read path for already-published media?

## A
Already-published media has its derivatives (resized images, transcoded video renditions) already generated and stored in object storage, and the read path serves those bytes directly through the CDN and origin without ever involving the transcoding worker pool. A worker pool outage only prevents new uploads from progressing past their 'processing' status and getting their derivatives generated; once workers recover, they resume consuming the pipeline queue from where they left off, so no user needs to re-upload and no previously published content is affected.

## Q zh
在一个图片/视频分享系统中，如果转码/缩放工作节点池完全不可用，为什么这只会影响写路径（从上传到发布），而不影响已经发布的媒体的读路径？

## A zh
已经发布的媒体，其衍生版本（缩放后的图片、转码后的视频版本）早已生成并存放在对象存储中，读路径直接通过 CDN 和源站提供这些字节，全程不涉及转码工作节点池。工作节点池故障只会导致新上传的媒体停留在'处理中'状态、无法生成衍生版本；节点池恢复后，它们从断点继续消费处理管道队列即可，不需要用户重新上传，也不影响任何已发布的历史内容。
