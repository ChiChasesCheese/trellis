---
id: correctness-ledger-cutoff-settlement
node: correctness.ledger
type: qa
---
## Q
Why does a ledger need a business date and cutoff time distinct from event timestamps, and what happens to entries that arrive after cutoff?

## A
Reports, reconciliation, and settlement all run against a **closed accounting day**: "balance as of end of business date D" must be **frozen** — re-runnable forever with the same result — or every downstream report and payout is unstable.

- Each entry gets a **business/posting date** assigned at write time; at cutoff (e.g. 23:59 in a declared timezone) the day closes and its totals freeze.
- A late-arriving event (processor webhook at 00:30 for yesterday's charge) **posts to the current open day**, carrying its original event time as an attribute — never inserted into the closed day.
- Settlement runs on closed windows: payout for day D = sum of D's closed entries; late items ride the next window.

Same immutability logic as [[correctness-ledger-immutability]], applied to time: closed periods are append-never.

## Q zh
为什么账本需要与事件时间戳不同的业务日期和截止时间，截止后到达的分录怎么处理？

## A zh
报表、对账和清算都针对**已关闭的会计日**：「截至业务日期 D 末日的余额」必须**冻结** — 永远可重新运行得到相同结果 — 否则每个下游报表和支付都不稳定。

- 每条分录在写入时被分配**业务/过账日期**；到截止时间（如声明的时区 23:59）该日关闭，总额冻结。
- 晚到事件（处理方 webhook 在 00:30 关于昨日扣款）**过账到当前开放日**，作为属性携带其原始事件时间 — 绝不插入已关闭日期。
- 清算针对已关闭窗口：D 日支付 = D 日已关闭分录总和；晚到项乘下一窗口。

与 [[correctness-ledger-immutability]] 相同的不变性逻辑，应用到时间：已关闭期间仅追加。
