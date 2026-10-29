---
id: uth-kafka-compaction-3-skimpy-probe
node: kafka.compaction
type: qa
step: 4
---
## Q
**表冲突了怎么办：用指纹本身当探测序列**｜Kafka · 4.0

压实用的哈希表（`SkimpyOffsetMap`）里，两个 key 算到同一个槽位时怎么办？

## A
**背景。** 哈希表把 key 算成一个整数，再对槽数取余来选槽位；不同的 key 可能选到同一个槽，这叫冲突。常见的办法是每个槽挂一条链表，代价是一堆小对象和指针。

**结构。** 这张表用开放寻址（open addressing）：冲突了就换一个槽接着找空位，找槽的过程叫探测（probe）。整张表是一块连续的 `ByteBuffer`，每槽 24 字节（MD5 16 字节 + 偏移量 8 字节），没有指针、没有链表。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">探测 n 取 MD5 的第 n 到 n+3 字节, 对槽数取模</text>
<rect x="12" y="62" width="36" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="52" y="62" width="36" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="92" y="62" width="36" height="30" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="110" y="81.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<text x="110" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="132" y="62" width="36" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="172" y="62" width="36" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="212" y="62" width="36" height="30" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="230" y="81.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<text x="230" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="252" y="62" width="36" height="30" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="292" y="62" width="36" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="310" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="270" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新</text>
<circle cx="110" cy="40" r="9" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="110" y1="49" x2="110" y2="62" stroke="currentColor" stroke-width="1.2"/>
<circle cx="230" cy="40" r="9" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="230" y1="49" x2="230" y2="62" stroke="currentColor" stroke-width="1.2"/>
<circle cx="270" cy="40" r="9" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="270" y1="49" x2="270" y2="62" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="119" y1="40" x2="215" y2="40" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polygon points="221,40 215.0,43.0 215.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="239" y1="40" x2="255" y2="40" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polygon points="261,40 255.0,43.0 255.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每槽 24 字节: MD5 16 + 偏移 8</text>
</svg>
```

**细节。**

- 第 0 次探测取 MD5 的第 0–3 字节当整数，对槽数取余得位置；第 1 次取第 1–4 字节，依次到第 12–15 字节，共 13 次。
- 13 次都冲突，就退化为线性探测（逐个往后一槽）：在最后那个整数上逐次加 1。

**为什么。** 不需要第二个哈希函数：16 个字节本身就够出 13 个探测起点；整张表是一块连续内存，没有对象开销。

**例题：** LC 706 设计哈希映射

不用内建哈希表，实现 `MyHashMap`：`put(key, value)` 插入或更新，`get(key)` 不存在返回 `-1`，`remove(key)` 删除映射。`0 <= key, value <= 10^6`。例：依次 `put(1,1)`、`put(2,2)`、`get(1)`、`get(3)`、`put(2,1)`、`get(2)`、`remove(2)`、`get(2)`，返回 `1, -1, 1, -1`。

这份解答用拉链法（每个桶挂一条列表）处理冲突，对照上图的“换槽”做法。

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
