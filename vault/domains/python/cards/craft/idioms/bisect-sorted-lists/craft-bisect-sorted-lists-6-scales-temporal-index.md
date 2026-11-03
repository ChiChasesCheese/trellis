---
id: craft-bisect-sorted-lists-6-scales-temporal-index
node: craft.idioms.bisect-sorted-lists
type: qa
step: 6
---
## Q
**bisect 与有序列表 · 从 Time Based Key-Value Store 到数据库的时间点查询**｜写法

LeetCode 的 Time Based Key-Value Store 要求 `get(key, ts)` 返回不晚于 `ts` 的最新值。同样的查询在数据库里（价格表、配置表按生效时间取当前版本）是怎么写和怎么加速的？

## A
**要点。** 三个尺度都是「有序的变化点 + 取 floor」。内存里是 `bisect_right` 减一；数据库里是 `WHERE effective_from <= ? ORDER BY effective_from DESC LIMIT 1`，加一个 `(key, effective_from)` 的联合索引：B 树索引就是磁盘版的有序列表，查询沿着树找到插入点，不用扫描全表。

```python
# LeetCode 981 Time Based Key-Value Store: set(key, value, ts) / get(key, ts) 取 ts 之前最近的值
class TimeMap:
    def __init__(self) -> None:
        self._ts: dict[str, list[int]] = defaultdict(list)
        self._vals: dict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, ts: int) -> None:
        self._ts[key].append(ts)            # 题目保证 ts 严格递增, 所以 append 保持有序
        self._vals[key].append(value)

    def get(self, key: str, ts: int) -> str:
        i = bisect_right(self._ts[key], ts) - 1
        return self._vals[key][i] if i >= 0 else ""

# 分布式 / 数据库: 同样的查询是「有序索引上取最后一个 <= ts 的版本」
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE price (sku TEXT, effective_from INT, amount INT)")
db.execute("CREATE INDEX idx ON price (sku, effective_from)")     # 有序索引 = 磁盘版的有序列表
db.executemany("INSERT INTO price VALUES (?,?,?)", [("a", 100, 5), ("a", 200, 6), ("a", 300, 7)])
def price_at(sku: str, t: int):
    row = db.execute("SELECT amount FROM price WHERE sku=? AND effective_from<=? "
                     "ORDER BY effective_from DESC LIMIT 1", (sku, t)).fetchone()
    return row[0] if row else None

tm = TimeMap(); tm.set("k", "v1", 1); tm.set("k", "v2", 4)
print([tm.get("k", t) for t in (0, 1, 3, 4, 9)])
print([price_at("a", t) for t in (99, 100, 250, 300)])
print(db.execute("EXPLAIN QUERY PLAN SELECT amount FROM price WHERE sku='a' AND effective_from<=250 "
                 "ORDER BY effective_from DESC LIMIT 1").fetchall()[0][-1])
```

实际输出：

```
['', 'v1', 'v1', 'v2', 'v2']
[None, 5, 6, 7]
SEARCH price USING INDEX idx (sku=? AND effective_from<?)
```

**变化。** 内存里数据放得下，只追加（时间戳递增）就能保持有序，查询不需要任何锁；数据库里还要处理并发写入、历史修订（回溯更正一个旧版本），常见做法是给每行加上「有效区间」`[valid_from, valid_to)` 或者只追加不改（append-only），修正就写一个新的版本。

**代价。** 联合索引的列顺序决定能不能被用到：`(key, effective_from)` 先定位到 key，再在其中有序；反过来则不行。时间点查询若用墙钟排序，不同机器的时钟偏差会让「最新」不明确，要么用数据库统一赋值的时间戳或序号，要么用版本号（见「时间类型」）。

**信号。** 「查某一时刻生效的配置、价格、权限」或「回放到某个时间点的状态」。
