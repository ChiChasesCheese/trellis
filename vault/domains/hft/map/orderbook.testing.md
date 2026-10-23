%% trellis:begin %%
# 订单簿的正确性：不变量与回放测试
*订单簿与撮合引擎的实现*

买一必须低于卖一、数量非负、序列号连续等不变量；用历史行情回放对比参考实现。

**Requires:** [[domains/hft/map/orderbook.building|从逐笔行情重建订单簿]]

## Drills
- [[orderbook-std-map-p99|练习：订单簿用了 std::map，p99 会从哪里来]]

## Cards (4)
1. [[hft-testing-invariants]]
2. [[hft-testing-crossed-book]]
3. [[hft-testing-replay]]
4. [[hft-testing-fault-injection]]
%% trellis:end %%

## Notes
