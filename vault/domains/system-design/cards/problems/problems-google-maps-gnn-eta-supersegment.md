---
id: problems-google-maps-gnn-eta-supersegment
node: problems.geo.google-maps
type: qa
step: 5
tags: [grown]
---
## Q
In Google Maps' production ETA system (described in a September 2020 Google DeepMind blog post), how does the graph neural network (GNN) model traffic, and what real-world accuracy gain did it report?

## A
The model groups adjacent road segments that share significant traffic volume into units called 'Supersegments,' then represents the local road network as a graph where each route segment is a node and edges connect segments that are consecutive on the same road or meet at an intersection; a message-passing algorithm lets the predicted state of upstream segments propagate to influence predictions for downstream segments, and the model combines this with historical traffic patterns rather than relying only on a live snapshot. Google DeepMind reported real-time ETA accuracy improvements of up to 50% in cities such as Berlin, Jakarta, Sao Paulo, Sydney, Tokyo, and Washington D.C. (51% in Taichung), though smaller gains (16%) in London and Copenhagen — the wide spread shows the gain is highly dependent on local road structure and historical data density, not a uniform global effect.

## Q zh
在 Google Maps 生产环境的 ETA 系统中（2020 年 9 月 Google DeepMind 官方博客所述），图神经网络（GNN）是如何建模路况的？它公开报告的真实准确率提升幅度是多少？

## A zh
该模型把共享显著交通量的相邻路段组合成称为超级路段（Supersegment）的单元，再把局部路网表示成一个图——每个路段是一个节点，同一条路上相邻或在交叉口相连的路段之间连边；用消息传递（message passing）算法让上游路段的预测状态传播、影响下游路段的预测，并把这个结果和历史路况模式结合，而不是只依赖实时快照。Google DeepMind 报告在柏林、雅加达、圣保罗、悉尼、东京、华盛顿特区等城市把实时 ETA 准确率提升最多达 50%（台中达 51%），但伦敦和哥本哈根的提升幅度较小（16%）——这个差异说明提升幅度高度依赖当地路网结构和历史数据密度，不是一个全球统一的效果。
