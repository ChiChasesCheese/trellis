---
nodes: [problems.media.video-streaming]
url: http://techblog.netflix.com/2015/12/per-title-encode-optimization.html
tags: []
---
# Per-Title Encode Optimization

值得读：Netflix 官方工程博客披露了按标题定制码率阶梯（per-title encoding）替代固定
阶梯后，在相同主观质量下把存储和分发成本降低 15%–20% 的真实数据，是本题解「容量估算」
与「深入探讨」第 2 节相关数字的直接来源，而不是猜测出来的比例。本文在此基础上进一步
讨论了 Netflix 2018 年上线的按镜头定制（Dynamic Optimizer，见另一篇引用）如何再省
17.1% 码率，并说明为什么本设计只对头部高播放量内容采用这类需要额外探测编码成本的方案，
这是这篇原始博客没有展开的取舍论证。

%% trellis:begin %%
## Source
[Open the original ↗](http://techblog.netflix.com/2015/12/per-title-encode-optimization.html)
%% trellis:end %%
