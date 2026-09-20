---
id: problems-live-comments-per-video-ordering
node: problems.social.live-comments
type: qa
step: 5
tags: [grown]
---
## Q
What ordering guarantee should a live-comments system provide for comments on the same video, and how is it implemented without requiring global linearizability across all viewers?

## A
The guarantee is scoped to a single video: comments get a monotonically increasing `seq` assigned within that video (not a global order across all videos or all viewers' clocks), and the pub/sub layer partitions by video id, so the same video's comments are consumed and forwarded in write order within their partition (partition-level ordering is a basic property of a partitioned log/queue). Clients buffer incoming comments for a short window (roughly 1-2 seconds) and re-sort by `seq` before rendering, which absorbs network-path jitter. This does not guarantee two different viewers see identical screen content at the exact same physical instant — network delay differs per viewer — but it does guarantee each viewer's own view is internally self-consistent and monotonic, which is what the product actually needs.

## Q zh
直播评论系统应该为同一视频的评论提供什么顺序保证？如何在不要求跨全体观众全局线性化的前提下实现？

## A zh
保证的范围限定在单个视频内：评论在该视频内获得一个单调递增的 `seq`（不是跨所有视频或所有观众时钟的全局顺序），pub/sub 层按 video id 分区，同一视频的评论在其分区内按写入顺序被消费和转发（分区内有序是分区化日志/队列的基本性质）。客户端对收到的评论做一个短窗口（约 1-2 秒）的缓冲，按 `seq` 重新排序后再渲染，用来吸收网络路径抖动。这不保证两个不同观众在同一物理瞬间看到完全相同的屏幕内容——网络延迟因观众而异——但保证每个观众自己看到的视图内部自洽、单调，这正是产品实际需要的。
