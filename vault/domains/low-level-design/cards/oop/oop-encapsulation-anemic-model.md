---
id: oop-encapsulation-anemic-model
node: oop.pillars
type: qa
---
## Q
```java
ticket.setStatus(PAID);
ticket.setPaidAt(now);
wallet.setBalance(wallet.getBalance() - fee);
```
Name the smell and the refactor.

## A
**Anemic domain model** — encapsulation broken by getter/setter pairs: the invariants (paid ⇒ `paidAt` set; balance never negative) must be re-implemented by every caller.

Refactor to tell-don't-ask: `ticket.markPaid(now)`, `wallet.debit(fee)`. The operation moves to the data owner, which validates the transition once and can reject illegal states.

## Q zh
```java
ticket.setStatus(PAID);
ticket.setPaidAt(now);
wallet.setBalance(wallet.getBalance() - fee);
```
说出这里的坏味道，以及该怎么重构。

## A zh
**Anemic domain model（贫血领域模型）** —— 封装被成对的 getter/setter 破坏了：不变量（已支付 ⇒ `paidAt` 必须有值；余额不能为负）现在得由每一个调用方各自重新实现一遍。

按 tell-don't-ask 重构：`ticket.markPaid(now)`、`wallet.debit(fee)`。操作搬到数据的所有者身上，由它一次性校验这次状态转移，并且有能力拒绝非法状态。
