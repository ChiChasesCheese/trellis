---
id: uth-redis-sds-dict-2-rehash
node: redis.sds-dict
type: qa
step: 2
---
## Q
**渐进式 rehash 是怎么搬的**｜Redis · 8.10

一个有几百万个键的哈希表要扩容，Redis 怎么避免一次性卡住几百毫秒？

## A
**背景。** 哈希表元素多了，要新开一张更大的表，把所有元素按新桶数重新分一遍（rehash）。几百万个键一次搬完要卡几百毫秒，而 Redis 命令是单线程执行的，所有客户端都得等。办法：边用边搬，每次操作顺手搬一点。

**结构。** `dict` 里有两张哈希表和一个游标 `rehashidx`；扩容就是新建大表，再一点一点搬。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">dict: 两张哈希表 + 游标 rehashidx</text>
<text x="8" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧表 ht[0]</text>
<rect x="10" y="42" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="50" y="42" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="90" y="42" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="130" y="42" width="36" height="24" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="148" y="58" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">●</text>
<rect x="170" y="42" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="188" y="58" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">●</text>
<rect x="210" y="42" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="228" y="58" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">●</text>
<text x="130" y="84" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑ rehashidx</text>
<text x="8" y="104" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新表 ht[1] (约两倍大)</text>
<rect x="10" y="112" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="21" y="127.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">●</text>
<rect x="36" y="112" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="47" y="127.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">●</text>
<rect x="62" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="88" y="112" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="99" y="127.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">●</text>
<rect x="114" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="140" y="112" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="151" y="127.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">●</text>
<rect x="166" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="192" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="218" y="112" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="229" y="127.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">●</text>
<rect x="244" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="270" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="296" y="112" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="8" y="160" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每次增删改查顺手搬 1 个桶; 新键直接进新表</text>
<text x="8" y="176" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">查找要查两张表; serverCron 每轮再花约 1 毫秒帮忙</text>
<text x="8" y="198" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">把 O(n) 的搬迁摊到许多次操作上, 单次只多一个桶</text>
</svg>
```

**细节。**

- 元素数达到桶数（负载因子 1）就开约两倍大的新表；初始大小 4
- 搬迁期间，每次增删改查顺手搬 1 个桶；新键直接进新表，查找要查两张表
- 定时任务 `serverCron` 每轮再花约 1 毫秒帮忙搬

**为什么。** 把 O(n) 的搬迁摊到许多次操作上，单次延迟只多一个桶；代价是搬迁期间两张表同时占内存。

**例题：** LC 706 设计哈希映射（同类：LC 705 设计哈希集合）

不用内建哈希表，实现 `MyHashMap`：`put`、`get`、`remove`。例：`put(1,1)`、`put(2,2)`、`get(1)` → `1`、`get(3)` → `-1`。下面是定长桶加链的版本；Redis 的 `dict` 在它的基础上，表满了就新开一张大表、再逐步搬迁。

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
