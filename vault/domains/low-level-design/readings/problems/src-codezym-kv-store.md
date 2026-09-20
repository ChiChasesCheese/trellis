---
nodes: [problems.components.kv-store]
url: https://codezym.com/lld/amazon
tags: [no-archive]
---
# CodeZym — Amazon machine coding questions

值得读：CodeZym 对亚马逊一类分级机考题的公开纲要页，2026 年 9 月的报告样本里包含一道
键值存储题，把"每个 key 是一张字段表"这个设定和分关的节奏交代得比较清楚。本题解和它的
分歧在于关卡顺序——它把事务放在 TTL 之前，本题解遵照任务书给定的顺序（TTL 第 3 关、
事务第 4 关），因为"事务里设置的 TTL 提交/回滚后是否正确"本身是检验撤销日志实现是否
正确的最佳测试，放在 TTL 之后更能形成递进关系，而不是两个互相独立的能力。

%% trellis:begin %%
## Source
[Open the original ↗](https://codezym.com/lld/amazon)
%% trellis:end %%
