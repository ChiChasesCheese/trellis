---
id: cc-chrono-parsing-weekday-tokens
node: chrono.parsing
type: qa
---
## Q
A rule's applicable days arrive as `Mon-Wed/Fri`. Expand it, and say which date's weekday decides whether the rule fires.

## A
**Expand to a set of weekday indices once, at parse time** — never re-parse the token inside the per-day loop.

```python
DAYS = "Mon Tue Wed Thu Fri Sat Sun".split()
def weekdays(spec):
    out = set()
    for chunk in spec.split("/"):
        a, _, b = chunk.partition("-")
        i, j = DAYS.index(a), DAYS.index(b or a)
        out |= {k % 7 for k in range(i, j + 7 * (j < i) + 1)}   # Fri-Mon wraps
    return out
```

- The weekday is that of the **local** date, not the UTC date: a `-8` region's Friday shift lands on UTC Saturday ([[cc-chrono-arithmetic-offset-day-wrap]]).
- A missing `days` field means *every* day — make that default explicit rather than letting it fall through as an empty set.
- Duplicate or overlapping rules are harmless if you union the sets; they are not if you sum anything.

## Q zh
一条规则的适用日以 `Mon-Wed/Fri` 的形式给出。把它展开，并说明是哪个日期的星期几决定规则是否触发。

## A zh
**在解析时一次性展开成星期序号的集合** —— 绝不要在按天循环里反复解析这个 token。

```python
DAYS = "Mon Tue Wed Thu Fri Sat Sun".split()
def weekdays(spec):
    out = set()
    for chunk in spec.split("/"):
        a, _, b = chunk.partition("-")
        i, j = DAYS.index(a), DAYS.index(b or a)
        out |= {k % 7 for k in range(i, j + 7 * (j < i) + 1)}   # Fri-Mon 会跨周
    return out
```

- 星期几取的是**本地**日期而不是 UTC 日期：`-8` 区域的周五班次落在 UTC 的周六（[[cc-chrono-arithmetic-offset-day-wrap]]）。
- 缺少 `days` 字段意味着*每一天* —— 把这个默认值写明，而不是让它变成空集合悄悄漏过去。
- 重复或重叠的规则在做集合并集时无害；如果你对什么做了求和，那就有害了。
