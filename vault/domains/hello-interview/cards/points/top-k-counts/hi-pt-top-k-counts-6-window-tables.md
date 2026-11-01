---
id: hi-pt-top-k-counts-6-window-tables
node: qb.sd.top-k-counts.points
type: qa
step: 6
---
## Q
**Top-K 热门榜 · 窗口怎么算才快**｜出自：Top-K 热门榜 › 深入 3

查最近 1 小时/1 天/1 个月前 K，朴素 `GROUP BY` 为什么慢？怎么改？

## A
**朴素。** 对最近 N 小时的行求和再排序，扫上百 GB，几分钟起步。
**层级汇总。** 维护小时、天、月三个粒度，月窗口只加 30 个日桶，但有跨粒度同步延迟。
**选用。** 每个窗口一张当前值表（如 `views_last_hour`）并在计数列建索引，`ORDER BY count DESC LIMIT k`，读 O(k)；代价是每次写更新 4 张表。
