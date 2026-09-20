---
id: problems-payment-system-write-intent-before-call
node: problems.commerce.payment-system
type: qa
step: 3
tags: [grown]
---
## Q
In a payment system's charge flow, why does the payment service write a pending ledger entry BEFORE calling the PSP, rather than after receiving the PSP's response?

## A
If the intent is only recorded after a successful PSP response, a crash between calling the PSP and recording the result leaves no trace that the attempt ever happened — recovery has nothing to reconcile against and no way to tell a genuine no-op apart from an unresolved attempt. Writing a pending entry first means a mid-call crash always leaves a durable "we intended to do this" record, which the timeout-recovery path (querying the PSP's true state) can resolve, instead of the attempt silently vanishing.

## Q zh
在支付系统的收款流程中，为什么支付服务要在调用 PSP 之前就写入一条 pending 状态的账本条目，而不是等收到 PSP 响应之后再写？

## A zh
如果只在 PSP 成功响应之后才记录意图，那么进程在调用 PSP 之后、记录结果之前崩溃时，不会留下任何“这次尝试发生过”的痕迹——恢复逻辑没有任何依据可以核对，也无法区分“真的什么都没发生”和“发生了但结果未知”。先写 pending 条目意味着调用中途崩溃总会留下一条持久的“我们曾打算做这件事”的记录，超时恢复路径（查询 PSP 真实状态）可以据此核实，而不是让这次尝试无迹可查地消失。
