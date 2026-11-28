---
id: mlp-deepdive-incident-amex
node: deepdive.incidents
type: qa
step: 2
---
## Q
**Amex 管线出过什么事、怎么知道对不对**｜项目深挖

“What broke in the pipeline, and how do you know it's correct?”

## A
先说出过的两件真事，再说三层正确性。

- **文件时机：** Amex 有时把文件放进“昨天”的日期目录，而我们已经翻到今天。你改成用 `PATTERN` 正则扫所有日期分区，靠 `COPY INTO` 的加载历史去重。代价：迟到文件下次跑才被捡起，那几天下游已经出过一版少数据的结果。
- **拒付标志：** 同一笔交易可以先结算、后拒付。你把 `MERGE` 的键做成复合键：参考号加拒付指示位，两种状态并存，由校验决定取舍。
- **行级：** `TRY_TO_DECIMAL` 和 `TRY_TO_DATE`，坏字段不会炸整批，被拒的记录留下而不是丢掉。
- **批级：** 健康检查断言每笔已结算交易都有手续费。
- **对账级：** 手续费总额对 Amex 自己发的汇总记录；不一致就让任务停下，并呼叫值班，值班就是你。

**英文答法。**
- Two things broke. **File timing**: Amex dropped a file into **yesterday's folder** after we'd moved on, so I scan **every date partition** with a `PATTERN` regex and rely on **load history for dedup**.
- The **reject flag**: a transaction can appear as settled and later rejected, so the `MERGE` key is **reference number plus reject indicator**, and the validator decides which wins.
- Correctness has **three layers**: row level, batch level, and **reconciliation against Amex's own summary record**.
- A mismatch **halts the task and pages the on-call** — which has been me.

**追问。**
- **Anything you would call a bug in your own work?** The late-file window: the downstream had already produced a version with missing data.
