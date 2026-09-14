---
id: distributed-mvcc-visibility
node: distributed.transactions.concurrency-control
type: cloze
---
MVCC visibility rules — when transaction T (with its snapshot) may see a row version: the version's creator must have {{c1::committed before T's snapshot was taken}}, and the creator must not be in {{c2::the list of transactions that were still in progress at snapshot time (recorded when the snapshot is taken)}}, nor aborted, nor have a txid later than the snapshot. A deleted row stays visible to T until {{c3::the deleting transaction is itself visible under the same rules — deletes just mark the version with the deleter's txid; physical removal is garbage collection's job}}.

## zh
MVCC 的可见性规则——事务 T（带着它的快照）什么时候可以看到某个行版本：创建这个版本的事务必须{{c1::在 T 的快照生成之前就已提交}}，而且这个创建者不能出现在{{c2::快照生成那一刻仍在进行中的事务列表里（这个列表在取快照时记录下来）}}，也不能是已中止的，txid 也不能晚于快照。被删除的行对 T 仍然可见，直到{{c3::执行删除的那个事务本身按同一套规则变得可见——删除只是给版本打上删除者的 txid；真正的物理清除是垃圾回收的活}}。
