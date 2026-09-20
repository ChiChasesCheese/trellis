---
nodes: [problems.search.typeahead]
url: https://www.linkedin.com/blog/engineering/open-source/cleo-open-source-technology-behind-linkedins-typeahead-search
---
# Cleo: the open source technology behind LinkedIn's typeahead search

值得读：LinkedIn 工程博客披露了他们真实的 typeahead 服务 Cleo——基于实体（会员、公司、
群组等）而非查询日志聚合，新实体创建后几乎立刻可被联想到，服务约 1.5 亿会员、平均响应
时间约 20 毫秒，并区分"network-agnostic"（纯全局流行度）和"network-aware"（结合个人
社交网络的个性化）两种排序模式。本题解的主线场景（基于历史查询日志聚合的通用搜索框）
数据源和 Cleo（基于实体表）不同，因此新鲜度的实现方式也不同——本题解需要一整套离线
聚合管道，Cleo 的信号直接来自实体表变更；「深入探讨」第 4 节的个性化叠加思路借鉴了 Cleo
"全局分数与个人分数分层存储、独立调权"这一原则。
