---
nodes: [problems.social.news-feed]
url: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md
---
# System Design Primer — Twitter timeline & search

值得读：donnemartin/system-design-primer（MIT 协议的开源社区仓库，非商业课程）给出了
推（push）/拉（pull）两种 fan-out 模型最基础的对比，以及用 Redis 原生 list 结构存储
时间线的思路，是入门这道题最常被引用的免费资料之一。与本题解不同的地方在于：本题解没有
采用它"对高粉丝账号完全依赖搜索合并"的做法，而是把"读时合并"限定在用户自己关注的极少数
几个名人账号范围内，因为对普通用户而言需要合并的名人账号通常是个位数到十位数，比全局
搜索合并代价小得多，也不需要额外维护一套独立的搜索索引。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md)

## Archived copy
![[src-donnemartin-news-feed-clip]]
%% trellis:end %%
