---
id: hi-sd-top-k-8-approx
node: sd.problem-breakdowns.top-k
type: qa
step: 8
---
## Q
**近似 Top K：Count-Min Sketch**｜系统设计 · 题目拆解

YouTube Top K 如果允许少量误差，可用 Count-Min Sketch（CMS）省掉几百 GB 的精确计数。请说明它怎样配合有序结构完成 Top K，在 Redis 和 Flink 中各怎么落地，以及各自的短板。

## A
**原理。** CMS 用多个哈希函数把元素映射到二维计数器，只记次数不记元素，内存只要几百 MB，操作是 add 和 estimate，估计值是真实值的上界。它不能列出元素，所以要配一个只保留前 1000 的有序列表或堆：每来一次播放就 add，随即 estimate，再更新有序列表。每个窗口各一套。

**Redis。** 每个事件执行 `CMS.INCRBY`、`CMS.QUERY`、`ZADD`，并裁剪有序集合。短板：事件可能已更新 CMS 却没更新有序集合，持久化的 AOF 也无法对应到 Kafka 偏移，难以精确恢复。

**Flink。** 把 CMS 和有序列表放进带检查点的状态，故障后从 Kafka 重放，更可靠、更快，但需要面试官和你都熟悉 Flink。

**易错。** 滑动窗口要从 CMS 里删除旧数据，Redis 不支持减，要用 Flink 或自写结构，超出面试期望。
