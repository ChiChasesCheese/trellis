---
id: hi-c-lld-inventory-management-x01-toctou
node: lld.problem-breakdowns.inventory-management.exam
type: qa
step: 1
---
## Q
**库存管理 · 找出"先查再调拨"的竞态**｜考点 · 必会

下面的调拨有什么问题？给出一个会出错的交错顺序：`if from.check(pid, q): from.remove(pid, q); to.add(pid, q)`，`check` 和 `remove` 各自单独加锁。

## A
- **问题：** 检查与动作之间锁被释放，是典型的 check-then-act（TOCTOU）。
- **交错：** 东仓有 50。线程 A 的 `check(50)` 返回真；线程 B 完整执行了一次 50 的出库，库存变 0；线程 A 继续 `remove(50)`，因为仓库自己校验，返回假且不扣；但 A 没看返回值，继续 `to.add(50)`，西仓凭空多出 50 个。
- **如果 `remove` 不校验：** 东仓变成 −50，违反不变量。
- **修法一，看返回值：** 去掉 `check`，`if from.remove(pid, q): to.add(pid, q)`，解决凭空多出库存；但 `remove` 之后、`add` 之前有一个窗口，汇总库存会少 q。
- **修法二，持两把锁：** 在两个仓库都锁住的情况下完成扣减与入库，不会看到中间状态。
- **看穿：** 同一个模式出现在订座、限流和库存里：检查和动作必须放在同一个临界区。
