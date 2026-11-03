---
id: hi-pt-tt-query-condition-parser-8-like
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 8
---
## Q
**条件解析与内存表查询 · LIKE 转正则的坑**｜出自：条件解析与内存表查询 › 完整实现 2

把 `LIKE` 的模式转成正则匹配，要注意什么？

## A
**要点。** `%` 转 `.*`，`_` 转 `.`，其他字符必须 `re.escape`，否则 `.`、`(` 会被当成正则语法。用 `re.fullmatch`，因为 `LIKE` 要匹配整个字符串。

**易错。** 用 `re.search` 时 `'ab' LIKE 'a'` 会错误匹配；`.` 默认不匹配换行，要加 `re.S`。
