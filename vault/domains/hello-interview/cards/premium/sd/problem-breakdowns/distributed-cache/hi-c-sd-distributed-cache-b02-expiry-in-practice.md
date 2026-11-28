---
id: hi-c-sd-distributed-cache-b02-expiry-in-practice
node: sd.problem-breakdowns.distributed-cache.beyond
type: qa
step: 2
---
## Q
**分布式缓存 · 拓展：过期清理不能全表扫描，实际怎么做**｜拓展 · 加分

后台清理如果每分钟遍历全部键，在几千万键的节点上有什么问题？Redis 是怎么做的？用堆怎么写？

## A
- **全扫的问题：** O(n) 的遍历在单线程模型里会长时间占住事件循环，请求延迟出现尖峰；扫描频率与键数成正比；绝大部分键没过期，白做功。
- **Redis 的做法：** 惰性删除（访问时检查）加主动过期：每一轮从设置了 TTL 的键里抽样 20 个检查并删除过期的，若超过 10% 已过期（5.0 及以前是 25%）就立刻再来一轮，否则停下，并限制每轮占用的时间。这样清理量跟着过期率走，不跟总键数走。
- **用最小堆：** 按到期时间排序，每轮只弹出堆顶已到期的，复杂度 O(处理条数 × log n)。覆盖写会让堆里留下旧记录，所以弹出时要核对：当前存的到期时间与堆里记录是否一致，不一致就是陈旧记录，跳过（惰性删除）。
- **代价：** 堆多占内存，每次 set 多一次 O(log n) 的插入；抽样法省内存但清理不及时。
- **模式。** 惰性删除：不去改堆里已作废的记录，弹出时再丢弃，省掉 O(n) 的定位。

```python
def sweep(self, budget=100):          # 每轮最多处理 budget 条
    removed, now = 0, self.clock()
    while self.heap and self.heap[0][0] <= now and budget:
        exp, key = heapq.heappop(self.heap); budget -= 1
        cur = self.data.get(key)
        if cur and cur[1] == exp:     # 记录与当前一致才算真过期
            del self.data[key]; removed += 1
    return removed
```
