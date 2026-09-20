---
id: problems-meeting-scheduler-local-time-plus-zone
node: problems.booking.meeting-scheduler
type: qa
step: 7
tags: [grown]
---
## Q
会议室预订设计里，周期会议为什么要存“本地时间 + 时区”，而不是把第一次的具体时刻换算成一个固定的 UTC 瞬间、之后每周原样加 7 天？

## A
如果先把第一次场次冻结成固定的 UTC 瞬间、再靠加整数天数往后推，跨过一次夏令时（DST）切换后，换回本地时间会整体漂移一个小时——比如美国东部时间某周一 9 点（标准时间，UTC−5）换算成 UTC 是 14:00，切换到夏令时（UTC−4）之后同一个 14:00 UTC 换回本地时间就变成了 10 点。存“本地时间 + 时区”、每次查询时用当天的规则重新换算 UTC 偏移，才能让约定的“9 点”在夏令时切换前后都还是 9 点——这正是 `zoneinfo` 这类时区库存在的意义。
