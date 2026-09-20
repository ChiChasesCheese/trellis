---
id: problems-digital-wallet-tcc-dangling-fence
node: problems.commerce.digital-wallet
type: qa
step: 4
tags: [grown]
---
## Q
In a digital wallet's TCC (Try-Confirm-Cancel) flow for external top-ups, what is the "dangling" (suspension) failure mode, and how does a fencing log prevent it?

## A
Dangling happens when a Cancel message arrives and executes before its corresponding Try (because of network delay), and only afterward does the delayed Try finally arrive — it reserves a resource that will now never be confirmed or cancelled again, leaving it permanently stuck. A fencing log (one row per transaction branch, tracking status such as TRIED/COMMITTED/ROLLBACKED/SUSPENDED, written in the same local transaction as the business operation) prevents this by inserting a SUSPENDED marker when a Cancel arrives with no prior Try record; the late-arriving Try is then rejected outright because that marker already occupies its key, instead of executing and reserving a resource nothing will ever release.

## Q zh
在数字钱包给外部充值使用的 TCC（Try-Confirm-Cancel）流程中，“悬挂（dangling/suspension）”这种故障模式是什么？一张 fencing 日志表如何防止它？

## A zh
悬挂指的是：由于网络延迟，Cancel 消息先于它对应的 Try 到达并执行完毕，之后姗姗来迟的 Try 才真正抵达——它会预留一份资源，而这份资源以后再也不会被确认或取消，永久卡在预留状态。一张 fencing 日志表（每个事务分支一行，记录 TRIED/COMMITTED/ROLLBACKED/SUSPENDED 等状态，且与业务操作在同一个本地事务里写入）通过以下方式防止这个问题：当 Cancel 到达但日志里没有 Try 记录时，插入一条 SUSPENDED 标记；之后姗姗来迟的 Try 会因为这个标记已经占据了它的主键而被直接拒绝执行，而不是执行后预留一份永远不会被释放的资源。
