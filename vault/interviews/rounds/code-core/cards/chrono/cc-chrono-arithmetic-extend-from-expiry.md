---
id: cc-chrono-arithmetic-extend-from-expiry
node: chrono.arithmetic
type: qa
---
## Q
A subscription expiring on day 11 is renewed for 4 more days on day 2. Is the new expiry 6 or 15? And if the renewal had arrived after expiry?

## A
**An extension is measured from the current expiry, not from the event's day**: `new_expiry = current_expiry + extra` → 15. Adding to "now" silently shortens the term the customer paid for.

- If the term has already expired (or was cancelled), a renewal starts a fresh period from its own timestamp: `expiry = t + d`.
- "Still active at `t`" must use the same boundary predicate as the read path ([[cc-chrono-arithmetic-inclusive-end]]) — with an inclusive end, a renewal landing exactly on the expiry instant still extends.
- An unlimited term is not shortened by a later finite one unless the spec says "replace"; "replace" and "accumulate" are two different parts of the same problem, so keep the rule in one function with a flag.
- Recompute derived dates (warning emails, invoice dates) from the new expiry, and do not un-send anything already dated before the event.

## Q zh
一个第 11 天到期的订阅，在第 2 天续期 4 天。新的到期日是 6 还是 15？如果续期发生在到期之后呢？

## A zh
**延期是从当前到期日算起，而不是从事件当天算起**：`new_expiry = current_expiry + extra` → 15。加在「现在」上会悄悄缩短客户已付费的周期。

- 如果已经过期（或已取消），续期从它自己的时间戳开启新周期：`expiry = t + d`。
- 「在 `t` 时仍有效」必须用与读路径相同的边界谓词（[[cc-chrono-arithmetic-inclusive-end]]）—— 右端闭合时，恰好落在到期时刻的续期仍然延长。
- 除非 spec 说「替换」，否则无限期不会被之后的有限期缩短；「替换」和「累加」是同一问题的两个 part，所以用一个函数加一个开关来表达。
- 从新的到期日重算派生日期（提醒邮件、账单日），并且不要撤销任何日期早于该事件的已发内容。
