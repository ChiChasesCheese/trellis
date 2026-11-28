---
id: hi-c-sd-job-scheduler-x07-dst
node: sd.problem-breakdowns.job-scheduler.exam
type: qa
step: 7
---
## Q
**分布式任务调度器 · 找错：cron 遇到夏令时**｜考点 · 必会

用户在纽约时区创建了每天 02:30 执行的作业。2026 年 3 月 8 日（春季调时）和 11 月 1 日（秋季调时）当天会发生什么？如果用户设的是 01:30 呢？调度器应该怎么存？

## A
- **春季（3 月 8 日）：** 02:00 直接跳到 03:00，02:30 这个本地时间当天不存在。实现不同，行为不同：跳过、或推迟到 03:00 之后执行。必须事先定好规则，并对用户可见。
- **秋季（11 月 1 日）：** 01:00–02:00 这一小时出现两次。01:30 会出现两次（UTC 05:30 和 06:30），要决定执行一次还是两次；02:30 只出现一次。
- **实测（Python zoneinfo）：** 春季 02:30 返回空；春季 03:30 对应 UTC 07:30；秋季 01:30 返回 UTC 05:30 和 06:30 两个时刻；秋季 02:30 对应 UTC 07:30。
- **存储做法：** 作业定义里存 cron 表达式加 IANA 时区名（不是固定偏移 -05:00），每次生成下一次执行时，用带时区的库计算出该次的 UTC 时间戳，Executions 里只存 UTC。
- **规则：** 缺失的时间在间隙后第一刻执行（或跳过），重复的时间只执行第一次；写进文档并测试。
- **要点：** 用偏移量存时间会在调时当天错一小时；调度器的所有内部时间用 UTC，转换只在计算下一次触发时发生。

```python
def fire_times(day, hour, minute):   # NY 时区下，本地时间对应的 UTC 触发时刻
    out = []
    for fold in (0, 1):              # fold=0 首次出现，fold=1 第二次出现
        local = datetime(day.year, day.month, day.day, hour, minute, tzinfo=NY, fold=fold)
        utc = local.astimezone(timezone.utc)
        if utc.astimezone(NY).replace(tzinfo=None) == local.replace(tzinfo=None) and utc not in out:
            out.append(utc)          # 往返一致才说明这个本地时间真实存在
    return out
```
