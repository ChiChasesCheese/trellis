# 05 · 时间、日期、窗口、区间

---

## 1. 先统一表示

进程序的第一件事：把所有时间戳变成**一种**表示，之后不再转换。

| 场景 | 用什么 | 理由 |
|---|---|---|
| 只比较先后、算差值 | **epoch 秒（int）** | 加减就是加减，排序就是排序 |
| 只有 `HH:MM`，同一天内 | **分钟数 int**：`h*60+m` | 24:00 = 1440，天然可比 |
| 要跨月、要月末、要星期 | `datetime` / `date` | 日历规则太多，别手写 |
| 有时区偏移 | epoch 秒 + 单独存偏移**分钟数** | 偏移可能是 +5:30，不是整小时 |

**永远不要用浮点秒。** 也不要在两种表示之间来回转。

---

## 2. 解析

```python
from datetime import datetime, timezone

datetime.strptime("2026-08-27 13:45:00", "%Y-%m-%d %H:%M:%S")
datetime.fromisoformat("2026-08-27T13:45:00+00:00")     # 3.11+ 也吃 'Z'
int(dt.replace(tzinfo=timezone.utc).timestamp())        # → epoch 秒

h, m = map(int, "13:45".split(":"));  minutes = h * 60 + m
```

**naive vs aware**：`datetime` 没有 tzinfo 就是 naive，`.timestamp()` 会按**本地时区**解释 ——
在评测机上就是 UTC，在你机器上可能不是，于是"本地跑对了，提交挂了"。
**要么全程 naive 且约定为 UTC，要么全程 aware。**

**日期合法性**：`strptime` 会拒绝 `2026-02-30`，这正是你想要的校验。
题面要求"丢弃非法日期的行"时，直接：

```python
try:
    dt = datetime.strptime(s, "%Y-%m-%d")
except ValueError:
    return None            # 这一行是坏行
```

---

## 3. 时长 vs 日历

**时长算术**（`timedelta`）：秒、分、时、天、周。**没有月，没有年。**

```python
dt + timedelta(days=30)         # 精确 30×86400 秒
```

**日历算术**要手写。加月 + 月末夹取：

```python
import calendar
from datetime import date

def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))

add_months(date(2026, 1, 31), 1)   # → 2026-02-28   ← 夹取
add_months(date(2026, 3, 31), 1)   # → 2026-04-30
```

**订阅锚点**：1 月 31 日订阅，2 月扣 28 日，3 月要回到 31 日还是留在 28 日？
Stripe 的真实行为是**回到 31 日**（锚点是原始日期，每次从锚点重算，不是从上次扣款日递推）。
题面没说时，从锚点重算是更常见的答案，写注释声明。

---

## 4. 时区偏移与跨日

偏移以**分钟**为单位（India +330、Nepal +345、Newfoundland -210）。

```python
utc_minutes = local_minutes - offset_minutes
day_shift, utc_minutes = divmod(utc_minutes, 1440)   # divmod 自动处理跨日
```

`divmod` 对负数也正确：`divmod(-30, 1440) == (-1, 1410)`，即前一天 23:30。
**这就是为什么用 `divmod` 而不是 `//` 和 `%` 分开写。**

星期也要跟着 `day_shift` 转：`weekday = (weekday + day_shift) % 7`。

---

## 5. 桶 vs 窗口

**这是两个不同的东西，题面里经常混着说。**

| | 固定桶（bucket） | 滚动窗口（rolling window） |
|---|---|---|
| 定义 | `ts // 3600` 相同的算一组 | `now - ts < 3600` 的算一组 |
| 边界 | 13:59 和 14:01 **不同组** | 13:59 和 14:01 **同组** |
| 状态 | `Counter[bucket_id]` | 每 key 一个 `deque` |
| 题面用语 | "per hour"、"hourly" | "within the last hour"、"in any 60-minute period" |

