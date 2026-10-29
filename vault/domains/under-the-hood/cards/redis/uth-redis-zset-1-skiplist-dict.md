---
id: uth-redis-zset-1-skiplist-dict
node: redis.zset
type: qa
step: 1
---
## Q
**有序集合为什么要存两份**｜Redis · 8.10

Redis 的 ZSET 底层是什么？`ZSCORE` 和 `ZRANGE` 为什么都很快？

## A
**背景。** 有序集合要回答两种完全不同的问题：某个成员的分数是多少（按成员查），第 10 到 20 名是谁（按分数排序）。一张哈希表答不了第二个，一个有序结构又很难快速答第一个。所以存两份，各管一种。跳表（skip list）是在有序链表上多叠几层“快车道”，查找时先走高层、再逐层下来。

**结构。** 一张哈希表（成员 → 分数）加一个跳表（按分数排序），两者共用同一份成员字符串。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">哈希表: 成员 → 分数 (查分数 O(1))</text>
<rect x="10" y="24" width="64" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="42" y="39.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a → 1</text>
<rect x="80" y="24" width="64" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="112" y="39.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b → 2</text>
<rect x="150" y="24" width="64" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="182" y="39.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c → 3</text>
<rect x="220" y="24" width="64" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="252" y="39.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">d → 4</text>
<text x="8" y="74" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">跳表: 按分数排序, L0 是有序链表, 上层是快车道</text>
<rect x="26" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="42" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">头</text>
<rect x="78" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="94" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="130" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="146" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b</text>
<rect x="182" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="198" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c</text>
<rect x="234" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="250" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">d</text>
<rect x="286" y="142" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="302" y="155.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">e</text>
<line x1="58" y1="152" x2="78" y2="152" stroke="currentColor" stroke-width="1"/>
<polygon points="78,152 72.0,154.7 72.0,149.3" fill="currentColor"/>
<line x1="110" y1="152" x2="130" y2="152" stroke="currentColor" stroke-width="1"/>
<polygon points="130,152 124.0,154.7 124.0,149.3" fill="currentColor"/>
<line x1="162" y1="152" x2="182" y2="152" stroke="currentColor" stroke-width="1"/>
<polygon points="182,152 176.0,154.7 176.0,149.3" fill="currentColor"/>
<line x1="214" y1="152" x2="234" y2="152" stroke="currentColor" stroke-width="1"/>
<polygon points="234,152 228.0,154.7 228.0,149.3" fill="currentColor"/>
<line x1="266" y1="152" x2="286" y2="152" stroke="currentColor" stroke-width="1"/>
<polygon points="286,152 280.0,154.7 280.0,149.3" fill="currentColor"/>
<rect x="26" y="116" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="116" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="234" y="116" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="126" x2="130" y2="126" stroke="currentColor" stroke-width="1"/>
<polygon points="130,126 124.0,128.7 124.0,123.3" fill="currentColor"/>
<line x1="162" y1="126" x2="234" y2="126" stroke="currentColor" stroke-width="1"/>
<polygon points="234,126 228.0,128.7 228.0,123.3" fill="currentColor"/>
<rect x="26" y="90" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="90" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="100" x2="130" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="130,100 124.0,102.7 124.0,97.3" fill="currentColor"/>
<text x="4" y="156" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L0</text>
<text x="4" y="130" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L1</text>
<text x="4" y="104" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L2</text>
<text x="8" y="184" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">节点随机分层: 升一层的概率 1/4, 最多 32 层</text>
<text x="8" y="202" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两个结构共用同一份成员字符串, 各管一种查询</text>
<text x="8" y="220" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只有跳表: 按成员找分数要 O(n); 只有哈希表: 没有顺序</text>
</svg>
```

**细节。**

- 哈希表：`ZSCORE` 是 O(1)
- 跳表：插入、删除、范围查找平均 O(log n)，最底层是有序链表
- 节点随机分层：升一层的概率 P = 1/4，最多 32 层
- 条目不超过 128 个、每个不超过 64 字节时，改用 listpack

**为什么。** 只用哈希表没有顺序，只用跳表按成员找分数要 O(n)；两个结构各管一种查询。

**例题：** LC 432 全 O(1) 的数据结构（同类：LC 146 LRU 缓存）

设计 `AllOne`：`inc(key)`、`dec(key)` 让计数加一、减一，`getMaxKey()`、`getMinKey()` 返回计数最大、最小的键，每个操作都要 O(1)。例：`inc("a")`、`inc("b")`、`inc("b")` 后，最大键是 `b`，最小键是 `a`。一个哈希表管“按键查位置”，一条有序链表管“按计数排序”，是同样的两份结构。

```python
class Bucket:
    __slots__ = ("cnt", "keys", "prev", "next")

    def __init__(self, cnt: int = 0) -> None:
        self.cnt = cnt
        self.keys: set[str] = set()
        self.prev: Bucket | None = None
        self.next: Bucket | None = None


class AllOne:
    def __init__(self) -> None:
        self.head, self.tail = Bucket(0), Bucket(-1)   # 哨兵：head.next 是最小计数桶，tail.prev 是最大
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}              # key -> 它当前所在的桶

    def _insert_after(self, node: Bucket, cnt: int) -> Bucket:
        new = Bucket(cnt)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def _remove(self, node: Bucket) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def inc(self, key: str) -> None:
        cur = self.where.get(key)
        anchor = self.head if cur is None else cur      # 新桶（计数 +1）该插在 anchor 后面
        target = anchor.next
        new_cnt = anchor.cnt + 1
        if target.cnt != new_cnt:                       # 相邻桶不是 cnt + 1 就新建一个
            target = self._insert_after(anchor, new_cnt)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:
                self._remove(cur)                       # 空桶要摘掉，否则 getMinKey 会读到空集合

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]                         # 计数归零：key 彻底删除
        else:
            target = cur.prev
            if target.cnt != cur.cnt - 1:
                target = self._insert_after(cur.prev, cur.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        cur.keys.discard(key)
        if not cur.keys:
            self._remove(cur)

    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))          # 任取一个即可

    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```
