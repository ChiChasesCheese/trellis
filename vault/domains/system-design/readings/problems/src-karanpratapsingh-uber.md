---
nodes: [problems.geo.ride-hailing]
url: https://www.karanpratapsingh.com/courses/system-design/uber
tags: [no-archive]
---
# Uber

值得读：Karan Pratap Singh 系统设计课程对这道题的拆解，给出了微服务拆分（客户、
司机、撮合、行程、支付、通知）、gRPC 优先于 REST 的服务间通信建议，以及基本的
请求/驱动/行程数据模型。与本题解不同的地方在于：本题解没有展开服务间通信协议的
选型——这不是这道题最容易出错的地方——而是把篇幅集中在撮合并发正确性（排他锁）和
位置摄入相对撮合请求两个数量级的负载不对称上，这两点在该课程里只是一带而过，没有
展开具体的数量级论证。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.karanpratapsingh.com/courses/system-design/uber)
%% trellis:end %%
