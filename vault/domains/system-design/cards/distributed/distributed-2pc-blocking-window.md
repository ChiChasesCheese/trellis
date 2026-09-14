---
id: distributed-2pc-blocking-window
node: distributed.transactions.distributed
type: cloze
---
2PC's cost model, in numbers you can quote: a commit needs {{c1::two round trips to the slowest participant, plus a durable log flush (fsync) at every participant and at the coordinator}}. Availability of the transaction is {{c2::the product of all participants' availabilities — five 99.9% services give 99.5%, so the composite is worse than any member}}. The blocking window when the coordinator dies is {{c3::not a timeout but the coordinator's full recovery time — in-doubt participants hold their locks for as long as it takes a human or a failover to restore the coordinator's log}}, and if that log is lost the only resolution is {{c4::a heuristic decision by an operator, which may commit one participant and abort another — silently breaking atomicity, with reconciliation left to the business}}. The structural fix used by Spanner/CockroachDB is {{c5::making the coordinator itself a replicated state machine (its decision log lives in a Raft/Paxos group), so coordinator failure costs an election, not an outage}}.

## zh
2PC 的成本模型用数字表示：一次提交需要{{c1::两个往返到最慢参与者加上每个参与者和协调者的持久日志刷写（fsync）}}。事务的可用性是{{c2::所有参与者可用性的乘积——五个 99.9% 的服务给出 99.5%，所以复合可用性比任何单个成员都差}}。协调者宕机时的阻塞窗口是{{c3::不是超时，而是协调者完全恢复的时间——未确定的参与者会一直持有锁直到人工或故障转移恢复协调者日志}}，如果日志丢失，唯一的解决方案是{{c4::操作员的启发式决策，可能提交一个参与者而中止另一个——无声地破坏原子性，调和留给业务}}。Spanner/CockroachDB 使用的结构修复是{{c5::使协调者本身成为复制状态机（其决策日志存在于 Raft/Paxos 组中），所以协调者故障成本是选举，不是停机}}。
