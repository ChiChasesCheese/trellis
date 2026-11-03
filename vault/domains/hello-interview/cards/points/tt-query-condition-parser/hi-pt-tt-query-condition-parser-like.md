---
id: hi-pt-tt-query-condition-parser-like
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 12
---
## Q
**条件解析与内存表查询 · LIKE 转正则的坑**｜加分 · 出自：条件解析与内存表查询 › 取舍与追问

把 `LIKE` 模式转成正则，要注意什么？

## A
**要点。** `%` 转 `.*`，`_` 转 `.`，其他字符 `re.escape`；用 `re.fullmatch`，因为要匹配整个字符串。

**易错。** 用 `re.search` 时 `'ab' LIKE 'a'` 会错误匹配。
