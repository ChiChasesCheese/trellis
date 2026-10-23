%% trellis:begin %%
# 价格档位怎么存：数组、有序树与排序 vector
*订单簿与撮合引擎的实现*

以价格为下标的数组、红黑树（std::map / TreeMap）、按价格排序的小 vector 各自的复杂度和缓存表现；为什么"大 O 好"不等于快。

**Requires:** [[domains/hft/map/orderbook.requirements|订单簿要支持的操作与复杂度]]

**Unlocks:** [[domains/hft/map/orderbook.matching-engine|撮合引擎的实现]], [[domains/hft/map/orderbook.building|从逐笔行情重建订单簿]], [[domains/hft/map/orderbook.memory-layout|订单簿的内存布局：预分配与对象池]]

## Drills
- [[orderbook-std-map-p99|练习：订单簿用了 std::map，p99 会从哪里来]]

## Cards (4)
1. [[hft-price-levels-array]]
2. [[hft-price-levels-tree]]
3. [[hft-price-levels-sorted-vector]]
4. [[hft-price-levels-choice]]
%% trellis:end %%

## Notes
