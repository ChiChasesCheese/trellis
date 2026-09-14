---
id: analytics-lakehouse-snapshot-isolation
node: analytics.warehouse
type: qa
---
## Q
Object storage has no transactions. How do Iceberg/Delta provide snapshot isolation and atomic commits on top of it?

## A
Data files are **immutable**; a commit writes new data + a new metadata tree, then atomically swings a single **root pointer** to it — via a catalog compare-and-swap or a conditional PUT (`If-None-Match`/`If-Match`, which S3 now supports).

- **Readers** pin the root they started from, so they see one consistent snapshot for the whole query — snapshot isolation for free from immutability.
- **Writers** use optimistic concurrency: if the pointer moved since you read it, your CAS fails and you retry/rebase the commit.

The entire ACID story reduces to one atomic pointer swap; everything else is immutable files.

## Q zh
对象存储没有 transaction。Iceberg/Delta 如何在顶部提供快照隔离和原子提交？

## A zh
数据文件是**不可变的**；提交写新数据 + 新元数据树，然后原子性地摆动单一**根指针** — 通过 catalog compare-and-swap 或条件 PUT（`If-None-Match`/`If-Match`，S3 现在支持）。

- **Reader** 钉住他们开始的根，所以他们看到整个查询的一个一致快照 — 快照隔离来自不可变性的自由。
- **Writer** 使用乐观并发：如果指针自读以来移动，你的 CAS 失败且你重试/rebase 提交。

整个 ACID 故事减少到一个原子指针交换；其他所有是不可变文件。
