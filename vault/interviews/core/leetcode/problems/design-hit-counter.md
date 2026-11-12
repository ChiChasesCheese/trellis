---
slug: design-hit-counter
---
## Q
**LC 362 敲击计数器**｜Medium

设计 `HitCounter`：`hit(t)` 记录第 `t` 秒的一次敲击，`getHits(t)` 返回 `(t-300, t]` 内的敲击数，时间戳单调不减。

## A
**一句话。** 时间戳追加到队尾，查询时从队头弹掉过期的，剩下的长度就是答案。

```python
class HitCounter:
    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp):
        self.hits.append(timestamp)   # 同一秒多次就存多份

    def getHits(self, timestamp):
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()       # 窗口 (t-300, t]
        return len(self.hits)
```

**复杂度。** 时间 `hit` 为 `O(1)`，`getHits` 均摊 `O(1)`，空间 `O(窗口内敲击数)`。

**易错点。**
- 边界写成 `<`：`getHits(301)` 会返回 `4`，应为 `3`，因为 `1` 已不在 `(1, 301]` 里。
- 同一秒的多次敲击用集合去重：要各算一次。

**追问。**
- 每秒上百万次敲击怎么办？：改成 300 个环形桶，存 `(秒, 次数)`，内存固定 `O(300)`，与流量无关；桶里秒数过期要先清零。
- 窗口长度可变呢？：队列有序，二分找最早未过期位置，`O(log n)`，且不能边查边弹。

**同模式。** LC 359 日志速率限制器、LC 933 最近的请求次数、LC 346 数据流中的移动平均值
