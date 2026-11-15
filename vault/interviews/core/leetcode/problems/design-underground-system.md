---
slug: design-underground-system
---
## Q
**LC 1396 设计地铁系统**｜Medium

实现 `check_in(id, station, t)`、`check_out(id, station, t)` 和 `get_average_time(start, end)`：后者返回所有从 `start` 站到 `end` 站（有方向）的完整行程的平均用时。

## A
**一句话。** 一个字典记「乘客现在在哪站、几点进的」，另一个按 `(起点, 终点)` 累计总时长和次数。

```python
class UndergroundSystem:
    def __init__(self):
        self.riding = {}    # id -> (起点站, 进站时间)
        self.stat = {}      # (起点, 终点) -> [总时长, 次数]

    def check_in(self, id, station, t):
        self.riding[id] = (station, t)

    def check_out(self, id, station, t):
        start, t0 = self.riding.pop(id)
        rec = self.stat.setdefault((start, station), [0, 0])
        rec[0] += t - t0
        rec[1] += 1

    def get_average_time(self, start, end):
        total, cnt = self.stat[(start, end)]
        return total / cnt
```

**复杂度。** 三个操作都是 `O(1)`，空间 `O(乘客数 + 站点对数)`。

**易错点。**
- 平均数里存每次用时的列表：每次查询要重新求和，改存总和与次数就是 `O(1)`。
- 键写成无序的站点对：`A -> B` 与 `B -> A` 是两条不同路线。
- 出站后不删 `riding`：同一乘客再次进站会覆盖，但占着内存。

**追问。**
- 乘客可能不出站怎么办？：题目保证一定出站；实际系统要给 `riding` 设过期清理。
- 并发调用？：对 `riding` 和 `stat` 加锁，或按乘客 `id` 分片。

**同模式。** LC 1166 设计文件系统、LC 362 敲击计数器、LC 359 日志速率限制器、LC 2034 股票价格波动
