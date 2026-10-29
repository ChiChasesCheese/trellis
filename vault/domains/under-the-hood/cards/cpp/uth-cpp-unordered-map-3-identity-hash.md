---
id: uth-cpp-unordered-map-3-identity-hash
node: cpp.unordered-map
type: qa
step: 3
---
## Q
**int 的哈希为什么能被攻击**｜C++ · libstdc++ / libc++

怎样构造一批 `int` key，让 `unordered_map` 的每次操作都退化成 O(n)？

## A
**背景。** 哈希表快的前提是 key 被均匀打散到各个桶里。可在这两个库里，`int` 的哈希函数什么都不做，原样返回，所以桶号 = key 除以桶数的余数。知道桶数的人，就能故意挑出全落进同一个桶的 key。

**结构。** 桶号 = `hash(key) % 桶数`，而 `std::hash<int>` 是恒等函数。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">key 全是 97 的倍数, 桶数 97</text>
<rect x="10" y="26" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">97</text>
<rect x="56" y="26" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="76" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">194</text>
<rect x="102" y="26" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="122" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">291</text>
<rect x="148" y="26" width="40" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="168" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">388</text>
<text x="198" y="42" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">key % 97 = 0</text>
<rect x="10" y="70" width="40" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="30" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="10" y="92" width="40" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="30" y="106.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="10" y="114" width="40" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="30" y="128.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="10" y="136" width="40" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="30" y="150.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="66" y="71" width="46" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="89" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<line x1="50" y1="80" x2="66" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="66,80 60.0,82.7 60.0,77.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="126" y="71" width="46" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="149" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<line x1="110" y1="80" x2="126" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="126,80 120.0,82.7 120.0,77.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="186" y="71" width="46" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="209" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3</text>
<line x1="170" y1="80" x2="186" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="186,80 180.0,82.7 180.0,77.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="246" y="71" width="46" height="18" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="269" y="84.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k4</text>
<line x1="230" y1="80" x2="246" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="246,80 240.0,82.7 240.0,77.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="180" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全落进同一个桶: 每次查找沿链扫 n 个节点 = O(n)</text>
</svg>
```

**细节。**

- 实测：`hash(5)` 就是 5，`hash(123456)` 就是 123456
- 桶数是质数 97，把 50 个 97 的倍数插进去，实测全落进同一个桶，最长链 50
- 知道桶数的人（或在线评测的恶意数据）就能这样构造

**为什么。** 恒等哈希几乎零成本，质数取模能打散 1024 的倍数这类常见规律；但它不防刻意构造的输入。

**坑。** 面对对抗数据，换成带随机种子的哈希（如 splitmix64 加时间戳）。

**例题：** LC 706 设计哈希映射（同类：LC 705 设计哈希集合）

不用内建哈希表，实现 `MyHashMap`：`put`、`get`、`remove`。例：`put(1,1)`、`put(2,2)`、`get(1)` → `1`、`get(3)` → `-1`。下面用质数个桶、每个桶一条链，桶号就是 `hash(key) % SIZE`。

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
