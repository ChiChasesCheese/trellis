%% trellis:begin %%
# 架构理解（Architecture）
*编码功力（Coding Craft）*

类之上的判断：依赖方向、事务边界、哪里值得抽象，以及同一设计从单进程到分布式怎么变。

## Topics
- [[domains/python/map/craft.architecture.functional-core-imperative-shell|函数式核心 + 命令式外壳（functional core, imperative shell）]]
- [[domains/python/map/craft.architecture.lock-lives-with-the-invariant|锁跟着不变量走：谁拥有不变量，谁拥有锁（aggregate owns its lock）]]
- [[domains/python/map/craft.architecture.lock-as-transaction-boundary|一把锁就是一个事务：临界区边界 = 原子性边界]]
- [[domains/python/map/craft.architecture.dependency-direction-consumer-owns-interface|依赖方向：接口由使用方定义，核心不依赖基础设施]]
- [[domains/python/map/craft.architecture.source-of-truth-and-derived-caches|真相与派生缓存：谁是真相、谁是投影、漂移怎么办]]
- [[domains/python/map/craft.architecture.interface-only-when-earned|接口是挣来的：什么时候不抽象]]
- [[domains/python/map/craft.architecture.entity-vs-value-object|实体 vs 值对象：身份、可变性与谁拥有状态]]
- [[domains/python/map/craft.architecture.error-boundaries-and-failure-taxonomy|错误边界与失败分类：哪些吞、哪些抛、哪些变成值]]
- [[domains/python/map/craft.architecture.seams-for-testing|测试接缝：时钟、文件系统、sleep、可观测计数器]]
- [[domains/python/map/craft.architecture.in-process-to-distributed|从单进程到分布式：每个原语在生产里换成什么]]
- [[domains/python/map/craft.architecture.event-time-vs-processing-time|事件时间 vs 处理时间：乱序、重复、迟到的事实]]
- [[domains/python/map/craft.architecture.order-side-effects-by-reversibility|按可逆性给副作用排序：先做会失败的、可回滚的，最后做不可撤销的]]
- [[domains/python/map/craft.architecture.thin-service-fat-domain|服务层薄、领域对象厚：编排者不持有不变量]]
- [[domains/python/map/craft.architecture.lock-hierarchy-and-reentrancy|调用方向与可重入：谁能调谁，回调时手里不能有锁]]
- [[domains/python/map/craft.architecture.command-event-fact|命令、事件与事实：过去式、自带全部信息、不可变]]
- [[domains/python/map/craft.architecture.extension-points-worth-paying-for|扩展点值得付费的地方：数据代替代码、从第一天就预留的字段]]
- [[domains/python/map/craft.architecture.unit-of-inventory-modeling|库存的单位怎么选：房型夜、车的行程段、场次座位、航班实例]]
- [[domains/python/map/craft.architecture.composition-of-independent-axes|独立变化轴的组合：N×M 个组合只写 N+M 个小类]]
- [[domains/python/map/craft.architecture.explicit-non-goals-and-simplifications|明说的简化与非目标：说清楚没做什么、接缝在哪]]
- [[domains/python/map/craft.architecture.observability-as-design|可观测性是设计的一部分：丢弃必须计数，状态变化必须留痕]]
%% trellis:end %%

## Notes
