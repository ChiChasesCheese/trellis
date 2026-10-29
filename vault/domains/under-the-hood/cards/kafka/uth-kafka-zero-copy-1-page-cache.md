---
id: uth-kafka-zero-copy-1-page-cache
node: kafka.zero-copy
type: qa
step: 1
---
## Q
**不自建缓存：页缓存**｜Kafka · 4.0

Kafka broker 为什么不在 JVM 堆里缓存消息，而是把读写都交给操作系统的页缓存（page cache）？

## A
**背景。** 读写磁盘比读写内存慢得多，常见做法是程序自己在内存里缓存热数据。但 Kafka 是 Java 程序：堆里再缓存一份，数据就存了两遍，Java 对象还有额外开销，缓存一大，垃圾回收（GC）也会让程序卡顿。

**结构。** 操作系统本来就会把读写过的磁盘内容留在空闲内存里，叫页缓存。Kafka 写消息只是追加到文件，数据先停在页缓存，由操作系统异步写回磁盘。`log.flush.interval.messages` 默认是 `Long.MAX_VALUE`：Kafka 自己不主动 `fsync`（强制落盘），持久性靠多副本。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="8" y="18" width="80" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产者写</text>
<line x1="88" y1="32" x2="116.697" y2="47.1927" stroke="currentColor" stroke-width="1.2"/>
<polygon points="122,50 115.3,49.8 118.1,44.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="122" y="38" width="110" height="40" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="177" y="62.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页缓存 (内核)</text>
<rect x="8" y="70" width="80" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="88.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者读</text>
<line x1="122" y1="66" x2="95.3666" y2="79.3167" stroke="currentColor" stroke-width="1.2"/>
<polygon points="90,82 94.0,76.6 96.7,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="262" y="38" width="70" height="40" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297" y="62.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<line x1="232" y1="58" x2="256" y2="58" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polygon points="262,58 256.0,61.0 256.0,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="247" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内核异步刷盘</text>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka 自己不 fsync, 也不在堆里缓存</text>
</svg>
```

**细节。**

- 设计文档估算：32 GB 的机器，页缓存最多 28–30 GB，没有 GC 开销。
- broker 重启后页缓存仍是热的，进程内缓存却要重建。

**为什么。** 日志顺序追加、顺序读，内核的预读和回写本来就擅长；缓存淘汰（LRU 一类：踢掉最久没用的）也一并交给内核。

**例题：** LC 146 LRU 缓存

设计容量固定的 LRU 缓存：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要 O(1)。`1 <= capacity <= 3000`。

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()  # 队首最旧，队尾最新

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)
        return self.store[key]

    def put(self, key: int, value: int) -> None:
        # 先删后插，保证已存在的键也被移到队尾
        self.store.pop(key, None)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```
