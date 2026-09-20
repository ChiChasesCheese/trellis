---
nodes: [problems.search.web-crawler]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler
tags: [no-archive]
---
# Design a Web Crawler

值得读：给出了 SQS 前端队列 + DynamoDB 元数据 + S3 内容存储的具体技术选型，以及按域名加
Redis 分布式锁实现节流、多阶段流水线隔离故障的思路。本题解与它的不同在于：它的节流锁是
"每个域名一把锁"的运行时机制，锁和队列调度是两套分离的东西，没有说明优先级如何与节流共存；
本题解用 Mercator 式的前端/后端队列架构把优先级和节流放进同一套数据结构里统一调度。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)
%% trellis:end %%
