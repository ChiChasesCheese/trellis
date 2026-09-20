---
nodes: [problems.social.live-comments]
url: https://engineering.fb.com/2011/02/07/core-infra/live-commenting-behind-the-scenes/
---
# Live Commenting: Behind the Scenes

值得读：Facebook（Meta）工程博客一手材料，讲真实生产系统当年的规模（每分钟超 1 亿条
内容可能收到评论、约 65 万条评论/分钟需要路由）和"write locally, read globally"的
架构取舍——不做跨数据中心复制，而是评论提交时才实时聚合各数据中心的观众信息再推送。
比其他二手资料更精确的地方在于给出了真实的量级数字而不是笼统的"很多"。本题解没有采用
它的跨数据中心聚合模型（假设单区域部署更简单），只借用了"写入与广播分离、广播时才聚合"
的思路设计 Dispatcher 层；这篇文章未披露具体 pub/sub 技术选型，是本题解没有验证到的
部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://engineering.fb.com/2011/02/07/core-infra/live-commenting-behind-the-scenes/)

## Archived copy
![[src-meta-live-comments-clip]]
%% trellis:end %%
