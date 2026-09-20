---
nodes: [problems.social.news-feed]
url: https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/
---
# News Feed ranking, powered by machine learning

值得读：Meta 官方工程博客披露的真实排序架构——Pass 0 用轻量模型从每用户每天平均超过
1,000 条候选中筛出约 500 条，Pass 1 用多任务神经网络对这约 500 条逐条打分，Pass 2 应用
内容类型多样性等上下文规则重排。这是本题解「深入探讨」多阶段排序一节的直接依据。与本
题解不同的地方在于：本题解补充了"如果对全部候选直接跑重模型"这一反例在 2 亿日活假设下
的具体计算量（约 2×10^11 次推理/天），用来量化说明为什么必须分阶段收窄候选集，原文本身
没有给出这个对比数字。

%% trellis:begin %%
## Source
[Open the original ↗](https://engineering.fb.com/2021/01/26/ml-applications/news-feed-ranking/)

## Archived copy
![[src-meta-engineering-news-feed-clip]]
%% trellis:end %%
