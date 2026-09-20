---
nodes: [problems.foundations.job-scheduler]
url: https://eng.uber.com/cadence-multi-tenant-task-processing/
tags: []
---
# Cadence Multi-Tenant Task Processing

值得读：Uber Cadence 用按租户速率限制、动态优先级、加权轮询、多游标虚拟队列实现
多租户公平性的真实生产设计，包括把 worker goroutine 数从 16K 降到 100（降低 95%
以上）同时维持同等负载的具体优化数字。本题解「深入探讨」第 6 节的多租户公平调度
方案直接参考了这套模型，但把虚拟队列拆分的判定标准简化为"是否持续超出配额"，没有
覆盖 Cadence 原文里更细的队列分裂深度限制等运维细节。

%% trellis:begin %%
## Source
[Open the original ↗](https://eng.uber.com/cadence-multi-tenant-task-processing/)
%% trellis:end %%
