---
nodes: [problems.social.news-feed]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed
tags: [no-archive]
---
# Design Facebook's News Feed

值得读：Hello Interview 对信息流这道题给出了完整的推/拉/混合三段式演进框架，并明确点出
两个关键结论——"最多 1 分钟陈旧"的一致性目标，以及用冗余只读缓存（把热帖复制到多个独立
缓存实例，按请求而非按 key 路由）解决名人热帖的读侧热点。与本题解不同的地方在于：本题解
把"naive 全量推送"和"剔除头部账号后的混合推送"两种写放大都用具体的幂律粉丝分布假设算了
出来（分别约 260,764 QPS 和 29,282 QPS，降低约 8.9 倍），而不是停留在"名人会造成写放大"
这样的定性描述。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed)
%% trellis:end %%
