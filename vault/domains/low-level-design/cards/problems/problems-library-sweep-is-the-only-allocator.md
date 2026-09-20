---
id: problems-library-sweep-is-the-only-allocator
node: problems.booking.library
type: qa
step: 3
tags: [grown]
---
## Q
图书馆管理（Library Management）里，「哪本副本归哪位预约者」这个决定该写在还书那一步吗？还是该用定时器？

## A
都不该。把分配规则收敛成**一个方法**，在每次读写入口惰性调用：

```python
def _sweep(self, now: datetime) -> None:
    self._holds.expire(now)                       # 过期的先下架
    for title_id in self._holds.queued_titles():  # 再按队列依次上架
        while self._holds.queue_length(title_id):
            free = self._free_barcodes(title_id)
            if not free:
                break
            member_id = self._holds.pop(title_id)
            self._holds.place_on_shelf(free[0], HoldEntry(member_id, title_id, expires))
```

- **写在还书里**的问题：新入藏一册、取消预约、保留到期时同样需要重新分配，于是这段逻辑被复制三遍（更常见的是漏写两遍）。
- **定时器**的问题：一万条活跃预约就是一万个定时任务，而且**测试无法控制时间**，只能靠 `sleep` 去验。

代价要说清：惰性过期意味着**只读属性也得先跑一次 `_sweep`**，否则会把早该下架的条目报给调用方。换来的是整个系统没有一个后台线程。
