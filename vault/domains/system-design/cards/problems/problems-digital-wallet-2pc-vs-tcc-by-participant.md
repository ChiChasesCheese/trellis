---
id: problems-digital-wallet-2pc-vs-tcc-by-participant
node: problems.commerce.digital-wallet
type: qa
step: 2
tags: [grown]
---
## Q
In a digital wallet design, why does a wallet-to-wallet transfer use internal two-phase commit (2PC) while a top-up from an external bank or PSP uses Try-Confirm-Cancel (TCC) instead?

## A
The two wallet shards in a transfer are both part of the same internally-operated, strongly-consistent storage system — each shard is a replicated group, so a participant "failure" is a sub-second leader election, not an indefinitely stuck transaction, which is exactly the case where 2PC is architecturally sound rather than the failure-prone case seen with protocols spanning independently-operated systems. An external PSP or bank cannot be made to participate in that internal coordination protocol — it has no way to receive our prepare/commit messages as a protocol participant. TCC solves this because it only requires the external side to expose three ordinary, idempotent, independently-callable operations (Try/Confirm/Cancel), not participation in a shared coordination protocol.

## Q zh
在数字钱包设计中，为什么钱包间转账使用内部两阶段提交（2PC），而从外部银行或 PSP 充值却改用 Try-Confirm-Cancel（TCC）？

## A zh
一次转账涉及的两个钱包分片都属于同一个内部运维、强一致的存储系统——每个分片是一个复制组，参与者“故障”是一次亚秒级的 leader 选举，而不是一笔无限期悬置的事务，这正是 2PC 在架构上可行、而不是像跨独立运维系统那样容易出问题的场景。外部的 PSP 或银行无法被拉进这套内部协调协议——它没有办法作为协议参与者接收我们的 prepare/commit 消息。TCC 解决了这一点，因为它只要求外部一侧暴露三个普通的、幂等的、可独立调用的操作（Try/Confirm/Cancel），而不需要参与一个共享的协调协议。
