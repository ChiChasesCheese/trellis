---
id: problems-instagram-media-status-gates-fanout
node: problems.social.instagram
type: qa
step: 6
tags: [grown]
---
## Q
In a photo/video sharing app that reuses a generic news-feed fan-out mechanism, why must publishing a post (triggering fan-out to followers) be gated on the referenced media's processing status rather than happening immediately after the client finishes uploading?

## A
Media processing (resizing images or transcoding video into multiple renditions) takes measurably longer than the upload itself, so if fan-out is triggered the moment upload completes, followers can receive a feed item whose media derivatives are not yet ready — resulting in broken or blank media in their feed. Gating publication on a media status field (only allowing the post-creation call to succeed once status is 'ready') ensures fan-out only ever propagates posts whose media can already be displayed, at the cost of a short wait between 'upload complete' and 'post published' rather than making that wait block the upload confirmation itself.

## Q zh
在一个复用通用信息流 fan-out 机制的图片/视频分享应用中，为什么必须把'发布帖子（从而触发对粉丝的 fan-out）'这个动作用媒体的处理状态来门控，而不是客户端一上传完就立刻发布？

## A zh
媒体处理（图片缩放或视频转码成多档版本）耗时明显长于上传本身，如果上传一完成就立刻触发 fan-out，粉丝的信息流里就可能出现一条媒体衍生版本还没就绪的帖子——表现为破损或空白的媒体。用一个媒体状态字段来门控发布（只有当状态变为'就绪'时，创建帖子的调用才允许成功），能保证 fan-out 传播出去的帖子背后的媒体一定已经可以展示，代价只是'上传完成'和'帖子发布'之间多了一小段等待，而不是让这段等待去阻塞上传本身的确认响应。
