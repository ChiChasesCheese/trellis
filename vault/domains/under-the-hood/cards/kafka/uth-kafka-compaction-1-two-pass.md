---
id: uth-kafka-compaction-1-two-pass
node: kafka.compaction
type: qa
step: 1
---
## Q
**日志太长怎么办：只留每个 key 的最新值**｜Kafka · 4.0

主题里的每条消息带一个 key（比如用户号），同一个 key 的新值不断追加进来，日志只增不减。`cleanup.policy=compact` 怎样把日志变短，又不丢“每个 key 现在的值”？

## A
**背景。** 日志只能在末尾追加，不能原地改，同一个 key 的旧值会越积越多。最笨的清理法，是对每条消息都去后面找“有没有同 key 的新消息”：每条都要再扫一遍日志，慢得没法用。

**结构。** 压实（compaction）只扫两遍。第一遍从头扫“脏段”（上次清理之后追加的段，不含正在写的活动段），用哈希表（一张 key 到数据的小表，查一次是 O(1)）记下每个 key 最后一次出现的偏移量（offset，消息在日志里的序号）。第二遍重写段文件，只留下偏移量不小于表中记录的消息。图里 A 出现了三次，清理后只剩 A:5。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 158">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">脏段 (追加的消息, key:偏移)</text>
<rect x="8" y="20" width="48" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="32" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A:0</text>
<rect x="61" y="20" width="48" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="85" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B:1</text>
<rect x="114" y="20" width="48" height="26" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="138" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A:2</text>
<rect x="167" y="20" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="191" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C:3</text>
<rect x="220" y="20" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B:4</text>
<rect x="273" y="20" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="297" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A:5</text>
<line x1="170" y1="48" x2="170" y2="62" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,68 167.0,62.0 173.0,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第一趟: 记最新偏移</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表</text>
<rect x="70" y="74" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="94" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A:5</text>
<rect x="123" y="74" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="147" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B:4</text>
<rect x="176" y="74" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="200" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C:3</text>
<line x1="170" y1="102" x2="170" y2="114" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,120 167.0,114.0 173.0,114.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第二趟: 只留表中那条</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">压实后</text>
<rect x="167" y="124" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="191" y="141.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C:3</text>
<rect x="220" y="124" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="244" y="141.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B:4</text>
<rect x="273" y="124" width="48" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="297" y="141.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A:5</text>
</svg>
```

**为什么。** 两遍各扫一次，代价只和日志长度成正比；表里只记最新位置，不用把整条消息装进内存。

**例题：** LC 706 设计哈希映射

不用内建哈希表，实现 `MyHashMap`：`put(key, value)` 插入或更新，`get(key)` 不存在返回 `-1`，`remove(key)` 删除映射。`0 <= key, value <= 10^6`。例：依次 `put(1,1)`、`put(2,2)`、`get(1)`、`get(3)`、`put(2,1)`、`get(2)`、`remove(2)`、`get(2)`，返回 `1, -1, 1, -1`。

```python
class MyHashMap:
    SIZE = 1009                               # 质数个桶：key 有规律时也分得开

    def __init__(self) -> None:
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.SIZE)]   # 每个桶是一条链：[[key, value], ...]

    def _bucket(self, key: int) -> list[list[int]]:
        return self.buckets[hash(key) % self.SIZE]

    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:                # 已存在：原地更新，不能再追加一条
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]        # 链内顺序无所谓：和最后一个交换再弹出，O(1) 删除
                bucket.pop()
                return
```
