---
nodes: [problems.geo.ride-hailing]
url: http://highscalability.com/blog/2015/9/14/how-uber-scales-their-real-time-market-platform.html
---
# How Uber Scales Their Real-time Market Platform

值得读：对 Uber 2015 年一场工程分享的整理，披露了 DISCO 撮合系统把"供给"（司机）和
"需求"（乘客）拆成独立服务、用 Google S2 第 12 级（单元面积 3.31–6.38 平方公里）做
地理分片键、司机每 4 秒上报一次位置、以及"让一切都可重试、可被杀死"这类可用性设计
原则。本题解把这些引用为历史上报道过的架构事实，而不是当作 Uber 当前生产系统的权威
描述。与本题解不同的地方在于：本题解独立推导了在当前披露的司机规模下，同样的 4 秒
上报间隔会产生多大的摄入 QPS（约 363,750 QPS），原文只描述了架构本身，没有给出这个
量级换算。

%% trellis:begin %%
## Source
[Open the original ↗](http://highscalability.com/blog/2015/9/14/how-uber-scales-their-real-time-market-platform.html)

## Archived copy
![[src-highscalability-uber-dispatch-clip]]
%% trellis:end %%
