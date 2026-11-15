---
slug: design-log-storage-system
---
## Q
**LC 635 设计日志存储系统**｜Medium

日志有 `id` 与时间戳 `Year:Month:Day:Hour:Minute:Second`（如 `2017:01:01:23:59:59`，补零）。设计 `LogSystem`：`put(id, timestamp)` 存日志；`retrieve(start, end, granularity)` 返回时间戳在 `[start, end]` 内的日志 id，比较只精确到 `granularity` 指定的单位。

## A
**一句话。** 时间戳补零，字典序等于时间顺序；比较时只截取到给定粒度对应的前缀长度，对前缀比较大小。

```python
class LogSystem:
    LEN = {'Year': 4, 'Month': 7, 'Day': 10,
           'Hour': 13, 'Minute': 16, 'Second': 19}

    def __init__(self):
        self.logs = []                    # (时间戳, id)

    def put(self, id, timestamp):
        self.logs.append((timestamp, id))

    def retrieve(self, start, end, granularity):
        n = self.LEN[granularity]         # 只比较这么长的前缀
        s, e = start[:n], end[:n]
        return [i for t, i in self.logs if s <= t[:n] <= e]
```

**复杂度。** 时间 `put` 为 `O(1)`，`retrieve` 为 `O(日志数)`，空间 `O(日志数)`。

**易错点。**
- 把时间戳解析成数字再比：多此一举，补零的定宽字符串直接按字典序比较。
- 前缀长度算错：`2017:01` 占 7 位（含冒号），各粒度依次是 4、7、10、13、16、19。
- 只截取 `start` 不截取 `end`：两端都要截到同一精度，才能让「同一天」之类的范围闭合。

**追问。**
- 日志很多、查询频繁怎么办？：按时间戳排序存，用二分找到范围的两端，`O(log n + 结果数)`。
- 为什么截断后比较是对的？：例如粒度为天时，`end` 截到天，同一天内的任何时刻都不超过它。

**同模式。** LC 362 敲击计数器、LC 981 基于时间的键值存储、LC 2034 股票价格波动、LC 1166 设计文件系统
