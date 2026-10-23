%% trellis:begin %%
# 订单索引与侵入式链表
*订单簿与撮合引擎的实现*

用哈希表按 order id 找订单，同价位订单用侵入式双向链表（intrusive list）保持时间顺序，实现 O(1) 撤单。

**Requires:** [[domains/hft/map/orderbook.requirements|订单簿要支持的操作与复杂度]]

**Unlocks:** [[domains/hft/map/orderbook.matching-engine|撮合引擎的实现]], [[domains/hft/map/orderbook.building|从逐笔行情重建订单簿]]

## Readings
- [[wiki-hash-table|哈希表（hash table）]]

## Drills
- [[orderbook-std-map-p99|练习：订单簿用了 std::map，p99 会从哪里来]]

## Cards (4)
1. [[hft-order-index-cancel-path]]
2. [[hft-order-index-intrusive-list]]
3. [[hft-order-index-time-priority]]
4. [[hft-order-index-primitive-map]]
%% trellis:end %%

## Notes
