---
id: hi-c-sd-multi-step-processes-n09-temporal-deployment
node: sd.patterns.multi-step-processes.notes
type: qa
step: 9
---
## Q
**多步流程 · Temporal 的部署构成与信号**｜摘要 · 必会

一个典型 Temporal 部署有哪些部分？流程里的"等待"如何实现而不占资源？

## A
- **Temporal Server：** 记账员。派发任务、跟踪超时、记录进度，从不运行你的代码。
- **历史数据库：** 只追加地记录所有工作流决策和 Activity 结果。
- **Worker 池：** 你运行、托管代码的进程。工作流 worker 运行 Workflow 函数决定下一步，活动 worker 执行 Activity，可同进程也可分开部署以隔离。
- **调用过程：** Workflow 执行到 `await processPayment()` 时并不自己调支付服务，而是告诉 Server"调度这个 Activity"，Server 把任务排给活动 worker，由它调用并回报结果，工作流 worker 再从历史末尾继续决定下一步。区别于编舞：流程明确写在一段代码里，而不是隐含在谁消费哪个主题中。
- **信号（signal）：** 等外部事件（如人工拣货完成）时，工作流等待信号，比轮询高效、延迟低；等待期间不占线程不耗 CPU，引擎持久化状态并释放 worker，信号到来再恢复。所以可以"等 30 天签字"而没有成本。
