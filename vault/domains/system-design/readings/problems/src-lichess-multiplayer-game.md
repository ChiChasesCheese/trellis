---
nodes: [problems.realtime.multiplayer-game]
url: https://github.com/lichess-org/lila
---
# lila — lichess.org: the forever free, adless and open source chess server

值得读：Lichess 完全开源的主服务代码本身（Scala，模块化单体架构），每局对弈由一个
AsyncActor 实例持有可变状态、串行化并发走子请求，官方与社区文档披露日常稳定维持超过
10 万并发玩家、MongoDB 存储超过 120 亿局对弈。本题解用这两个数字交叉验证了自己的容量
估算假设没有偏离真实系统的数量级，并直接采用了"每局一个 actor"的状态机设计思路。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/lichess-org/lila)
%% trellis:end %%
