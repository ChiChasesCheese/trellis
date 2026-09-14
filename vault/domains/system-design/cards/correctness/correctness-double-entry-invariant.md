---
id: correctness-double-entry-invariant
node: correctness.ledger
type: qa
---
## Q
Why do payment systems store money as double-entry ledger entries instead of a `balance` column, and what invariant does every transaction maintain?

## A
Every transaction posts **two or more entries that sum to zero** (each debit matched by credits) — money is never created or destroyed, only moved between accounts, and external money movements are posted against internal counterpart accounts (e.g. a processor clearing account).

What this buys over a mutable balance column:
- **Auditability**: the balance is *derivable* from history; a bare column can't explain itself or be audited.
- **Error detection**: any bug that loses or invents money breaks the zero-sum invariant and is mechanically detectable.
- **Concurrency**: appending entries avoids read-modify-write races on a single balance row.

## Q zh
为什么支付系统用复式分录账本存储资金而不是用 `balance` 列，每笔交易维护什么不变量？

## A zh
每笔交易**记多条总和为零的分录**（每笔借方对应贷方）— 金钱既不创造也不消灭，只在账户间转移，外部资金流动记录在内部对方账户（如处理方清算账户）。

相比可变 balance 列的优势：
- **可审计性**：balance 从历史*可推导*；裸字段无法自证或审计。
- **错误检测**：任何导致丢失或凭空创造金钱的 bug 都会破坏零和不变量，机械可检测。
- **并发性**：追加分录避免单个 balance 行的读改写竞态。
