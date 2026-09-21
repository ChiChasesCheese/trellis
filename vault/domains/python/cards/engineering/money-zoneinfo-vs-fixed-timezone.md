---
id: money-zoneinfo-vs-fixed-timezone
node: engineering.money-time
type: qa
source: python-docs
---
## Q
`datetime.timezone` 固定偏移量和 `zoneinfo.ZoneInfo` 有什么区别？处理「纽约时间」这种地区时区该用哪个？

## A
`datetime.timezone` 只能表示一个相对 UTC 的固定偏移（如 UTC+8），无法表示同一地区在一年中因夏令时（DST）切换偏移量的情况，也不知道历史上偏移规则的变更。`zoneinfo` 模块引入 IANA 时区数据库（IANA time zone database，即 tz/Olson 数据库），记录各地区历史与现行的夏令时与偏移规则并定期更新，能正确处理如「America/New_York」这样会变化偏移的地区时区，是官方推荐的做法。
