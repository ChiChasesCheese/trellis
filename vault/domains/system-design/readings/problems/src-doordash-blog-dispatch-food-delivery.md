---
nodes: [problems.geo.food-delivery]
url: https://careersatdoordash.com/blog/using-ml-and-optimization-to-solve-doordashs-dispatch-problem/
---
# Using ML and Optimization to Solve DoorDash's Dispatch Problem

值得读：DoorDash 官方工程博客，描述了他们的 DeepRed 调度系统——一层机器学习模型预测
指派某个骑手后的取送时间和接单可能性，另一层混合整数规划（MIP）在批量窗口内对订单和
骑手的候选配对联合求解，决定打包（batching）和是否延迟指派。本题解「深入探讨」第 3
节"批量优化而不是逐单贪心"的架构决策和"批量率"这一权衡指标均直接引自该文；比多数刷题
站只停留在"用优化算法做匹配"这一层更进一步，给出了两层结构（预测 + 优化）的具体分工。

%% trellis:begin %%
## Source
[Open the original ↗](https://careersatdoordash.com/blog/using-ml-and-optimization-to-solve-doordashs-dispatch-problem/)
%% trellis:end %%
