---
id: tlc-tt-login-count-per-user-per-day-0-whole
node: a.tt-login-count-per-user-per-day
type: qa
---
## Q
**日志流中统计每个用户每天登录次数**｜Easy · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-02-24（面试记录）

日志逐行到达，每行格式为 `"YYYY-MM-DD HH:MM:SS 用户名"`（用户名不含空白字符）。输出每个用户每天登录了多少次，结果是 `(用户名, 日期, 次数)` 的列表，按用户名排序，同一用户内按日期排序。同时要检查非法记录（格式不对、不存在的日期如 2 月 30 日、25 点这类时间），非法行不计入统计，单独返回。日志可以很长，不要求一次性装进内存。例：`["2026-10-24 09:00:01 bob", "2026-10-24 10:30:00 alice", "2026-10-23 23:59:59 alice", "2026-10-24 11:00:00 alice", "2026-02-30 08:00:00 bob", "2026-10-24 25:00:00 bob", "garbage", "2026-10-24 09:00:01", "2024-02-29 00:00:00 carol"]` → 统计 `[("alice","2026-10-23",1), ("alice","2026-10-24",2), ("bob","2026-10-24",1), ("carol","2024-02-29",1)]`，非法行是 `2026-02-30 ...`、`2026-10-24 25:00:00 ...`、`garbage`、`2026-10-24 09:00:01`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 `Counter` 以 `(用户, 日期)` 为键逐行累加；先用定宽正则确认格式，再用 `date()`、`time()` 构造器确认日期时间真实存在（不存在时它们抛 `ValueError`）；最后对 `counter.items()` 排序，键是元组，天然先按用户、再按日期排。

**识别。** 「按两个维度分组计数」是复合键的哈希计数；「日志流」意味着逐行消费，内存只能与不同的 `(用户, 日期)` 数成正比，而不是日志行数；「检查非法记录」是解析和校验的细节题，评分点在于是否严格；「按用户再按日期排序」交给元组的字典序。

**推导。** 暴力：读入全部日志，对每个用户的每一天再扫一遍计数，`O(n * m)`；或者先对全部记录排序再 `groupby`，需要装下整个日志 → 浪费：分组计数不需要排序，也不需要保存原始记录 → 洞察：一遍扫描，`Counter[(用户, 日期)] += 1`；ISO 格式的日期字符串字典序等于时间序，所以对最终的 `m` 个键排序即可，总成本 `O(n + m log m)`。

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

运行：上面的例子 → 统计 `[('alice', '2026-10-23', 1), ('alice', '2026-10-24', 2), ('bob', '2026-10-24', 1), ('carol', '2024-02-29', 1)]`，非法行 `['2026-02-30 08:00:00 bob', '2026-10-24 25:00:00 bob', 'garbage', '2026-10-24 09:00:01']`；空输入 → `([], [])`；`2024-02-29`（闰日）合法。

**复杂度。** 时间 `O(n + m log m)`，`m` 为不同的 `(用户, 日期)` 数；空间 `O(m)`，不保存原始日志行（非法行除外）。

**易错点。**
- 只用正则、不校验真实日期：`2026-02-30 08:00:00 bob` 能通过格式检查，被计成 `('bob', '2026-02-30', 1)`；`25:00:00` 同理。必须用 `date()`、`time()` 或 `strptime` 再验一次。
- 只用 `strptime` 而不检查定宽：`datetime.strptime("2026-1-5 1:2:3", "%Y-%m-%d %H:%M:%S")` 会成功，得到 `2026-01-05 01:02:03`，但这一行不符合 `YYYY-MM-DD HH:MM:SS` 格式；定宽正则把它挡掉。
- 日期字符串当排序键只在 ISO 格式下成立；换成 `MM/DD/YYYY` 就不再等于时间顺序，要解析成 `date` 再排。

**追问。**
- 日志按时间有序、流很长：当日期变化时就输出前一天的统计并清空 `Counter`，内存只与一天内的用户数有关。
- 登录时间带时区：先转换成统一时区（或用户所在时区）再取日期，否则同一次登录可能被算到不同的日子。
- 非法记录要报告行号：`for no, line in enumerate(lines, 1)`，把 `(no, line)` 收进 `invalid`。

**同模式。** LC 811 子域名访问计数、LC 1396 设计地铁系统、LC 359 日志速率限制器、LC 692 前 K 个高频单词。
