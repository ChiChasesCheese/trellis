---
id: cc-python-stdlib-collections-calls
node: python.stdlib
type: qa
---
## Q
Group rows by key, count occurrences with a ranking, and keep a bounded FIFO of recent events. Name the three `collections` types, the one call each that saves a line, and the trap in the first.

## A
```python
from collections import defaultdict, Counter, deque
by_key = defaultdict(list); by_key[k].append(row)   # no membership test needed
c = Counter(codes); c.most_common(3)                # [(value, count), ...] descending
c2 = Counter(a) - Counter(b)                        # multiset difference, drops <= 0
q = deque(maxlen=5); q.append(x); q.popleft()       # O(1) at both ends
```

- **`defaultdict` creates the entry on read**, so `if d[k]:` inserts an empty list and changes what you later iterate. Use `d.get(k)` to inspect ([[cc-python-idioms-setdefault-vs-defaultdict]]).
- `Counter[missing]` returns `0` without inserting — the safe read.
- `deque(maxlen=n)` silently discards from the far end: a free fixed-size window.

## Q zh
按 key 分组、带排名地计数、以及维护一个定长的近期事件 FIFO。说出这三个 `collections` 类型、各自那个省一行的调用，以及第一个的陷阱。

## A zh
```python
from collections import defaultdict, Counter, deque
by_key = defaultdict(list); by_key[k].append(row)   # 不需要先判断是否存在
c = Counter(codes); c.most_common(3)                # [(值, 计数), ...] 降序
c2 = Counter(a) - Counter(b)                        # 多重集差，丢弃 <= 0 的项
q = deque(maxlen=5); q.append(x); q.popleft()       # 两端都是 O(1)
```

- **`defaultdict` 在读取时就会建条目**，所以 `if d[k]:` 会插入一个空 list，改变你之后遍历到的内容。查看用 `d.get(k)`（[[cc-python-idioms-setdefault-vs-defaultdict]]）。
- `Counter[missing]` 返回 `0` 而不插入 —— 这才是安全的读。
- `deque(maxlen=n)` 会从远端静默丢弃：白送的定长窗口。
