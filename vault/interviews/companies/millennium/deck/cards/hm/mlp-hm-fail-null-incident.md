---
id: mlp-hm-fail-null-incident
node: hm.failure
type: qa
step: 1
---
## Q
**最难的 bug：费用静默消失**｜经理面与行为面

“Tell me about a production incident you handled under pressure. What was the hardest bug you've fixed?”

## A
用 ACH 费用 NULL 传播事故。它同时有定位、决定、复盘和结构性修复，而且是你自己建的检查抓到的。

- **发现：** 你建的每日健康检查“每笔已结算交易都有手续费”报警。你把告警转给自己，几分钟内在线程里给出根因。
- **定位：** 缺费用的 100% 是新标准 ACH 路径上的银行账户交易，约 200 个商户、每天约一千万美元交易额。费用品类是 `'BT_' || sub_kind`，这批数据的 sub_kind 是 `NULL`，SQL 里 NULL 拼接得 NULL，匹配不到品类，所以不报错、不出费用。
- **为什么是 NULL：** 同一个函数有两个重载，共享的最终 `MERGE` 用了没有银行账户分支的那个，覆盖了已算对的值。
- **你的决定：** 有人建议把 ACH 加进排除名单，你把数字写下来，检查保留。写了复盘，说明端到端测试漏掉它的四个原因，然后整体删掉双重载设计。
- **边界：** 止血的 PR 是同事先合入的；你负责根因、复盘和结构性修复。

**英文答法。**
- A daily health check I'd built, **every settled transaction has its fee**, paged the on-call; I forwarded it to myself and had the **root cause in the thread within minutes**.
- All missing fees were **bank-account transactions on the new ACH path**; `'BT_' || NULL` is `NULL`, so the category matched nothing and **no fee was written, silently**.
- Two overloads of one function: the shared `MERGE` used the one **without a bank-account branch**.
- I wrote the postmortem, **four reasons the tests missed it**, then removed the two-overload design with a versioned migration.

**追问。**
- **Did you backfill?** Method: fix forward with a backfill if needed; in billing the wrong state is already consumed downstream, so you need a correcting entry, not a reversal.
- **How do you prevent the class?** An unmappable instrument must **fail loudly, not emit nothing**; the fix is a rule at the seam.
- **Why didn't tests catch it?** Routing was asserted but not fees, the fixture used a card payload, sub-kind wasn't asserted on pending rows, and nothing spanned promotion to fee generation.
