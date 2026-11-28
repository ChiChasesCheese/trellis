---
id: hi-c-sd-change-data-capture-n11-cache-invalidation
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 11
---
## Q
**变更数据捕获 · 用 CDC 做缓存失效有必要吗**｜摘要 · 必会

用户资料缓存在 Redis，行变了要删缓存。监听 users 表来删 key 好吗？

## A
- **能用但多余：** 改行的那段代码手里本来就有 user ID，在同一请求、同一代码路径里直接删对应的 key 即可，简单而且立即生效。
- **多出来的机器：** 绕道 CDC 要引入连接器、主题和消费者，只为重新发现写入方早就知道的事。
- **甚至不用主动失效：** 能接受资料旧一分钟，设一个短 TTL 就够。
- **和搜索索引的区别：** 缓存不需要每次变更的持久流；漏掉一次失效，会随 TTL 过期，之后按需重新加载。
