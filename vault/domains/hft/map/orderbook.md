%% trellis:begin %%
# 订单簿与撮合引擎的实现

用什么数据结构在纳秒级完成挂单、撤单、成交，以及怎样从逐笔行情重建订单簿并保证它正确。

## Topics
- [[domains/hft/map/orderbook.requirements|订单簿要支持的操作与复杂度]]
- [[domains/hft/map/orderbook.price-levels|价格档位怎么存：数组、有序树与排序 vector]]
- [[domains/hft/map/orderbook.order-index|订单索引与侵入式链表]]
- [[domains/hft/map/orderbook.matching-engine|撮合引擎的实现]]
- [[domains/hft/map/orderbook.building|从逐笔行情重建订单簿]]
- [[domains/hft/map/orderbook.memory-layout|订单簿的内存布局：预分配与对象池]]
- [[domains/hft/map/orderbook.testing|订单簿的正确性：不变量与回放测试]]
%% trellis:end %%

## Notes
