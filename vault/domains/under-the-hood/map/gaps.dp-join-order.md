%% trellis:begin %%
# 动态规划：数据库怎样选多表连接顺序
*考点补全：后端系统里的算法*

n 张表的连接顺序有指数种：PostgreSQL 按子集大小逐层 DP，先算两表组合的最优，再在此基础上算三表……；表数超过阈值改用遗传算法（GEQO）。

## Cards (4)
1. [[uth-gaps-dp-join-order-1-levels]]
2. [[uth-gaps-dp-join-order-2-bushy]]
3. [[uth-gaps-dp-join-order-3-geqo]]
4. [[uth-gaps-dp-join-order-4-collapse-limit]]
%% trellis:end %%

## Notes
