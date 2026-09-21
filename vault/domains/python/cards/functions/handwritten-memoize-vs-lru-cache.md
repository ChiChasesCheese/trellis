---
id: handwritten-memoize-vs-lru-cache
node: functions.decorator-patterns
type: qa
tags: [grown]
---
## Q
手写一个 memoize 装饰器（用字典缓存参数到返回值的映射），相比直接用标准库的 `functools.lru_cache`，什么情况下才值得自己写？

## A
标准库 `lru_cache` 已经处理了「淘汰旧结果」「线程安全」「参数必须可哈希」这些细节，大多数场景直接用它就够。值得手写的场景是：需要按值而不是按对象哈希（比如把列表参数转成 tuple 后再做 key）、需要跨进程或跨重启持久化缓存（写到 Redis、磁盘），或者需要按业务规则设置过期时间（TTL）而不是按调用次数淘汰——这些都超出了 `lru_cache` 的能力范围。
