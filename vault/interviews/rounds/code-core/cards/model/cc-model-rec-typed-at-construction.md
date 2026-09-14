---
id: cc-model-rec-typed-at-construction
node: model.records
type: qa
---
## Q
A record is built from a parsed line. Should its `amount` field hold `"1000"` or `1000`?

## A
**`1000` — convert at construction, so nothing downstream ever re-parses.**

A record holding strings pushes `int(...)` into every rule, every comparison and every render, which means the validation of that field happens in several places and eventually in none. It also makes a comparison silently wrong: `"1000" > "999"` is `False`.

Do the conversion once, in the parser, where the failure has somewhere to go (skip the row, count it, report the reason). After that boundary the record is typed data and the rules can be about the rules.

## Q zh
一条记录由解析后的行构造。它的 `amount` 字段应该存 `"1000"` 还是 `1000`？

## A zh
**存 `1000` —— 在构造时转换，让下游永远不再重新解析。**

存字符串的记录会把 `int(...)` 推进每条规则、每次比较、每次渲染，意味着这个字段的校验散落在好几处，最终哪一处都不做。它还会让比较悄悄出错：`"1000" > "999"` 是 `False`。

只在解析器里转换一次，那里正好有地方安放失败（跳过该行、计数、报告原因）。越过这道边界之后，记录就是带类型的数据，规则也就能只谈规则。
