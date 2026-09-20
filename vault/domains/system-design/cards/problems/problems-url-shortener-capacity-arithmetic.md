---
id: problems-url-shortener-capacity-arithmetic
node: problems.foundations.url-shortener
type: cloze
step: 1
tags: [grown]
---
In a URL shortener design that creates {{c1::1,000,000}} new short links per day with a {{c2::100:1}} read-to-write (redirect-to-create) ratio, average write QPS is about {{c3::12}} (1,000,000 ÷ 86,400 seconds/day) and average read (redirect) QPS is about {{c4::1,160}} (100,000,000 redirects/day ÷ 86,400).

## zh
在一个每天新增 {{c1::1,000,000}} 条短链接、读写比（重定向 : 创建）为 {{c2::100:1}} 的短链接设计中，平均写 QPS 约为 {{c3::12}}（1,000,000 ÷ 86,400 秒/天），平均读（重定向）QPS 约为 {{c4::1,160}}（每天 1 亿次重定向 ÷ 86,400）。
