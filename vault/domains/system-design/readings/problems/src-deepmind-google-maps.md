---
nodes: [problems.geo.google-maps]
url: https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/
---
# Traffic prediction with advanced Graph Neural Networks

值得读：Google DeepMind 官方博客（2020 年 9 月），公开了 Google Maps 生产环境里用于
ETA 预测的图神经网络（GNN）方案——把相邻路段组合成 Supersegment、用消息传递建模路段
之间的传播关系、结合历史模式与实时快照，并给出多个城市的实际 ETA 准确率提升幅度（最高
超过 50%，伦敦/哥本哈根仅 16%）。本题解「深入探讨」第 3 节的 ETA 模型设计和具体提升
数字均直接引自该文；和商业刷题站泛泛提到"用机器学习预测 ETA"相比，这是唯一能给出
真实模型架构和量化效果的一手来源。
