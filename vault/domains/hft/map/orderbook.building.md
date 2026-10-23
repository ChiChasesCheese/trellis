%% trellis:begin %%
# 从逐笔行情重建订单簿
*订单簿与撮合引擎的实现*

用 ITCH 消息维护 L3（每笔订单）订单簿，再聚合出 L2（每档总量）；处理改单、部分成交与订单删除。

**Requires:** [[domains/hft/map/orderbook.price-levels|价格档位怎么存：数组、有序树与排序 vector]], [[domains/hft/map/orderbook.order-index|订单索引与侵入式链表]], [[domains/hft/map/protocols.itch-messages|ITCH 5.0 关键消息与字段]]

**Unlocks:** [[domains/hft/map/orderbook.testing|订单簿的正确性：不变量与回放测试]]

## Readings
- [[nasdaq-itch-5|Nasdaq TotalView-ITCH 5.0 规范]]

## Cards (4)
1. [[hft-building-rules]]
2. [[hft-building-example]]
3. [[hft-building-l2-l3]]
4. [[hft-building-unknown-order]]
%% trellis:end %%

## Notes
