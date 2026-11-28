---
id: hi-c-sd-distributed-cache-b03-stampede
node: sd.problem-breakdowns.distributed-cache.beyond
type: qa
step: 3
---
## Q
**分布式缓存 · 拓展：热键过期瞬间的缓存击穿**｜拓展 · 加分

热键恰好过期，同一瞬间一万个请求都未命中并去查数据库，怎么办？

## A
- **现象：** 缓存击穿（stampede，也叫 thundering herd）：热键一过期，所有未命中请求同时回源，数据库瞬间被压垮。
- **单飞（single-flight）：** 同一个键同一时刻只让一个请求去加载，其他请求等它的结果。20 个线程并发请求同一个键，实测只触发 1 次加载。
- **其他手段：** 给 TTL 加随机抖动（避免大批键同一时间过期）；热键在过期前提前异步刷新；短时间缓存"不存在"的结果，防止穿透；过期后仍短暂返回旧值（stale-while-revalidate）并后台刷新。
- **实现要点：** 锁只保护"登记/查找 Future"，不要包住慢的加载；加载失败也要把异常传给追随者并清理登记，否则追随者永远等下去。
- **取舍：** 单飞只在单进程内有效，多实例要用分布式锁或让缓存本身提供，且增加了领头者变慢拖累所有人的风险，所以要给加载加超时。
- **模式。** 请求合并：把对同一昂贵资源的并发请求折叠成一次。

```python
def do(self, key, load):
    with self.lock:                       # 锁只管登记，不包加载
        fut = self.inflight.get(key)
        leader = fut is None
        if leader: fut = self.inflight[key] = Future()
    if not leader:
        return fut.result()               # 追随者等同一个结果
    try: fut.set_result(load())
    except Exception as e: fut.set_exception(e)
    finally:
        with self.lock: del self.inflight[key]
    return fut.result()
```
