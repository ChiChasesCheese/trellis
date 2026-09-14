---
id: cc-input-del-writing-back
node: input.delimited
type: qa
---
## Q
You must emit a delimited line whose fields can contain the delimiter or a quote. What is wrong with `",".join(fields)`?

## A
**It produces a line your own reader cannot parse back** — a value containing a comma silently becomes two fields, and a value containing a quote breaks the quoting a reader expects.

If the output format is CSV, write it with `csv.writer` (which quotes and doubles quotes for you). If the output format is a fixed template the statement dictates, do the opposite: emit exactly the template, and rely on the statement's guarantee that the values are safe. The mistake is mixing the two — hand-joining fields you did not verify are delimiter-free.

## Q zh
你要输出一行分隔文本，而字段里可能含有分隔符或引号。`",".join(fields)` 有什么问题？

## A zh
**它产出的行连你自己的读取器都解析不回来** —— 含逗号的值悄悄变成两个字段，含引号的值破坏读取端预期的引用规则。

如果输出格式就是 CSV，就用 `csv.writer` 来写（它会替你加引号并把引号翻倍）。如果输出格式是题面规定的固定模板，那就反过来：严格按模板打印，依赖题面对值安全性的保证。错误在于把两者混着做 —— 手工拼接那些你并未确认不含分隔符的字段。
