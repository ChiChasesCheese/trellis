---
nodes: [problems.social.live-comments]
url: https://blog.twitch.tv/en/2015/12/18/twitch-engineering-an-introduction-and-overview-a23917b71a25/
---
# Twitch Engineering: An Introduction and Overview

值得读：Twitch 工程博客一手材料，介绍其聊天系统 Edge（同时支持原始 TCP 上的 IRC 协议
和 WebSocket）+ Pubsub（在 Edge 节点间分发消息）的分层扇出架构，并给出其聊天服务每天
投递超过 100 亿条消息的公开数字。和本题解的差异：Twitch 聊天允许观众间高频、双向的
互动（更接近聊天室），本题解的直播评论场景里观众到服务器方向流量稀疏得多，因此本文
选择 SSE 而不是 Twitch 这种保留双向协议支持的架构；本文也没有说明 Twitch 具体的分区
键选择和排序保证，是本题解无法从这篇文章验证的部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.twitch.tv/en/2015/12/18/twitch-engineering-an-introduction-and-overview-a23917b71a25/)

## Archived copy
![[src-twitch-live-comments-clip]]
%% trellis:end %%
