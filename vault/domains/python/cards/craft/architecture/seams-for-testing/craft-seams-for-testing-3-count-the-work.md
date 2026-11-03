---
id: craft-seams-for-testing-3-count-the-work
node: craft.architecture.seams-for-testing
type: qa
step: 3
---
## Q
**测试接缝 · 怎样测「索引真的起作用了」「缓存真的命中了」**｜架构

一个带索引的内存表，有索引和没索引时 `select` 返回的结果完全一样。只比较结果的测试，哪怕索引代码被整个删掉也照样通过。性能性质（索引缩小扫描范围、缓存省了步骤、增量重算只算受影响的格子）该怎么断言？

## A
**要点。** 暴露一个记录工作量的只读计数器：`last_scan_count`（最近一次查询真正检查了多少行）。测试同时断言结果相同和工作量更少。这类计数器把「惰性」「剪枝」「缓存命中」变成确定性事实，不依赖计时，不会有抖动。

```python
class Table:
    def __init__(self, rows: list[dict], indexed: bool) -> None:
        self._rows = rows
        self._index: dict | None = None
        if indexed:
            self._index = {}
            for i, r in enumerate(rows):
                self._index.setdefault(r["city"], []).append(i)
        self.last_scan_count = 0                       # 最近一次 select 真正检查了多少行

    def select_city(self, city: str) -> list[dict]:
        positions = range(len(self._rows)) if self._index is None else self._index.get(city, [])
        self.last_scan_count = len(positions)
        return [self._rows[i] for i in positions if self._rows[i]["city"] == city]   # 候选一定复查

rows = [{"id": i, "city": "北京" if i % 100 == 0 else "上海"} for i in range(1000)]
plain, fast = Table(rows, indexed=False), Table(rows, indexed=True)
a, b = plain.select_city("北京"), fast.select_city("北京")
print("结果相同:", a == b, "| 命中", len(a), "行")
print("无索引扫描", plain.last_scan_count, "行；有索引扫描", fast.last_scan_count, "行")
```

1000 行，其中每 100 行有一行在北京，实际输出：

```
结果相同: True | 命中 10 行
无索引扫描 1000 行；有索引扫描 10 行
```

**为什么。** 同样的做法还有：表格引擎的 `eval_count`（改一个格子，只重算依赖它的格子、每格恰好一次）、图像流水线的 `steps_executed`（前缀缓存命中后少跑了几步）、文件搜索的 `FindStats.visited`（剪枝后没进入被剪的目录）。

**易错。** 计数器是只读的、在锁内更新；测试不要去改它，也不要靠读私有字段，那样重构内部实现就会弄坏测试。
