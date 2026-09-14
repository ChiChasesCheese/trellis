---
id: distributed-linearizability-composability
node: distributed.consistency
type: cloze
---
Linearizability is a {{c1::composable ("local") property — if each object is linearizable, the system of all objects is linearizable}}, and it concerns {{c2::single operations on single objects, ordered against real time}}. Serializability is {{c3::not composable — running transactions serializably on two separate databases does not make cross-database executions serializable}}, which is one reason splitting a transactional workload across stores silently weakens its guarantees.

## zh
linearizability 是一个{{c1::可组合的（"local"）性质——只要每个对象各自是 linearizable 的，由这些对象组成的系统整体就是 linearizable 的}}，而它关心的是{{c2::单个对象上的单个操作，按真实时间（real time）定序}}。serializability 则{{c3::不可组合——在两个独立的数据库上各自以 serializable 执行事务，并不能让跨库的执行整体是 serializable 的}}，这正是把一份事务型负载拆到多个存储上会悄悄削弱其保证的原因之一。
