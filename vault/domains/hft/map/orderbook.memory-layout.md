%% trellis:begin %%
# 订单簿的内存布局：预分配与对象池
*订单簿与撮合引擎的实现*

启动时预分配订单对象池，热路径不调用 malloc；数据紧凑放置以命中缓存。

**Requires:** [[domains/hft/map/orderbook.price-levels|价格档位怎么存：数组、有序树与排序 vector]]

**Unlocks:** [[domains/hft/map/cpp.no-alloc|热路径不分配内存：对象池与 arena]]

## Drills
- [[orderbook-std-map-p99|练习：订单簿用了 std::map，p99 会从哪里来]]

## Cards (4)
1. [[hft-memory-layout-pool]]
2. [[hft-memory-layout-arrays]]
3. [[hft-memory-layout-cache-line]]
4. [[hft-memory-layout-exhaustion]]
%% trellis:end %%

## Notes
