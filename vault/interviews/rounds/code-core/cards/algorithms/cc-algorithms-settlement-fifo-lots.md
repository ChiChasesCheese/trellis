---
id: cc-algorithms-settlement-fifo-lots
node: algorithms.settlement
type: qa
---
## Q
Points arrive as dated lots and must be consumed oldest-first. The adds are not in timestamp order, and some are negative corrections. Design it.

## A
**Keep mutable lots `[ts, seq, owner, remaining]` and order by `(ts, seq)` before every consumption.**

- `seq` is the insertion index. It makes equal timestamps deterministic, and it is the **only** thing that does — sorting on `ts` alone leaves ties to whatever the sort last saw ([[cc-output-ordering-total-order]]).
- Apply **negative corrections first**, each against its own owner's oldest remaining lots. A correction dated *before* the lot it cancels still belongs to that owner, so the netting is per owner and not global.
- **Check the total up front** (`spend > sum(balances)` → error) so a failed request leaves every lot untouched. A half-consumed queue cannot be rolled back afterwards.
- Report consumption aggregated per owner, in the order owners were first consumed; the lots themselves are an implementation detail, not output.
- Owners with a zero balance are still listed if the spec enumerates owners ([[cc-output-sentinels-zero-rows]]).

## Q zh
积分以带日期的批次到达，必须按最旧优先消耗。增加项并非按时间戳有序，而且有些是负数更正。设计它。

## A zh
**维护可变的批次 `[ts, seq, owner, remaining]`，每次消耗前按 `(ts, seq)` 排序。**

- `seq` 是插入下标。它让时间戳相同的情形确定化，而且是**唯一**能做到这点的东西 —— 只按 `ts` 排序会把并列交给排序最后看到的顺序（[[cc-output-ordering-total-order]]）。
- **先应用负数更正**，每一项都对着它自己所属方最旧的剩余批次抵扣。日期*早于*它所抵消批次的更正仍然属于那一方，所以抵扣是按所属方进行而非全局。
- **先检查总量**（`spend > sum(balances)` → 报错），这样失败的请求不会动到任何批次。消耗了一半的队列事后是回滚不了的。
- 按所属方汇总消耗量输出，顺序按各方首次被消耗的先后；批次本身是实现细节，不是输出。
- 如果 spec 枚举的是所属方，余额为零的一方仍要列出（[[cc-output-sentinels-zero-rows]]）。
