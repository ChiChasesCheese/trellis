---
nodes: [problems.realtime.leaderboard]
url: https://systemdesign.one/leaderboard-system-design/
tags: [no-archive]
---
# Leaderboard System Design (systemdesign.one)

值得读：覆盖了分片策略对比（按分数区间/按玩家 id/一致性哈希）、好友榜、时间窗口
榜单等和本题相近的范围，用于横向核对本题解的方案列表有没有遗漏明显选项。该文给出
的具体数字（DAU、QPS、内存估算）是这个站点自己假设的场景参数，本题解没有沿用，而是
基于本题解自己的 DAU/QPS 假设独立计算得出不同的数字，两者不能直接对比；该文对"近似
排名 vs 精确排名"的头部/长尾分流讨论不如本题解深入，本题解在此基础上补充了具体的
精度与陈旧窗口权衡。

%% trellis:begin %%
## Source
[Open the original ↗](https://systemdesign.one/leaderboard-system-design/)
%% trellis:end %%
