%% trellis:begin %%
# 热路径不分配内存：对象池与 arena
*低延迟 C++*

malloc / new 的成本和不确定性；启动时预分配、对象池（pool）、arena 分配器、std::pmr。

**Requires:** [[domains/hft/map/orderbook.memory-layout|订单簿的内存布局：预分配与对象池]]

## Drills
- [[cpp-hot-path-review|练习：评审一段 C++ 热路径，按对 p99.9 的伤害排序]]

## Cards (4)
1. [[hft-cpp-no-alloc-why-malloc-slow]]
2. [[hft-cpp-no-alloc-fixed-pool]]
3. [[hft-cpp-no-alloc-arena-vs-pool]]
4. [[hft-cpp-no-alloc-pool-pitfalls]]
%% trellis:end %%

## Notes
