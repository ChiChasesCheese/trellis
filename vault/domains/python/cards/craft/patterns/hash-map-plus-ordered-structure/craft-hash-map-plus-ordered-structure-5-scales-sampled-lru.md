---
id: craft-hash-map-plus-ordered-structure-5-scales-sampled-lru
node: craft.patterns.hash-map-plus-ordered-structure
type: qa
step: 5
---
## Q
**哈希表 + 有序结构 · 缓存大到链表都嫌贵时，Redis 怎么淘汰**｜架构

精确 LRU 要为每个条目维护链表指针，每次访问都要改链表。Redis 这类缓存里有上亿个键，它怎么近似 LRU？近似会损失多少命中率？

## A
**要点。** 不维护全局顺序，只给每个键存「最后访问时间」；要淘汰时随机抽几个键，淘汰其中最久未用的。省掉链表的内存和每次访问的链表操作，抽样数越大越接近精确 LRU。

```python
def sampled_lru(sample):
    last = {}                                  # 只存「最后访问时间」，不维护链表
    for t, k in enumerate(trace):
        if k in last: hit += 1
        elif len(last) >= CAP:
            cand = random.sample(list(last), sample)       # 抽样
            del last[min(cand, key=last.__getitem__)]      # 淘汰其中最久未用的
        last[k] = t
```

偏斜的访问序列（少数热点占大部分访问），容量 200：

```
精确 LRU     命中率 0.615
抽样 5 个    命中率 0.609
抽样 1 个    命中率 0.563（等于随机淘汰）
```

模拟里为了简单用 `list(last)` 抽样，每次淘汰是 O(n)，只用来比较命中率，不代表真实实现的成本。

**尺度对照。** 一个进程：dict + 链表，精确且 O(1)；一台缓存机器：近似 LRU，用少量精度换内存和吞吐；Caffeine 等用 TinyLFU（频率草图）进一步提高命中率。订单簿同样是「按价格再按时间」的优先级，交易所撮合引擎的核心结构。

**信号。** 条目数量大到每条记录一份额外指针就嫌贵，或访问路径要尽可能无锁。
