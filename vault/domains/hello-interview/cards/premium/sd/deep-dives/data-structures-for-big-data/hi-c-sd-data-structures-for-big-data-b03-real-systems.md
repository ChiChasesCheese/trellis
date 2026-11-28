---
id: hi-c-sd-data-structures-for-big-data-b03-real-systems
node: sd.deep-dives.data-structures-for-big-data.beyond
type: qa
step: 3
---
## Q
**大数据结构 · 拓展：这些结构在真实系统里在哪**｜拓展 · 加分

面试官问：你说的布隆过滤器和 Count-Min Sketch，真实系统里有用吗？

## A
- **LSM 存储引擎：** Cassandra、HBase、RocksDB 给每个 SSTable 配布隆过滤器，查键时先排除不含它的文件，省下读盘。这是布隆过滤器最经典的用法。
- **缓存准入：** Caffeine（Java 缓存库）的 TinyLFU 用 Count-Min Sketch 估计访问频率，决定新条目是否值得挤掉旧条目；而它不用来存全部计数，因此很省内存。
- **CDN 防止一次性内容占缓存：** 内容第一次被请求时只记入布隆过滤器，第二次才真正缓存，避免只被访问一次的对象占满缓存。
- **规律：** 在已有精确系统前面放一个小而近似的过滤器，近似错误只会导致多做一点事，而不会出错。这才是概率结构敢用的前提。
