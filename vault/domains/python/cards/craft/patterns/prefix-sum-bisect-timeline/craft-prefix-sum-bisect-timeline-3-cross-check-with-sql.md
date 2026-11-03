---
id: craft-prefix-sum-bisect-timeline-3-cross-check-with-sql
node: craft.patterns.prefix-sum-bisect-timeline
type: qa
step: 3
---
## Q
**前缀和时间线 · 同一个模型再写一遍 SQL，当作测试的对照**｜架构

内存里的 `Timeline` 用二分和前缀和数组回答人数查询，边界（同一秒多个事件、区间无事件、区间早于所有事件）很容易写错。怎样得到一个独立于实现的"标准答案"来对拍？

## A
**要点。** 同一个模型（只存事件，人数 = 到某时刻为止的 `delta` 之和）可以直接翻译成 SQL：`SUM(delta) WHERE ts <= :t` 就是 `count_at`；窗口函数 `SUM(delta) OVER (ORDER BY ts, seq)` 就是前缀和数组，`seq` 在同一秒内给事件定序。区间最大值同样需要基线行：用 `UNION ALL` 补一行"区间开始时的累计值"。SQL 版几乎没有边界上的巧思，所以适合当对照。

```python
import bisect, random, sqlite3

times, counts = [], []                                   # Timeline：时间 + 前缀和
def append(ts, d): times.append(ts); counts.append((counts[-1] if counts else 0) + d)
def count_at(ts):
    i = bisect.bisect_right(times, ts) - 1
    return counts[i] if i >= 0 else 0
def max_in(a, b):
    lo, hi = bisect.bisect_left(times, a), bisect.bisect_right(times, b)
    return max([count_at(a), *counts[lo:hi]])

SQL_MAX_IN = """
WITH running AS (SELECT ts, SUM(delta) OVER (ORDER BY ts, seq) AS cnt FROM ev)
SELECT MAX(cnt) FROM (
  SELECT cnt FROM running WHERE ts BETWEEN :a AND :b
  UNION ALL
  SELECT COALESCE((SELECT SUM(delta) FROM ev WHERE ts <= :a), 0)   -- 区间开始时的基线
)"""

rng = random.Random(5)
events = [(ts, rng.choice([1, -1])) for ts in sorted(rng.randint(0, 100) for _ in range(200))]   # 随机进出事件
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE ev(seq INTEGER PRIMARY KEY, ts INT, delta INT)")
db.executemany("INSERT INTO ev(ts, delta) VALUES (?, ?)", events)
for t, d in events: append(t, d)

bad = 0
for _ in range(500):
    a = rng.randint(-2, 102); b = a + rng.randint(0, 40)
    bad += db.execute(SQL_MAX_IN, {"a": a, "b": b}).fetchone()[0] != max_in(a, b)
print("500 组随机查询，内存版与 SQL 版不一致的次数:", bad)
```

200 个随机进出事件，500 组随机区间（含在事件之前、之后、其间无事件的情形），把内存版的区间最大值和内存 SQLite 逐个对拍：

```
500 组随机查询，内存版与 SQL 版不一致的次数: 0
```

**为什么。** 对拍测试（differential testing）的价值是：两个实现的错误不会一样。手写的二分版可能在边界上错；SQL 版是对定义的直译，不会错在那里。反过来，如果两者不一致，说明至少有一个理解错了，这是发现需求歧义的好办法（比如同一秒的事件顺序）。

**代价。** 需要为 SQL 版造数据加载代码；`COALESCE(..., 0)` 这类空值处理要想清楚（没有事件时 `SUM` 是 `NULL`）。

**信号。** 数据是追加的事件流、查询是"某时刻的值"或"某段时间的最大/最小"时，先想"这在 SQL 里是一个窗口函数"：如果是，SQL 版就是现成的测试标准。
