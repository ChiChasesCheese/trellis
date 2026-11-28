---
id: mlp-traps-cache-leak
node: traps.cache-thread
type: qa
step: 1
---
## Q
**只增不减的会话缓存**｜语言陷阱与读代码

服务上线几天后内存一路上涨，最后被系统杀掉。代码里有这么一段，问题在哪？

```python
sessions = {}
def login(uid, n):
    sessions[(uid, n)] = bytearray(1000)
```

## A
- **问题：** 缓存只有写入，没有淘汰（eviction）；每次登录都新增一条，从不删除，条目数随时间无限增长，直到内存耗尽。运行 1000 次登录后 `len(sessions)` 就是 1000。
- **不是垃圾回收的错：** 字典持有对象的引用，对象一直可达，垃圾回收器（GC）不会清理；这叫"逻辑上的内存泄漏"，Java 里典型的是静态 `Map`。
- **键设计也会放大：** 键里带了登录序号，同一用户每次登录都是新条目；改成只用 `uid` 作键，同一用户只占一条。
- **修法一，设上限：** 容量到了就淘汰最久没用的（LRU），Java 用 `LinkedHashMap`，Python 用 `functools.lru_cache(maxsize=...)`。
- **修法二，设过期时间（TTL）：** 每条记录带过期时刻，读取时发现过期就删，或者后台定期清理。
- **修法三，生命周期结束就删：** 用户登出、会话关闭时显式 `pop`；缓存放到外部服务（如 Redis）并设过期。
- **怎么发现：** 看内存曲线是否只升不降；Java 用堆转储（heap dump）看哪个集合最大，Python 用 `tracemalloc` 比较两次快照。

**英文答法。**
- "The cache has **no eviction**, so it grows without bound; the GC can't free entries it still references."
- "I'd add a **size limit with LRU**, plus a **TTL**, and remove entries on logout."
