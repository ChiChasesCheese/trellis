---
id: tlc-tt-login-count-per-user-per-day-2-code
node: a.tt-login-count-per-user-per-day
type: qa
step: 2
---
## Q
**日志流中统计每个用户每天登录次数**｜写出 Python 实现

输入是逐行到达的日志（`Iterable[str]`），每行 `"YYYY-MM-DD HH:MM:SS 用户名"`，用户名不含空白。返回两个值：`(用户名, 日期, 次数)` 的列表（按用户名、再按日期排序），以及非法行的列表（格式不对，或日期、时间不存在）。非法行不计入统计。

## A
**思路。** 逐行用定宽正则匹配；匹配成功后用 `date()` 和 `time()` 构造器校验日期时间；通过的行把 `(用户, 日期)` 计入 `Counter`。最后对 `counter.items()` 排序，输出展平的元组。

```python
import re
from collections import Counter
from collections.abc import Iterable
from datetime import date, time

LINE = re.compile(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) (\S+)", re.ASCII)


def login_counts(lines: Iterable[str]) -> tuple[list[tuple[str, str, int]], list[str]]:
    counts: Counter[tuple[str, str]] = Counter()    # (用户, 日期) -> 登录次数
    invalid: list[str] = []
    for line in lines:                              # 逐行消费，不要求一次装进内存
        m = LINE.fullmatch(line.strip())
        if m is None:
            invalid.append(line)
            continue
        y, mo, d, h, mi, s = map(int, m.group(1, 2, 3, 4, 5, 6))
        try:
            day = date(y, mo, d)                    # 2月30日、13月会在这里抛 ValueError
            time(h, mi, s)                          # 25:00:00 会在这里抛 ValueError
        except ValueError:
            invalid.append(line)
            continue
        counts[m.group(7), day.isoformat()] += 1
    result = [(user, day, n) for (user, day), n in sorted(counts.items())]   # 元组天然先按用户、再按日期排序
    return result, invalid
```

运行：`["2026-10-24 09:00:01 bob", "2026-10-24 10:30:00 alice", "2026-10-23 23:59:59 alice", "2026-10-24 11:00:00 alice", "2026-02-30 08:00:00 bob", "2026-10-24 25:00:00 bob", "garbage", "2026-10-24 09:00:01", "2024-02-29 00:00:00 carol"]` → 统计 `[('alice', '2026-10-23', 1), ('alice', '2026-10-24', 2), ('bob', '2026-10-24', 1), ('carol', '2024-02-29', 1)]`，非法行 `['2026-02-30 08:00:00 bob', '2026-10-24 25:00:00 bob', 'garbage', '2026-10-24 09:00:01']`；空输入 → `([], [])`；传入生成器也可以。

**复杂度。** 时间 `O(n + m log m)`；空间 `O(m)`。

**写法要点。** `re.fullmatch` 要求整行都匹配，不会被尾部多余内容骗过；`re.ASCII` 让 `\d` 只匹配 `0-9`，不接受其他文字系统的数字；`m.group(1, 2, 3, 4, 5, 6)` 一次取出多个分组，配 `map(int, ...)` 解包；`date()` / `time()` 的构造器自带闰年和范围检查，不需要手写；`counts[a, b] += 1` 的键是元组 `(a, b)`；`sorted(counts.items())` 比较 `((用户, 日期), 次数)`，先比键，所以顺序是用户再日期。
