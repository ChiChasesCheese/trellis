---
id: leetcode-c-kotlin-channel-backpressure-application
node: topics.uncategorised
type: qa
anki: 1787365292129
tags: [algorithm::backpressure, algorithm::bounded-buffer, algorithm::producer-consumer-queue, algorithm::rendezvous, application, case, case::kotlin-channel-backpressure, category::runtimes-os, chapter::01, chapter::08, chapter::17, leetcode, system::kotlin, system::kotlinx-coroutines]
---
## Q
Kotlin Channel 的 rendezvous、bounded buffer 和 unlimited buffer 分别怎样处理背压？

## A
容量 0 时 send 与 receive 必须配对，背压最强；有限 buffer 允许 producer 暂时领先，满时默认挂起 producer；unlimited 几乎不挂起 producer，只把长期速率不平衡变成不断增长的内存 backlog。

**Evidence**

Kotlin 官方 Channels 文档明确区分 rendezvous、buffered、unlimited 与 conflated channel，并说明满 buffer 时 producer suspension/overflow behavior。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FKotlin%20Channel%EF%BC%9ARendezvous%E3%80%81Bounded%20Buffer%20%E4%B8%8E%E8%83%8C%E5%8E%8B)
