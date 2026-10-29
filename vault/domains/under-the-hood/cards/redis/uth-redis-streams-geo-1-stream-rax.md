---
id: uth-redis-streams-geo-1-stream-rax
node: redis.streams-geo
type: qa
step: 1
---
## Q
**Stream 里的消息怎么存**｜Redis · 8.10

Redis Stream 的 `XADD` 追加消息、`XRANGE` 按 ID 范围读，底下是什么结构？

## A
**结构。** 基数树（radix tree），键是 128 位的消息 ID，值是一个 listpack，每个 listpack 装一批消息。

**细节。**

- ID = 毫秒时间戳 + 序号，各 64 位，按大端编码，所以树里的字典序就是时间顺序
- 一个 listpack 默认最多 100 条消息或 4096 字节，满了开新节点
- 追加只动最后一个节点；按 ID 范围读，先在树里定位再顺序扫 listpack

**为什么。** 一条消息一个树节点太费内存，整条流一个 listpack 又没法快速定位；一批一个节点是折中。

**对应 LeetCode：** LC 208 实现前缀树 · LC 981 基于时间的键值存储
