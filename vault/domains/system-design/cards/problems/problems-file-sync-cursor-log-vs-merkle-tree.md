---
id: problems-file-sync-cursor-log-vs-merkle-tree
node: problems.media.file-sync
type: qa
step: 6
tags: [grown]
---
## Q
In a file sync system, why is a monotonically increasing, append-only change log with per-device cursors NOT equivalent to a Merkle-tree directory diff, even though both make reconnect-sync cheaper than comparing every file?

## A
A cursor-based change log only answers 'what does the server believe changed since cursor X' — it is cheap because the device just requests entries after its last known cursor instead of comparing every file, but it silently assumes the log is complete, that the device correctly applied every prior entry, and that no file was modified outside the sync mechanism (e.g. edited on disk directly, or corrupted). A Merkle-tree diff answers a strictly stronger question — 'do the local and remote trees actually match right now' — by comparing content hashes bottom-up, so it can catch a missed log entry, an unapplied change, or local corruption that a cursor log has no way to detect, since a cursor log never compares actual state, only log position. Because of this, a design should run the cursor log for everyday low-cost syncing and a periodic Merkle-tree reconciliation as a correctness safety net, not treat the change log as a full substitute for tree comparison.

## Q zh
在文件同步系统中，为什么一条单调递增、只追加写入、每台设备各自维护游标的变更日志，和默克尔树目录差异比对并不等价，即使两者都能让重连后的同步比逐文件比较更便宜？

## A zh
基于游标的变更日志只回答"服务器认为自游标 X 之后发生了什么变化"——它便宜是因为设备只需要请求自己上次已知游标之后的日志条目，而不用逐文件比较，但它默默假设了日志本身是完整的、设备此前正确应用了每一条记录、且没有文件在同步机制之外被动过手脚（例如被直接改了本地磁盘文件，或发生了损坏）。默克尔树差异比对回答的是一个严格更强的问题——"本地和远端的文件树现在是否真的一致"——它自底向上比较内容哈希，因此能发现游标日志发现不了的问题：遗漏的日志条目、未正确应用的变更、或本地损坏，因为游标日志从不比较真实状态，只比较日志位置。因此设计上应该让游标日志承担日常的低成本同步，同时定期跑一次默克尔树校验作为正确性的安全网，而不是把变更日志当成树比较的完全替代品。
