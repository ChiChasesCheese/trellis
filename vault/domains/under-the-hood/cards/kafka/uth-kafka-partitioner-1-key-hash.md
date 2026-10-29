---
id: uth-kafka-partitioner-1-key-hash
node: kafka.partitioner
type: qa
step: 1
---
## Q
**带 key 的消息怎么选分区**｜Kafka · 4.0

主题有几个分区，生产者发一条带 key（比如用户号）的消息，该写进哪个分区？为什么同一个 key 总是落到同一个分区？

## A
**背景。** 同一个用户的消息要保持先后顺序，而 Kafka 只保证单个分区内有序，所以同一个 key 必须永远进同一个分区。随机选或轮流选，同一用户的消息就散开了；记一张“key → 分区”的表，又要全局共享，还会越长越大。

**结构。** 用哈希函数（把任意内容算成一个整数的函数）：分区号 = `toPositive(murmur2(keyBytes)) % numPartitions`。同一个 key 每次算出同一个整数，取余后分区号永远一样；每个生产者各自算，不用互相打听。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 158">
<rect x="8" y="18" width="72" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key u7</text>
<line x1="80" y1="32" x2="90" y2="32" stroke="currentColor" stroke-width="1.2"/>
<polygon points="96,32 90.0,35.0 90.0,29.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="96" y="18" width="84" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hash = 17</text>
<line x1="180" y1="32" x2="190" y2="32" stroke="currentColor" stroke-width="1.2"/>
<polygon points="196,32 190.0,35.0 190.0,29.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="196" y="18" width="100" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="246" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17 % 3 = 2</text>
<rect x="20" y="88" width="60" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="106.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="140" y="88" width="60" height="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="106.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="260" y="88" width="60" height="28" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="106.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<line x1="256" y1="48" x2="284.135" y2="81.4105" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288,86 281.8,83.3 286.4,79.5" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">示意数字: 真实哈希值是个大整数</text>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个 key 每次都进 p2</text>
</svg>
```

**细节。**

- `murmur2` 是一个很快的 32 位哈希函数，种子固定，结果可重复。
- `toPositive` 就是 `& 0x7fffffff`，清掉最高位的符号位，保证非负。不用 `Math.abs`：`Math.abs(Integer.MIN_VALUE)` 按规范仍返回负数。
- `partitioner.ignore.keys=true` 可以让 key 不参与选分区。

**为什么。** 无状态：不用查表，任何生产者都能独立算出同一个分区，同 key 的消息因此有序。

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
