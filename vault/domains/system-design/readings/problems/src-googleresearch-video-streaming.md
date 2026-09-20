---
nodes: [problems.media.video-streaming]
url: https://research.google/pubs/pub50300/
tags: []
---
# Warehouse-Scale Video Acceleration: Co-design and Deployment in the Wild

值得读：Google Research 官方论文页（ASPLOS 2021），披露自研视频编码单元（VCU/Argos）
在 YouTube 规模的转码负载上，相对调优良好的非加速软件基线取得了 **20–33 倍**的效率
提升，是本题解「容量估算」转码算力一段"ASIC 加速"数字的一手来源。本题解与它的区别在
于：论文报告的是一个区间而不是单点数字，本题解出于保守只取 10 倍作为下界假设，并在
正文里明确算出按论文真实区间折算会得到更少的机器数（170–281 台），不把保守假设包装
成论文的原始结论。
