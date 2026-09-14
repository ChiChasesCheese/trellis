---
id: distributed-mvcc-defaults
node: distributed.transactions.concurrency-control
type: cloze
---
MVCC lets readers and writers avoid blocking each other: each transaction reads {{c1::a snapshot of versions committed before it started}}, while writers create new row versions instead of overwriting. The cost is {{c2::version garbage that must be cleaned up (Postgres vacuum; long-running transactions hold the snapshot horizon back and cause bloat)}}. Default isolation in Postgres and MySQL/InnoDB respectively: {{c3::read committed and repeatable read}}.

## zh
MVCC 让读者和写者互不阻塞：每个事务读到的是{{c1::由它开始之前已经提交的那些版本构成的快照}}，而写者不覆盖旧值，只创建新的行版本。代价是{{c2::产生必须被清理的版本垃圾（Postgres 的 vacuum；长事务会把快照 horizon 拖住不放，造成 bloat）}}。Postgres 与 MySQL/InnoDB 的默认隔离级别分别是：{{c3::read committed 和 repeatable read}}。
