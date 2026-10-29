%% trellis:begin %%
# 前缀和与差分：监控计数器与 rate()
*考点补全：后端系统里的算法*

Prometheus 的计数器只增不减，本质是前缀和；rate() 和 increase() 用两点之差算一段时间的增量，还要处理进程重启后计数归零；Kafka 的消费延迟也是两个累计值相减。

## Cards (3)
1. [[uth-gaps-prefix-sum-1-counter]]
2. [[uth-gaps-prefix-sum-2-reset]]
3. [[uth-gaps-prefix-sum-3-kafka-lag]]
%% trellis:end %%

## Notes
