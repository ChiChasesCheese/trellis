---
id: uth-java-hashmap-1-buckets
node: java.hashmap
type: qa
step: 1
---
## Q
**HashMap 怎么定位桶、何时扩容**｜Java · OpenJDK 25

`HashMap` 怎么按 key 秒查？把 key 放进哪个桶？默认容量和负载因子是多少，第几个元素触发扩容？

## A
**背景。** 按键找值，逐个比较是 O(n)。办法是用公式（`hashCode`，把对象变成一个整数）直接算出它该放在哪一格（桶，bucket）。两个 key 算到同一个桶（冲突）时，就把它们串成一条链表。

**结构。** 一个 `Node[]` 桶数组，每个桶是一条链表（冲突多时转红黑树）；桶下标 = `(n - 1) & hash`，`n` 是数组长度。例：长 16 的数组，`hash = 37`，`37 & 15 = 5`，放进第 5 个桶；再来一个也算到 5 的 key，接在它后面。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="20" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Node[16] 桶数组</text>
<rect x="18" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="37" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="56" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="75" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="94" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="113" y="40" width="19" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="132" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="151" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="189" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="208" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="227" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="246" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="265" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="284" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="303" y="40" width="19" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="122" y1="24" x2="122" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="122.0,38.0 119.5,33.0 124.5,33.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="130" y="26" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hash=37  37 &amp; 15 = 5</text>
<rect x="100" y="96" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128" y="113" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">37</text>
<line x1="122" y1="64" x2="122" y2="94" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122.0,94.0 119.5,89.0 124.5,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="140" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="128" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">21</text>
<line x1="128" y1="122" x2="128" y2="140" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,140.0 126.0,136.0 130.0,136.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="172" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">37 和 21 都是 5</text>
<text x="172" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">串成链表</text>
<text x="170" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标 = hash &amp; (n-1)</text>
</svg>
```

**细节。**

- 容量始终是 2 的幂，所以用位与代替取模。
- 默认初始容量 16，负载因子 0.75：元素超过 12 个（即放入第 13 个）时扩成 32。实测 `size` 12 时表长 16，13 时 32。

**为什么。** 位与比取模快；0.75 是空间与冲突概率的折中，太低浪费内存，太高链表变长。

**坑。** 预知元素个数时用 Java 19 起的 `HashMap.newHashMap(n)`，免得反复扩容。

**例题：** LC 706 设计哈希映射

不用内建哈希表，设计 `MyHashMap`：`put(key, value)` 已存在则更新；`get(key)` 不存在返回 `-1`；`remove(key)` 删除映射。`0 <= key, value <= 10^6`，最多调用 `10^4` 次。

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
