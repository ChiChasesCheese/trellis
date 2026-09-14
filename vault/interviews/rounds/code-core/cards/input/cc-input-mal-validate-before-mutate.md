---
id: cc-input-mal-validate-before-mutate
node: input.malformed
type: qa
---
## Q
A transfer line debits one account and credits another. The credit side turns out to be invalid. What must the program's state look like afterwards?

## A
**Exactly as it did before the line — validate the whole record, then apply it.**

```python
if not valid(row):
    rejected.append(row_id); return
apply(row)                       # no check inside apply()
```

A rejected row that already moved half the money is the hardest class of bug in a ledger problem: the totals stay plausible and only the final balance is wrong. The rule generalizes past money — a rejected command must not have advanced a state machine, consumed an id, or bumped a counter. Two phases, always: decide, then mutate. See [[cc-model-sm-guard-then-effect]].

## Q zh
一行 transfer 从一个账户扣款、给另一个账户入账。结果入账方是非法的。之后程序的状态应当是什么样？

## A zh
**和处理这一行之前一模一样 —— 先校验整条记录，再应用它。**

```python
if not valid(row):
    rejected.append(row_id); return
apply(row)                       # no check inside apply()
```

一条已经挪了一半钱的被拒记录，是账本类题目里最难查的一类 bug：总额看起来仍然合理，只有最终余额是错的。这条规则不止适用于钱 —— 被拒绝的命令不得推进过状态机、占用过 id，或者加过计数器。永远分两段：先判定，再改动。见 [[cc-model-sm-guard-then-effect]]。
