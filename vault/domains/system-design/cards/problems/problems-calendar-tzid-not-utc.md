---
id: problems-calendar-tzid-not-utc
node: problems.realtime.calendar
type: qa
step: 4
tags: [grown]
---
## Q
Why should a recurring calendar event store its start time as local time plus an IANA time zone identifier (e.g. `DTSTART;TZID=America/New_York:...`) rather than a precomputed UTC instant, and what real, dated example shows time zone rules actually changing?

## A
Daylight-saving and UTC-offset rules for a time zone can change over time — the IANA Time Zone Database's 2026d release (published September 11, 2026) included a region in Canada's Northwest Territories permanently switching to UTC-06 and no longer observing DST. If a recurring 'every Monday 9am' event had its UTC instant baked in at creation time, every future occurrence would silently fire at the wrong UTC moment once such a rule changes. Storing local time plus a zone identifier means the correct UTC instant is recomputed at read/use time against whatever the current time zone rules say, so a rule change doesn't require touching any stored event data.

## Q zh
为什么一个循环日历事件应该把开始时间存成本地时间加 IANA 时区标识符（例如 `DTSTART;TZID=America/New_York:...`），而不是预先算好的 UTC 时刻？有什么真实的、带日期的例子能说明时区规则确实会变化？

## A zh
一个时区的夏令时和 UTC 偏移规则会随时间变化——IANA 时区数据库 2026d 版本（2026 年 9 月 11 日发布）就包含加拿大西北地区某地永久转为 UTC-06、不再执行夏令时这一变更。如果一个「每周一上午 9 点」的循环事件在创建时就把 UTC 时刻固化下来，一旦这类规则变化，所有未来的发生都会悄悄在错误的 UTC 时刻触发。存本地时间加时区标识符，意味着正确的 UTC 时刻是在读取/使用的那一刻，按当前生效的时区规则重新算出来的，规则变化不需要改动任何已存储的事件数据。
