%% trellis:begin %%
# 订单簿要支持的操作与复杂度
*订单簿与撮合引擎的实现*

新增、撤单、改单、成交、查询最优价；操作频率分布（撤单远多于成交）决定了哪些操作必须 O(1)。

**Requires:** [[domains/hft/map/protocols.itch-model|ITCH 行情模型：逐笔订单（order-by-order）]]

**Unlocks:** [[domains/hft/map/orderbook.price-levels|价格档位怎么存：数组、有序树与排序 vector]], [[domains/hft/map/orderbook.order-index|订单索引与侵入式链表]]

## Readings
- [[wiki-order-book|订单簿（order book）]]

## Drills
- [[orderbook-std-map-p99|练习：订单簿用了 std::map，p99 会从哪里来]]

## Cards (4)
1. [[hft-requirements-operations]]
2. [[hft-requirements-cancel-dominates]]
3. [[hft-requirements-budget]]
4. [[hft-requirements-exchange-vs-client]]
%% trellis:end %%

## Notes
