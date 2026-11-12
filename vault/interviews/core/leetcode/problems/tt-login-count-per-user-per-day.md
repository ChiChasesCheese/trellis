---
slug: tt-login-count-per-user-per-day
---
## Q
**日志流中统计每个用户每天登录次数**｜Easy

日志逐行到达，格式 `"YYYY-MM-DD HH:MM:SS 用户名"`。输出每个用户每天的登录次数 `(用户名, 日期, 次数)`，按用户、日期排序；格式错误或日期时间不存在（2 月 30 日、25 点）的行不计入，单独返回。日志很长，不要一次装进内存。

## A
**一句话。** 用 `Counter` 以 `(用户, 日期)` 为键逐行累加，定宽正则查格式，`date()`、`time()` 构造器查真实存在，最后对元组键排序。

```python
LINE = re.compile(
    r"(\d{4})-(\d{2})-(\d{2}) "
    r"(\d{2}):(\d{2}):(\d{2}) (\S+)", re.ASCII)

def login_counts(lines):
    cnt, bad = Counter(), []
    for line in lines:          # 逐行消费
        m = LINE.fullmatch(line.strip())
        if m is None:
            bad.append(line)
            continue
        y, mo, d, h, mi, s = map(int, m.groups()[:6])
        try:
            day = date(y, mo, d)    # 2 月 30 日在这里抛错
            time(h, mi, s)          # 25 点在这里抛错
        except ValueError:
            bad.append(line)
            continue
        cnt[m.group(7), day.isoformat()] += 1
    res = [(u, d, n) for (u, d), n in sorted(cnt.items())]
    return res, bad
```

**复杂度。** 时间 `O(n + m log m)`，空间 `O(m)`（`m` 为不同的 `(用户, 日期)` 数）。

**易错点。**
- 只用正则、不验真实日期：`2026-02-30 08:00:00 bob` 通过格式检查，被误计。
- 只用 `strptime` 不管定宽：`2026-1-5 1:2:3` 也能解析成功，但不符合格式。

**追问。**
- 日志按时间有序、流很长？：日期一变就输出前一天并清空 `Counter`，内存只与一天内的用户数有关。
- 登录时间带时区？：先转成统一时区再取日期，否则同一次登录会落到不同的日子。

**同模式。** LC 811 子域名访问计数、LC 359 日志速率限制器、LC 692 前 K 个高频单词
