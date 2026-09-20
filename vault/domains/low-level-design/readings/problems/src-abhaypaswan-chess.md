---
nodes: [problems.games.chess]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/chess
tags: [no-archive]
---
# lld-python — Design Chess

值得读：少见的**纯 Python** 国际象棋题解，而且开篇一句就点破了这道题的要害——易位、吃过路兵、
升变和牵制看起来像是事后补的特例，其实是设计必须绕着它们成形的东西。它的结构和本题解最接近：
滑行棋子与跳步棋子分成两层抽象基类，一手棋的记录里带着撤销所需的旧状态，合法性靠"先生成伪合法
再 make/unmake 过滤"。两点不同值得对照：它把"这个子动过没有"留在棋子上，本题解改成棋盘上的
易位权集合加一张"格子被离开或被吃就丢权"的小表（这样"车在原地被吃"不会漏）；它不跟踪三次重复，
本题解用含该谁走、易位权、吃过路兵格的局面指纹实现了，并保证那张计数表会随悔棋收缩。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/chess)
%% trellis:end %%
