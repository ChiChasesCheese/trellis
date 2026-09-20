---
nodes: [problems.foundations.cdn]
url: https://www.usenix.org/legacy/publications/login/2010-06/openpdfs/nygren.pdf
tags: []
---
# The Akamai Network: A Platform for High-Performance Internet Applications

值得读：Akamai 工程团队自己写的架构综述，讲清楚一个真实的、数万台服务器规模的多租户
CDN 如何用全球分布式 DNS 加一个独立的"映射系统"做请求路由，而不是依赖 anycast。题解
用它做「深入探讨」第 1 节里 DNS-based 路由这一支的第一手依据，并明确指出本题选择了
和它不同的 anycast-为主的路线。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/legacy/publications/login/2010-06/openpdfs/nygren.pdf)
%% trellis:end %%