**"within one hour" 到底是 `<=` 还是 `<`**：LC 1604 的官方定义是
"in a one-hour period" = `t3 - t1 <= 60`（分钟，非严格）。
题面没说时，非严格（`<=`）更常见，但一定要写注释，并把另一种留成一个常量。

**滚动窗口模板**：

```python
from collections import defaultdict, deque
win = defaultdict(deque)

def hit(key, ts, window, limit) -> bool:
    dq = win[key]
    while dq and ts - dq[0] > window:      # 严格大于 = 窗口闭区间
        dq.popleft()
    if len(dq) >= limit:                   # 已满 → 拒绝
        return False
    dq.append(ts)
    return True
```

**空闲清理**：10^6 个 key 各留一个 deque 会撑爆 256 MB。定期或按需删掉空的：

```python
if not dq:
    del win[key]
```

---

## 6. 令牌桶

不要用定时器，**用时再补**：

```python
class Bucket:
    __slots__ = ("tokens", "last")
    def __init__(self, cap): self.tokens, self.last = cap, 0

def allow(b, now, cap, rate) -> bool:      # rate = 每秒补多少
    b.tokens = min(cap, b.tokens + (now - b.last) * rate)
    b.last = now
    if b.tokens >= 1:
        b.tokens -= 1
        return True
    return False
```

`rate` 是小数时，把 tokens 也乘上一个比例因子留在整数里（例如 tokens 以"千分之一个"计）。

---

## 7. 区间

**第一件事：在文件顶部声明惯例，然后全程只用它。**

```python
# 全文件惯例：闭区间 [lo, hi]，整数域
```

**闭区间（整数）**：

```python
overlap  = a_lo <= b_hi and b_lo <= a_hi
adjacent = a_hi + 1 == b_lo               # 整数域独有
gap      = (a_hi + 1, b_lo - 1)           # 仅当 a_hi + 1 <= b_lo - 1
length   = hi - lo + 1
```

**半开区间 `[lo, hi)`**（时间区间通常用这个）：

```python
overlap  = a_lo < b_hi and b_lo < a_hi
adjacent = a_hi == b_lo
length   = hi - lo
```

**合并**（闭区间、整数域，相邻也要合）：

```python
def merge(ivs):
    ivs = sorted(ivs)
    out = []
    for lo, hi in ivs:
        if out and lo <= out[-1][1] + 1:          # +1 处理相邻
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out
```

半开区间版本去掉 `+ 1`。

**补集（找空隙）**，在全域 `[LO, HI]` 内：

```python
def gaps(merged, LO, HI):
    out, cur = [], LO
    for lo, hi in merged:
        if lo > cur:
            out.append((cur, lo - 1))
        cur = max(cur, hi + 1)
    if cur <= HI:
        out.append((cur, HI))
    return out
```

**被完全覆盖的区间**（LC 1288）：按 `(lo 升序, hi 降序)` 排序，然后：

```python
best = -inf
for lo, hi in sorted(ivs, key=lambda t: (t[0], -t[1])):
    if hi <= best:  covered += 1
    else:           best = hi
```

`hi` 降序是关键 —— 否则 `[1,10]` 和 `[1,4]` 的顺序会让 `[1,10]` 被判为被覆盖。

---

## 8. 自检清单

- [ ] 所有时间戳统一成一种表示了吗？
- [ ] naive/aware 混用了吗？`.timestamp()` 会按本地时区解释 naive datetime
- [ ] 加"月"用了 `timedelta` 吗？（它没有月）
- [ ] 月末夹取处理了吗？（Jan 31 + 1 month）
- [ ] 时区偏移当成整小时了吗？（+5:30 会挂）
- [ ] 跨日用了 `divmod` 吗？星期跟着转了吗？
- [ ] 桶还是窗口，分清了吗？
- [ ] 窗口边界是 `<` 还是 `<=`，写注释了吗？
- [ ] 区间惯例（闭 / 半开）在文件顶部声明了吗？
- [ ] 整数域的相邻区间合并了吗？
- [ ] 空闲 key 清理了吗？（内存预算）
