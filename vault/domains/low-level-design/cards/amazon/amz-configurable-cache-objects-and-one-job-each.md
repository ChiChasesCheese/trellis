---
id: amz-configurable-cache-objects-and-one-job-each
node: amazon.amz-configurable-cache
type: qa
step: 2
tags: [grown]
---
## Q
在可配置缓存设计里，有哪几个核心对象？各自只负责哪一件事？

## A
`Cache`：编排一次读写、守容量上限，不知道淘汰谁、数据放哪；`EvictionPolicy`（`LruPolicy`/`LfuPolicy`）：只记 key 的使用顺序或次数，不存值；`Store`（`MemoryStore`/`FileStore`）：只按 key 存取值，不懂顺序；`CacheConfig`：把「lru」「file」这样的名字翻成对象。划分依据：策略只依赖 key，后端只依赖值，两者互不引用，才能自由组合。
