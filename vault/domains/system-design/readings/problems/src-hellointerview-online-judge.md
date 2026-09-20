---
nodes: [problems.realtime.online-judge]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode
tags: [no-archive]
---
# Design LeetCode

值得读：Hello Interview 给出了面向 LeetCode 规模（几十万用户）的基础架构——容器沙箱、
SQS 队列缓冲、Redis 有序集合做排行榜、基于 CPU 的自动伸缩组处理十万人级竞赛。本题解与
它的分歧在于隔离强度：本题解认为容器与宿主机共享内核的边界，对"匿名公开提交、可达十万人
竞赛"这个信任模型不够，选择了 Firecracker microVM 这一更强的虚拟化边界，并把它笼统提到的
"自动伸缩"具体化为利特尔法则驱动、按已知开考时间预热的扩容方案。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode)
%% trellis:end %%
