%% trellis:begin %%
# 事件总线：事件类型 → 订阅者集合
*数据结构组合：开源框架里的类设计*

Guava EventBus 注册时按事件类型建一张“类型 → 订阅者集合”的表、订阅者集合用写时复制；Spring 存一个监听器总集合，再按（事件类型，来源类型）缓存查找结果，有变动就清空缓存。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-event-bus-1-needs]]
2. [[uth-compose-event-bus-2-structures]]
3. [[uth-compose-event-bus-3-invariants-code]]
4. [[uth-compose-event-bus-4-real]]
5. [[uth-compose-event-bus-5-pubsub]]
%% trellis:end %%

## Notes
