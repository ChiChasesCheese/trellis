---
id: hi-pt-restaurant-waitlist-api-5-bucket
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 5
---
## Q
**餐厅候位 API · 分桶队列**｜追问 · 出自：餐厅候位 API › 逐步扩展 1

名单有一千个团，每次 `finish` 都从头扫整个列表太慢。怎样让取"第一个坐得下的人"接近 O(k)（k 是团的最大人数）？

## A
**结构。** 按人数分桶，每桶一个 `OrderedDict`（哈希表加双向链表，按到达顺序），值是全局到达序号；另有 `id → 人数` 字典。

**取人。** 只看人数不超过桌子容量的那几个桶的队首，取序号最小的。

```python
heads = [(seq, pid) for b in self._buckets[1:capacity + 1] if b
         for pid, seq in [next(iter(b.items()))]]
```
**数字。** 假设 1,000 个团、k = 10，比较次数从最多 1,000 降到最多 10；删除和判重 O(1)。
