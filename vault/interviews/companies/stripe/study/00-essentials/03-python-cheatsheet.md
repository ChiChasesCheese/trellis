# 03 · Python 语法 · 标准库 · 惯用法速查

> 只收**在 60 分钟里真的会用到**的东西。每一条都要能不查文档写出来。
> 想在别的语言里做这类题，看最后一节的对照表。

---

## 1. 读入与输出

```python
import sys

def main(stdin=sys.stdin, stdout=sys.stdout):
    lines = stdin.read().splitlines()          # 一次读完，最快；已去掉换行符
    if lines and lines[0].startswith("PART"):  # 多 part 题的 dispatch
        part, lines = int(lines[0].split()[1]), lines[1:]
    else:
        part = 0
    out = {1: part1, 2: part2}.get(part, part_default)(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))

if __name__ == "__main__":
    main()
```

要点：
- `stdin.read().splitlines()` 一次读完，比逐行 `input()` 快一个数量级，且自动处理 `\r\n`。
- 输出用 `"\n".join(...)` 一次写出，比循环 `print` 快得多（10^5 行时差别明显）。
- **调试只往 stderr**：`print(f"{x=}", file=sys.stderr)`。
- 把 `main()` 写成接受 `stdin`/`stdout` 参数的形式，测试时可以传 `io.StringIO`。

---

## 2. collections

```python
from collections import defaultdict, Counter, deque, OrderedDict

d = defaultdict(int)          # d[k] += 1 不用先判断
g = defaultdict(list)         # g[k].append(v)
r = defaultdict(dict)         # 邻接表 r[u][v] = w

c = Counter(words)            # {word: count}
c.most_common(3)              # [(w, n), ...]，按计数降序；**平手时按插入序**，不确定 → 自己再排
c1 + c2, c1 - c2              # 计数加减（减法会丢掉 <=0 的项）

dq = deque()
dq.append(x); dq.appendleft(x); dq.pop(); dq.popleft()   # 两端 O(1)
dq = deque(maxlen=5)          # 满了自动挤掉另一端

od = OrderedDict()
od.move_to_end(k)             # LRU 的核心操作
od.popitem(last=False)        # 弹出最久未用的
```

**`defaultdict` 的陷阱**：任何 `d[k]` 的**读取**都会建键。
查询一律用 `d.get(k)` 或 `if k in d`，只有确实要写入时才用 `d[k]`。

---

## 3. heapq（最小堆）

```python
import heapq

h = []
heapq.heappush(h, (load, server_id))     # 元组比较 = 先比 load，平手比 id
load, sid = heapq.heappop(h)             # 最小的
heapq.heapify(lst)                       # 原地 O(n)
heapq.nsmallest(3, items, key=...)       # 小规模 top-k，不用手写堆
```

**最大堆**：把键取负 `heapq.heappush(h, (-score, id))`。
字符串不能取负 → 用 `cmp_to_key` 或反转排序。

**惰性删除（重要）**：堆里的条目在负载变化后会过期。不要试图从堆中间删，改成：

```python
while h:
    load, sid = heapq.heappop(h)
    if load == current_load[sid]:        # 是最新的才用
        break
    # 否则丢弃，继续弹
```

---

## 4. bisect

```python
from bisect import bisect_left, bisect_right, insort

i = bisect_left(a, x)    # 第一个 >= x 的位置（x 存在时指向最左的 x）
j = bisect_right(a, x)   # 第一个 >  x 的位置
count_of_x       = j - i
count_in_[lo,hi] = bisect_right(a, hi) - bisect_left(a, lo)
insort(a, x)             # 插入并保持有序，O(n) 搬移但常数极小
a[bisect_right(a, t) - 1]   # <= t 的最大元素（"某时刻的最新版本"）
```

Python 3.10+ 支持 `bisect_left(a, x, key=lambda r: r.ts)`，低版本要么存平行的键列表，
要么存元组让第一个字段就是键。

---

## 5. 排序

