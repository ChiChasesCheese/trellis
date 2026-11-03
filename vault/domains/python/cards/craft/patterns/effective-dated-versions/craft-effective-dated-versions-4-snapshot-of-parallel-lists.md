---
id: craft-effective-dated-versions-4-snapshot-of-parallel-lists
node: craft.patterns.effective-dated-versions
type: qa
step: 4
---
## Q
**生效时间版本 · 为什么版本表是一个不可变的 Schedule，而不是两个并行列表**｜写法

`starts` 和 `versions` 两个等长、同下标的容器。写成实例上的两个可变列表，读的人先对 `starts` 二分、再用得到的下标去取 `versions`。多线程下，写者发布新版本时，读者可能看到什么？

## A
**要点。** 并行容器（parallel containers）的不变量是「两个容器的长度和下标对应」，任何一次不原子的修改都会让读者看到半成品。做法：把两者放进一个 frozen 的 `_Schedule`（元组），发布时造一个新的 `_Schedule` 整体替换；读者开头读一次引用，之后全程使用这一份快照，不需要锁。

```python
@dataclass(frozen=True, slots=True)
class _Schedule:
    starts: tuple[int, ...] = ()
    versions: tuple[tuple[Rule, ...], ...] = ()

# 发布：校验在锁外，整体替换在锁内
ordered = _in_dependency_order(rules)
with self._publish_lock:
    self._schedules[merchant] = _Schedule(old.starts + (effective_from,), old.versions + (ordered,))

# 读取：一次读取，之后用的是同一份快照
sched = self._schedules.get(txn.merchant, _Schedule())
```

```python
from bisect import bisect_right

# 反例：两个并行列表，写者在读者的两次读取之间改动了它们（这里以在最前面插入一个版本为例）
starts, rates = [100, 200], [290, 250]

def reader_bad(ts):
    i = bisect_right(starts, ts)                 # 第一次读：查版本号
    # ---- 此刻写者发布了一个更早生效的版本，两个列表依次被改 ----
    starts.insert(0, 50); rates.insert(0, 300)
    return rates[i - 1]                          # 第二次读：下标已经错位

print("ts=150 本应是 290，并行列表读到:", reader_bad(150))
```

反例：读者在第一次读（二分）和第二次读（取值）之间，写者改动了两个列表：

```
ts=150 本应是 290，并行列表读到: 300
```

**为什么。** 示例里为了好演示用了在前面插入；只追加的列表也不安全：读者可能看到 `starts` 已追加而 `versions` 还没追加，用新长度算出的下标 `v - 1` 越界。快照把「查与取」变成对同一份不可变数据的两次读，天然一致，而且读路径无锁：只有发布者之间需要互斥。

**代价。** 每次发布复制两个元组，O(版本数)；发布频率远低于查询时是好交易。发布得极频繁时，换成持久化数据结构，或者引入读写锁。

**易错。** 必须只读一次引用：`self._schedules[m].starts` 和 `self._schedules[m].versions` 分开写，两次取到的可能是不同的快照。
