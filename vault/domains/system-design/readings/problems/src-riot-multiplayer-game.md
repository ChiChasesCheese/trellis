---
nodes: [problems.realtime.multiplayer-game]
url: https://www.riotgames.com/en/news/peeking-valorants-netcode
---
# Peeking into VALORANT's Netcode

值得读：Riot 官方技术博客，明确写出"服务器绝不能信任客户端对世界状态的上报"这条权威
服务器的核心原则，并披露 VALORANT 128 tick/秒的服务器模拟频率、基于时间线同步的滞后
补偿机制（客户端上报开火时本地看到的时间点，服务器据此回退判定命中），以及优化到约
2.3 毫秒的单帧处理时间使一个 CPU 核心能容纳三局并发游戏。本题解用这组第一手数字，和
自己算出的回合制走子密度做了量化对比（约 878 倍的事件速率差异），说明回合制和快节奏
实时游戏的权威服务器虽然原则相同，运转频率却差了近三个数量级。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.riotgames.com/en/news/peeking-valorants-netcode)

## Archived copy
![[src-riot-multiplayer-game-clip]]
%% trellis:end %%