```python
rows.sort(key=lambda r: (-r.score, r.name))     # 数值降序 + 字符串升序
rows.sort(key=lambda r: r.name)                 # 稳定排序：从次要键开始
rows.sort(key=lambda r: r.score, reverse=True)  # 再排主要键

from functools import cmp_to_key
rows.sort(key=cmp_to_key(lambda a, b: -1 if ... else 1 if ... else 0))
```

- `sorted()` / `list.sort()` **保证稳定**，可以放心用"从次要到主要"多趟排。
- `sorted(d.items())` 按 key 排；`sorted(d)` 只得到 key。
- 混合类型不能比较（`int` vs `str` → `TypeError`），元组键里各列类型要一致。

---

## 6. Decimal（钱）

```python
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN, getcontext

getcontext().prec = 28                       # 默认够用
d = Decimal("10.99")                         # **一定从字符串构造**，不要 Decimal(10.99)
cents = int(d.scaleb(2))                     # 10.99 → 1099（输入保证两位时）
d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

- `round()` 是 banker's rounding：`round(2.5) == 2`、`round(0.5) == 0`。
  题面说 "round half up" 时**不能**用它。
- 整数版 half-up：`(a * 2 + b) // (2 * b)` 对正数成立（`a/b` 四舍五入）。
- 整数版向下取整：`a // b`（注意负数 `-7 // 2 == -4`，是向下不是向零）。
- 向零截断：`int(a / b)` 有浮点风险，用 `-((-a) // b) if a < 0 else a // b`。

---

## 7. datetime

```python
from datetime import datetime, timedelta, timezone, date

dt = datetime.strptime("2026-08-27 13:45", "%Y-%m-%d %H:%M")
dt = datetime.fromisoformat("2026-08-27T13:45:00+00:00")   # 3.11+ 支持 Z
ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
dt.strftime("%Y-%m-%d")
dt + timedelta(days=30, hours=2, minutes=15)               # 没有 months=！
(d2 - d1).days                                             # 天数差
dt.weekday()        # 周一=0 … 周日=6
dt.isoweekday()     # 周一=1 … 周日=7
```

**加月要手写**（`timedelta` 没有月）：

```python
import calendar
def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))   # 月末夹取
```

`HH:MM` 直接转分钟往往比 `datetime` 更省事：

```python
h, m = map(int, s.split(":")); minutes = h * 60 + m
```

---

## 8. csv / json

```python
import csv, io, json

for row in csv.DictReader(io.StringIO(text)):     # 按表头取字段，含引号内逗号
    row["amount"]
for fields in csv.reader(io.StringIO(text)):      # 无表头
    ...
obj = json.loads(line)                            # JSON lines
json.dumps(obj, sort_keys=True, separators=(",", ":"))   # 确定性输出
```

`csv` 的价值就一条：**正确处理带引号的字段里的逗号**。手写 `split(",")` 处理不了。

---

## 9. itertools / functools

```python
from itertools import groupby, accumulate, product, combinations, permutations, chain, pairwise
from functools import lru_cache, cmp_to_key, reduce

# groupby 只对**已排序**的数据有效
data.sort(key=keyf)
for k, grp in groupby(data, key=keyf):
    items = list(grp)                # grp 是一次性迭代器！

accumulate([1,2,3])                  # 1, 3, 6  前缀和
accumulate(a, max)                   # 前缀最大值
product("0123456789", repeat=k)      # 掩码补全：10^k 种
pairwise([1,2,3])                    # (1,2), (2,3)   3.10+

@lru_cache(maxsize=None)             # 记忆化 DP，参数必须可哈希
def f(i, mask): ...
```

---

## 10. dataclass

```python
from dataclasses import dataclass, field

@dataclass
class Account:
    id: str
    total: int = 0
    fraud: int = 0
    charges: dict = field(default_factory=dict)   # 可变默认值必须用 field！

@dataclass(frozen=True)     # 不可变 → 可哈希，可以当 dict 的 key
class Point:
    x: int
    y: int

@dataclass(order=True)      # 自动生成 <, > （按字段顺序比较）
class Task:
    priority: int
    name: str
```

