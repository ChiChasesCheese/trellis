---
id: distributed-election-disruption
node: distributed.consensus
type: qa
---
## Q
A Raft node is cut off by a flaky network link. While isolated, it repeatedly times out and increments its term; when the link heals, its inflated term forces the healthy leader to step down even though nothing was wrong. Name the two standard defenses.

## A
The bug pattern: raw Raft treats **any higher term as authority**, so one flapping node can repeatedly depose a working leader — each heal triggers a needless election and a brief write outage.

- **Pre-vote**: before incrementing its term, a candidate runs a trial round asking "*would* you vote for me?" Peers say yes only if they haven't heard from a live leader within their timeout. An isolated node keeps failing pre-vote, never inflates its term, and rejoins quietly as a follower.
- **Check-quorum (leader-side)**: a leader that can't reach a majority within a timeout steps down on its own — so a leader stranded on the minority side of a partition stops serving (important for lease-based reads), letting the majority's new leader proceed without a term war.

etcd exposes both as options; production Raft deployments are expected to enable them. Interview one-liner: term numbers give safety; pre-vote/check-quorum restore *liveness under flaky links*.

## Q zh
一个 Raft 节点被一条时好时坏的网络链路隔离。隔离期间它反复超时、不断递增自己的 term；链路恢复后，它虚高的 term 迫使健康的 leader 退位——尽管一切本来正常。说出两种标准防御。

## A zh
Bug 模式在于：原始 Raft 把**任何更高的 term 都当作权威**，于是一个链路抖动的节点可以反复废黜正常工作的 leader——每次链路恢复都触发一次无谓的选举和短暂的写入中断。

- **Pre-vote（预投票）**：候选者在递增 term 之前先跑一轮试探："你*会*投我吗？" 同伴只有在自己的超时窗口内没听到活着的 leader 时才答应。被隔离的节点会一直通不过 pre-vote，term 不再虚高，恢复后安静地以 follower 身份归队。
- **Check-quorum（leader 侧）**：leader 在一个超时内联系不上多数派就主动退位——这样被隔离在少数派一侧的 leader 会停止服务（对基于 lease 的读很重要），让多数派选出的新 leader 顺利接手，不打 term 战争。

etcd 把两者都做成了选项；生产环境的 Raft 部署默认应当开启。面试一句话：term 数字给的是安全性；pre-vote/check-quorum 找回的是*链路抖动下的活性*。
