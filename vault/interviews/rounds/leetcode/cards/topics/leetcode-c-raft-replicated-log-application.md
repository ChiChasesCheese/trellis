---
id: leetcode-c-raft-replicated-log-application
node: topics.uncategorised
type: qa
anki: 1787359912993
tags: [algorithm::consensus, algorithm::majority-quorum, algorithm::randomized-timeout, algorithm::replicated-log, application, case, case::raft-replicated-log, category::distributed-streaming, leetcode, system::etcd, system::raft]
---
## Q
Raft 为什么同时需要 term、日志前缀匹配和 majority quorum？只说“多数派复制成功”缺了什么？

## A
term 标识 leader epoch；前缀匹配保证 followers 的日志不会在同一 index 上保留冲突历史；多数集合必相交，使新 leader 的选举约束能继承 committed entries。leader 只按 Raft 的 current-term commit 规则推进 commitIndex，再按序应用到 state machine。

**Evidence**

Raft 原论文 Figure 2 定义 Election Safety、Log Matching、Leader Completeness、State Machine Safety 以及 current-term entry 的 commit 规则。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdistributed-streaming%2FRaft%EF%BC%9A%E5%A4%9A%E6%95%B0%E6%B4%BE%E3%80%81%E5%A4%8D%E5%88%B6%E6%97%A5%E5%BF%97%E4%B8%8E%E7%8A%B6%E6%80%81%E6%9C%BA)
