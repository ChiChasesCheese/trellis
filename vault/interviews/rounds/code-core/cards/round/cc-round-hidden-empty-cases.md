---
id: cc-round-hidden-empty-cases
node: round.hidden-tests
type: qa
---
## Q
Name the four "empty" cases a grader probes for a program that reads records and prints a summary per entity.

## A
**Empty input · an entity with no records · a record whose value is zero · a result set with nothing in it.**

They fail differently: empty input crashes an unguarded `max()` or prints a header you should not have printed; an entity with no records must often still appear with its base value; a zero value is real data, not absence (`if not amount` is a bug); and the empty result set needs the specified sentinel, not a blank line.

Run all four against *every* part — a Part 4 command usually never saw the empty case its Part 1 loop handled.

## Q zh
对一个"读入记录、按实体输出汇总"的程序，说出评测机会探测的四种"空"情形。

## A zh
**空输入 · 没有任何记录的实体 · 值为零的记录 · 空的结果集。**

它们的失败方式各不相同：空输入会让没有保护的 `max()` 崩溃，或者打印出本不该打印的表头；没有记录的实体往往仍要带着基础值出现；零是真实数据而非缺失（`if not amount` 就是个 bug）；空结果集需要题面指定的 sentinel，而不是一个空行。

对**每一个**部分都跑这四种 —— Part 4 的命令通常从没见过 Part 1 的循环早已处理好的空情形。
