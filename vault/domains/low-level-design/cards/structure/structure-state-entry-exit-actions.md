---
id: structure-state-entry-exit-actions
node: structure.state-machines
type: qa
---
## Q
Entering SHIPPED must email the customer, stop the cancellation timer, and release the reserved stock. Where do these side effects belong, and what's the ordering rule?

## A
On the machine, not the callers — otherwise every call site must remember the full list:

- **Exit action** of the old state: undo what the state owned (stop the cancel timer, release the hold).
- **Entry action** of the new state (Moore) — runs no matter which transition arrived. Effects specific to *one* transition go on that transition (Mealy).

Ordering rule: **guard → mutate state → then effects**, and effects must run *outside* any lock and after the state change is committed. Otherwise you email "shipped" for a transition that then fails a later check, or an exception mid-effect leaves the entity between states.

Make effects a list of collected commands the machine emits and the caller executes — that also keeps the transition logic testable without stubbing the mailer.


## Q zh
进入 SHIPPED 必须给客户邮件、停止取消计时器、释放预留的库存。这些副作用在哪里属于，顺序规则是什么?

## A zh
在机器上，不是调用者 — 否则每个调用站点必须记住完整的列表:

- 旧状态的**退出动作**: 撤销状态拥有的什么（停止取消计时器、释放保留）。
- 新状态的**进入动作**（Moore）— 运行不管哪个转变到达。特定于**一个**转变的效果进入那个转变（Mealy）。

顺序规则: **保护 → 改变状态 → 然后效果**，效果必须运行**在任何锁之外**并且在状态改变被提交之后。否则你给"已发货"邮件给一个转变然后失败一个后期检查，或一个异常中期效果离开实体在状态之间。

制造效果一个命令的列表机器发出的和调用者执行的 — 那也保持转变逻辑可测试没有存根邮件。
