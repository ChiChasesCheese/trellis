---
id: problems-atm-reversal-not-rollback
node: problems.machines.atm
type: qa
step: 5
tags: [grown]
---
## Q
ATM 已经扣了账，钞票却没到客户手上（卡钞，或者客户走了没取）。机器应该把余额加回去吗？流水怎么记？

## A
不能自己加回去。正确做法是向银行发一笔**冲正（reversal）**：`network.reverse(account_id, amount, ref)`，带上原交易的 `ref`，由银行做一次补偿记账；在 `except` 里写 `account.balance += amount` 不是回滚，是伪造账目——那笔扣款真的发生过。流水上同样不许改：原来那条状态为 `OK` 的记录保持原样，冲正是**新增**一条引用同一 `ref`、状态为 `REVERSED` 的记录。事后必须能同时看到『发生过』和『被抵消了』，改掉原记录等于销毁证据。钞票则收进回收箱而不是放回钞箱——来路已不确定的钞票再吐给下一位客户，会把一次纠纷变成两次。
