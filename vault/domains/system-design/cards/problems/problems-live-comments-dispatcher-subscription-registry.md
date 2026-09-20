---
id: problems-live-comments-dispatcher-subscription-registry
node: problems.social.live-comments
type: qa
step: 3
tags: [grown]
---
## Q
When a new comment is published for a live video, how does a dispatcher layer avoid broadcasting it to every gateway server in the fleet, and why does that matter at scale?

## A
Each gateway registers, in a subscription registry (an in-memory store keyed by video id), which live videos it currently holds viewer connections for. The dispatcher consuming a new comment for a given video first queries the registry for the small set of gateways that actually hold connections for that video's viewers, and forwards only to those — not to the entire fleet. Since a platform typically runs thousands of concurrent live videos, most gateways at any moment hold no connections for a given video, so broadcasting to the whole fleet would waste effort proportional to total fleet size; targeted forwarding instead scales with how many gateways a specific video's viewers happen to be spread across, which is usually far smaller.

## Q zh
当一场直播视频产生一条新评论时，dispatcher 层如何避免把它广播给舰队里的每一台网关服务器？这在规模化时为什么重要？

## A zh
每台网关在一个按 video id 建索引的内存注册表（subscription registry）里登记自己当前持有哪些直播的观众连接。消费到某个视频新评论的 dispatcher，先查询注册表得到真正持有该视频观众连接的一小撮网关，只转发给这些网关，而不是整个舰队。因为一个平台通常同时有成千上万场直播在进行，任意时刻大多数网关对于某一场直播都没有持有任何连接，广播给整个舰队的浪费和舰队总规模成正比；按需转发则只随这场直播观众实际分布覆盖的网关数扩展，通常小得多。
