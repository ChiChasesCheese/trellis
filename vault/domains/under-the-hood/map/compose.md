%% trellis:begin %%
# 数据结构组合：开源框架里的类设计

类设计题考的是怎样把几种数据结构拼成一个类、让每个操作都够快、几份结构始终一致：先学六种组合骨架，再看 Spring、Caffeine、Java 线程池、Kubernetes、Go、HikariCP、ORM、Disruptor 怎样用它们。

## Topics
- [[domains/under-the-hood/map/compose.patterns|组合模式总览：设计题的六种骨架]]
- [[domains/under-the-hood/map/compose.spring-three-level-cache|Spring 单例 Bean 的三级缓存：为什么是三层]]
- [[domains/under-the-hood/map/compose.spring-bean-registry|Spring 的 Bean 注册表：Map + 列表与双向依赖表]]
- [[domains/under-the-hood/map/compose.interceptor-chain|拦截器链与 Filter 链：列表 + 游标]]
- [[domains/under-the-hood/map/compose.caffeine|Caffeine 缓存：哈希表 + 访问队列 + 频率草图 + 时间轮]]
- [[domains/under-the-hood/map/compose.indexed-heap|可删除、可改优先级的堆：堆 + 下标]]
- [[domains/under-the-hood/map/compose.thread-pool|Java 线程池：一个原子整数、一个任务队列、一组工人]]
- [[domains/under-the-hood/map/compose.k8s-workqueue|Kubernetes workqueue：队列 + 待处理集合 + 处理中集合]]
- [[domains/under-the-hood/map/compose.k8s-indexer|client-go 的 Indexer：主存储 + 二级索引]]
- [[domains/under-the-hood/map/compose.go-sync-map|Go 的 sync.Map：只读表 + 脏表，以及 1.24 起的并发哈希字典树]]
- [[domains/under-the-hood/map/compose.singleflight|singleflight：合并同时到来的重复请求]]
- [[domains/under-the-hood/map/compose.connection-pool|连接池：HikariCP 的 ConcurrentBag]]
- [[domains/under-the-hood/map/compose.event-bus|事件总线：事件类型 → 订阅者集合]]
- [[domains/under-the-hood/map/compose.http-router|HTTP 路由表：每个方法一棵基数树]]
- [[domains/under-the-hood/map/compose.orm-session|ORM 的 Session：身份映射 + 工作单元]]
- [[domains/under-the-hood/map/compose.ring-buffer|LMAX Disruptor：环形数组 + 序号]]
%% trellis:end %%

## Notes
