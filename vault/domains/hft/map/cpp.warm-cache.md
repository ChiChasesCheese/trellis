%% trellis:begin %%
# 缓存预热：让热路径保持热
*低延迟 C++*

大部分时间不下单，下单代码和数据会被挤出缓存；定期用不真正发送的假订单走一遍热路径（cache warming）。

**Requires:** [[domains/hft/map/machine.cache-lines|缓存行、局部性与预取]], [[domains/hft/map/architecture.hot-cold-path|快路径与慢路径分离]]

## Drills
- [[cpp-hot-path-review|练习：评审一段 C++ 热路径，按对 p99.9 的伤害排序]]

## Cards (4)
1. [[hft-cpp-warm-cache-cold-order-path]]
2. [[hft-cpp-warm-cache-dummy-orders]]
3. [[hft-cpp-warm-cache-startup-vs-continuous]]
4. [[hft-cpp-warm-cache-risks]]
%% trellis:end %%

## Notes
