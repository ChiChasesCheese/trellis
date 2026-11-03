---
id: craft-source-of-truth-and-derived-caches-3-index-must-be-rebuildable
node: craft.architecture.source-of-truth-and-derived-caches
type: qa
step: 3
---
## Q
**真相与派生缓存 · 索引总是跟不上行：怎么发现、怎么防**｜架构

内存表（`Table`）把行存在列表里，并为 `city` 列维护一个「值 → 行号」的索引加速查询。`insert` 同步更新了索引，后来有人新增了 `update_city`，只改行，忘了动索引。查询会怎样？有什么办法让这类 bug 在测试里立刻暴露？

## A
**要点。** 索引是行的派生物，所以每条会改行的写路径，都要在同一个方法里同步更新索引，漏一处就是漂移。防护办法：派生物必须能从真相整体重建，于是写一个 `check_index()` 从行重建索引再与现有的比较，在测试里每次写操作之后断言它。

```python
class Table:
    def __init__(self) -> None:
        self._rows: list[dict] = []                    # 真相
        self._index: dict[object, list[int]] = {}      # 派生：city -> 行号

    def insert(self, row: dict) -> None:
        self._rows.append(dict(row))
        self._index.setdefault(row["city"], []).append(len(self._rows) - 1)   # 同一方法里更新

    def update_city(self, i: int, city: str) -> None:
        self._rows[i]["city"] = city          # bug：改了真相，忘了动索引

    def select_city(self, city: str) -> list[dict]:
        return [self._rows[i] for i in self._index.get(city, [])]

    def check_index(self) -> bool:            # 索引永远能从真相重建
        rebuilt: dict[object, list[int]] = {}
        for i, r in enumerate(self._rows):
            rebuilt.setdefault(r["city"], []).append(i)
        return rebuilt == self._index

t = Table()
t.insert({"name": "甲", "city": "北京"})
t.update_city(0, "上海")
print("查上海:", t.select_city("上海"), "查北京:", t.select_city("北京"))
print("索引与行一致:", t.check_index())
```

插入「甲，北京」，把它改成上海，再查，实际输出：

```
查上海: [] 查北京: [{'name': '甲', 'city': '上海'}]
索引与行一致: False
```

**为什么。** 症状有两个：该查到的查不到，不该查到的反而出现，而且行本身是对的，只有走索引的路径错，这是找漂移的典型线索。

**易错。** 另一种更稳的做法是让所有写入只经过一个入口（`_put`、`_remove`），由它们统一维护索引，其他方法只调用这两个入口。写路径散落多处时，每多一处就多一次漏更新的机会。
