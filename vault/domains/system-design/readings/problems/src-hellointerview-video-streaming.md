---
nodes: [problems.media.video-streaming]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube
tags: [no-archive]
---
# Design a Video Streaming Platform (YouTube)

值得读：Hello Interview 给出了这道题最完整的免费题解框架——预签名直传对象存储、用
DAG 编排转码流水线、断点续传的分片指纹机制，并按 mid/senior/staff 分层写出面试官对每
个深度的期望。它把码率阶梯当作对所有视频统一生成的常量，本题解不同的地方在于：本文
用容量估算算出无差别生成全套阶梯会带来 6.1 倍的存储放大，并据此论证了长尾内容必须做
按需/分层转码（见本题解「深入探讨」第 4 节），这是它没有展开的部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube)
%% trellis:end %%