`@dataclass` 免费送 `__repr__`，调试时 `print(acct, file=sys.stderr)` 就能看到全部字段 ——
这在没有断点的浏览器 IDE 里是实打实的时间。

---

## 11. 字符串

```python
s.strip() / .lstrip() / .rstrip()
s.casefold()                 # 比 lower() 更彻底的大小写折叠
s.split(",", 2)              # maxsplit：保护含逗号的尾字段
s.partition(":")             # → (before, sep, after)，只切第一个
s.removeprefix("a") / .removesuffix("b")    # 3.9+
s.isdigit() / .isalnum() / .isascii()
f"{n:016d}"  f"{x:.2f}"  f"{n:,}"  f"{s:<10}"  f"{s:>10}"
f"{x=}"                      # 输出 "x=3"，调试神器
"".join(parts)               # 永远比 += 快
```

正则：

```python
import re
re.fullmatch(r"[A-Z]{2}\d{4}", s)      # 整串匹配，比 match 安全
re.sub(r"\s+", " ", s)
m = re.match(r"(\w+)=(\d+)", s);  m.group(1), m.group(2)
```

---

## 12. 十个会丢分的坑

1. **可变默认参数**：`def f(x, acc=[])` —— `acc` 在所有调用间共享。用 `None` 哨兵。
2. **负数整除**：`-7 // 2 == -4`（向下取整），`-7 % 2 == 1`（结果非负）。
   要"向零截断"必须自己写。
3. **浮点相等**：`0.1 + 0.2 != 0.3`。钱和比例都不要碰浮点。
4. **浅拷贝**：`b = a[:]` 只复制一层；嵌套结构要 `copy.deepcopy`。
5. **闭包晚绑定**：`[lambda: i for i in range(3)]` 三个都返回 2。用 `lambda i=i: i`。
6. **迭代中修改**：`for k in d: del d[k]` → `RuntimeError`。用 `for k in list(d)`。
7. **`defaultdict` 读取建键**：见 §2。
8. **`sort` 的稳定性**：可以依赖（文档保证），但只在"多趟排序"里用，单趟还是写全元组更清楚。
9. **`is` vs `==`**：只有 `None` / `True` / `False` 用 `is`。小整数缓存是实现细节，别依赖。
10. **递归深度**：默认 1000 层。10^5 个节点的 DFS 一定要写成迭代或
    `sys.setrecursionlimit(300000)` + 加大栈（后者在 HackerRank 上未必生效，**优先写迭代**）。

---

## 13. 换语言的对照表

| Python | Java | Go | TypeScript |
|---|---|---|---|
| `dict` | `HashMap` | `map[K]V` | `Map` / 对象 |
| `defaultdict(int)` | `map.merge(k,1,Integer::sum)` | `m[k]++`（零值即 0） | `m.set(k,(m.get(k)??0)+1)` |
| `Counter` | `Map<T,Integer>` 手写 | 手写 | 手写 |
| `deque` | `ArrayDeque` | `container/list` 或切片 | 数组（`shift` 是 O(n)！） |
| `heapq`（最小堆） | `PriorityQueue` | `container/heap`（要实现接口） | 无内置，手写 |
| `bisect` | `Collections.binarySearch` | `sort.SearchInts` | 手写 |
| `sorted(key=)` | `list.sort(Comparator)` | `sort.Slice` | `arr.sort(cmp)` |
| `Decimal` | `BigDecimal` | `math/big.Rat` 或整数分 | 无，只能用整数分 |
| `@dataclass` | `record` | `struct` | `interface` + 字面量 |

**60 分钟的现实**：Python 打字量最小、标准库最全，Stripe 的工程师公开建议不要用 Java。
Go 没有内置堆和二分，写这类题会慢。TypeScript 缺 `Decimal`，金额必须自己用整数分。
除非你对某语言的熟练度**明显**更高，否则 Python 是这类 OA 的默认选择。
