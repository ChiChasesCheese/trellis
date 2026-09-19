%% trellis:begin %%
# 负无穷（-inf）（dp-stock-trading-states）
*动态规划：线性与背包（linear DP / knapsack）*

在股票交易的多状态DP中，hold（持有股票）状态应初始化为 负无穷（-inf），以避免出现「没有买入就卖出」的非法转移路径；而未持有状态初始化。
%% trellis:end %%

## Notes
