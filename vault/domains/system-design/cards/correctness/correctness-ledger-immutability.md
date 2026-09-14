---
id: correctness-ledger-immutability
node: correctness.ledger
type: qa
---
## Q
A posted ledger entry turns out to be wrong (wrong amount, wrong account). What does a payments-grade ledger do, and what is banned?

## A
**Banned**: `UPDATE` or `DELETE` on posted entries. The ledger is append-only; history that auditors and past reports saw must never change.

Correct move: post a **reversal entry** (equal and opposite) and then the corrected entry — three entries total, all preserved, each linking to the original for traceability. The current balance is right *and* the mistake remains visible.

Enforce it structurally: no update/delete grants on the entries table, and corrections go through the same posting API (idempotent, zero-sum-checked) as normal transactions.

## Q zh
过账的分录转身可能是错的（金额错误、账户错误）。支付级账本做什么，什么被禁止？

## A zh
**禁止**：对已过账分录的 `UPDATE` 或 `DELETE`。账本是仅追加；审计员和过去报表看到的历史必须永不改变。

正确做法：过账一条**冲销分录**（相等反向），然后过账改正分录 — 总共三条分录，全部保留，各自链接原始分录用于溯源。当前余额是对的*且*错误保持可见。

结构上强制：entries 表无更新/删除权限，改正通过同一过账 API（幂等、零和检查）如常规交易。
