---
id: cc-model-rec-class-earns-behavior
node: model.records
type: qa
---
## Q
What is the signal that a record should become a class with methods rather than staying a dict?

## A
**An invariant that more than one call site must not break.**

A loan balance that may never go below zero, a payment whose amount may only change in one state, a lock whose expiry and last-used timestamp must move together: put the rule in a method and every caller gets it.

```python
def pay(self, amount):           # invariant lives here, once
    paid = min(amount, self.balance)
    self.balance -= paid
    return paid
```

Without the method, "cap at zero" is copied into `PAY`, `TRANSACTION_PROCESSED` and the transfer path, and one of the three forgets it. A record with no invariant gains nothing from a class — leave it a dict.

## Q zh
什么信号说明一个记录该从 dict 升级成带方法的类？

## A zh
**存在一个不能被多个调用点破坏的不变量。**

贷款余额永不低于零；付款金额只在某一个状态下可改；锁的到期时间和最近使用时间必须一起更新 —— 把规则放进方法，所有调用者就都拿到了它。

```python
def pay(self, amount):           # invariant lives here, once
    paid = min(amount, self.balance)
    self.balance -= paid
    return paid
```

没有这个方法，「封底为零」就会被复制到 `PAY`、`TRANSACTION_PROCESSED` 和转账路径里，三处中总有一处忘掉。没有不变量的记录从类里得不到任何东西 —— 让它保持 dict。
