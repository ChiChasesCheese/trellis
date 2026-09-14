---
id: distributed-cap-real-claim
node: distributed.cap
type: qa
---
## Q
What does the CAP theorem actually constrain — and why is calling a system "CA" a red flag in an interview?

## A
It constrains behavior **only during a network partition**: a replicated system must then either refuse some requests (choose **C**, staying linearizable) or answer with possibly-stale/divergent data (choose **A**). It says nothing about normal operation.

"CA" is a red flag because partitions are not optional in a distributed system — you can't choose to forfeit P; you can only choose what to sacrifice *when* one happens. Also note "C" here means linearizability and "A" means every non-failed node answers — much narrower than everyday "consistency" and "high availability".

## Q zh
CAP 定理实际上约束的是什么？为什么在面试中把一个系统称为 "CA" 是个危险信号？

## A zh
它**只在网络分区期间**约束行为：一个复制系统此时必须要么拒绝一些请求（选择 **C**，保持线性一致），要么用可能陈旧/分歧的数据来回答（选择 **A**）。它对正常运行时期什么都没有约束。

"CA" 是个危险信号，因为在分布式系统中分区不是可选项——你无法选择放弃 P；你只能选择分区*发生时*要牺牲什么。另外注意这里的 "C" 指的是线性一致性，"A" 指的是每个未失败的节点都会应答——比日常语言里的"一致性"和"高可用性"要窄得多。
