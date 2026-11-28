---
id: hi-c-sd-distributed-cache-n04-single-node-ttl
node: sd.problem-breakdowns.distributed-cache.notes
type: qa
step: 4
---
## Q
**分布式缓存 · 单机哈希表与 TTL**｜摘要 · 必会

最简单的缓存是什么？加上过期时间后，为什么光在读时检查还不够？

## A
- **起点：** 缓存的核心就是哈希表（Python 的 dict、Java 的 HashMap、Go 的 map），get / set / delete 都是 O(1)，哈希表自己处理冲突和扩容。单机放一个 Cache 实例，请求来了解析后调对应方法。面试写伪代码时不用管语法，也先别管键不存在这类边界，先确认面试官允许。
- **加 TTL：** 值旁边存到期时间戳，存成 `(value, expiry)`。get 时检查已过期就删掉并返回空；set 时由 TTL 算出到期时间。
- **只在读时检查的问题：** 没人再请求的过期键永远不会被发现，缓存里堆满死数据，白占内存。
- **补一个后台清理（janitor）：** 周期性扫描并删除已过期的键，可按固定间隔（比如每分钟）或在内存压力达到阈值时触发。
- **取舍：** 扫得勤，过期数据走得快，但耗 CPU；扫得稀，省 CPU，但内存里死数据多。
