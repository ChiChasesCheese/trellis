---
nodes: [problems.social.live-comments]
url: https://engineering.fb.com/2020/10/22/video-engineering/live-streaming/
---
# Scaling Live Video Streaming for Millions of Viewers

值得读：Meta 工程博客一手材料，披露 2020 年欧冠决赛巴西/拉美赛区直播峰值并发观众达
720 万，并讲了用 request coalescing 和 cache sharding 缓解"惊群"（thundering herd）、
把里约热内卢本地互联带宽从 20 Gbps 扩容到 120 Gbps 的真实案例。这篇讲的是视频流本身
的分发，不涉及评论广播，本题解引用它只是为了用一个有源可查的真实并发观众数量级
（720 万）校验容量估算里 1,000 万这个假设峰值处在合理的同一数量级，而不是凭空拍出来的
数字；文章没有给出评论/聊天层的任何架构细节，是它和本题主题的差距所在。

%% trellis:begin %%
## Source
[Open the original ↗](https://engineering.fb.com/2020/10/22/video-engineering/live-streaming/)

## Archived copy
![[src-meta-live-streaming-scale-clip]]
%% trellis:end %%
