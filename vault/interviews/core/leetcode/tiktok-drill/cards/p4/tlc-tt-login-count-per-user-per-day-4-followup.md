---
id: tlc-tt-login-count-per-user-per-day-4-followup
node: p4.tt-login-count-per-user-per-day
type: qa
step: 4
---
## Q
**日志流中统计每个用户每天登录次数**｜追问

面试官接着问：（1）日志按时间有序且非常长，不同的 `(用户, 日期)` 也装不下，怎么办；（2）登录时间带时区；（3）非法记录要带行号报告。

## A
1. **按时间有序的长日志**：日期一变就输出前一天的统计并清空，内存只与「一天内出现的用户数」成正比。输出顺序变成「先日期、再用户」；如果仍要「先用户、再日期」，需要把每天的输出落盘后做外部归并排序。

```python
from collections import Counter
from collections.abc import Iterable, Iterator


def daily_counts_stream(lines: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    day = ""
    counts: Counter[str] = Counter()
    for line in lines:                                # 假设每行已经通过校验
        date_part, _, rest = line.partition(" ")
        user = rest.split()[-1]
        if date_part != day:                          # 日期变了：前一天结束，输出并清空
            for u in sorted(counts):
                yield u, day, counts[u]
            day, counts = date_part, Counter()
        counts[user] += 1
    for u in sorted(counts):
        yield u, day, counts[u]
```

`["2026-10-23 23:59:59 alice", "2026-10-24 09:00:01 bob", "2026-10-24 10:30:00 alice", "2026-10-24 11:00:00 alice"]` → `[('alice', '2026-10-23', 1), ('alice', '2026-10-24', 2), ('bob', '2026-10-24', 1)]`。
2. **时区**：先决定「一天」按谁的时区算（UTC 还是用户所在地），再用带时区的 `datetime.fromisoformat(...).astimezone(tz)` 转换后取 `.date()`，否则同一个登录在不同时区会被计到不同的日子。
3. **报告行号**：`for no, line in enumerate(lines, 1)`，非法时把 `(no, line)` 放进 `invalid`；行号从 `1` 开始，符合编辑器和日志工具的习惯。

**Python 提醒**：`str.partition(" ")` 只在第一个空格处切分，返回三元组 `(前, 分隔符, 后)`，找不到分隔符时后两项是空串，不会像 `split` 那样让解包失败；`Counter` 在迭代 `sorted(counts)` 时不能被修改，所以先输出再重新赋值一个新的 `Counter`。
