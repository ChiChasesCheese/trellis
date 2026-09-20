---
nodes: [problems.search.ad-click-aggregation]
url: https://medium.com/pinterest-engineering/building-a-real-time-user-action-counting-system-for-ads-88a60d9c9a
tags: []
---
# Building a real-time user action counting system for ads

值得读：Pinterest 工程博客描述了一个真实的去重/计数服务 Aperture：用 RocksDB 做存储引擎、
按用户 id + 时间桶分 key，按 `insertion_id + action + viewtype` 识别一次广告展示、以完整
事件字节去重，报告的 SLA 是峰值约 20 万 QPS 下个位数毫秒的 P99。和本题不同的是，Aperture
把去重推迟到**查询时**才做（存下所有原始事件，serving 时现算），而不是本题选择的摄入时
流式去重——这是两种可行的设计取舍，前者省去了摄入路径的强一致写，代价是每次查询都要扫
一段时间窗口内的原始事件。

%% trellis:begin %%
## Source
[Open the original ↗](https://medium.com/pinterest-engineering/building-a-real-time-user-action-counting-system-for-ads-88a60d9c9a)
%% trellis:end %%
